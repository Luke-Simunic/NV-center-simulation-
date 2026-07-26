import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh  # For Hermitian matrix diagonalization
from matplotlib.gridspec import GridSpec  # For arranging subplots
from scipy.integrate import solve_ivp  # To solve ODEs (Schrödinger equation)
from scipy.signal import argrelextrema  # To find local extrema
# Optional science plot style
# import scienceplots
# plt.style.use('science')

# Constants (in Hz)
D0 = 2.87e9       # Zero-field splitting of NV center ground state (Hz)
gamma_NV = 2.8e6  # NV gyromagnetic ratio (Hz/G)

class NVHamiltonian:
    def __init__(self):
        self.verbose = False  # Enables detailed Hamiltonian printing for debugging

    def build_hamiltonian(self, B_parallel, B_perpendicular=0,
                          sigma_parallel=0, sigma_x=0, sigma_y=0,
                          A_iso=0, print_matrix=False):
        """
        Construct the NV center Hamiltonian with given parameters.
        All terms are in frequency units (Hz).
        """

        # Diagonal terms: affected by axial magnetic field, strain, and hyperfine interaction
        a = D0 + sigma_parallel + gamma_NV * B_parallel + A_iso
        d = D0 + sigma_parallel - gamma_NV * B_parallel + A_iso

        # Off-diagonal terms:
        #   b handles B_perpendicular + sigma_y (complex)
        #   c handles sigma_x (real)
        b = (gamma_NV * B_perpendicular / np.sqrt(2)) - 1j * sigma_y
        b_star = np.conj(b)
        c = sigma_x

        # Construct full 3x3 complex Hermitian Hamiltonian
        H = np.array([
            [a, b, c],
            [b_star, 0 + A_iso, b],
            [c, b_star, d]
        ], dtype=complex)

        # Optional: print the matrix if debug flag or parameter is set
        if print_matrix or self.verbose:
            self._print_hamiltonian(H, B_parallel, B_perpendicular,
                                    sigma_parallel, sigma_x, sigma_y, A_iso)

        return H

    def _print_hamiltonian(self, H, B_parallel, B_perpendicular,
                           sigma_parallel, sigma_x, sigma_y, A_iso):
        """
        Nicely formatted printout of the Hamiltonian matrix and its components.
        """
        print("\n" + "=" * 60)
        print("NV Center Hamiltonian Composition:")
        print(f"B_parallel = {B_parallel} G, B_perpendicular = {B_perpendicular} G")
        print(f"Strain: sigma_parallel = {sigma_parallel} Hz, sigma_x = {sigma_x} Hz, sigma_y = {sigma_y} Hz")
        print(f"Hyperfine: A_iso = {A_iso} Hz")
        print("\nFull Hamiltonian Matrix (Hz):")
        for row in H:
            print("[", end="")
            for val in row:
                if np.iscomplex(val):
                    print(f"{val.real:12.2f}{val.imag:+12.2f}j", end=" ")
                else:
                    print(f"{val.real:12.2f}{' ' * 12}", end=" ")
            print("]")
        print("=" * 60 + "\n")

    def diagonalize(self, H):
        """
        Diagonalize the Hamiltonian to get eigenvalues and eigenvectors.
        """
        evals, evecs = eigh(H)
        return evals, evecs

    def plot_energy_levels_vs_field(self, B_range=(-10, 10), n_points=1000,
                                    B_perpendicular=0, sigma_parallel=0,
                                    sigma_x=0, sigma_y=0, A_iso=0):
        """
        Plot NV center energy levels as a function of B_parallel field.
        Useful for visualizing Zeeman and strain-induced level shifts.
        """
        B_values = np.linspace(B_range[0], B_range[1], n_points)
        energies = []

        # Loop over magnetic field values and compute eigenvalues
        for B in B_values:
            H = self.build_hamiltonian(B, B_perpendicular, sigma_parallel,
                                       sigma_x, sigma_y, A_iso)
            evals, _ = self.diagonalize(H)
            energies.append(evals)

        energies = np.array(energies).T  # Shape: (3, n_points)
        spin_labels = ['$m_s=0$', '$m_s=+1$', '$m_s=-1$']

        # Plotting
        plt.figure(figsize=(12, 8))
        for i in range(3):
            plt.plot(B_values, energies[i]/1e6, label=spin_labels[i], linewidth=2)
        plt.title(f'NV Center Energy Levels vs $B_\\parallel$\n'
                  f'(Strain: $\\sigma_x={sigma_x:.1e}$ Hz, $\\sigma_y={sigma_y:.1e}$ Hz, $B_\\perp={B_perpendicular:.1f}$ G)')
        plt.xlabel('Parallel Magnetic Field $B_\\parallel$ (G)')
        plt.ylabel('Energy (MHz)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        return B_values, energies

    def time_varying_strain_simulation(self, t_max=10, n_steps=2000,
                                       B_parallel=0, B_perpendicular=0,
                                       sigma_parallel=0, A_iso=0,
                                       strain_freq=1, strain_amp=1e6):
        """
        Simulate the NV center energy levels as a function of time-varying strain.
        sigma_x and sigma_y vary sinusoidally with time.
        """
        t_values = np.linspace(0, t_max, n_steps)
        # Define time-dependent strain components
        sigma_x_values = strain_amp * np.sin(2 * np.pi * strain_freq * t_values)
        sigma_y_values = strain_amp * np.cos(2 * np.pi * strain_freq * t_values)

        energies_vs_time = []

        for i, t in enumerate(t_values):
            # Print matrix at beginning, middle, and end for debugging
            print_matrix = (i == 0) or (i == len(t_values) // 2) or (i == len(t_values) - 1)
            H = self.build_hamiltonian(B_parallel, B_perpendicular,
                                       sigma_parallel,
                                       sigma_x_values[i], sigma_y_values[i],
                                       A_iso,
                                       print_matrix=print_matrix)
            evals, _ = self.diagonalize(H)
            energies_vs_time.append(evals)

        energies_vs_time = np.array(energies_vs_time).T  # Shape: (3, n_steps)

        # Plotting: energy levels
        fig = plt.figure(figsize=(15, 10))
        gs = GridSpec(2, 1, height_ratios=[2, 1])
        ax1 = fig.add_subplot(gs[0])
        spin_labels = ['$m_s=0$', '$m_s=+1$', '$m_s=-1$']
        for i in range(3):
            ax1.plot(t_values, energies_vs_time[i]/1e6, label=spin_labels[i], linewidth=2)
        ax1.set_title('Energy Levels Under Time-Varying Strain')
        ax1.set_ylim(-3000, 10000)
        ax1.set_ylabel('Energy (MHz)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plotting: strain signals
        ax2 = fig.add_subplot(gs[1])
        ax2.plot(t_values, sigma_x_values / 1e6, label=r'$\sigma_x(t)$ [MHz]', color='red')
        ax2.plot(t_values, sigma_y_values / 1e6, label=r'$\sigma_y(t)$ [MHz]', color='blue')
        ax2.set_xlabel('Time (arb. units)')
        ax2.set_ylabel('Strain (MHz)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        plt.tight_layout()
        plt.show()

        return t_values, energies_vs_time, sigma_x_values, sigma_y_values

    @staticmethod
    def find_anti_crossings(B_values, energies, threshold=1e7):
        """
        Identify anti-crossing points where the gap between energy levels
        reaches a local minimum below a defined threshold.
        """
        energies = np.atleast_2d(energies)
        if energies.shape[0] < energies.shape[1]:
            energies = energies.T  # Ensure rows = levels

        anti_crossings = []
        num_levels, num_points = energies.shape

        # Loop over adjacent levels
        for i in range(num_levels - 1):
            # Compute gap between adjacent levels
            gaps = np.abs(energies[i + 1] - energies[i])
            minima = argrelextrema(gaps, np.less)[0]  # Local minima indices

            for idx in minima:
                if gaps[idx] < threshold:
                    anti_crossings.append((B_values[idx], gaps[idx], i, i + 1))

        print(f"\nFound {len(anti_crossings)} anti-crossing(s):")
        for B, gap, i1, i2 in anti_crossings:
            print(f"Between levels {i1} and {i2} at B = {B:.2f} G with gap = {gap / 1e6:.3f} MHz")
        return anti_crossings
        def time_dependent_population(self, initial_state_index=1,
                                  B_parallel=0, B_perpendicular=0,
                                  sigma_parallel=0, A_iso=0,
                                  strain_freq=1e6, strain_amp=1e6,
                                  t_max=5e-6, n_steps=2000):
    

        # Time vector
            t_values = np.linspace(0, t_max, n_steps)

        def hamiltonian(t):
            # Strain components vary sinusoidally with time
            sigma_x = strain_amp * np.sin(2 * np.pi * strain_freq * t)
            sigma_y = strain_amp * np.cos(2 * np.pi * strain_freq * t)
            # Construct instantaneous Hamiltonian
            return self.build_hamiltonian(B_parallel, B_perpendicular,
                                          sigma_parallel, sigma_x, sigma_y, A_iso)

        def schrodinger_rhs(t, psi):
            """
            Right-hand side of the time-dependent Schrödinger equation:
            dψ/dt = -i/ħ * H(t) * ψ
            Using ħ = 1 (natural units), so:
            dψ/dt = -i * H(t) * ψ
            """
            H_t = hamiltonian(t)
            return -1j * H_t.dot(psi)

        # Initialize in one of the eigenstates at t=0
        H0 = hamiltonian(0)
        _, evecs = self.diagonalize(H0)
        psi0 = evecs[:, initial_state_index]

        # Solve the time-dependent Schrödinger equation
        solution = solve_ivp(schrodinger_rhs, (0, t_max), psi0, t_eval=t_values, rtol=1e-8)

        # Compute state populations over time for each basis state
        populations = np.abs(solution.y) ** 2  # shape: (3, n_steps)

        # Plot population dynamics
        plt.figure(figsize=(12, 6))
        for i in range(3):
            plt.plot(t_values * 1e6, populations[i], label=f'State {i}', linewidth=2)
        plt.title('Quantum State Population Evolution Under Phonon Driving')
        plt.xlabel('Time (μs)')
        plt.ylabel('Population Probability')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

        return t_values, populations, solution
        