#!/usr/bin/env python
from __future__ import annotations
# Shared copy; consider centralizing later.
import os, sys, xml.etree.ElementTree as ET, argparse
from pathlib import Path

def find_file(explicit: str | None):
    candidates = [explicit] if explicit else []
    candidates += ["coverage-combined.xml", "coverage.xml"]
    for c in candidates:
        if c and Path(c).is_file():
            return Path(c)
    return None

def parse_rate(p: Path) -> float:
    root = ET.parse(p).getroot()
    rate = root.get('line-rate')
    if rate is None:
        raise RuntimeError('line-rate missing')
    return float(rate) * 100

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--percent-file', default=None)
    args = parser.parse_args()
    xml = find_file(os.getenv('COVERAGE_FILE'))
    if not xml:
        print('COVERAGE: no xml found (skip)')
        return 0
    try:
        pct = parse_rate(xml)
    except Exception as e:
        print(f'COVERAGE: parse error: {e}')
        return 0
    thresh_raw = os.getenv('COVERAGE_FAIL_UNDER')
    thresh = None
    if thresh_raw:
        try:
            thresh = float(thresh_raw)
        except ValueError:
            print(f'COVERAGE: invalid threshold {thresh_raw!r}')
    if args.percent_file:
        try:
            with open(args.percent_file, 'w') as f:
                f.write(f'{pct:.2f}\n')
        except OSError as e:
            print(f'COVERAGE: write error {e}')
    summary_path = os.getenv('GITHUB_STEP_SUMMARY')
    if summary_path:
        try:  # pragma: no cover
            with open(summary_path, 'a') as f:
                f.write(f"\n### Coverage\n\nObserved: {pct:.2f}%\n")
        except OSError:
            pass
    hard_fail = os.getenv('COVERAGE_HARD_FAIL') == '1'
    if thresh is None:
        print(f'COVERAGE: observed {pct:.2f}% (soft mode)')
        return 0
    if pct + 1e-9 < thresh:
        if hard_fail:
            print(f'COVERAGE: {pct:.2f}% below {thresh:.2f}% (FAIL)')
            return 1
        print(f'COVERAGE: {pct:.2f}% below {thresh:.2f}% (soft fail)')
        return 0
    print(f'COVERAGE: {pct:.2f}% meets {thresh:.2f}%')
    return 0

if __name__ == '__main__':
    sys.exit(main())
