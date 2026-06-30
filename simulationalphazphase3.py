import numpy as np
import networkx as nx
from collections import defaultdict

class SpaceTime4DAggregator:
    def __init__(self, spatial_engine, time_rounds=5):
        """
        Takes an operational 3D lattice engine and duplicates its registers
        along a temporal horizon to assemble a 4D space-time decoding network.
        """
        self.spatial = spatial_engine
        self.T = time_rounds
        
        # Define the unified 4D Space-Time Matching Graph for the X-Sector
        self.x_spacetime_graph = nx.Graph()
        self._compile_4d_x_graph()

    def _compile_4d_x_graph(self):
        """
        Interlinks spatial 3D cells with vertical temporal edges across time rounds.
        Nodes are identified by tuples: (cell_id, time_tick)
        """
        self.x_spacetime_graph.add_node('Boundary')
        
        # 1. Populate all spacetime nodes and draw vertical time-edges
        for t in range(self.T):
            for cell_id in self.spatial.cell_volume_registry.keys():
                node_now = (cell_id, t)
                self.x_spacetime_graph.add_node(node_now)
                
                # Connect sequentially through time (Temporal Edges tracking measurement faults)
                if t > 0:
                    node_prev = (cell_id, t - 1)
                    # The weight corresponds to log(1/p_measurement)
                    self.x_spacetime_graph.add_edge(node_prev, node_now, type='time', weight=1.0)

        # 2. Replicate spatial 3D architecture layout inside every distinct time slice
        for t in range(self.T):
            for q_idx, connected_cells in self.spatial.qubit_to_cells.items():
                if len(connected_cells) == 2:
                    u = (connected_cells[0], t)
                    v = (connected_cells[1], t)
                    self.x_spacetime_graph.add_edge(u, v, type='space', qubit=q_idx, weight=1.0)
                elif len(connected_cells) == 1:
                    u = (connected_cells[0], t)
                    self.x_spacetime_graph.add_edge(u, 'Boundary', type='space', qubit=q_idx, weight=1.0)

    def decode_spacetime_defects(self, active_spacetime_defects):
        """
        Decodes a global history of defects scattered across space and time.
        """
        if not active_spacetime_defects:
            return []

        # Maintain global parity constraints
        if len(active_spacetime_defects) % 2 != 0:
            active_spacetime_defects.append('Boundary')

        # Build standard distance graph across space-time locations
        matching_graph = nx.Graph()
        for i, node1 in enumerate(active_spacetime_defects):
            for node2 in active_spacetime_defects[i+1:]:
                path_length = nx.dijkstra_path_length(self.x_spacetime_graph, node1, node2)
                matching_graph.add_edge(node1, node2, weight=-path_length)

        best_matching = nx.max_weight_matching(matching_graph, maxcardinality=True)
        
        # Accumulate the true data qubit corrections while ignoring pure temporal blips
        corrected_qubits = set()
        for node1, node2 in best_matching:
            path = nx.dijkstra_path(self.x_spacetime_graph, node1, node2)
            for step in range(len(path) - 1):
                u, v = path[step], path[step+1]
                edge_data = self.x_spacetime_graph[u][v]
                if edge_data['type'] == 'space' and 'qubit' in edge_data:
                    corrected_qubits.add(edge_data['qubit'])
                    
        return list(corrected_qubits)

# =====================================================================
# INTEGRATION TESTING HARNESS
# =====================================================================
if __name__ == "__main__":
    from simulationalpha3d3 import XSectorMatchingEngine
    
    # Initialize our d=5 spatial structure
    spatial_code = XSectorMatchingEngine(distance=5)
    
    # Scale to 4D Spacetime Aggregator over 5 consecutive cycles
    aggregator = SpaceTime4DAggregator(spatial_code, time_rounds=5)
    
    print("--- 4D Space-Time Graph Aggregator Online ---")
    print(f"Total Spacetime Graph Nodes Registered : {len(aggregator.x_spacetime_graph.nodes)}")
    print(f"Total Spacetime Edge Channels Compiled : {len(aggregator.x_spacetime_graph.edges)}")
