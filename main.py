

from typing import List, Tuple, Dict
from core.state import State
from core.Action import Action
from search.bfs import BFSSearch
from search.astar import AStarSearch
from adversarial.minimax import MinimaxSearch, AlphaBetaSearch
from csp.solver import ResourceAllocationCSP, BacktrackingSolver


class MDADSS:
    """
    Main MD-ADSS Engine
    Integrates all search and planning algorithms
    """
    
    def __init__(self):
        self.bfs = BFSSearch(max_depth=4)
        self.astar = AStarSearch(max_depth=6)
        self.minimax = MinimaxSearch(max_depth=3)
        self.alphabeta = AlphaBetaSearch(max_depth=4)
        self.csp_solver = BacktrackingSolver()
    
    def analyze_situation(self, state: State) -> Dict:
        """
        Comprehensive situation analysis
        
        Returns:
            Dictionary with recommendations from all algorithms
        """
        initial_state = state.copy()
        
        results = {
            'bfs_recommendations': [],
            'astar_recommendations': [],
            'minimax_recommendation': None,
            'alphabeta_recommendation': None,
            'csp_allocations': {},
            'statistics': {}
        }
        
        # 1. BFS - Generate all possible tactical options
        print("Running BFS search...")
        bfs_paths = self.bfs.search_all_paths(state, depth=3)
        results['bfs_recommendations'] = bfs_paths[:5]  # Top 5
        results['statistics']['bfs'] = self.bfs._get_stats()
        
        # 2. A* - Find optimal paths
        print("Running A* search...")
        astar_plans = self.astar.find_top_k_plans(state, k=3, depth=3)
        results['astar_recommendations'] = astar_plans
        results['statistics']['astar'] = self.astar._get_stats()
        
        # 3. Minimax - Predict enemy reactions
        print("Running Minimax adversarial analysis...")
        minimax_action, minimax_value = self.minimax.search(state, initial_state)
        results['minimax_recommendation'] = (minimax_action, minimax_value)
        results['statistics']['minimax'] = self.minimax.get_stats()
        
        # 4. Alpha-Beta - Optimized adversarial search
        print("Running Alpha-Beta pruning...")
        ab_action, ab_value = self.alphabeta.search(state, initial_state)
        results['alphabeta_recommendation'] = (ab_action, ab_value)
        results['statistics']['alphabeta'] = self.alphabeta.get_stats()
        
        # 5. CSP - Resource allocation
        print("Running CSP for resource allocation...")
        results['csp_allocations'] = self._solve_csp_constraints(state)
        
        return results
    
    def _solve_csp_constraints(self, state: State) -> Dict:
        """Solve various CSP problems for the current state"""
        allocations = {}
        
        # Unit assignment CSP
        if len(state.friendly_units) >= 2:
            unit_ids = [u.id for u in state.friendly_units]
            sectors = ["NORTH", "SOUTH", "EAST", "WEST", "BASE"]
            base_sector = "BASE"
            
            problem = ResourceAllocationCSP.create_unit_assignment_problem(
                unit_ids, sectors, base_sector, min_base_defenders=1
            )
            
            assignment = self.csp_solver.solve(problem)
            if assignment:
                allocations['unit_assignments'] = assignment
                allocations['csp_stats'] = self.csp_solver.get_stats()
        
        # Fuel allocation CSP
        if state.resources.fuel > 0:
            unit_ids = [u.id for u in state.friendly_units if u.fuel < 50]
            if unit_ids:
                problem = ResourceAllocationCSP.create_fuel_allocation_problem(
                    unit_ids, 
                    total_fuel=min(state.resources.fuel, 200.0),
                    min_fuel_per_unit=10.0
                )
                fuel_assignment = self.csp_solver.solve(problem)
                if fuel_assignment:
                    allocations['fuel_allocation'] = fuel_assignment
        
        return allocations
    
    def generate_recommendations(self, state: State, top_k: int = 3) -> List[Dict]:
        """
        Generate top K tactical recommendations for commander
        
        Returns:
            List of recommendation dictionaries with actions, rationale, and expected outcomes
        """
        analysis = self.analyze_situation(state)
        
        recommendations = []
        
        # Combine A* and Minimax recommendations
        astar_recs = analysis['astar_recommendations']
        minimax_action, minimax_value = analysis['minimax_recommendation']
        
        # Recommendation 1: A* Optimal Path (if available)
        if astar_recs:
            actions, result_state, utility = astar_recs[0]
            recommendations.append({
                'rank': 1,
                'title': 'Optimal Path (A*)',
                'actions': actions[:3],  # First 3 actions
                'expected_utility': utility,
                'rationale': 'Shortest path to objectives with minimal resource consumption',
                'algorithm': 'A* Search',
                'risk_level': 'Low'
            })
        
        # Recommendation 2: Adversarial-Aware (Minimax/Alpha-Beta)
        if minimax_action:
            recommendations.append({
                'rank': 2,
                'title': 'Adversarial Defense',
                'actions': [minimax_action],
                'expected_utility': minimax_value,
                'rationale': 'Accounts for enemy counter-moves and minimizes worst-case outcomes',
                'algorithm': 'Minimax with Alpha-Beta Pruning',
                'risk_level': 'Medium'
            })
        
        # Recommendation 3: Alternative A* path
        if len(astar_recs) > 1:
            actions, result_state, utility = astar_recs[1]
            recommendations.append({
                'rank': 3,
                'title': 'Alternative Route',
                'actions': actions[:3],
                'expected_utility': utility,
                'rationale': 'Secondary path with different tactical approach',
                'algorithm': 'A* Search',
                'risk_level': 'Medium'
            })
        
        # Add CSP resource allocation to all recommendations
        csp_alloc = analysis.get('csp_allocations', {})
        for rec in recommendations:
            rec['resource_allocation'] = csp_alloc
        
        return recommendations[:top_k]
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics for all algorithms"""
        return {
            'bfs': self.bfs._get_stats(),
            'astar': self.astar._get_stats(),
            'minimax': self.minimax.get_stats(),
            'alphabeta': self.alphabeta.get_stats()
        }


def run_example():
    """Run example scenario"""
    from domains.ground import GroundScenario
    
    print("="*60)
    print("MD-ADSS - Multi-Domain Adversarial Decision Support System")
    print("="*60)
    print()
    
    # Create scenario
    print("Creating ground defensive scenario...")
    state = GroundScenario.create_defensive_scenario()
    
    print(f"Friendly units: {len(state.friendly_units)}")
    print(f"Enemy units: {len(state.enemy_units)}")
    print(f"Resources: Fuel={state.resources.fuel}, Ammo={state.resources.ammo}")
    print()
    
    # Run MD-ADSS
    system = MDADSS()
    print("Analyzing tactical situation...")
    print()
    
    recommendations = system.generate_recommendations(state, top_k=3)
    
    print("\n" + "="*60)
    print("TACTICAL RECOMMENDATIONS")
    print("="*60)
    
    for rec in recommendations:
        print(f"\n[Recommendation #{rec['rank']}] {rec['title']}")
        print(f"Algorithm: {rec['algorithm']}")
        print(f"Expected Utility: {rec['expected_utility']:.2f}")
        print(f"Risk Level: {rec['risk_level']}")
        print(f"Rationale: {rec['rationale']}")
        print(f"\nActions:")
        for i, action in enumerate(rec['actions'], 1):
            print(f"  {i}. {action}")
        
        if rec.get('resource_allocation'):
            print(f"\nResource Allocation:")
            for key, value in rec['resource_allocation'].items():
                print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("ALGORITHM PERFORMANCE")
    print("="*60)
    stats = system.get_performance_stats()
    for algo, stat in stats.items():
        print(f"\n{algo.upper()}:")
        for key, value in stat.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    run_example()
