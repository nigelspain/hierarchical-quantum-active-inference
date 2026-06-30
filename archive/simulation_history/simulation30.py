import numpy as np
import time

# =====================================================================
# 1. GRID INITIALIZATION & COHERENT NON-EQUILIBRIUM STATE TRACES
# =====================================================================
N = 1000
dt = 0.01

# Continuous, stable non-equilibrium density trace sequence (Manas Profile)
t_arr = np.arange(N) * dt
state_traces = np.sin(2 * np.pi * t_arr) * np.exp(-0.2 * t_arr)

# =====================================================================
# 2. THE GEOMETRIC GUNA PARAMETERIZATION (The State-Space Spectrum)
# =====================================================================
M = 3  # Number of distinct Samskara memory modes

# Mode 3 sits at absolute zero (0 + 0j) to explicitly verify singularity robustness
tamas_damping = np.array([0.1, 0.4, 0.0])     # Gamma(theta) -> Attenuation Envelope
rajas_frequency = np.array([0.5, 2.5, 0.0])   # Omega(rho)   -> Kinetic Feedback Frequency
sattva_weights = np.array([1.0, 0.8, 0.3])    # Sigma(sigma)  -> Memory Fidelity Weighting

# Map Rajasic/Tamasic combinations into complex conjugate eigenvalue poles via Euler's Formula
# lambda = -Gamma(theta) + i*Omega(rho)
complex_poles = -tamas_damping + 1j * rajas_frequency

# Global array pre-allocation to maintain strict scope execution
volterra_karmic_load = np.zeros(N)
samskara_karmic_load = np.zeros(N)

# =====================================================================
# BACKEND A: Brute-Force Non-Markovian Volterra Path Integral, O(N^2)
# =====================================================================
t_start_volterra = time.time()
print(" -> Running Backend A (Brute-Force Volterra Memory Convolution)...")

for t_idx in range(N):
    # Historical convolution calculates past accumulated states from k = 0 to t_idx inclusive
    k_indices = np.arange(t_idx + 1)
    delta_t = (t_idx - k_indices) * dt
    
    # Evaluate the analytical Guna memory kernel across the historical grid
    kernel_grid = np.zeros_like(delta_t)
    for j in range(M):
        kernel_grid += sattva_weights[j] * np.exp(-tamas_damping[j] * delta_t) * np.cos(rajas_frequency[j] * delta_t)
        
    # Standard Left-Summation rectangular integration pass
    volterra_karmic_load[t_idx] = np.sum(state_traces[:t_idx+1] * kernel_grid) * dt

t_end_volterra = time.time()


# =====================================================================
# BACKEND B: Singularity-Robust Complex State-Space Spectrum, O(1)
# =====================================================================
t_start_samskara = time.time()
print(" -> Running Backend B (Optimized Complex Samskara Parallel Engine)...")

# Allocate buffer registers with explicit complex datatype tracking
samskara_buffers = np.zeros(M, dtype=complex)

for t_idx in range(N):
    current_trace = state_traces[t_idx]
    
    # STEP B.1: Inject the fresh state trace impulse into the registers.
    # To match Backend A's rectangular left-summation, the injection behaves 
    # as a pure delta shock scaled by raw dt before any analytical exponential steps are evaluated.
    samskara_buffers = samskara_buffers + current_trace * dt
    
    # STEP B.2: Extract the real-valued backflow weighted by the Sattvic parameters immediately.
    # Sampling here accurately captures the historical memory state at t_idx inclusive.
    karmic_feedback = np.sum(np.real(samskara_buffers) * sattva_weights)
    samskara_karmic_load[t_idx] = karmic_feedback
    
    # STEP B.3: Advance the complex-conjugate state buffers forward in time for the next index step.
    samskara_buffers = samskara_buffers * np.exp(complex_poles * dt)

t_end_samskara = time.time()


# =====================================================================
# PART 3: RE-EVALUATION OF NUMERICAL CONVERGENCE
# =====================================================================
abs_numerical_deviation = np.max(np.abs(volterra_karmic_load - samskara_karmic_load))

print("\n=================== RE-RUN BENCHMARK METRICS ===================")
print(f" -> Volterra Path-Integral Execution Time: {t_end_volterra - t_start_volterra:.5f} seconds")
print(f" -> Optimized Samskara Spectrum Run Time : {t_end_samskara - t_start_samskara:.5f} seconds")
print(f" -> Absolute Numerical Deviation         : {abs_numerical_deviation:.2e}")
print("=================================================================\n")

# Assert flawless mathematical equivalence between the two backends
assert abs_numerical_deviation < 1e-11, "Mathematical divergence detected between frameworks!"
print(" -> Validation Complete! Absolute convergence achieved at sub-precision thresholds.")
