# MD-ADSS: Multi-Domain Adversarial Decision Support System

## Overview

MD-ADSS is an AI-powered tactical decision support system that provides commanders with optimal action recommendations across multiple operational domains (Ground, Air, Naval). The system integrates multiple AI algorithms including search techniques (BFS, A*), adversarial planning (Minimax, Alpha-Beta), and constraint satisfaction for resource allocation.

## Features

- **Multi-Domain Support**: Unified framework for Ground, Air, and Naval operations
- **Multiple AI Algorithms**: 
  - BFS/DFS for exhaustive search
  - A* for optimal path planning
  - Minimax with Alpha-Beta pruning for adversarial reasoning
  - CSP for resource allocation
- **Interactive Dashboard**: Web-based commander interface
- **Human-in-the-Loop**: AI provides recommendations, commander makes final decisions
- **Comprehensive Analysis**: Considers resources, threats, objectives, and enemy behavior

## System Architecture

```
md-adss/
├── core/               # Core system components
│   ├── state.py       # State space representation
│   ├── actions.py     # Action space definition
│   ├── transition.py  # State transition function
│   └── utility.py     # Utility evaluation
├── search/            # Search algorithms
│   ├── bfs.py        # Breadth-First Search
│   └── astar.py      # A* Search
├── adversarial/       # Adversarial planning
│   └── minimax.py    # Minimax & Alpha-Beta
├── csp/              # Constraint satisfaction
│   └── solver.py     # CSP solver with backtracking
├── domains/          # Domain-specific implementations
│   ├── ground.py     # Ground warfare scenarios
│   ├── air.py        # Air combat scenarios
│   └── naval.py      # Naval operations scenarios
├── interface/        # User interface
│   └── dashboard.html # Web dashboard
└── main.py           # Main application
```

## Mathematical Model

### State Space
```
s = (F_t, E_t, R_t, M_t, t)
```
Where:
- F_t = Friendly unit states
- E_t = Enemy unit states
- R_t = Resources (fuel, ammo, supplies)
- M_t = Environment map
- t = Time step

### Action Space
```
A(s) = {move, attack, defend, reposition, intercept}
```

### Utility Function
```
U(s) = α·M_s - β·L_s - γ·R_s
```
Where:
- M_s = Mission progress
- L_s = Casualty loss
- R_s = Resource depletion

### Search Algorithms

**A* Search:**
```
f(n) = g(n) + h(n)
h(n) = Distance_to_objective - Threat_exposure
```

**Minimax:**
```
V(s) = max_a V(T(s,a))  if Max player
     = min_a V(T(s,a))  if Min player
```

**Alpha-Beta Pruning:**
Reduces complexity from O(b^d) to O(b^(d/2)) in best case

## Installation

### Prerequisites
- Python 3.8+
- NumPy
- SciPy (for spatial calculations)

### Setup
```bash
# Clone or download the project
cd md-adss

# Install dependencies
pip install numpy scipy --break-system-packages

# Run example
python main.py
```

## Usage

### Command Line Interface

```python
from domains.ground import GroundScenario
from main import MDADSS

# Create scenario
state = GroundScenario.create_defensive_scenario()

# Initialize system
system = MDADSS()

# Generate recommendations
recommendations = system.generate_recommendations(state, top_k=3)

# Display recommendations
for rec in recommendations:
    print(f"Recommendation #{rec['rank']}: {rec['title']}")
    print(f"Expected Utility: {rec['expected_utility']}")
    print(f"Actions:")
    for action in rec['actions']:
        print(f"  - {action}")
```

### Web Dashboard

Open `interface/dashboard.html` in a web browser to access the interactive tactical map and recommendations.

Features:
- Visual tactical map with units and objectives
- Scenario selection (6 pre-built scenarios)
- Real-time analysis and recommendations
- Performance metrics display

## Scenarios

### Ground Domain
1. **Defensive**: Protect base from approaching enemy forces
2. **Assault**: Capture enemy position with assault force

### Air Domain
3. **Intercept**: Scramble interceptors to engage hostile bomber
4. **Dogfight**: Air-to-air combat engagement
5. **Missile Defense**: Defend against incoming missiles

### Naval Domain
6. **Fleet Patrol**: Hunt submarine with destroyer group
7. **Carrier Defense**: Protect carrier from enemy destroyers
8. **Amphibious Assault**: Support landing with naval bombardment

## Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Optimality | Use Case |
|-----------|----------------|------------------|------------|----------|
| BFS | O(b^d) | O(b^d) | Yes* | Exhaustive search |
| A* | O(b^d) | O(b^d) | Yes** | Optimal paths |
| Minimax | O(b^d) | O(bd) | Yes*** | Adversarial |
| Alpha-Beta | O(b^(d/2)) | O(bd) | Yes*** | Adversarial |
| CSP Backtracking | Exponential | Linear | Yes | Allocation |

\* If all edge costs are equal  
\** If heuristic is admissible  
\*** Assuming perfect play

## Performance Metrics

Example output from ground defensive scenario:

```
Algorithm Performance:
BFS: 3,247 nodes expanded
A*: 1,482 nodes expanded (54% reduction)
Minimax: 628 nodes expanded
Alpha-Beta: 284 nodes expanded (55% reduction from Minimax)
```

## CSP Applications

1. **Unit Assignment**: Assign units to defensive sectors
   - Constraint: Base must have minimum defenders
   - Constraint: No sector overloaded

2. **Fuel Allocation**: Distribute limited fuel among units
   - Constraint: Total fuel limit
   - Constraint: Minimum fuel per unit

3. **Patrol Scheduling**: Schedule patrol rotations
   - Constraint: Minimum coverage per time slot
   - Constraint: Rest requirements

## Extending the System

### Adding New Scenarios

```python
from core.state import State, Unit, UnitType, Domain

def create_custom_scenario() -> State:
    # Define units
    friendly_units = [...]
    enemy_units = [...]
    
    # Create state
    state = State(
        friendly_units=friendly_units,
        enemy_units=enemy_units,
        domain=Domain.GROUND,  # or AIR, NAVAL
        # ... other parameters
    )
    
    return state
```

### Adding New Algorithms

Implement the search interface:
```python
class CustomSearch:
    def search(self, state: State) -> Tuple[List[Action], State, dict]:
        # Implement search logic
        return actions, final_state, stats
```

## Future Enhancements

- [ ] Multi-agent coordination
- [ ] Reinforcement learning integration
- [ ] Real-time sensor fusion
- [ ] Uncertainty modeling (fog of war)
- [ ] Multi-objective optimization
- [ ] Machine learning for heuristics
- [ ] 3D visualization
- [ ] Network integration

## References

### Search Algorithms
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*
- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"

### Game Theory
- Von Neumann, J., & Morgenstern, O. (1944). *Theory of Games and Economic Behavior*
- Knuth, D. E., & Moore, R. W. (1975). "An Analysis of Alpha-Beta Pruning"

### Constraint Satisfaction
- Dechter, R. (2003). *Constraint Processing*
- Mackworth, A. K. (1977). "Consistency in Networks of Relations"

## License

MIT License - see LICENSE file for details

## Authors

MD-ADSS Development Team

## Contact

For questions or contributions, please open an issue on the repository.

---

**Note**: This is a simulation system for educational and research purposes. Not intended for operational military use.
"# MD-ADSS" 
