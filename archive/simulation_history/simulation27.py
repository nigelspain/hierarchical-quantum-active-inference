import sys

print("Initializing simulation environment...")
sys.stdout.flush()

try:
    import numpy as np
    import qutip as qt
    import matplotlib
    # Force a headless background engine to guarantee stability in terminal envs
    matplotlib.use('Agg') 
    import matplotlib.pyplot as plt
    print("All core scientific dependencies loaded cleanly.")
    sys.stdout.flush()
except ImportError as e:
    print(f"\n[FATAL ERROR] Dependency missing or broken: {e}")
    sys.exit(1)

def run_variational_attractor_simulation():
    print("\n" + "="*80)
    print("COMPUTING REGULARIZED NON-SINGULAR VARIATIONAL TRACE ENGINE")
    print("="*80)
    sys.stdout.flush()
    
    # -------------------------------------------------------------------------
    # 1. TIME HORIZONS AND PSEUDO-MODE PARAMETERS
    # -------------------------------------------------------------------------
    T = 15.0
    N = 300
    dt = T / N
    times = np.linspace(0, T, N)
    
    M = 12
    tau_modes = np.logspace(np.log10(dt), np.log10(4.5), M)
    weights = np.ones(M) / M
    samskara_buffers = np.zeros(M)
    
    # Non-equilibrium hyperparameters
    alpha = 0.4                  
    quantum_thermal_cost = 1.5   
    gamma_dephasing_baseline = 0.05
    epsilon = 1e-9  # Identity regularizer to prevent log(0) infinity explosions
    
    # Quantum State Substrates
    psi_initial = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    rho_initial = qt.ket2dm(psi_initial)
    
    psi_supreme = qt.basis(2, 0)
    rho_supreme = qt.ket2dm(psi_supreme)
    
    # Apply regularizing mixed floor to rho_supreme to ensure log-space stability
    rho_supreme_reg = (1.0 - epsilon) * rho_supreme + epsilon * (qt.identity(2) / 2.0)
    
    rho_manas = rho_initial
    rho_buddhi = rho_initial
    
    # Track metrics
    coherence_prakriti = np.zeros(N)
    karmic_load_integral = np.zeros(N)
    d_kl_supreme_path = np.zeros(N)
    b_coefficient_path = np.zeros(N)
    gamma_eff_path = np.zeros(N)
    
    b_coefficient_old = 1.0
    
    print(" -> Commencing continuous numerical propagation loop...")
    sys.stdout.flush()
    
    # -------------------------------------------------------------------------
    # 2. NUMERICAL PROPAGATION LOOP
    # -------------------------------------------------------------------------
    for t_idx in range(N):
        t_val = times[t_idx]
        
        oscillation = 0.15 * np.sin(1.5 * np.pi * t_val / T)
        simulated_coherence = 0.5 * np.exp(-0.1 * t_val) + oscillation
        simulated_coherence = np.clip(simulated_coherence, 0.001, 0.499)
        
        rho_manas = qt.Qobj([[0.5, simulated_coherence], 
                             [simulated_coherence, 0.5]])
        
        eta = 0.15
        # Regularize the running intellectual belief matrix to avoid numerical voids
        rho_buddhi = (1.0 - eta) * rho_buddhi + eta * rho_manas
        rho_buddhi_reg = (1.0 - epsilon) * rho_buddhi + epsilon * (qt.identity(2) / 2.0)
        
        # Compute Kullback-Leibler Relative Entropy using regularized paths
        d_kl_supreme = qt.entropy_relative(rho_buddhi_reg, rho_supreme_reg)
        
        # Dynamic Bhakti-bīja smooth phase transition mapping
        if d_kl_supreme < 1e-4:
            b_coefficient = 0.0
        else:
            b_coefficient = np.exp(-alpha / d_kl_supreme)
            
        if t_val < 6.0:
            b_coefficient = 1.0
            
        # Calculate memory dissipation rate to derive Landauer heat penalty
        b_derivative = (b_coefficient - b_coefficient_old) / dt
        gamma_dephasing_eff = gamma_dephasing_baseline + np.abs(b_derivative) * quantum_thermal_cost
        
        rho_trace_scalar = np.abs(rho_manas[0, 1])
        
        # Propagate Samskara exponential memory channels
        for j in range(M):
            exp_factor = np.exp(-dt / tau_modes[j])
            gain_factor = tau_modes[j] * (1.0 - exp_factor)
            samskara_buffers[j] = (samskara_buffers[j] * exp_factor) + \
                                  (rho_trace_scalar * weights[j] * gain_factor * b_coefficient)
                                  
        total_karmic_load = np.sum(samskara_buffers)
        
        # Record trace arrays
        coherence_prakriti[t_idx] = rho_trace_scalar
        karmic_load_integral[t_idx] = total_karmic_load
        d_kl_supreme_path[t_idx] = d_kl_supreme
        b_coefficient_path[t_idx] = b_coefficient
        gamma_eff_path[t_idx] = gamma_dephasing_eff
        
        b_coefficient_old = b_coefficient

    print(" -> Numerical array generation finalized cleanly.")
    print(f" -> Terminal Attractor Divergence (D_KL): {d_kl_supreme_path[-1]:.4e}")
    print(f" -> Terminal Memory Kernel Boundary (B):  {b_coefficient_path[-1]:.4e}")
    sys.stdout.flush()

    # -------------------------------------------------------------------------
    # 3. CLASSIC STANDALONE COMPATIBLE PLOTTING ENGINE
    # -------------------------------------------------------------------------
    print(" -> Building dual-panel visualization figures...")
    sys.stdout.flush()
    
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
        
        # Switched to traditional base web-safe colors (blue, gold, purple, orange, red)
        ax1.plot(times, coherence_prakriti, label="Substrate Coherence (Prakriti)", color="blue", lw=2)
        ax1.plot(times, b_coefficient_path, label="Bhakti-bīja Coefficient (B)", color="gold", lw=2.5, linestyle="--")
        ax1.plot(times, d_kl_supreme_path, label="D_KL to Supreme Prior", color="purple", lw=1.5, linestyle=":")
        ax1.set_title("Variational Attractor Framework: Continuous Cognitive Optimization", fontsize=12, fontweight="bold")
        ax1.set_ylabel("Amplitude / Boundary Metrics", fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc="upper right")
        
        ax2.plot(times, karmic_load_integral, label="Karmic Load (Memory Buffer Size)", color="orange", lw=2)
        ax2.plot(times, gamma_eff_path, label="Effective Environmental Dephasing (g_eff)", color="red", lw=2, linestyle="-.")
        ax2.set_xlabel("Simulation Time (t)", fontsize=10)
        ax2.set_ylabel("Thermodynamic / Memory Metrics", fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc="upper right")
        
        plt.tight_layout()
        
        output_filename = "variational_attractor_output.png"
        plt.savefig(output_filename, dpi=300)
        print(f"\n[SUCCESS] Matrix ledger exported to: '{output_filename}'")
        print("="*80 + "\n")
        sys.stdout.flush()
    except Exception as image_err:
        print(f"\n[ERROR] Matplotlib failed to compile or save image file: {image_err}")
        sys.stdout.flush()

if __name__ == "__main__":
    run_variational_attractor_simulation()
