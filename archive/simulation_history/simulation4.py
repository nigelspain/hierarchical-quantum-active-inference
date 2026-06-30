import numpy as np
import matplotlib
# Force a clean file-based rendering backend to avoid GUI/X11 environment crashes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity
from scipy.linalg import logm

# =============================================================================
# 1. PARAMETERS & CONFIGURATION (Contemplative Processing Architecture)
# =============================================================================
steps = 400
times = np.linspace(0, 10.0, steps)
dt = times[1] - times[0]

# Physical coupling and open system dissipation variables (Prakriti Baseline)
gamma_phi = 2.0       # Strong measurement dephasing
Gamma_down = 1.0      # Energy relaxation rate of the register
t_coupling = 2.5      # Maximum interaction strength at the boundary

# Cognitive tuning parameters
Buddhi_tolerance = 1e-4  # Convergence threshold for Buddhi's decisive matrix
learning_rate = 0.01     # Lowered to make Buddhi highly contemplative
beta_sensitivity = 15.0  # Controls the sharpness of the Ahankara gate trigger
div_threshold = 0.05     # Sensitivity boundary to spark systemic doubt

# =============================================================================
# 2. HILBERT SPACE & OPERATOR SETUP
# =============================================================================
# Substrate (Prakriti): Two-level system representing Majorana parity boundaries
sigma_z_sub = Qobj([[1, 0], [0, -1]])  

# Register (Manas/Buddhi Interface): Quantum Dot creation/annihilation operators
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

# Global 4x4 Tensor Product Matrices
H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())

# Lindblad Environmental Dissipation Channels acting on the Register
c_ops = [
    np.sqrt(2 * gamma_phi) * tensor(identity(2), n_dot),   # Charge dephasing
    np.sqrt(Gamma_down) * tensor(identity(2), d_operator)  # Energy relaxation
]

# =============================================================================
# 3. INITIAL STATE SETUP (Uncollapsed Superposition)
# =============================================================================
# Substrate begins in a pure non-local coherent state; Quantum dot is empty
psi_initial = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))
current_rho = psi_initial * psi_initial.dag()

# Initialize Buddhi's historical tracking matrix as a completely mixed state
rho_buddhi = Qobj(identity(2).data / 2.0)

# Data arrays for visual tracking
coherence_history = []
kl_divergence_history = []
delta_history = []

# =============================================================================
# 4. ITERATIVE COGNITIVE LOOP (Manas-to-Buddhi Dynamic Feedback)
# =============================================================================
print("Executing autopoietic cognitive loop...")
for idx in range(steps):
    # Tracing out the register to isolate the fluid mind (Manas) state space
    rho_manas = current_rho.ptrace(0)
    coherence_history.append(np.abs(rho_manas[0, 1]))
    
    # Extract dense arrays for standard matrix log calculation
    m_manas = rho_manas.full()
    m_buddhi = rho_buddhi.full()
    
    # Calculate Quantum Relative Entropy (Kullback-Leibler Divergence)
    eps = 1e-10
    log_manas = logm(m_manas + eps * np.eye(2))
    log_buddhi = logm(m_buddhi + eps * np.eye(2))
    kl_div = np.abs(np.trace(m_manas @ (log_manas - log_buddhi)))
    kl_divergence_history.append(kl_div)
    
    # Buddhi integrates the fluid variations of Manas via an accumulation moving average
    rho_buddhi = (1.0 - learning_rate) * rho_buddhi + learning_rate * rho_manas
    
    # Ahankara Controller Logic: Map cognitive divergence to physical gate voltages
    if kl_div > Buddhi_tolerance:
        # Sigmoid function maps systemic doubt to high detuning values
        current_delta = 5.0 * (1.0 / (1.0 + np.exp(-beta_sensitivity * (kl_div - div_threshold))))
    else:
        current_delta = 0.0  # Total intellectual resolution (Nirnaya) achieved
        
    delta_history.append(current_delta)
    
    # Tunneling amplitude scales inversely to protect or collapse the state
    current_tunneling = t_coupling * (1.0 - (current_delta / 5.0))
    
    # Reconstruct the effective Hamiltonian for this specific time increment dt
    H_inst = (current_delta * H_reg_base) + (current_tunneling * H_interaction)
    
    # Step the master equation solver forward unitarily by one slice of dt
    if idx < steps - 1:
        res = mesolve(H_inst, current_rho, [0, dt], c_ops, e_ops=[])
        current_rho = res.states[-1]

# =============================================================================
# 5. POST-PROCESSING AND GRAPHICAL PLOTTING
# =============================================================================
fig, ax1 = plt.subplots(figsize=(11, 6))

color = 'tab:blue'
ax1.set_xlabel('Simulation Time (t)', fontsize=12)
ax1.set_ylabel('Substrate Coherence |ρ_io| (Prakriti Baseline)', color=color, fontsize=12)
ax1.plot(times, coherence_history, color=color, linewidth=2.5, label='Coherence (Prakriti)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()  
color = 'tab:purple'
ax2.set_ylabel('Quantum Relative Entropy / Detuning Δ', color=color, fontsize=12)
ax2.plot(times, kl_divergence_history, color=color, linestyle='--', linewidth=2, label='KL Divergence (Manas || Buddhi)')
ax2.plot(times, delta_history, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ')
ax2.tick_params(axis='y', labelcolor=color)

# Consolidated legend layout
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Evolved Manas-to-Buddhi Architectural Simulation\nContemplative Intellect Layer Extending Computational Superposition', fontsize=14, fontweight='bold')
fig.tight_layout()

# Save the finalized plot directly to the drive to avoid GUI backend dependency
output_filename = 'buddhi_transition_profile.png'
plt.savefig(output_filename, dpi=300)
print(f"Simulation completed cleanly! Graphical matrix output saved to: {output_filename}")
