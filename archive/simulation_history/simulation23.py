import numpy as np
import qutip as qt
import time

def run_high_fidelity_validation():
    print("="*70)
    print("RUNNING HIGH-FIDELITY SYNCHRONIZED TENSOR & MEMORY BENCHMARK")
    print("="*70)
    
    # PART 1: VERIFICATION OF CHITTA TENSOR SCALING
    rho_chitta_seed = qt.rand_dm(4)
    identity_macro = qt.identity(2)
    identity_sub2  = qt.identity(4)
    
    # Embed the local Chitta seed into Subsystem 1's slot within the global macro architecture
    rho_chitta_scaled = qt.tensor(identity_macro, rho_chitta_seed, identity_sub2)
    assert rho_chitta_scaled.shape == (32, 32), "Tensor dimensionality scaling failed!"
    print(f" -> Chitta Matrix successfully scaled from 4x4 to hierarchical {rho_chitta_scaled.shape}")
    
    # PART 2: O(1) PSEUDO-MODE VS VOLTERRA PATH-INTEGRAL CONVOLUTION
    T, N = 5.0, 100
    dt = T / N
    times = np.linspace(0, T, N)
    
    M = 12
    tau_modes = np.logspace(np.log10(dt), np.log10(4.5), M)
    weights = np.ones(M) / M
    
    # Generate a continuous, smoothly evolving physical trajectory using a coherent Hamiltonian
    initial_state = qt.rand_dm(4)
    H_drive = qt.rand_herm(4)  # Constant driving Hamiltonian
    state_history = []
    for t_val in times:
        # Evolve smoothly using the unitary evolution operator U = exp(-i*H*t)
        U = (-1j * H_drive * t_val).expm()
        state_history.append(U * initial_state * U.dag())
    
    # Backend A: Brute-Force Volterra Path-Integral Convolution, O(t^2)
    t_start_volterra = time.time()
    volterra_karmic_load = np.zeros(N)
    for t_idx in range(N):
        integral_sum = 0.0
        for t_prime_idx in range(t_idx + 1):
            t_curr, t_prime = times[t_idx], times[t_prime_idx]
            kernel = np.sum(weights * np.exp(-(t_curr - t_prime) / tau_modes))
            integral_sum += kernel * state_history[t_prime_idx].tr() * dt
        volterra_karmic_load[t_idx] = integral_sum
    t_end_volterra = time.time()
    
    # Backend B: Optimized Parallel State-Space Spectrum, O(1)
    t_start_samskara = time.time()
    samskara_buffers = np.zeros(M)
    samskara_karmic_load = np.zeros(N)
    for t_idx in range(N):
        rho_trace = state_history[t_idx].tr()
        for j in range(M):
            exp_factor = np.exp(-dt / tau_modes[j])
            gain_factor = tau_modes[j] * (1.0 - exp_factor)
            samskara_buffers[j] = (samskara_buffers[j] * exp_factor) + (rho_trace * weights[j] * gain_factor)
        samskara_karmic_load[t_idx] = np.sum(samskara_buffers)
    t_end_samskara = time.time()
    
    # PART 3: NUMERICAL CONVERGENCE ASSERTION
    abs_numerical_deviation = np.max(np.abs(volterra_karmic_load - samskara_karmic_load))
    print(f" -> Volterra Path-Integral Compute Time : {t_end_volterra - t_start_volterra:.5f} seconds")
    print(f" -> Optimized Samskara State-Space Time : {t_end_samskara - t_start_samskara:.5f} seconds")
    print(f" > Benchmark Execution Wall-Clock       : {t_end_samskara - t_start_samskara:.4f} seconds")
    print(f" > Absolute Numerical Deviation         : {abs_numerical_deviation:.2e}")
    print("="*70)
    
    if abs_numerical_deviation < 1e-12:
        print("SUCCESS: 12-Pseudo-Mode Mapping Proven Mathematically Perfect proxy.")
    else:
        print("WARNING: Truncation error or structural drift detected.")
    print("="*70)

if __name__ == "__main__":
    run_high_fidelity_validation()
