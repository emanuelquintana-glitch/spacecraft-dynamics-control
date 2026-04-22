# Spacecraft Dynamics and Control - Problem Solutions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Book Reference](https://img.shields.io/badge/Reference-Canuto%20et%20al.-green.svg)](https://www.wiley.com/en-us/Spacecraft+Dynamics+and+Control%3A+An+Introduction-p-9781118342336)

> **A comprehensive problem-solving companion** for "Spacecraft Dynamics and Control: An Introduction" by Canuto, Acuna-Bravo, Molano, and Perez-Montenegro (Wiley, 2013)

##  Project Vision

This repository provides **complete, verified solutions** to problems from the textbook, with:
-  Step-by-step mathematical derivations
-  Working Python implementations
-  Professional visualizations
-  Simulation results and validation
-  Educational explanations and insights

##  Repository Structure

```
problems/
├── chapter_01_introduction/
│   ├── README.md                    # Chapter overview
│   └── exercises/                   # No computational problems
│
├── chapter_02_attitude_representation/
│   ├── README.md                    # Theory summary
│   ├── problem_2_1_euler_angles.py
│   ├── problem_2_2_quaternions.py
│   ├── problem_2_3_rotation_matrices.py
│   └── solutions/
│       ├── problem_2_1_solution.md
│       ├── problem_2_2_solution.md
│       └── figures/
│
├── chapter_03_orbital_dynamics/
│   ├── README.md
│   ├── problem_3_1_two_body.py
│   ├── problem_3_2_kepler.py
│   ├── problem_3_3_perturbations.py
│   └── solutions/
│
├── chapter_04_environmental_perturbations/
│   ├── README.md
│   ├── problem_4_1_gravity_gradient.py
│   ├── problem_4_2_solar_radiation.py
│   ├── problem_4_3_atmospheric_drag.py
│   └── solutions/
│
├── chapter_05_attitude_dynamics/
│   ├── README.md
│   ├── problem_5_1_euler_equations.py
│   ├── problem_5_2_torque_free_motion.py
│   ├── problem_5_3_spin_stabilization.py
│   └── solutions/
│
├── chapter_06_attitude_kinematics/
│   ├── README.md
│   ├── problem_6_1_poisson_equation.py
│   ├── problem_6_2_quaternion_kinematics.py
│   └── solutions/
│
├── chapter_07_attitude_determination/
│   ├── README.md
│   ├── problem_7_1_triad_algorithm.py
│   ├── problem_7_2_quest_method.py
│   ├── problem_7_3_wahba_problem.py
│   └── solutions/
│
├── chapter_08_sensors_actuators/
│   ├── README.md
│   ├── problem_8_1_star_tracker.py
│   ├── problem_8_2_gyroscopes.py
│   ├── problem_8_3_reaction_wheels.py
│   └── solutions/
│
├── chapter_09_attitude_control/
│   ├── README.md
│   ├── problem_9_1_pd_control.py
│   ├── problem_9_2_momentum_wheels.py
│   ├── problem_9_3_magnetic_control.py
│   └── solutions/
│
├── chapter_10_drag_free_control/
│   ├── README.md
│   ├── problem_10_1_goce_mission.py
│   ├── problem_10_2_accelerometers.py
│   └── solutions/
│
└── chapter_11_embedded_model_control/
    ├── README.md
    ├── problem_11_1_state_predictor.py
    ├── problem_11_2_disturbance_rejection.py
    └── solutions/
```

##  Problem Categories

### By Difficulty Level

| Level | Description | Example Topics |
|-------|-------------|----------------|
| ⭐ Basic | Fundamental concepts | Coordinate transforms, basic kinematics |
| ⭐⭐ Intermediate | Applied problems | Orbital propagation, attitude control |
| ⭐⭐⭐ Advanced | Complex systems | Multi-body dynamics, optimal control |

### By Type

-  **Analytical**: Mathematical derivations and proofs
-  **Computational**: Numerical simulations and algorithms
-  **Design**: System design and optimization problems
-  **Analysis**: Performance analysis and trade studies

##  Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/spacecraft-dynamics-control.git
cd spacecraft-dynamics-control

# Setup environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running a Problem

```bash
# Navigate to chapter
cd problems/chapter_05_attitude_dynamics

# Run problem solution
python problem_5_1_euler_equations.py

# View solution document
cat solutions/problem_5_1_solution.md
```

### Interactive Notebooks

```bash
# Start Jupyter
jupyter notebook

# Navigate to problems/notebooks/
# Open desired chapter notebook
```

##  Solution Format

Each problem follows a standardized format:

### Code Structure

```python
"""
Problem X.Y: [Title]

Reference: Canuto et al., Section X.Y, Page ###
Difficulty: ⭐⭐
Type: Computational/Analytical
"""

# 1. PROBLEM STATEMENT
"""
[Complete problem statement from book]
"""

# 2. ANALYTICAL SOLUTION
"""
Step-by-step derivation:
...
"""

# 3. NUMERICAL IMPLEMENTATION
def solve_problem():
    """Implementation with detailed comments."""
    pass

# 4. VISUALIZATION
def plot_results():
    """Publication-quality plots."""
    pass

# 5. VALIDATION
def validate_solution():
    """Compare with expected results."""
    pass

if __name__ == "__main__":
    # Run complete solution
    results = solve_problem()
    plot_results(results)
    validate_solution(results)
```

### Documentation Format (Markdown)

```markdown
# Problem X.Y: [Title]

## Problem Statement
[From textbook]

## Given
- Parameter 1: value
- Parameter 2: value

## Required
Find/Derive/Compute...

## Solution

### Part 1: Mathematical Derivation
[Step by step with equations]

### Part 2: Numerical Results
[Tables and values]

### Part 3: Discussion
[Physical interpretation]

## Code Implementation
```python
# Working code
```

## Results
![Figure](figures/problem_xy_result.png)

## Validation
✓ Matches textbook example
✓ Physically reasonable
✓ Conservation laws satisfied

## References
- Textbook: Section X.Y, Page ###
- Additional: [relevant papers]
```

