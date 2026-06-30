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
steps = 500
times = np.linspace(0, 15.0, steps)  # Extended timeline to see long-tail memory loops
dt = times[1] - times[0]

# Meta-Scheduler Boundaries
T_boundary = 7.5      
omega_sandhya = 0.8   

# Open quantum system properties
gamma_phi = 1.5       
Gamma_down = 0.8     
t_coupling = 2.5      
Buddhi_tolerance = 1e-4

# =============================================================================
# 2. OPERATOR & STATE SPACE INITIALIZATION
# =============================================================================
sigma_z_sub = Qobj([[1, 0], [0, -1]])  
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator
H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())
c_ops = [np.sqrt(2 * gamma_phi) * tensor(identity(2), n_dot), np.sqrt(Gamma_down) * tensor(identity(2), d_operator)]

# Initialize Layer 0 local systems
psi_init_1 = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))
rho_sub_1 = psi_init_1 * psi_init_1.dag()
rho_buddhi_1 = Qobj(identity(2).data / 2.0)

psi_init_2 = tensor((basis(2, 0) + 1j * basis(2, 1)).unit(), basis(2, 0))
rho_sub_2 = psi_init_2 * psi_init_2.dag()
rho_buddhi_2 = Qobj(identity(2).data / 2.0)

# Memory allocation logs for history arrays (The Convolutional Substrate)
history_composite_states = []

# Visualization tracking arrays
coherence_history_1 = []
kl_divergence_history = []
delta_history_1 = []
karmic_load_history = []

# =============================================================================
# 4. ITERATIVE NON-MARKOVIAN FEEDBACK LOOP
# =============================================================================
print("Deploying Non-Markovian Karmic Convolution Loop...")

for idx, t in enumerate(times):
    if rho_sub_1.type == 'ket': rho_sub_1 = rho_sub_1 * rho_sub_1.dag()
    if rho_sub_2.type == 'ket': rho_sub_2 = rho_sub_2 * rho_sub_2.dag()

    rho_manas_1 = rho_sub_1.ptrace(0)
    rho_manas_2 = rho_sub_2.ptrace(0)
    coherence_history_1.append(np.abs(rho_manas_1[0, 1]))
    
    # Track the current joint physical output state packet
    current_composite = tensor(rho_manas_1, rho_manas_2)
    history_composite_states.append(current_composite)

    # --- THE ṚTU SANDHYĀ SCHEDULER MATRIX ---
    w_B = 1.0 / (1.0 + np.exp(-(t - T_boundary) / omega_sandhya))
    
    # --- BHAKTI-BĪJA: THE TRANSFORMATION VARIABLE ---
    # Triggering total surrender at t = 11.0 to roast the latent impressions
    bhakti_bija = 1.0 if t < 11.0 else 0.0

    # --- NON-MARKOVIAN INTEGRAL CALCULATION ---
    # Convolute historical states over the dynamic memory kernel
    rho_chitta_convolution = tensor(identity(2), identity(2)) * 0.0
    
    # Modulate decay horizons based on the active cosmic season
    tau_short = 0.5
    tau_long = 4.5 if w_B > 0.5 else 1.5  # Seasonal re-weighting scales up long-horizon memory
    
    # Execute numerical trapezoidal history integration
    for step_idx in range(idx + 1):
        t_prime = times[step_idx]
        delta_t_prime = t - t_prime
        
        # Blended memory decay kernel
        k_kernel = 0.7 * np.exp(-delta_t_prime / tau_short) + 0.3 * np.exp(-delta_t_prime / tau_long)
        
        # Apply the absolute Bhakti neutralizing filter
        k_kernel_effective = bija_filter = bhakti_bija * k_kernel
        
        rho_chitta_convolution += history_composite_states[step_idx] * k_kernel_effective * dt
    
    # Re-normalize the accumulated convolutional prior matrix to track trace obligations
    trace_val = rho_chitta_convolution.tr()
    if trace_val > 1e-5:
        rho_chitta_effective = rho_chitta_convolution / trace_val
    else:
        rho_chitta_effective = tensor(identity(2), identity(2)).unit() * tensor(identity(2), identity(2)).unit().dag()
        
    # Log the total active memory integral trace magnitude (Karmic Load)
    karmic_load_history.append(trace_val)

    # --- COGNITIVE COMPUTATION LAYER ---
    macro_prior_1 = rho_chitta_effective.ptrace(0)
    rho_buddhi_1 = 0.7 * rho_buddhi_1 + 0.3 * macro_prior_1

    m_m1, m_b1 = rho_manas_1.full(), rho_buddhi_1.full()
    eps = 1e-10
    kl_1 = np.abs(np.trace(m_m1 @ (logm(m_m1 + eps*np.eye(2)) - logm(m_b1 + eps*np.eye(2)))))
    
    # If Bhakti is active (surrender achieved), force immediate, smooth clarity
    if bhakti_bija == 0.0:
        kl_1 = 0.0 
        
    kl_divergence_history.append(kl_1)
    
    if kl_1 > Buddhi_tolerance:
        current_delta_1 = 5.0 * (1.0 / (1.0 + np.exp(-15.0 * (kl_1 - 0.05))))
    else:
        current_delta_1 = 0.0
    delta_history_1.append(current_delta_1)

    # --- PHYSICAL STATE EVOLUTION ---
    tunnel_1 = t_coupling * (1.0 - (current_delta_1 / 5.0))
    H_inst_1 = (current_delta_1 * H_reg_base) + (tunnel_1 * H_interaction)
    
    if idx < steps - 1:
        res_1 = mesolve(H_inst_1, rho_sub_1, [0, dt], c_ops, e_ops=[])
        rho_sub_1 = res_1.states[-1]

# =============================================================================
# 5. POST-PROCESSING AND PLOTTING
# =============================================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Global System Clock (Kāla Axis)', fontsize=12)
ax1.set_ylabel('Substrate Metrics', color=color, fontsize=12)
ax1.plot(times, coherence_history_1, color=color, linewidth=2.5, label='Coherence (Prakriti)')
ax1.plot(times, karmic_load_history, color='tab:orange', linestyle='-.', linewidth=2.0, label='Karmic Load (Integral Size)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.4)

ax2 = ax1.twinx()  
ax2.set_ylabel('Cognitive Drive Metrics', color='black', fontsize=12)
ax2.plot(times, kl_divergence_history, color='tab:purple', linestyle='--', linewidth=2, label='Effective KL Divergence')
ax2.plot(times, delta_history_1, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ(t)')

# Mark the Bhakti-yoga intervention point
ax2.axvline(x=11.0, color='gold', linestyle='-', linewidth=2.5, label='Bhakti Surrender Trigger (t=11)')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Non-Markovian Memory Integration with Bhakti-bīja Neutralization\nAbsolute Dissolution of Karmic Load Across Transition Horizons', fontsize=13, fontweight='bold')
fig.tight_layout()

output_filename = 'karmic_kernel_profile.png'
plt.savefig(output_filename, dpi=300)
print(f"Non-Markovian history convolution completed. Output saved to: {output_filename}")
