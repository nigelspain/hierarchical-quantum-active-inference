import numpy as np
import matplotlib
# Force clean file-based rendering backend to avoid GUI environment crashes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity, fidelity
from scipy.linalg import logm

# =============================================================================
# 1. PARAMETERS & CONFIGURATION
# =============================================================================
steps = 400
times = np.linspace(0, 10.0, steps)
dt = times[1] - times[0]

# Physical subsystem constants
gamma_phi = 1.5       
Gamma_down = 0.8     
t_coupling = 2.5      
Buddhi_tolerance = 1e-4

# Hierarchical feedback weights
macro_learning_rate = 0.02
top_down_influence = 0.3  # Strength of macro expectations overriding local prior tracking

# =============================================================================
# 2. HILBERT SPACE OPERATORS (Lower Subsystems)
# =============================================================================
sigma_z_sub = Qobj([[1, 0], [0, -1]])  
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())

c_ops = [
    np.sqrt(2 * gamma_phi) * tensor(identity(2), n_dot),
    np.sqrt(Gamma_down) * tensor(identity(2), d_operator)
]

# =============================================================================
# 3. STATE INITIALIZATION (Multi-Layer Network)
# =============================================================================
# Subsystem 1: Initialized in a pure symmetric superposition
psi_init_1 = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))
rho_sub_1 = psi_init_1 * psi_init_1.dag()
rho_buddhi_1 = Qobj(identity(2).data / 2.0)

# Subsystem 2: Initialized with a phase offset to represent asymmetric environment
psi_init_2 = tensor((basis(2, 0) + 1j * basis(2, 1)).unit(), basis(2, 0))
rho_sub_2 = psi_init_2 * psi_init_2.dag()
rho_buddhi_2 = Qobj(identity(2).data / 2.0)

# Higher Macroscopic Controller State Space (Tracks composite alignment)
# Initialized as a tranquil, uninformative 4x4 matrix representation (Śāntatvam)
rho_macro_chitta = tensor(identity(2), identity(2)).unit()
rho_macro_chitta = rho_macro_chitta * rho_macro_chitta.dag()

# Tracking history logs
coherence_history_1 = []
coherence_history_2 = []
delta_history_1 = []
delta_history_2 = []
macro_error_history = []

# =============================================================================
# 4. ITERATIVE HIERARCHICAL COGNITIVE LOOP
# =============================================================================
print("Executing Hierarchical Active Inference Network Loop...")

