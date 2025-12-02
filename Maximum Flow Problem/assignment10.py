"""
CS3C, Assignment #10, Maximum flow
Selma Emekci
"""
import math
from graph10 import *

class FlowEdge(Edge):
    """Edge subclass with capacity, flow, and residual semantics for max flow."""
    def __init__(self, id_, src, dst, weight=1, original=True):
        super().__init__(id_, src, dst, weight)
        self.capacity = weight
        self.flow = 0
        self.original = original

    @property
    def residual_capacity(self):
        return self.weight

    def is_usable(self):
        return self.weight > 0


class FlowVertex(Vertex):
    """Vertex subclass that uses FlowEdge."""
    EdgeClass = FlowEdge
    def add_edge(self, id_, dst, weight=1, original=True):
        """Create and attach a FlowEdge from this vertex to dst."""
        edge = self.EdgeClass(id_, self, dst, weight, original=original)
        self.out_edges.add(edge)
        return edge

class FlowGraph(Graph):
    """Graph subclass that can compute max flow between a source and sink."""
    VertexClass = FlowVertex
    def __init__(self, id_, vertices=None, edges=None):
        super().__init__(id_, vertices, edges)
        self._original_edges = set(self.edges.keys())
        for edge_id in list(self._original_edges):
            src_id, dst_id = edge_id
            src_v = self.vertices[src_id]
            dst_v = self.vertices[dst_id]
            rev_id = Edge.edge_id(dst_v, src_v)
            if rev_id not in self.edges:
                rev_edge = dst_v.add_edge(rev_id, src_v, weight=0, original=False)
                self.edges[rev_id] = rev_edge
        self._reset_flows_and_residual()

    def _reset_flows_and_residual(self):
        """Reset all flows to zero and residual capacities to initial values."""
        for edge in self.edges.values():
            edge.flow = 0
        for edge in self.edges.values():
            if edge.original:
                edge.weight = edge.capacity
            else:
                edge.weight = 0

    def _update_residual_from_flows(self):
        """Update residual capacities on all edges based on current flows."""
        for edge_id in self._original_edges:
            edge = self.edges[edge_id]
            src_v = edge.src
            dst_v = edge.dst
            forward_residual = edge.capacity - edge.flow
            if forward_residual < 0:
                forward_residual = 0
            edge.weight = forward_residual
            rev_id = Edge.edge_id(dst_v, src_v)
            rev_edge = self.edges[rev_id]
            if not rev_edge.original:
                rev_edge.weight = edge.flow

    def _find_augmenting_path(self, source, sink):
        """Use shortest-path finder on current residual graph to get a path."""
        path, distance = self.spf(source, sink)
        if not path or path[0] != source or path[-1] != sink:
            return None
        if math.isinf(distance):
            return None
        return path

    def max_flow(self, source, sink):
        """Compute the maximum flow from source to sink and return flow set."""
        if source == sink:
            raise ValueError("source and sink must be different vertices")
        if source not in self.vertices or sink not in self.vertices:
            return set()
        self._reset_flows_and_residual()
        while True:
            path = self._find_augmenting_path(source, sink)
            if path is None or len(path) < 2:
                break
            capacities = []
            for u, v in zip(path, path[1:]):
                edge = self.edges[(u, v)]
                capacities.append(edge.weight)
            bottleneck = min(capacities) if capacities else 0
            if bottleneck <= 0:
                break
            for u, v in zip(path, path[1:]):
                edge = self.edges[(u, v)]
                if edge.original:
                    edge.flow += bottleneck
                else:
                    rev_edge = self.edges[(v, u)]
                    if rev_edge.original:
                        rev_edge.flow -= bottleneck
            self._update_residual_from_flows()
        result = set()
        for edge_id in self._original_edges:
            edge = self.edges[edge_id]
            if edge.flow > 0:
                result.add((edge.src.id, edge.dst.id, edge.flow))
        return result
