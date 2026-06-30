import numpy as np
import qutip as qt
import time
import matplotlib
# Force Matplotlib to use the 'Agg' backend to safely render in headless sandboxes
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run_high_fidelity_validation():
    print("="*70)
    print("RUNNING HIGH-FIDELITY SYNCHRONIZED TENSOR & MEMORY BENCHMARK")
    print("VĀSUDEVA STATE AND KRONECKER TENSOR-PRODUCT SCALING SIMULATION")
    print("="*70)

    # PART 1: VERIFICATION OF CHITTA TENSOR SCALING (MICRO-TO-MACROCOSM)
    rho_chitta_seed = qt.rand_dm(4)
    identity_macro = qt.identity(2)
    identity_sub2 = qt.identity(4)

    rho_chitta_scaled = qt.tensor(identity_macro, rho_chitta_seed, identity_sub2)
    assert rho_chitta_scaled.shape == (32, 32), "Tensor dimensionality scaling failed!"
    print(f" -> Chitta Matrix successfully scaled from 4x4 to hierarchical {rho_chitta_scaled.shape}")

    # PART 2: O(1) PSEUDO-MODE SPECTRUM VS VOLTERRA CONVOLUTION
    T, N = 5.0, 100
    dt = T / N
    times = np.linspace(0, T, N)
    M = 12
    tau_modes = np.logspace(np.log10(dt), np.log10(4.5), M)
    weights = np.ones(M) / M

    # State trace definition: Ahaṅkāra vs Vāsudeva phases
    state_traces = []
    for t_val in times:
        if t_val < T / 2.0:
            state_traces.append(1.0 + 0.2 * np.sin(2 * np.pi * t_val / (T / 2.0)))
        else:
            state_traces.append(1.0)
    state_traces = np.array(state_traces)

    # Pre-calculate time-dependent Bhakti-bīja gating profile for unified execution
    B_profile = np.array([0.5 if t_val >= T / 2.0 else 1.0 for t_val in times])

    # Backend A: Exactly Synchronized Piecewise Volterra Path-Integral, O(t^2)
    t_start_volterra = time.time()
    volterra_karmic_load = np.zeros(N)
    for t_idx in range(N):
        integral_sum = 0.0
        for j in range(M):
            mode_sum = 0.0
            for k in range(t_idx + 1):
                steps_remaining = t_idx - k
                decay_to_now = np.exp(-steps_remaining * dt / tau_modes[j])
                exp_factor = np.exp(-dt / tau_modes[j])
                gain_factor = tau_modes[j] * (1.0 - exp_factor)
                
                # FIXED: The historical memory point 'k' must respect its respective gating state
                mode_sum += state_traces[k] * B_profile[k] * weights[j] * gain_factor * decay_to_now
            integral_sum += mode_sum
        volterra_karmic_load[t_idx] = integral_sum
    t_end_volterra = time.time()

    # Backend B: Optimized Parallel Samskara State-Space Spectrum, O(1)
    t_start_samskara = time.time()
    samskara_buffers = np.zeros(M)
    samskara_karmic_load = np.zeros(N)
    for t_idx in range(N):
        rho_trace = state_traces[t_idx]
        B_t = B_profile[t_idx]

        for j in range(M):
            exp_factor = np.exp(-dt / tau_modes[j])
            gain_factor = tau_modes[j] * (1.0 - exp_factor)
            
            # Recursive state update equation integrated with Bhakti-bīja multiplier
            samskara_buffers[j] = (samskara_buffers[j] * exp_factor) + B_t * (rho_trace * weights[j] * gain_factor)
        samskara_karmic_load[t_idx] = np.sum(samskara_buffers)
    t_end_samskara = time.time()

    # PART 3: NUMERICAL CONVERGENCE ASSERTION
    abs_numerical_deviation = np.max(np.abs(volterra_karmic_load - samskara_karmic_load))
    print("\n" + "="*70)
    print("                  LIVE SIMULATION EXECUTION METRICS")
    print("="*70)
    print(f" -> Volterra Compute Horizon (O(t^2)) : {t_end_volterra - t_start_volterra:.5f} seconds")
    print(f" -> Samskara Spectrum Update (O(1))   : {t_end_samskara - t_start_samskara:.5f} seconds")
    print(f" > Absolute Numerical Discretization Dev: {abs_numerical_deviation:.2e}")
    print("="*70)
    
    # Machine precision or tight step-integration boundaries usually sit securely below 1e-14
    if abs_numerical_deviation < 1e-10:
        print(" STATUS LOG: SUCCESS (O(1) Memory Engine track verified with clean synchronization)")
    else:
        print(" STATUS LOG: WARNING (Numerical variance threshold exceeded)")
    print("="*70)

    # Regenerate plot without unphysical spikes
    fig = plt.figure(figsize=(12, 6))
    plt.plot(times, volterra_karmic_load, 'b-', linewidth=3, label='Synchronized Volterra Baseline ($O(t^2)$)')
    plt.plot(times, samskara_karmic_load, 'r--', linewidth=2, label='Optimized Samskara Spectrum Backend ($O(1)$)')
    
    plt.axvline(x=T/2.0, color='g', linestyle=':', linewidth=2, label='Vāsudeva / Bhakti Gating Boundary')
    plt.text(1.0, 0.5 * np.max(samskara_karmic_load), "Ahaṅkāra Fluctuation Phase\n(Egoic Search)", fontsize=9, color='blue', bbox=dict(facecolor='white', alpha=0.6))
    plt.text(2.8, 0.5 * np.max(samskara_karmic_load), "Vāsudeva Alignment Phase\n(Sattva Equilibrium)", fontsize=9, color='darkgreen', bbox=dict(facecolor='white', alpha=0.6))

    plt.title('Memory Backend Verification: Vāsudeva Structural Alignment Scan\nPerfect Unified Synchronization Across Compute Horzon Backends', fontsize=12)
    plt.xlabel('Simulation Time Timeline (t) [Kāla Axis]', fontsize=10)
    plt.ylabel('Compiled Karmic Load (Integral Size)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='lower left')
    plt.tight_layout()

    output_filename = 'memory_verification.png'
    plt.savefig(output_filename, dpi=300)
    print(f"\n[FILE WRITE] Graphical plot successfully saved to disk as: {output_filename}")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_high_fidelity_validation()
