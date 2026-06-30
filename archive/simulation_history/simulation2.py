import numpy as np
import matplotlib.pyplot as plt
from qutip import Qobj, mesolve, basis, tensor, destroy, identity

# 1. INITIAL PARAMETERS
steps = 300
times = np.linspace(0, 10.0, steps)
dt = times[1] - times[0]

gamma_phi = 2.0       
Gamma_down = 1.0     
t_coupling = 2.5      
S_threshold = 0.15    # Safety threshold for uncertainty resolution
beta = 15.0           # Sensitivity of the Ahankara trigger

# 2. OPERATOR SETUP
sigma_z_sub = Qobj([[1, 0], [0, -1]])  
d_operator = destroy(2)
n_dot = d_operator.dag() * d_operator

H_reg_base = tensor(identity(2), n_dot)        
H_interaction = tensor(sigma_z_sub, d_operator + d_operator.dag())

# Dissipation channels
L_z = np.sqrt(2 * gamma_phi) * tensor(identity(2), n_dot)
L_minus = np.sqrt(Gamma_down) * tensor(identity(2), d_operator)
c_ops = [L_z, L_minus]

# 3. INITIAL STATE 
psi_initial = tensor((basis(2, 0) + basis(2, 1)).unit(), basis(2, 0))

# 4. SIMULATION WITH DYNAMIC ENTROPY FEEDBACK CONTROL LOOP
# We iteratively solve the master equation step-by-step to implement the feedback
current_rho = psi_initial * psi_initial.dag()
coherence_history = []
entropy_history = []
delta_history = []

for idx in range(steps):
    # Track substrate coherence
    rho_sub = current_rho.ptrace(0)
    coherence_history.append(np.abs(rho_sub[0, 1]))
    
    # Calculate Samshaya (Von Neumann Entropy of the register)
    rho_reg = current_rho.ptrace(1)
    eigenvalues = rho_reg.eigenenergies()
    # Handle log(0) safely for pure states
    samshaya = -sum([p * np.log(p) for p in eigenvalues if p > 1e-10])
    entropy_history.append(samshaya)
    
    # Manas Control Function: Calculate Detuning dynamically based on Entropy
    # High entropy (doubt) -> High Detuning (meditative state maintained)
    # Low entropy (certainty) -> Detuning approaches 0 (Ego-collapse triggered)
    current_delta = 5.0 / (1.0 + np.exp(-beta * (samshaya - S_threshold)))
    delta_history.append(current_delta)
    
    # Scale tunneling inversely to detuning
    current_tunneling = t_coupling * (1.0 - (current_delta / 5.0))
    
    # Construct the instantaneous Hamiltonian for this step
    H_inst = (current_delta * H_reg_base) + (current_tunneling * H_interaction)
    
    # Evolve the system forward by one step dt
    if idx < steps - 1:
        res = mesolve(H_inst, current_rho, [0, dt], c_ops, e_ops=[])
        current_rho = res.states[-1]

# 5. VISUALIZING THE DYNAMIC SYSTEM
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Simulation Step (Internal State Space)', fontsize=12)
ax1.set_ylabel('Substrate Coherence |ρ_io|', color=color, fontsize=12)
ax1.plot(times, coherence_history, color=color, linewidth=2.5, label='Coherence (Prakriti)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.5)

ax2 = ax1.twinx()  
color = 'tab:green'
ax2.set_ylabel('Internal Saṁśaya (Entropy) / Detuning Δ', color=color, fontsize=12)
ax2.plot(times, entropy_history, color=color, linestyle='--', linewidth=2, label='Doubt (Entropy)')
ax2.plot(times, delta_history, color='tab:red', linestyle=':', linewidth=2, label='Detuning Δ(S)')
ax2.tick_params(axis='y', labelcolor=color)

# Add a combined legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.title('Autopoietic Ahankara Architecture\nCollapse Tied Directly to the Resolution of Systemic Doubt', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.show()