##  Learning Path

### Beginner Track (Chapters 1-4)
1. Start with coordinate transformations
2. Master attitude representations
3. Understand orbital mechanics basics
4. Study environmental perturbations

### Intermediate Track (Chapters 5-8)
1. Attitude dynamics and Euler's equations
2. Kinematics and quaternions
3. Attitude determination algorithms
4. Sensors and actuators

### Advanced Track (Chapters 9-12)
1. Control system design
2. Drag-free control
3. Embedded model control
4. Case studies and missions

##  Chapter Summaries

### Chapter 2: Attitude Representation (15 problems)
Key topics: Euler angles, quaternions, rotation matrices
- Problems 2.1-2.5: Basic transformations ⭐
- Problems 2.6-2.10: Quaternion operations ⭐⭐
- Problems 2.11-2.15: Advanced topics ⭐⭐⭐

### Chapter 5: Attitude Dynamics (20 problems)
Key topics: Euler equations, torque-free motion
- Problems 5.1-5.7: Fundamental dynamics ⭐
- Problems 5.8-5.15: Stability analysis ⭐⭐
- Problems 5.16-5.20: Complex systems ⭐⭐⭐

### Chapter 9: Attitude Control (25 problems)
Key topics: PD control, momentum exchange
- Problems 9.1-9.8: Basic controllers ⭐
- Problems 9.9-9.18: Advanced control ⭐⭐
- Problems 9.19-9.25: Optimal design ⭐⭐⭐

##  Problem Index

Complete searchable index:

| Problem | Topic | Difficulty | Type | Page |
|---------|-------|------------|------|------|
| 2.1 | Euler angles | ⭐ | Analytical | 45 |
| 2.2 | Quaternion basics | ⭐ | Computational | 47 |
| 3.1 | Two-body problem | ⭐⭐ | Analytical | 92 |
| 5.1 | Euler equations | ⭐⭐ | Computational | 315 |
| 7.1 | TRIAD algorithm | ⭐⭐ | Computational | 535 |
| 9.1 | PD controller | ⭐⭐ | Design | 625 |
| ... | ... | ... | ... | ... |

##  Tools and Utilities

### Validation Tools
```python
from validation import (
    check_quaternion_norm,
    verify_rotation_matrix,
    validate_energy_conservation
)
```

### Plotting Utilities
```python
from plotting import (
    plot_attitude_trajectory,
    plot_orbit_3d,
    plot_control_response
)
```

### Common Functions
```python
from utils import (
    euler_to_quaternion,
    quaternion_to_dcm,
    propagate_orbit
)
```

##  Progress Tracking

### Overall Completion

```
Chapter 1: Introduction              [════════════] 100% (0/0)
Chapter 2: Attitude Representation   [══════░░░░░░]  50% (8/15)
Chapter 3: Orbital Dynamics          [═══░░░░░░░░░]  30% (6/20)
Chapter 4: Perturbations             [══░░░░░░░░░░]  20% (3/15)
Chapter 5: Attitude Dynamics         [═░░░░░░░░░░░]  10% (2/20)
Chapter 6: Kinematics               [░░░░░░░░░░░░]   0% (0/18)
Chapter 7: Determination            [░░░░░░░░░░░░]   0% (0/22)
Chapter 8: Sensors & Actuators      [░░░░░░░░░░░░]   0% (0/16)
Chapter 9: Control                  [░░░░░░░░░░░░]   0% (0/25)
Chapter 10: Drag-Free              [░░░░░░░░░░░░]   0% (0/12)
Chapter 11: EMC                    [░░░░░░░░░░░░]   0% (0/15)
Chapter 12: Case Studies           [░░░░░░░░░░░░]   0% (0/10)
──────────────────────────────────────────────────
Total:                             [═░░░░░░░░░░░]  10% (19/188)
```

##  Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

### How to Add a Solution

1. Create problem file: `problem_X_Y_title.py`
2. Write complete solution with documentation
3. Add markdown documentation in `solutions/`
4. Generate validation results
5. Submit pull request

### Quality Standards

✓ Complete problem statement
✓ Step-by-step derivation
✓ Working, tested code
✓ Professional plots
✓ Validation against known results
✓ Clear documentation

##  Additional Resources

### Textbook
- **Primary**: Canuto et al., "Spacecraft Dynamics and Control" (2013)
- **Supplementary**: Wie, "Space Vehicle Dynamics and Control" (2008)
- **Advanced**: Schaub & Junkins, "Analytical Mechanics of Space Systems" (2018)

### Online Resources
- [NASA Technical Reports](https://ntrs.nasa.gov/)
- [ESA Documentation](https://www.esa.int/gsp/ACT/doc/)
- [AIAA Education Series](https://arc.aiaa.org/series/aiaa-education-series)

##  Achievements

Earn badges as you complete problems:

-  **Beginner**: Complete 10 basic problems
-  **Intermediate**: Complete 25 problems
-  **Advanced**: Complete 50 problems
-  **Expert**: Complete all problems in a chapter
-  **Master**: Complete all problems

##  Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/spacecraft-dynamics-control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/spacecraft-dynamics-control/discussions)
- **Email**: spacecraft.dynamics@example.com

##  License

MIT License - see [LICENSE](LICENSE) file

##  Acknowledgments

- Prof. Canuto and co-authors for the excellent textbook
- Aerospace engineering community
- All contributors

---

**Start solving problems today!** 

*Last updated: November 2024*
