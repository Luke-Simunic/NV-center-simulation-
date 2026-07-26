# Phonon-Driven Spin Dynamics in Nitrogen-Vacancy Centres

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)]()
[![Research](https://img.shields.io/badge/Research-Quantum%20Sensing-green.svg)]()

## Overview

This repository contains my undergraduate research project investigating the feasibility of **phonon-driven spin transitions in nitrogen-vacancy (NV) centres in diamond**.

The project explores whether time-dependent strain can coherently manipulate NV spin states as a potential alternative to conventional radio-frequency (RF) excitation. Such an approach could contribute towards RF-free quantum magnetometry, particularly for environments where microwave delivery is impractical.

The repository contains the complete Python simulation, research report, derivation of the Hamiltonian, conference poster, and figures generated throughout the project.

---

## Research Motivation

Nitrogen-vacancy (NV) centres are one of the most promising solid-state quantum systems for precision sensing due to their long coherence times and optical readout capabilities.

Traditional optically detected magnetic resonance (ODMR) relies on microwave excitation. This project investigates whether **time-dependent lattice strain (phonons)** can provide an alternative mechanism for driving spin transitions.

The simulation models the quantum dynamics of the NV centre under magnetic fields, hyperfine interactions and oscillating strain fields.

---

## Features

The simulation includes

- Construction of the complete spin-1 Hamiltonian
- Zero-field splitting
- Zeeman interaction
- Hyperfine interaction
- Static and time-varying strain terms
- Numerical diagonalisation of the Hamiltonian
- Energy level calculations
- Anti-crossing identification
- Time-dependent Schrödinger equation solver
- Population evolution under oscillating strain
- Automatic generation of publication-quality figures

---
## Quick Start

### Clone the repository

```bash
git clone https://github.com/Luke-Simunic/nv-center-simulation.git
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the simulation

```bash
python src/simulation.py

```

## Repository Structure

```text
src/
    simulation.py

plots/
    Energy_Level_Splitting.png
    ...
    Population_Dynamics.png

report/
    NV_Center_Research_Report.pdf
    Hamiltonian_Derivation.tex
    Faculty_Research_Poster.pdf
```

---

## Example Results

### Energy Level Splitting

![Energy Levels](plots/energy_level_splitting.png)

---

### Time-Varying Strain Simulation

![Population Dynamics](plots/population_dynamics.png)

---

### Anti-Crossing Behaviour

![Anti Crossing](plots/anti_crossing.png)

---

## Methodology

The numerical framework was developed entirely in Python.

Major components include

- Hamiltonian construction using matrix mechanics
- Eigenvalue decomposition of the spin Hamiltonian
- Numerical integration of the time-dependent Schrödinger equation using SciPy
- Dynamic strain modelling
- Population analysis
- Scientific data visualisation

---

## Technologies

- Python
- NumPy
- SciPy
- Matplotlib
- LaTeX
- Quantum Mechanics
- Scientific Computing
- Numerical Modelling

---

## Research Outputs

This repository includes

- Undergraduate research dissertation
- Complete simulation code
- Hamiltonian derivation
- Faculty research poster
- Generated simulation figures

---

## Future Work

Potential extensions include

- Full Lindblad master equation simulations
- Decoherence modelling
- Optical pumping dynamics
- Microwave-free ODMR optimisation
- Experimental validation against published NV centre measurements

---

## Author

**Luke Simunic**

Bachelor of Science (Physics)

RMIT University

Interests:

- Quantum sensing
- Scientific computing
- Numerical simulation
- Data analysis
- Quantum technologies
