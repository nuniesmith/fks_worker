"""fks_worker package marker.

Provides a stable package path for editable installs within Docker
builds. The service currently uses module-level scripts (e.g. app.py,
main.py); this namespace allows future consolidation without breaking
imports.
"""

from __future__ import annotations

__all__ = []
