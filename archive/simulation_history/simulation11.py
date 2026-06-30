import time
import numpy as np
from qutip import Qobj, tensor, identity

# -----------------------------------------------------------------------------
# 1. PARAMETERS & SPECTRAL BASIS SETUP
# -----------------------------------------------------------------------------
steps = 1000
dt = 0.03
times = np.linspace(0, 30.0, steps)

# Generate synthetic 4x4 joint density matrices
mock_states = [tensor(Qobj(identity(2).data/2.0), Qobj(identity(2).data/2.0)) for _ in range(steps)]

# REFINED O(1) RECURSIVE SPECTRAL BASIS (High-Fidelity Patch)
M = 12  # 12-channel basis to capture long-tail non-Markovian memory
tau_min = 0.05
tau_max = 12.0
tau_spectrum = np.logspace(np.log10(tau_min), np.log10(tau_max), M)

# Corrected Partition of Unity Weights
# Renormalized by total kernel area (0.7*0.5 + 0.3*average_tau) to preserve magnitude
raw_weights = np.array([0.4, 0.2, 0.1, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.005, 0.005])
kernel_area = 0.7 * 0.5 + 0.3 * np.mean([1.5, 4.5])
normalized_weights = (raw_weights / np.sum(raw_weights)) / kernel_area 

print("==============================================================")
print("RUNNING HIGH-FIDELITY MEMORY BENCHMARK: EXPANDED BASIS        ")
print("==============================================================")

# --- BACKEND 1: THE OLD O(t^2) PATH INTEGRAL REFERENCE ---
start_old = time.time()
old_load_trace = []
history_substrate = []

for idx, t in enumerate(times):
    current_composite = mock_states[idx]
    history_substrate.append(current_composite)
    
    rho_chitta_conv = tensor(identity(2), identity(2)) * 0.0
    tau_long = 4.5 if t > 15.0 else 1.5
    
    for step_idx in range(idx + 1):
        t_prime = times[step_idx]
        k_kernel = 0.7 * np.exp(-(t - t_prime) / 0.5) + 0.3 * np.exp(-(t - t_prime) / tau_long)
        rho_chitta_conv += history_substrate[step_idx] * k_kernel * dt
        
    old_load_trace.append(rho_chitta_conv.tr())
end_old = time.time()
print(f"-> Path Integral Loop Wall-Clock: {end_old - start_old:.4f} seconds")

# --- BACKEND 2: OPTIMIZED O(1) RECURSIVE SPECTRUM ---
start_new = time.time()
new_load_trace = []

# FIX: Initialize buffers ONCE outside the loop to allow persistent accumulation
S_buffers = [tensor(identity(2), identity(2)) * 0.0 for _ in range(M)]

for idx, t in enumerate(times):
    current_composite = mock_states[idx]
    
    rho_chitta_recursive = tensor(identity(2), identity(2)) * 0.0
    for j in range(M):
        tau_j = tau_spectrum[j]
        
        # EXACT ANALYTICAL UPDATE:
        # Prevents discretization drift using the exact integrated gain factor
        decay_factor = np.exp(-dt / tau_j)
        exact_gain = tau_j * (1 - decay_factor)
        
        # FIX: Discrete LTV update vector mapping with persistence
        S_buffers[j] = (S_buffers[j] * decay_factor) + (current_composite * normalized_weights[j] * exact_gain)
        rho_chitta_recursive += S_buffers[j]
        
    new_load_trace.append(rho_chitta_recursive.tr())
end_new = time.time()

print(f"-> Expanded State-Space Wall-Clock: {end_new - start_new:.4f} seconds")

# Re-evaluate absolute numerical divergence profile
max_diff = np.max(np.abs(np.array(old_load_trace) - np.array(new_load_trace)))
print(f"-> Absolute Numerical Deviation:     {max_diff:.2e}")
print("==============================================================")
