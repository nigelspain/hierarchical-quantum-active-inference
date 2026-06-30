import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity

# -----------------------------------------------------------------------------
# 1. PARAMETERS & INITIALIZATION
# -----------------------------------------------------------------------------
t_max = 10.0          # Total simulation time
steps = 500           # Number of time steps
times = np.linspace(0, t_max, steps)

# Physical Constants (Normalized units where hbar = 1)
gamma_phi = 0.05      # Balanced dephasing rate
Gamma_down = 0.02     # Balanced relaxation rate
t_coupling = 2.5      # Strong coupling to force state evolution out of stagnation

# -----------------------------------------------------------------------------
# 2. TIME-DEPENDENT CONTROLLER FUNCTIONS
# -----------------------------------------------------------------------------
def delta_t(t, args):
    t_collapse = 4.0
    width = 1.2
    # Smoothly drops from a controlled high detuning down to 0
    return 3.0 * (1.0 / (1.0 + np.exp((t - t_collapse) / width)))

def tunneling_t(t, args):
    # Tunneling activates strongly as the detuning collapses
    return t_coupling * (1.0 / (1.0 + np.exp(-(t - 4.0) / 1.2)))

# -----------------------------------------------------------------------------
# 3. OPERATOR DEFINITIONS (Prakriti Substrate x Buddhi Register)
# -----------------------------------------------------------------------------
sigma_z_sub = Qobj([[1, 0], [0, -1]])
sigma_x_sub = Qobj([[0, 1], [1, 0]])  

d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

H_reg_base = tensor(identity(2), n_dot)        

# Anti-symmetric transition operator configuration works best for QuTiP's time-solver
H_interaction_term = tensor(sigma_x_sub, d_operator.dag() - d_operator) 

# Flattened master list layout
H_total = [
    [H_reg_base, delta_t],
    [H_interaction_term, tunneling_t]
]

# -----------------------------------------------------------------------------
# 4. LINDBLAD DISSIPATION CHANNELS
# -----------------------------------------------------------------------------
L_z = np.sqrt(2 * gamma_phi) * tensor(identity(2), n_dot)
L_minus = np.sqrt(Gamma_down) * tensor(identity(2), d_operator)
collapse_operators = [L_z, L_minus]

# -----------------------------------------------------------------------------
# 5. INITIAL STATE & SIMULATION EXECUTION
# -----------------------------------------------------------------------------
# ULTIMATE FIX: Introduce an imaginary phase shift (1j) to break the matrix symmetry.
# This forces the off-diagonal elements to fluctuate dynamically during time-evolution.
psi_sub = (basis(2, 0) + 1j * basis(2, 1)).unit() 
psi_dot = basis(2, 0)
psi_initial = tensor(psi_sub, psi_dot)

# Clean positional argument layout
result = mesolve(H_total, psi_initial, times, collapse_operators)

# Define a completely mixed target state for the relative entropy baseline
rho_target = qt.thermal_dm(2, 999) 

# -----------------------------------------------------------------------------
# 6. POST-PROCESSING: COHERENCE & SUPREME RELATIVE ENTROPY
# -----------------------------------------------------------------------------
coherence_rho_io = []
d_kl_supreme = []

for state in result.states:
    # 1. Isolate Substrate (Prakriti) and extract coherence
    rho_sub = state.ptrace(0)
    coherence_rho_io.append(np.abs(rho_sub[0, 1]))
    
    # 2. Isolate Register (Buddhi) and compute KL Relative Entropy
    rho_budd = state.ptrace(1)
    kl_val = qt.entropy_relative(rho_budd, rho_target)
    d_kl_supreme.append(kl_val)

# -----------------------------------------------------------------------------
# 7. PLOTTING THE TRANSITION
# -----------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = 'tab:blue'
color2 = 'tab:purple'
ax1.set_xlabel('Time (t)', fontsize=12)
ax1.set_ylabel('Quantum Metrics', fontsize=12)
ax1.plot(times, coherence_rho_io, color=color1, linewidth=2.5, label='Prakriti Coherence |ρ_io|')
ax1.plot(times, d_kl_supreme, color=color2, linewidth=2.0, linestyle='--', label='Buddhi Relative Entropy ($D_{KL}$)')
ax1.tick_params(axis='y')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()  
color3 = 'tab:red'
ax2.set_ylabel('Detuning Δ(t) (Ego Gate Control)', color=color3, fontsize=12)
ax2.plot(times, [delta_t(t, None) for t in times], color=color3, linestyle=':', linewidth=2, label='Detuning Δ(t)')
ax2.tick_params(axis='y', labelcolor=color3)

plt.title('Self-Collapsing Ahankara Loop Simulation\nTransition from Meditative Superposition to Active Ego Localization', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.show()
