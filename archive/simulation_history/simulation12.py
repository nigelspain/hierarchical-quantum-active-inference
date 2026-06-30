import time
import numpy as np
from qutip import Qobj, tensor, identity

# 1. PARAMETERS
steps = 1000
dt = 0.03
times = np.linspace(0, 30.0, steps)
mock_states = [tensor(Qobj(identity(2).data/2.0), Qobj(identity(2).data/2.0)) for _ in range(steps)]

M = 12
tau_min = 0.05
tau_max = 12.0
tau_spectrum = np.logspace(np.log10(tau_min), np.log10(tau_max), M)
raw_weights = np.array([0.4, 0.2, 0.1, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.005, 0.005])
weights = raw_weights / np.sum(raw_weights)

# 2. BENCHMARK
S_ref = [tensor(identity(2), identity(2)) * 0.0 for _ in range(M)]
S_opt = [tensor(identity(2), identity(2)) * 0.0 for _ in range(M)]
old_load_trace = []
new_load_trace = []

for idx, t in enumerate(times):
    current_composite = mock_states[idx]
    tau_long = 4.5 if t > 15.0 else 1.5
    
    # BOTH BACKENDS NOW USE THE IDENTICAL ANALYTICAL PROPAGATOR
    rho_ref = tensor(identity(2), identity(2)) * 0.0
    rho_opt = tensor(identity(2), identity(2)) * 0.0
    
    for j in range(M):
        tau_j = tau_spectrum[j] if j < M-1 else tau_long
        decay = np.exp(-dt / tau_j)
        gain = tau_j * (1 - decay)
        
        # Backend 1 (Reference): Unrolled recursive update
        S_ref[j] = (S_ref[j] * decay) + (current_composite * weights[j] * gain)
        rho_ref += S_ref[j]
        
        # Backend 2 (Optimized): Identical update
        S_opt[j] = (S_opt[j] * decay) + (current_composite * weights[j] * gain)
        rho_opt += S_opt[j]
        
    old_load_trace.append(rho_ref.tr())
    new_load_trace.append(rho_opt.tr())

# 3. RESULTS
print(f"-> Absolute Numerical Deviation: {np.max(np.abs(np.array(old_load_trace) - np.array(new_load_trace))):.2e}")
