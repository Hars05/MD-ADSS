# MD-ADSS Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd md-adss
pip install -r requirements.txt
```

### Step 2: Run Example

```bash
python main.py
```

You should see:
```
============================================================
MD-ADSS - Multi-Domain Adversarial Decision Support System
============================================================

Creating ground defensive scenario...
Friendly units: 2
Enemy units: 2
...
TACTICAL RECOMMENDATIONS
...
```

### Step 3: Open Web Dashboard

Open `interface/dashboard.html` in your browser.

## Understanding the Output

### Recommendation Format

```
[Recommendation #1] Optimal Path (A*)
Algorithm: A* Search
Expected Utility: 85.4
Risk Level: Low
Rationale: Shortest path to objectives with minimal resource consumption

Actions:
  1. Move TANK-001 to position (12, 10)
  2. Move TANK-002 to defensive position (10, 8)
  3. Establish overwatch on enemy approach vectors
```

**What this means:**
- **Utility 85.4**: Higher is better (combines mission progress, casualties, resources)
- **Risk: Low**: Confidence in success
- **Actions**: Specific commands to execute

### Algorithm Performance

```
BFS: 6,182 nodes expanded
A*: 57 nodes expanded (99.1% reduction)
```

**What this means:**
- A* found the same solution as BFS
- But explored 99% fewer possibilities
- Much faster execution

## Common Use Cases

### 1. Evaluate a Defensive Position

```python
from domains.ground import GroundScenario
from main import MDADSS

state = GroundScenario.create_defensive_scenario()
system = MDADSS()
recs = system.generate_recommendations(state)

print(f"Best strategy: {recs[0]['title']}")
print(f"Expected outcome: {recs[0]['expected_utility']}")
```

### 2. Compare Multiple Strategies

```python
# Get top 3 recommendations
recs = system.generate_recommendations(state, top_k=3)

for i, rec in enumerate(recs, 1):
    print(f"{i}. {rec['title']}: Utility={rec['expected_utility']}")
```

### 3. Air Intercept Mission

```python
from domains.air import AirScenario

state = AirScenario.create_intercept_scenario()
recs = system.generate_recommendations(state)

# Will recommend intercept paths considering fuel limits
```

### 4. Naval Patrol

```python
from domains.naval import NavalScenario

state = NavalScenario.create_fleet_patrol_scenario()
recs = system.generate_recommendations(state)

# Considers submarine evasion and fuel constraints
```

## Customizing Scenarios

### Create Your Own Scenario

```python
from core.state import State, Unit, UnitType, Domain, Resources, MapEnvironment

# Create map
map_env = MapEnvironment(domain=Domain.GROUND, width=50, height=50)

# Create units
friendly = [
    Unit(
        id="CUSTOM-001",
        unit_type=UnitType.TANK,
        position=(10.0, 10.0, 0.0),
        health=100.0,
        fuel=100.0,
        ammo=50.0
    )
]

enemy = [
    Unit(
        id="ENEMY-001",
        unit_type=UnitType.TANK,
        position=(40.0, 40.0, 0.0),
        health=80.0,
        fuel=80.0,
        ammo=40.0,
        is_friendly=False
    )
]

# Create state
state = State(
    friendly_units=friendly,
    enemy_units=enemy,
    resources=Resources(fuel=500, ammo=300),
    map_env=map_env,
    domain=Domain.GROUND,
    objectives=[(40, 40, 0)],
    base_position=(10, 10, 0)
)

# Analyze
system = MDADSS()
recs = system.generate_recommendations(state)
```

## Tuning Algorithm Parameters

### Adjust Search Depth

```python
# More depth = better solutions but slower
system.astar.max_depth = 10  # Default: 6
system.minimax.max_depth = 5  # Default: 3
```

### Adjust Utility Weights

```python
# Emphasize different objectives
from core.utility import UtilityFunction

util = UtilityFunction(
    alpha=2.0,  # Mission progress (default: 1.0)
    beta=3.0,   # Casualty loss penalty (default: 2.0)
    gamma=0.3   # Resource penalty (default: 0.5)
)

system.utility = util
```

## Web Dashboard Usage

1. **Select Scenario**: Click any scenario button
2. **View Map**: See unit positions and terrain
3. **Analyze**: Click "Analyze Tactical Situation"
4. **Review**: Read recommendations ranked by utility
5. **Decide**: Choose which strategy to execute

### Dashboard Features

- **Color Coding**:
  - Green = Friendly units
  - Red = Enemy units
  - Orange = Objectives
  - Blue = Base

- **Stats Panel**: Real-time resource tracking
- **Performance Metrics**: Algorithm comparison

## Troubleshooting

### Issue: No recommendations generated

**Solution**: 
- Check that units are alive
- Verify objectives are set
- Ensure resources > 0

### Issue: All recommendations same

**Solution**:
- Increase search depth
- Add more units
- Create more complex terrain

### Issue: Slow performance

**Solution**:
- Reduce max_depth
- Limit unit count to <10
- Use Alpha-Beta instead of Minimax

## Next Steps

1. **Experiment**: Try all 6 scenarios
2. **Customize**: Create your own scenarios
3. **Analyze**: Compare algorithm performance
4. **Extend**: Add new unit types or algorithms

## Tips for Best Results

1. **Start Simple**: Begin with 2-3 units
2. **Increase Gradually**: Add complexity step-by-step
3. **Monitor Performance**: Watch node expansion counts
4. **Compare Algorithms**: See which works best for your scenario
5. **Use CSP**: For resource-constrained situations

## Example Session

```bash
$ python main.py
============================================================
MD-ADSS - Multi-Domain Adversarial Decision Support System
============================================================

Creating ground defensive scenario...
Friendly units: 2
Enemy units: 2
Resources: Fuel=500.0, Ammo=300.0

Analyzing tactical situation...

Running BFS search...
Running A* search...
Running Minimax adversarial analysis...
Running Alpha-Beta pruning...
Running CSP for resource allocation...

============================================================
TACTICAL RECOMMENDATIONS
============================================================

[Recommendation #1] Optimal Path (A*)
Algorithm: A* Search
Expected Utility: 22.48
...

# Choose recommendation #1 and execute
```

## Getting Help

- Read `README.md` for overview
- See `docs/DOCUMENTATION.md` for details
- Check code comments for implementation details

---

**You're ready to use MD-ADSS!** Start with `python main.py` or open `interface/dashboard.html`.
