import numpy as np
import time

def benchmark_models(horizon=5000):
    # 1. Integral-based approach: O(t^2)
    start = time.perf_counter()
    history = np.random.rand(horizon)
    # Simulating the O(t^2) convolution integral
    for t in range(horizon):
        conv = np.sum([history[i] * np.exp(-(t-i)/10.0) for i in range(t)])
    integral_time = time.perf_counter() - start

    # 2. Recursive state-space approach: O(N)
    start = time.perf_counter()
    phi = 0.0
    # Simulating the O(N) recursive update
    for t in range(horizon):
        phi = (-phi / 10.0 + history[t]) * 0.1
    recursive_time = time.perf_counter() - start

    print(f"{'Method':<20} | {'Time (s)':<10}")
    print("-" * 35)
    print(f"{'Integral (O(t^2))':<20} | {integral_time:<10.4f}")
    print(f"{'Recursive (O(N))':<20} | {recursive_time:<10.4f}")

if __name__ == "__main__":
    benchmark_models()
