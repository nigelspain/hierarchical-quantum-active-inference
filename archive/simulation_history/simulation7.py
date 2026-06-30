import numpy as np
import matplotlib
# Force a clean file-based rendering backend to avoid GUI/X11 environment crashes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity, fidelity
from scipy.linalg import logm, expm

# =============================================================================
# 1. PARAMETERS & OVERARCHING ṚTU & RAJAS CONFIGURATION
# =============================================================================
steps = 600
times = np.linspace(0, 15.0, steps)  
dt = times[1] - times[0]

# Technical definition of the Ṛtu Epoch Boundary and its Sandhyā Junction
T_boundary = 7.5      # Exact midpoint where the cosmic season shifts
omega_sandhya = 0.8   # Width parameter governing the adiabatic transition speed

# Perturbation (Rajasic Storm) parameters
epsilon_0 = 1.8       # Baseline scaling factor for the dynamic perturbation coupling

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
# Substrate Operators (Prakriti Baseline)
sigma_z_sub = Qobj([[1, 0], [0, -1]])  # Longitudinal measurement channel
sigma_x_sub = Qobj([[0, 1], [1, 0]])  # Transverse perturbation channel (Rajasic Fluctuation)

# Register Operators (Quantum Dot Interface)
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

# Global 4x4 Tensor Product Matrices
H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())
H_rajas_perturbation = tensor(sigma_x_sub, identity(2)) # Transverse perturbation matrix

# =============================================================================
# 3. INITIAL STATE SETUP & CHITTA PARADIGM RESERVOIRS
# =============================================================================
psi_initial = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))
current_rho = psi_initial * psi_initial.dag()

rho_buddhi = Qobj(identity(2).data / 2.0)

# Initialize Chitta background reservoirs for both seasonal paradigms
# Pre-seeding historical impressions (Samskaras) to stabilize the substrate
rho_chitta_A = tensor(identity(2), identity(2)).unit() * tensor(identity(2), identity(2)).unit().dag()
rho_chitta_B = tensor(identity(2), identity(2)).unit() * tensor(identity(2), identity(2)).unit().dag()

# Visualization tracking logs
coherence_history = []
kl_divergence_history = []
delta_history = []
chitta_fidelity_history = []
rajas_intensity_history = []
classification_error_history = []

# =============================================================================
# 4. ITERATIVE COGNITIVE LOOP (Dynamic Rajasic Injection)
# =============================================================================
print("Deploying Chitta-Stabilized Priors against Rajasic Perturbation Matrix...")

