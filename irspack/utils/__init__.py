from typing import Optional, Tuple
import random
import numpy as np

from ._util_cpp import (
    rowwise_train_test_split_d,
    rowwise_train_test_split_f,
    rowwise_train_test_split_i,
    sparse_mm_threaded,
)
from ..definitions import InteractionMatrix


def rowwise_train_test_split(
    X: InteractionMatrix, test_ratio: float, random_seed: Optional[int] = None
) -> Tuple[InteractionMatrix, InteractionMatrix]:
    if (test_ratio < 0) or (test_ratio > 1.0):
        raise ValueError("test_ratio must be a float within [0.0, 1.0]")
    if random_seed is None:
        random_seed = random.randint(-(2 ** 32), 2 ** 32 - 1)
    if X.dtype == np.float32:
        return rowwise_train_test_split_f(X, test_ratio, random_seed)
    elif X.dtype == np.float64:
        return rowwise_train_test_split_d(X, test_ratio, random_seed)
    elif X.dtype == np.int64:
        return rowwise_train_test_split_i(X, test_ratio, random_seed)
    else:
        original_dtype = X.dtype
        X_double = X.astype(np.float64)
        X_train_double, X_test_double = rowwise_train_test_split_d(
            X_double, test_ratio, random_seed
        )
        return (
            X_train_double.astype(original_dtype),
            X_test_double.astype(original_dtype),
        )
