"""
Graph implementation, with Dijkstra
Copyright 2022 Zibin Yang
"""
import heapq
import math
from typing import final


class Edge:
    """Class that represents a basic edge"""
    def __init__(self, id_, src, dst, weight=1):
        self.id = id_
        self.src = src
        self.dst = dst
        self.weight = weight

    def __str__(self):
        return f"{self.__class__.__name__}=({self.id}: {self.weight})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    @final
    def edge_id(src_v, dst_v):
        # Subclass should not override this method because Graph.add_edge()
        # is hardcoded to use it.
        # A tuple of source and destination id should unique identify the edge.
        return (src_v.id, dst_v.id)

    def is_usable(self):
        """Indicates if an edge is usable."""
        # If this returns False, spf() will not use this edge.
        return True

class Vertex:
    """Class that represents a basic vertex"""

    # Subclass may override this class attribute to use its own Edge class
    # (that inherits from Edge).
    EdgeClass = Edge

    # Class that holds Dijkstra-specific info
    class Path:
        def __init__(self):
            self.reset()

        def reset(self):
            self.weight = math.inf  # infinite initial cost/weight
            self.from_vertex = None

        def __str__(self):
            return f"{self.__class__.__name__}=({self.weight}," \
                   f" {self.from_vertex.id if self.from_vertex else '(None)'})"

    def __init__(self, id_):
        self.id = id_
        self.out_edges = set()
        self.path = Vertex.Path()

    def add_edge(self, id_, dst, weight=1):
        edge = self.EdgeClass(id_, self, dst, weight)
        self.out_edges.add(edge)
        return edge

    def __lt__(self, other):
        return self.path.weight < other.path.weight

    def __str__(self):
        return f"{self.__class__.__name__}=({self.id}, {self.out_edges}," \
               f" {self.path})"

    def __repr__(self):
        # This is what str(dict) str(list) calls for each element
        return str(self)


class Graph:
    """Class that represents a graph."""

    # Subclasses can override these two class attributes to use their own
    # Vertex class and Edge class (that inherit from Vertex/Edge).
    VertexClass = Vertex

    def __init__(self, id_, vertices=None, edges=None):
        self.id = id_
        self.vertices = dict()
        self.edges = dict()

        if vertices is not None:
            for vertex in vertices:
                self.add_vertex(vertex)

        if edges is not None:
            for edge in edges:
                self.add_edge(*edge)

    def add_vertex(self, id_):
        v = self.VertexClass(id_)
        self.vertices[id_] = v

    def add_edge(self, src, dst, weight=1):
        # The type hints need not (and cannot?) refer to self.VertexClass
        # since the vertex should be Vertex or inherit from it.
        src_v: Vertex = self.vertices[src]
        dst_v: Vertex = self.vertices[dst]
        edge_id = Edge.edge_id(src_v, dst_v)
        edge = src_v.add_edge(edge_id, dst_v, weight)
        self.edges[edge_id] = edge

    def __str__(self):
        vs = "\n".join([str(v) for v in self.vertices.values()])
        es = "\n".join([str(e) for e in self.edges.values()])
        return f"id={self.id}\n" \
               f"vertices:\n{vs}\n" \
               f"edges:\n{es}"

    def spf(self, src, dst):
        """
        This finds the shortest path between src and dst
        :param src: source vertex
        :param dst: destination vertex
        :return: tuple of a list of vertices from source to destination
                 and the distance.
        """
        src_v: Vertex = self.vertices[src]
        dst_v: Vertex = self.vertices[dst]

        # Reset all the path info for the vertices.
        self._reset_paths()

        src_v.path.weight = 0
        src_v.path.from_vertex = src_v
        # Start with the source vertex.
        partial_paths = [src_v]

        while len(partial_paths):
            # As long as there's a vertex in the queue (min heap), extract
            # the vertex with the smallest path cost/weight. That vertex
            # now has the known minimum cost/weight to the source.
            min_vertex: Vertex = heapq.heappop(partial_paths)

            for edge in min_vertex.out_edges:
                if not edge.is_usable():
                    # If edge is not usable, skip it.
                    continue
                # Go through all the outgoing edges in the new min vertex.
                # Calculate the new cost/weight to all destination of these
                # edges.
                dest_vertex: Vertex = edge.dst
                new_weight = min_vertex.path.weight + edge.weight

                if new_weight < dest_vertex.path.weight:
                    # If the new cost/weight is smaller than the currently
                    # known one for the destination, the new one is a shorter
                    # path, update it.
                    dest_vertex.path.weight = new_weight
                    dest_vertex.path.from_vertex = min_vertex

                    # If we've examined the destination vertex previous,
                    # its cost/weight has just changed, so heapify it.
                    # Otherwise, insert it into the queue.
                    if dest_vertex in partial_paths:
                        heapq.heapify(partial_paths)
                    else:
                        heapq.heappush(partial_paths, dest_vertex)

        # Done. Build and return the shortest path and its total cost/weight.
        return self._build_spf(src_v, dst_v)

    def _reset_paths(self):
        for v in self.vertices.values():
            v.path.reset()

    def _build_spf(self, src_v: Vertex, dst_v: Vertex):
        v = dst_v
        path = [v]
        # Start from the destination and go backwards.
        while v is not src_v and v.path.from_vertex is not None:
            path.insert(0, v.path.from_vertex)
            v = v.path.from_vertex

        return [v.id for v in path], dst_v.path.weight
