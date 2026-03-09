import numpy as np

def european_call(K):
    return lambda S: np.maximum(S - K, 0)

def european_put(K):
    return lambda S: np.maximum(K - S, 0)

def digital_call(K):
    return lambda S: (S > K).astype(float)

def digital_put(K):
    return lambda S: (S < K).astype(float)
