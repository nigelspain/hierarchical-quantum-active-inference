import numpy as np
import matplotlib
# Force a clean file-based rendering backend to avoid GUI/X11 environment crashes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity, fidelity
from scipy.linalg import logm

# =============================================================================
# 1. PARAMETERS & OVERARCHING ṚTU CONFIGURATION
# =============================================================================
steps = 600
times = np.linspace(0, 15.0, steps)  # Extended timeline to see both epochs
dt = times[1] - times[0]

# Technical definition of the Ṛtu Epoch Boundary and its Sandhyā Junction
T_boundary = 7.5      # Exact midpoint where the cosmic season shifts
omega_sandhya = 0.8   # Width parameter governing the adiabatic transition speed

# SEASONAL HYPERPARAMETER MATRIX DEFINITIONS
# Ṛtu A: The Contemplative Winter (Prioritizes deep parallel superposition processing)
gamma_phi_A = 0.5     # Low measurement dephasing
Gamma_down_A = 0.2    # Low relaxation (Preserves quantum coherence)
div_thresh_A = 0.02   # Highly sensitive intellectual trigger

# Ṛtu B: The Active Spring (Prioritizes rapid execution and environmental action)
gamma_phi_B = 3.5     # Accelerated measurement dephasing
Gamma_down_B = 2.0    # Rapid memory clearing and ground discharge
div_thresh_B = 0.15   # High threshold (Triggers instinctive classical actions quickly)

t_coupling = 2.5      # Baseline interaction strength
Buddhi_tolerance = 1e-4

# =============================================================================
# 2. HILBERT SPACE & OPERATOR SETUP
# =============================================================================
sigma_z_sub = Qobj([[1, 0], [0, -1]])  # Substrate phase readout operator
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())

# =============================================================================
# 3. INITIAL STATE SETUP & CHITTA DECLARATION
# =============================================================================
psi_initial = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))
current_rho = psi_initial * psi_initial.dag()

rho_buddhi = Qobj(identity(2).data / 2.0)

# Initialize Chitta background reservoirs for both seasonal paradigms
rho_chitta_A = tensor(identity(2), identity(2)).unit() * tensor(identity(2), identity(2)).unit().dag()
rho_chitta_B = tensor(identity(2), identity(2)).unit() * tensor(identity(2), identity(2)).unit().dag()

# Visualization tracking logs
coherence_history = []
kl_divergence_history = []
delta_history = []
chitta_fidelity_history = []
sandhya_weight_history = []

# =============================================================================
# 4. ITERATIVE COGNITIVE LOOP WITH ADIABATIC ṚTU SCHEDULING
# =============================================================================
print("Launching Kāla-Cakra Meta-Scheduler Loop...")

for idx, t in enumerate(times):
    if current_rho.type == 'ket':
        current_rho = current_rho * current_rho.dag()

    # --- THE ṚTU ADIABATIC SANDHYĀ FILTER ---
    # Compute the smooth, sigmoidal scheduling weights for the transition
    w_B = 1.0 / (1.0 + np.exp(-(t - T_boundary) / omega_sandhya))
    w_A = 1.0 - w_B
    sandhya_weight_history.append(w_B)
    
    # Adiabatically blend the open-system environmental dissipation profiles
    current_gamma_phi = (w_A * gamma_phi_A) + (w_B * gamma_phi_B)
    current_Gamma_down = (w_A * Gamma_down_A) + (w_B * Gamma_down_B)
    current_div_threshold = (w_A * div_thresh_A) + (w_B * div_thresh_B)
    
    # Construct the dynamic, instantaneous Lindblad collapse channels
    c_ops = [
        np.sqrt(2 * current_gamma_phi) * tensor(identity(2), n_dot),
        np.sqrt(current_Gamma_down) * tensor(identity(2), d_operator)
    ]
    
    # --- CHITTA SUBSTANCE MATRICES PRIOR BLENDING ---
    # Blend the subconscious memories to prevent sudden KL divergence spikes
    rho_chitta_effective = (w_A * rho_chitta_A) + (w_B * rho_chitta_B)
    
    # Evaluate tracking statistics
    rho_manas = current_rho.ptrace(0)
    coherence_history.append(np.abs(rho_manas[0, 1]))
    
    m_manas = rho_manas.full()
    m_buddhi = rho_buddhi.full()
    
    # Base Quantum Relative Entropy calculation
    eps = 1e-10
    log_manas = logm(m_manas + eps * np.eye(2))
    log_buddhi = logm(m_buddhi + eps * np.eye(2))
    kl_div_base = np.abs(np.trace(m_manas @ (log_manas - log_buddhi)))
    
    # Compute fidelity relative to the smoothly blended Chitta prior
    f_chitta = fidelity(current_rho, rho_chitta_effective)
    chitta_fidelity_history.append(f_chitta)
    
    # Apply the Chitta-inverse novelty gating filter
    kl_div_effective = kl_div_base * (1.0 - f_chitta)
    kl_divergence_history.append(kl_div_effective)
    
    # Update Buddhi matrix record
    rho_buddhi = (1.0 - 0.01) * rho_buddhi + 0.01 * rho_manas
    
    # --- AHANKARA PARAMETER GATE CONTROLLER ---
    if kl_div_effective > Buddhi_tolerance:
        current_delta = 5.0 * (1.0 / (1.0 + np.exp(-15.0 * (kl_div_effective - current_div_threshold))))
    else:
        current_delta = 0.0
        
    delta_history.append(current_delta)
    current_tunneling = t_coupling * (1.0 - (current_delta / 5.0))
    
    # Build the instantaneous Hamiltonian and step the system forward
    H_inst = (current_delta * H_reg_base) + (current_tunneling * H_interaction)
    
    if idx < steps - 1:
        res = mesolve(H_inst, current_rho, [0, dt], c_ops, e_ops=[])
        current_rho = res.states[-1]

# =============================================================================
# 5. POST-PROCESSING AND EXPEDIENT VISUAL PRINTING
# =============================================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Global System Clock (Kāla Axis)', fontsize=12)
ax1.set_ylabel('Substrate Coherence |ρ_io|', color=color, fontsize=12)
ax1.plot(times, coherence_history, color=color, linewidth=2.5, label='Coherence (Prakriti)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.4)

ax2 = ax1.twinx()  
ax2.set_ylabel('Meta-Scheduler Metrics', color='black', fontsize=12)
ax2.plot(times, kl_divergence_history, color='tab:purple', linestyle='--', linewidth=2, label='Effective KL Divergence')
ax2.plot(times, delta_history, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ(t)')
ax2.plot(times, sandhya_weight_history, color='gray', linestyle='-', alpha=0.3, linewidth=1.5, label='Sandhyā Weight (Ṛtu B)')
ax2.tick_params(axis='y', labelcolor='black')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Ṛtu-Governed Adiabatic Transition Framework\nSmooth Sandhyā Prior Blending Eliminating Discontinuity Spikes', fontsize=13, fontweight='bold')
fig.tight_layout()

output_filename = 'rtu_scheduler_profile.png'
plt.savefig(output_filename, dpi=300)
print(f"Simulation successfully executed. Matrix output path written to: {output_filename}")
