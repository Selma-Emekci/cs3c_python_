"""
CS3C, Assignment #10, Tests for Maximum Flow Probelm
Selma Emekci
"""

import unittest
from assignment10 import FlowGraph

class TestMaxFlow(unittest.TestCase):
    """Tests for FlowGraph.max_flow."""
    def test_single_edge(self):
        """Max flow on two-vertex single-edge graph equals its capacity."""
        graph = FlowGraph("single edge", "st", [("s", "t", 5)])
        expected = {("s", "t", 5)}
        self.assertSetEqual(graph.max_flow("s", "t"), expected)

    def test_sample_usage_graph(self):
        """Max flow on the sample usage graph."""
        graph = FlowGraph(
            "sample usage",
            "abcd",
            [
                ("a","b", 3),
                ("a", "c", 2),
                ("b", "d",2),
                ("c", "d",3),
                ("b", "c", 5),
            ],
        )
        expected = {
            ("a", "b", 3),
            ("b", "d", 2),
            ("a", "c", 2),
            ("c", "d", 3),
            ("b", "c", 1),
        }
        self.assertSetEqual(graph.max_flow("a", "d"), expected)

    def test_no_path_between_source_and_sink(self):
        """If there is no path from source to sink, max_flow returns empty set."""
        graph = FlowGraph("disconnected", "abcd", [("a", "b", 4), ("c", "d", 7)])
        self.assertSetEqual(graph.max_flow("a", "d"), set())

    def test_value_error_on_same_source_and_sink(self):
        """max_flow raises ValueError when source and sink are the same vertex."""
        graph = FlowGraph("same vertex", "a", [])
        with self.assertRaises(ValueError):
            graph.max_flow("a", "a")

    def test_custom_flow_network(self):
        """Max flow on a slightly larger custom network with multiple paths."""
        vertices = "sabcdt"
        edges = [
            ("s", "a", 7),
            ("s", "b", 4),
            ("a", "c", 5),
            ("b", "c", 3),
            ("a", "d", 3),
            ("c", "d", 4),
            ("c", "t", 6),
            ("d", "t", 5),
        ]
        graph = FlowGraph("custom", vertices, edges)
        result = graph.max_flow("s", "t")
        total_out_of_source = sum(flow for src, _, flow in result if src == "s")
        total_into_sink = sum(flow for _, dst, flow in result if dst == "t")
        self.assertEqual(total_out_of_source, 10)
        self.assertEqual(total_into_sink, 10)

    def test_multiple_calls_with_different_source_sink(self):
        """max_flow can be run multiple times with different sources and sinks."""
        graph = FlowGraph(
            "sample usage multi",
            "abcd",
            [
                ("a", "b", 3),
                ("a", "c", 2),
                ("b", "d", 2),
                ("c", "d", 3),
                ("b", "c", 5),
            ],
        )
        first = graph.max_flow("a", "d")
        second = graph.max_flow("a", "b")
        self.assertIn(("a", "b", 3), second)
        self.assertEqual(sum(flow for src, _, flow in second if src == "a"), 3)
    
    def test_readings_example_graph(self):
        """Max flow on a readings-style s–t network with intermediate vertices."""
        vertices = "sabtct"
        edges = [
            ("s", "a", 3),
            ("s", "b", 2),
            ("a", "b", 1),
            ("a", "c", 3),
            ("b", "c", 1),
            ("b", "t", 2),
            ("c", "t", 3),
        ]
        graph = FlowGraph("readings example", vertices, edges)

        result = graph.max_flow("s", "t")

        total_out_of_s = sum(flow for src, _, flow in result if src == "s")
        total_into_t = sum(flow for _, dst, flow in result if dst == "t")
        self.assertEqual(total_out_of_s, 5)
        self.assertEqual(total_into_t, 5)
        capacity = {}
        for u, v, cap in edges:
            capacity[(u, v)] = cap
        for u, v, flow in result:
            self.assertLessEqual(flow, capacity[(u, v)])
        for v in vertices:
            if v in ("s", "t"):
                continue
            inflow = sum(flow for src, dst, flow in result if dst == v)
            outflow = sum(flow for src, dst, flow in result if src == v)
            self.assertEqual(inflow, outflow)

if __name__ == "__main__":
    unittest.main()