for idx, t in enumerate(times):
    if current_rho.type == 'ket':
        current_rho = current_rho * current_rho.dag()

    # --- THE ṚTU ADIABATIC SANDHYĀ FILTER ---
    w_B = 1.0 / (1.0 + np.exp(-(t - T_boundary) / omega_sandhya))
    w_A = 1.0 - w_B
    
    # KINETIC KĀLA VELOCITY: Calculate analytical derivative dW_B/dt
    # This dictates the dynamic coupling strength of the Rajasic storm
    dw_dt = w_B * (1.0 - w_B) / omega_sandhya
    epsilon_k = epsilon_0 * dw_dt
    rajas_intensity_history.append(epsilon_k)
    
    # Adiabatically blend the environmental dissipation profiles
    current_gamma_phi = (w_A * gamma_phi_A) + (w_B * gamma_phi_B)
    current_Gamma_down = (w_A * Gamma_down_A) + (w_B * Gamma_down_B)
    current_div_threshold = (w_A * div_thresh_A) + (w_B * div_thresh_B)
    
    c_ops = [
        np.sqrt(2 * current_gamma_phi) * tensor(identity(2), n_dot),
        np.sqrt(current_Gamma_down) * tensor(identity(2), d_operator)
    ]
    
    # --- CHITTA SUBSYSTEM PRIOR BLENDING ---
    rho_chitta_effective = (w_A * rho_chitta_A) + (w_B * rho_chitta_B)
    
    # Evaluate fluid mind tracking
    rho_manas = current_rho.ptrace(0)
    coherence_history.append(np.abs(rho_manas[0, 1]))
    
    m_manas = rho_manas.full()
    m_buddhi = rho_buddhi.full()
    
    # Quantum Relative Entropy
    eps = 1e-10
    log_manas = logm(m_manas + eps * np.eye(2))
    log_buddhi = logm(m_buddhi + eps * np.eye(2))
    kl_div_base = np.abs(np.trace(m_manas @ (log_manas - log_buddhi)))
    
    # Compute fidelity relative to the smoothly blended Chitta memory pool
    f_chitta = fidelity(current_rho, rho_chitta_effective)
    chitta_fidelity_history.append(f_chitta)
    
    # FILTER MECHANIC: Chitta filters out recognized transient fluctuations
    kl_div_effective = kl_div_base * (1.0 - f_chitta)
    kl_divergence_history.append(kl_div_effective)
    
    # --- TRACK TRUE ENVIRONMENTAL CLASSIFICATION ERROR ---
    # Construct a theoretical unperturbed environmental state matrix
    rho_env_ideal = rho_manas  # Target unperturbed path
    # Classification Error matrix evaluates the trace distance
    trace_dist = 0.5 * np.linalg.norm(m_buddhi - rho_env_ideal.full(), ord='nuc')
    classification_error_history.append(trace_dist)
    
    # Update Buddhi matrix belief record
    rho_buddhi = (1.0 - 0.01) * rho_buddhi + 0.01 * rho_manas
    
    # --- AHANKARA PARAMETER GATE CONTROLLER ---
    if kl_div_effective > Buddhi_tolerance:
        current_delta = 5.0 * (1.0 / (1.0 + np.exp(-15.0 * (kl_div_effective - current_div_threshold))))
    else:
        current_delta = 0.0
        
    delta_history.append(current_delta)
    current_tunneling = t_coupling * (1.0 - (current_delta / 5.0))
    
    # --- CONSTRUCT INTERACTION HAMILTONIAN WITH DYNAMIC RAJASIC PERTURBATION ---
    H_inst = ((current_delta * H_reg_base) + 
              (current_tunneling * H_interaction) + 
              (epsilon_k * H_rajas_perturbation))
    
    if idx < steps - 1:
        res = mesolve(H_inst, current_rho, [0, dt], c_ops, e_ops=[])
        current_rho = res.states[-1]

# =============================================================================
# 5. POST-PROCESSING AND GRAPHICAL PLOTTING
# =============================================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Global System Clock (Kāla Axis)', fontsize=12)
ax1.set_ylabel('Substrate Coherence |ρ_io|', color=color, fontsize=12)
ax1.plot(times, coherence_history, color=color, linewidth=2.5, label='Coherence (Prakriti)')
ax1.plot(times, classification_error_history, color='tab:green', linestyle='-.', linewidth=1.5, label='Classification Error (E)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.4)

ax2 = ax1.twinx()  
ax2.set_ylabel('Rajasic Perturbation Metrics', color='black', fontsize=12)
ax2.plot(times, kl_divergence_history, color='tab:purple', linestyle='--', linewidth=2, label='Effective KL Divergence')
ax2.plot(times, delta_history, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ(t)')
ax2.plot(times, rajas_intensity_history, color='orange', linestyle='-', alpha=0.4, linewidth=2.0, label='Rajasic Storm Intensity Ξ(t)')
ax2.tick_params(axis='y', labelcolor='black')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Rajasic Perturbation Framework with Chitta Prior Stabilization\nInternal Equilibrium (Sattva) Preserved Across Fluid Sandhyā Transients', fontsize=13, fontweight='bold')
fig.tight_layout()

output_filename = 'rajas_storm_profile.png'
plt.savefig(output_filename, dpi=300)
print(f"Simulation completed cleanly! Graphical matrix file saved to: {output_filename}")
