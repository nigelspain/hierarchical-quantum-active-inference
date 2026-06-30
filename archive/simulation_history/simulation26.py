import numpy as np
import qutip as qt
import matplotlib
# 'Agg' ensures the script runs in all environments without GUI dependencies
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_variational_attractor_simulation():
    print("="*80)
    print("RUNNING VARIATIONAL ATTRACTOR CONTROL ENGINE (SIMULATION_26.PY)")
    print("="*80)
    
    # 1. TIMESTEP AND SIMULATION PARAMETERS
    T, N = 15.0, 300
    times = np.linspace(0, T, N)
    d_kl_path = np.zeros(N)
    
    # 2. SUBSTRATE INITIALIZATION
    rho_initial = qt.ket2dm((qt.basis(2, 0) + qt.basis(2, 1)).unit())
    rho_supreme = qt.ket2dm(qt.basis(2, 0))
    rho_buddhi = rho_initial
    
    # 3. DYNAMIC SIMULATION LOOP
    for i in range(N):
        # Manas-driven sensory oscillation
        oscillation = 0.15 * np.sin(1.5 * np.pi * times[i] / T)
        simulated_coherence = np.clip(0.5 * np.exp(-0.1 * times[i]) + oscillation, 0.001, 0.499)
        rho_manas = qt.Qobj([[0.5, simulated_coherence], [simulated_coherence, 0.5]])
        
        # Buddhi Register Update (Historical Synthesis)
        eta = 0.15
        rho_buddhi = (1.0 - eta) * rho_buddhi + eta * rho_manas
        
        # Data Commitment: Store systemic divergence
        d_kl_path[i] = qt.entropy_relative(rho_buddhi, rho_supreme)
    
    # SANITY CHECK: Print values to console to bypass graphical display issues
    print(f"Simulation Data Sample (First 5 steps): {d_kl_path[:5]}")
    print(f"Final Divergence: {d_kl_path[-1]:.6e}")

    # 4. ROBUST RENDERING
    plt.figure(figsize=(10, 6))
    plt.plot(times, d_kl_path, label='Systemic Doubt ($D_{KL}$)', color='darkblue')
    plt.title('Buddhi Register: Convergence towards Supreme Attractor')
    plt.xlabel('Temporal Progression ($T$)')
    plt.ylabel('Quantum Relative Entropy')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Save explicitly
    plt.savefig('convergence_darshana_final.png', dpi=300)
    print("Visual ledger 'convergence_darshana_final.png' successfully updated and saved to disk.")

if __name__ == "__main__":
    run_variational_attractor_simulation()