for idx in range(steps):
    # Ensure all lower density matrices maintain full trace operator formatting
    if rho_sub_1.type == 'ket': rho_sub_1 = rho_sub_1 * rho_sub_1.dag()
    if rho_sub_2.type == 'ket': rho_sub_2 = rho_sub_2 * rho_sub_2.dag()

    # Isolate fluid mind (Manas) projections from each localized subsystem
    rho_manas_1 = rho_sub_1.ptrace(0)
    rho_manas_2 = rho_sub_2.ptrace(0)
    
    coherence_history_1.append(np.abs(rho_manas_1[0, 1]))
    coherence_history_2.append(np.abs(rho_manas_2[0, 1]))

    # --- STEP A: TOP-DOWN EXPECTATION INJECTION ---
    # Macro-controller extracts localized expectations from its global Chitta pool
    macro_expect_1 = rho_macro_chitta.ptrace(0)  # Projected target for Subsystem 1
    macro_expect_2 = rho_macro_chitta.ptrace(1)  # Projected target for Subsystem 2
    
    # Intercept and modulate local Buddhi parameters using top-down predictions
    rho_buddhi_1 = (1.0 - top_down_influence) * rho_buddhi_1 + top_down_influence * macro_expect_1
    rho_buddhi_2 = (1.0 - top_down_influence) * rho_buddhi_2 + top_down_influence * macro_expect_2

    # --- STEP B: LOCAL REASONING & DIVERGENCE COMPILING (Layer 0) ---
    # Subsystem 1 Execution
    m_m1, m_b1 = rho_manas_1.full(), rho_buddhi_1.full()
    eps = 1e-10
    kl_1 = np.abs(np.trace(m_m1 @ (logm(m_m1 + eps*np.eye(2)) - logm(m_b1 + eps*np.eye(2)))))
    current_delta_1 = 5.0 * (1.0 / (1.0 + np.exp(-15.0 * (kl_1 - 0.05)))) if kl_1 > Buddhi_tolerance else 0.0
    delta_history_1.append(current_delta_1)
    
    # Subsystem 2 Execution
    m_m2, m_b2 = rho_manas_2.full(), rho_buddhi_2.full()
    kl_2 = np.abs(np.trace(m_m2 @ (logm(m_m2 + eps*np.eye(2)) - logm(m_b2 + eps*np.eye(2)))))
    current_delta_2 = 5.0 * (1.0 / (1.0 + np.exp(-15.0 * (kl_2 - 0.05)))) if kl_2 > Buddhi_tolerance else 0.0
    delta_history_2.append(current_delta_2)

    # --- STEP C: BOTTOM-UP CASCADE & MACRO UPDATING (Layer 1) ---
    # Construct composite evidence matrix from the states of both sub-loops
    rho_composite_evidence = tensor(rho_manas_1, rho_manas_2)
    
    # Calculate global tracking error at the macro level using Trace Distance
    macro_error = 0.5 * np.linalg.norm(rho_macro_chitta.full() - rho_composite_evidence.full(), ord='nuc')
    macro_error_history.append(macro_error)
    
    # Overarching Macro-Chitta updates its internal world model based on bottom-up error
    rho_macro_chitta = (1.0 - macro_learning_rate) * rho_macro_chitta + macro_learning_rate * rho_composite_evidence

    # --- STEP D: PHYSICAL STATE EVOLUTION (Unitary Integration) ---
    # Subsystem 1 Evolution
    tunnel_1 = t_coupling * (1.0 - (current_delta_1 / 5.0))
    H_inst_1 = (current_delta_1 * H_reg_base) + (tunnel_1 * H_interaction)
    if idx < steps - 1:
        res_1 = mesolve(H_inst_1, rho_sub_1, [0, dt], c_ops, e_ops=[])
        rho_sub_1 = res_1.states[-1]
        
    # Subsystem 2 Evolution
    tunnel_2 = t_coupling * (1.0 - (current_delta_2 / 5.0))
    H_inst_2 = (current_delta_2 * H_reg_base) + (tunnel_2 * H_interaction)
    if idx < steps - 1:
        res_2 = mesolve(H_inst_2, rho_sub_2, [0, dt], c_ops, e_ops=[])
        rho_sub_2 = res_2.states[-1]

# =============================================================================
# 5. POST-PROCESSING AND GRAPHICAL PLOTTING
# =============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Upper Plot: Localized Subsystem Tracking (Layer 0)
ax1.plot(times, coherence_history_1, color='tab:blue', linewidth=2.0, label='Coherence Subsystem 1')
ax1.plot(times, coherence_history_2, color='tab:cyan', linewidth=2.0, linestyle='--', label='Coherence Subsystem 2')
ax1.plot(times, delta_history_1, color='tab:red', linestyle=':', linewidth=1.8, label='Detuning Δ1')
ax1.plot(times, delta_history_2, color='tab:orange', linestyle=':', linewidth=1.8, label='Detuning Δ2')
ax1.set_ylabel('Subsystem Quantum States', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.legend(loc='upper right')
ax1.set_title('Hierarchical Active Inference Framework: Layer 0 Sub-Loops', fontsize=12, fontweight='bold')

# Lower Plot: Overarching Macroscopic Controller Tracking (Layer 1)
ax2.plot(times, macro_error_history, color='tab:purple', linewidth=2.5, label='Global Macro Prediction Error (E)')
ax2.set_xlabel('Global System Clock (Kāla Axis)', fontsize=12)
ax2.set_ylabel('Macroscopic Control Metrics', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.legend(loc='upper right')
ax2.set_title('Macroscopic Layer 1 Controller (Global Prior Management)', fontsize=12, fontweight='bold')

plt.tight_layout()
output_filename = 'hierarchical_inference_profile.png'
plt.savefig(output_filename, dpi=300)
print(f"Hierarchical execution complete. Visual diagnostics written to: {output_filename}")
