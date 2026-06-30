import numpy as np
import matplotlib
# Force a clean file-based rendering backend to avoid GUI/X11 environment crashes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity, fidelity
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

# Chitta Substrate parameters (Subconscious memory pool)
lambda_0 = 0.15          # Maximum baseline learning rate for structural engraving (Smṛti)

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
# 3. INITIAL STATE SETUP & CHITTA SUBSTRATE DECLARATION
# =============================================================================
# Substrate begins in a pure non-local coherent state; Quantum dot is empty
psi_initial = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))

# Explicitly cast current_rho as a 4x4 density matrix mapping [[2, 2], [2, 2]]
current_rho = psi_initial * psi_initial.dag()

# Initialize Buddhi's historical tracking matrix (2x2 subsystem projection)
rho_buddhi = Qobj(identity(2).data / 2.0)

# EXPLICIT 4x4 CHITTA MATRIX DECLARATION (The Mahat-tattva memory background)
# Enforced with explicit [[2,2],[2,2]] dimensions to guarantee fidelity matrix matching
rho_chitta = tensor(identity(2), identity(2)).unit()
rho_chitta = rho_chitta * rho_chitta.dag()

# Data arrays for visual tracking
coherence_history = []
kl_divergence_history = []
delta_history = []
chitta_fidelity_history = []

# =============================================================================
# 4. ITERATIVE COGNITIVE LOOP (Chitta-Filtered Feedback Mechanics)
# =============================================================================
print("Executing autopoietic cognitive loop with Chitta Substrate...")

for idx in range(steps):
    # Enforce current_rho to maintain a full density matrix format
    if current_rho.type == 'ket':
        current_rho = current_rho * current_rho.dag()

    # Trace out the register to isolate the fluid mind (Manas) state space (2x2)
    rho_manas = current_rho.ptrace(0)
    coherence_history.append(np.abs(rho_manas[0, 1]))
    
    # Extract dense arrays for standard matrix log calculation
    m_manas = rho_manas.full()
    m_buddhi = rho_buddhi.full()
    
    # Calculate Base Quantum Relative Entropy (KL Divergence) between Manas and Buddhi
    eps = 1e-10
    log_manas = logm(m_manas + eps * np.eye(2))
    log_buddhi = logm(m_buddhi + eps * np.eye(2))
    kl_div_base = np.abs(np.trace(m_manas @ (log_manas - log_buddhi)))
    
    # Calculate Quantum Fidelity between current global state and Chitta substrate (Both 4x4)
    f_chitta = fidelity(current_rho, rho_chitta)
    chitta_fidelity_history.append(f_chitta)
    
    # FILTER ACTION: If path is familiar (f_chitta -> 1), divergence drops rapidly.
    kl_div_effective = kl_div_base * (1.0 - f_chitta)
    kl_divergence_history.append(kl_div_effective)
    
    # Buddhi updates its internal belief matrix via its standard accumulation rate
    rho_buddhi = (1.0 - learning_rate) * rho_buddhi + learning_rate * rho_manas
    
    # Ahankara Controller Logic governed by Chitta-filtered Effective Divergence
    if kl_div_effective > Buddhi_tolerance:
        # Sigmoid function maps systemic doubt to high detuning values
        current_delta = 5.0 * (1.0 / (1.0 + np.exp(-beta_sensitivity * (kl_div_effective - div_threshold))))
    else:
        current_delta = 0.0  # Intellectual resolution (Nirnaya) reached!
        
    delta_history.append(current_delta)
    current_tunneling = t_coupling * (1.0 - (current_delta / 5.0))
    
    # Reconstruct the effective Hamiltonian for this specific step dt
    H_inst = (current_delta * H_reg_base) + (current_tunneling * H_interaction)
    
    # Step the master equation solver forward unitarily by one slice of dt
    if idx < steps - 1:
        res = mesolve(H_inst, current_rho, [0, dt], c_ops, e_ops=[])
        current_rho = res.states[-1]

# =============================================================================
# 5. SMṚTI (Memory Engraving State Update at Collapse Point)
# =============================================================================
if current_rho.type == 'ket':
    current_rho = current_rho * current_rho.dag()

# Compute the fidelity-driven dynamic learning rate lambda_n for the next cycle
lambda_n = lambda_0 * (1.0 - fidelity(current_rho, rho_chitta))

# Convex Bipartite Blending Function to permanently store the structural residue
rho_chitta = (1.0 - lambda_n) * rho_chitta + lambda_n * current_rho

print(f"Smṛti Complete. Dynamic Memory Gate λ_n calculated as: {lambda_n:.4f}")

# =============================================================================
# 6. POST-PROCESSING AND GRAPHICAL PLOTTING
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
ax2.set_ylabel('Quantum Metrics / Detuning Δ', color=color, fontsize=12)
ax2.plot(times, kl_divergence_history, color=color, linestyle='--', linewidth=2, label='Effective KL Divergence')
ax2.plot(times, delta_history, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ')
ax2.plot(times, chitta_fidelity_history, color='tab:orange', linestyle='-.', linewidth=1.5, label='Chitta Fidelity')
ax2.tick_params(axis='y', labelcolor=color)

# Consolidated legend layout
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Chitta-Integrated Cognitive Simulation Architecture\nSubconscious Matrix Regulating Effective Divergence and Decision Horizons', fontsize=14, fontweight='bold')
fig.tight_layout()

output_filename = 'buddhi_chitta_profile.png'
plt.savefig(output_filename, dpi=300)
print(f"Graphical matrix file exported successfully to: {output_filename}")
