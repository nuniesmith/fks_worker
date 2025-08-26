"""Meta-learner / ensemble scaffolding.

Provides a simple stacking interface: collect base model probabilities, fit meta model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
from shared_python.logging import get_logger  # type: ignore
from shared_python.exceptions import ModelError  # type: ignore

log = get_logger(__name__)


@dataclass
class StackingResult:
    meta_model: Any
    base_models: Dict[str, Any]
    params: Dict[str, Any]


class SimpleStackingEnsemble:
    def __init__(self, meta_model_factory, base_models: Dict[str, Any]):  # factories or fitted
        self.meta_model_factory = meta_model_factory
        self.base_models = base_models
        self.meta_model: Any | None = None

    def fit(self, X, y):  # X unused: we build meta features from base model probs
        import numpy as np  # type: ignore
        try:
            prob_cols: List[Any] = []
            for name, mdl in self.base_models.items():
                probs = mdl.predict_proba(X)
                prob_cols.append(probs)
            meta_X = np.hstack([p[:, 1].reshape(-1, 1) for p in prob_cols])  # use positive class prob
            self.meta_model = self.meta_model_factory()
            self.meta_model.fit(meta_X, y)
            return StackingResult(meta_model=self.meta_model, base_models=self.base_models, params={})
        except Exception as e:  # pragma: no cover
            raise ModelError(f"Stacking fit failed: {e}") from e

    def predict_proba(self, X):
        import numpy as np  # type: ignore
        if self.meta_model is None:
            raise ModelError("Meta model not fitted")
        prob_cols: List[Any] = []
        for _, mdl in self.base_models.items():
            probs = mdl.predict_proba(X)
            prob_cols.append(probs)
        meta_X = np.hstack([p[:, 1].reshape(-1, 1) for p in prob_cols])
        return self.meta_model.predict_proba(meta_X)