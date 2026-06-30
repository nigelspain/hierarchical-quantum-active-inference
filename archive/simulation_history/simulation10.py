import time
import numpy as np
from qutip import Qobj, tensor, identity

# Define state spaces for a quick structural benchmarking run
steps = 1000
dt = 0.03
times = np.linspace(0, 30.0, steps)

# Generate dummy 4x4 joint density matrices to simulate historical state packets
mock_states = [tensor(Qobj(identity(2).data/2.0), Qobj(identity(2).data/2.0)) for _ in range(steps)]

print("==============================================================")
print("RUNNING DISTRIBUTED MEMORY BENCHMARK: INTEGRAL VS RECURSIVE   ")
print("==============================================================")

# --- BACKEND 1: THE OLD O(t^2) CONTINUOUS CONVOLUTION LOOP ---
start_old = time.time()
old_load_trace = []
history_substrate = []

for idx, t in enumerate(times):
    current_composite = mock_states[idx]
    history_substrate.append(current_composite)
    
    # Literal integration over the accumulated database tape
    rho_chitta_conv = tensor(identity(2), identity(2)) * 0.0
    tau_long = 4.5 if t > 15.0 else 1.5
    
    for step_idx in range(idx + 1):
        t_prime = times[step_idx]
        k_kernel = 0.7 * np.exp(-(t - t_prime) / 0.5) + 0.3 * np.exp(-(t - t_prime) / tau_long)
        rho_chitta_conv += history_substrate[step_idx] * k_kernel * dt
        
    old_load_trace.append(rho_chitta_conv.tr())
end_old = time.time()
print(f"-> Baseline Integral Loop Wall-Clock: {end_old - start_old:.4f} seconds (O(t^2) Scaling)")

# --- BACKEND 2: THE REFINED O(1) RECURSIVE STATE-SPACE ---
start_new = time.time()
new_load_trace = []

# Initialize localized latent memory buffers (The Samskara-bija Tensors)
S_short = tensor(identity(2), identity(2)) * 0.0
S_long = tensor(identity(2), identity(2)) * 0.0

for idx, t in enumerate(times):
    current_composite = mock_states[idx]
    tau_long = 4.5 if t > 15.0 else 1.5
    
    # Recursive O(1) state updates - no lookups, no historical loops
    S_short = S_short * np.exp(-dt / 0.5) + current_composite * 0.7 * dt
    S_long = S_long * np.exp(-dt / tau_long) + current_composite * 0.3 * dt
    
    # Aggregate load evaluated via a simple linear combination
    rho_chitta_recursive = S_short + S_long
    new_load_trace.append(rho_chitta_recursive.tr())
end_new = time.time()
print(f"-> Refined State-Space Wall-Clock:   {end_new - start_new:.4f} seconds (O(1) Scaling)")

# Verify mathematical profile convergence
max_diff = np.max(np.abs(np.array(old_load_trace) - np.array(new_load_trace)))
print(f"-> Absolute Numerical Deviation:     {max_diff:.2e}")
print("==============================================================")
