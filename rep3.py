import numpy as np
import time
import matplotlib.pyplot as plt

def run_performance_benchmark(T=1000, M=12):
    # Setup
    dt = 1.0 / T
    tau_modes = np.logspace(np.log10(dt), np.log10(4.5), M)
    weights = np.ones(M) / M
    state_traces = np.array([1.0 + 0.2 * np.sin(2 * np.pi * t / T) for t in range(T)])
    
    # 1. Volterra Path-Integral (Baseline)
    t_start_v = time.perf_counter()
    volterra_load = np.zeros(T)
    for t in range(T):
        # O(T^2) complexity: Summation over all history
        integral_sum = 0.0
        for j in range(M):
            mode_sum = sum([state_traces[k] * weights[j] * tau_modes[j] * (1.0 - np.exp(-dt/tau_modes[j])) * np.exp(-(t-k) * dt / tau_modes[j]) for k in range(t+1)])
            integral_sum += mode_sum
        volterra_load[t] = integral_sum
    t_end_v = time.perf_counter()
    
    # 2. Antahkarana Recursive State-Space (Target)
    t_start_a = time.perf_counter()
    samskara_buffers = np.zeros(M)
    antahkarana_load = np.zeros(T)
    for t in range(T):
        # O(1) complexity: Recursive update
        for j in range(M):
            exp_factor = np.exp(-dt/tau_modes[j])
            gain = tau_modes[j] * (1.0 - exp_factor)
            samskara_buffers[j] = (samskara_buffers[j] * exp_factor) + \
                                  (state_traces[t] * weights[j] * gain)
        antahkarana_load[t] = np.sum(samskara_buffers)
    t_end_a = time.perf_counter()
    
    # Generate Plot
    plt.figure(figsize=(10, 6))
    plt.plot(volterra_load, label="Volterra Path-Integral", linestyle="--", color="red")
    plt.plot(antahkarana_load, label="Antahkarana Recursive", color="blue")
    plt.title("Empirical Convergence: Volterra vs. Antahkarana Backend")
    plt.xlabel("Simulation Time (t)")
    plt.ylabel("Historical Karmic Load")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("benchmark_convergence.png", dpi=300)
    
    # Output metrics
    print(f"Volterra Compute Time: {t_end_v - t_start_v:.6f}s")
    print(f"Antahkarana Compute Time: {t_end_a - t_start_a:.6f}s")
    print(f"Absolute Deviation: {np.max(np.abs(volterra_load - antahkarana_load)):.2e}")

if __name__ == "__main__":
    run_performance_benchmark()
