import numpy as np
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity
from scipy.linalg import logm

# 1. INITIAL PARAMETERS
steps = 300
times = np.linspace(0, 10.0, steps)
dt = times[1] - times[0]

gamma_phi = 2.0       
Gamma_down = 1.0     
t_coupling = 2.5      
Buddhi_tolerance = 1e-3  # Convergence threshold for Buddhi's decisive matrix

# 2. OPERATOR SETUP
sigma_z_sub = Qobj([[1, 0], [0, -1]])  
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())

c_ops = [
    np.sqrt(2 * gamma_phi) * tensor(identity(2), n_dot),
    np.sqrt(Gamma_down) * tensor(identity(2), d_operator)
]

# 3. INITIAL STATES
current_rho = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))
current_rho = current_rho * current_rho.dag()

# Initialize Buddhi's tracking matrix as a completely mixed identity state
rho_buddhi = Qobj(identity(2).data / 2.0)

coherence_history = []
kl_divergence_history = []
delta_history = []

# 4. ITERATIVE COGNITIVE LOOP: MANAS TO BUDDHI TRANSITION
for idx in range(steps):
    # Extract the fluid state from the substrate (Manas sampling)
    rho_manas = current_rho.ptrace(0)
    coherence_history.append(np.abs(rho_manas[0, 1]))
    
    # --- BUDDHI DECISIVE MATRIX CALCULATION ---
    # Convert QuTiP objects to standard NumPy arrays for matrix logarithm operations
    m_manas = rho_manas.full()
    m_buddhi = rho_buddhi.full()
    
    # Calculate Quantum Relative Entropy (KL Divergence) between Manas and Buddhi
    # Adds small epsilon to prevent log of zero eigenvalues
    eps = 1e-10
    log_manas = logm(m_manas + eps * np.eye(2))
    log_buddhi = logm(m_buddhi + eps * np.eye(2))
    kl_div = np.abs(np.trace(m_manas @ (log_manas - log_buddhi)))
    kl_divergence_history.append(kl_div)
    
    # Buddhi updates its internal belief matrix via a historical exponential moving average
    # This represents the transition of fluid samples into crystallized intelligence
    learning_rate = 0.05
    rho_buddhi = (1.0 - learning_rate) * rho_buddhi + learning_rate * rho_manas
    
    # --- PHYSICAL PARAMETER CONTROLLER ---
    # If the divergence is high, Manas is still oscillating (High Detuning Delta)
    # When divergence stabilizes (kl_div drops), Buddhi locks the decision (Delta -> 0)
    if kl_div > Buddhi_tolerance:
        current_delta = 5.0 * (1.0 / (1.0 + np.exp(-10.0 * (kl_div - 0.2))))
    else:
        current_delta = 0.0  # Buddhi absolute determination triggered
        
    delta_history.append(current_delta)
    current_tunneling = t_coupling * (1.0 - (current_delta / 5.0))
    
    # Construct and evolve the instantaneous Hamiltonian step
    H_inst = (current_delta * H_reg_base) + (current_tunneling * H_interaction)
    if idx < steps - 1:
        res = mesolve(H_inst, current_rho, [0, dt], c_ops, e_ops=[])
        current_rho = res.states[-1]

# 5. PLOTTING THE COGNITIVE TRANSITION
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Simulation Step (Internal State Space)', fontsize=12)
ax1.set_ylabel('Substrate Coherence |ρ_io| (Prakriti)', color=color, fontsize=12)
ax1.plot(times, coherence_history, color=color, linewidth=2.5, label='Coherence')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()  
color = 'tab:purple'
ax2.set_ylabel('Quantum Relative Entropy / Detuning Δ', color=color, fontsize=12)
ax2.plot(times, kl_divergence_history, color=color, linestyle='--', linewidth=2, label='KL Divergence (Manas || Buddhi)')
ax2.plot(times, delta_history, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ')
ax2.tick_params(axis='y', labelcolor=color)

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Mathematical Transition Framework: Manas to Buddhi\nDecisive Matrix Synthesis Regulating Wave Function Collapse', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.show()
