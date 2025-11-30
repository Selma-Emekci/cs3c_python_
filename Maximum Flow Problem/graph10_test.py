"""
Graph implementation, with Dijkstra, tests
Copyright 2021 Zibin Yang
"""
import unittest
from graph10 import *


class GraphTestCase(unittest.TestCase):
    def testGraph(self):
        # Example credit: Introduction to Algorithms, Cormen, Leiserson, Rivest
        graph = Graph("test", "suvxy", [
            ("s", "u", 10),
            ("s", "x", 5),
            ("u", "x", 2),
            ("u", "v", 1),
            ("x", "u", 3),
            ("x", "v", 9),
            ("x", "y", 2),
            ("v", "y", 4),
            ("y", "v", 6),
            ("y", "s", 7),
        ])
        print(graph)

    # This helps to verify our understanding of how heapq works
    def testHeapq(self):
        class Item:
            def __init__(self, item):
                self.item = item

            def __lt__(self, other):
                return self.item < other.item

            def __str__(self):
                return str(self.item)

            def __repr__(self):
                return str(self)

        item0 = Item(0)
        item1 = Item(1)
        hq = [item1, item0]
        heapq.heapify(hq)
        self.assertIs(item0, hq[0])
        self.assertIs(item1, hq[1])

        item0.item = 100
        heapq.heappush(hq, item0)
        # print(hq)

    def setUp(self):
        # Example credit: Introduction to Algorithms, Cormen, Leiserson, Rivest
        self.graph1 = Graph("test", "suvxyz", [
            ("s", "u", 10),
            ("s", "x", 5),
            ("u", "x", 2),
            ("u", "v", 1),
            ("x", "u", 3),
            ("x", "v", 9),
            ("x", "y", 2),
            ("v", "y", 4),
            ("y", "v", 6),
            ("y", "s", 7),
            # z is not connected to anything
        ])

    def testSpfSelf1(self):
        spf = self.graph1.spf("s", "s")
        self.assertEqual((["s"], 0), spf)

    def testSpfNotConnected1(self):
        spf = self.graph1.spf("s", "z")
        self.assertEqual((["z"], math.inf), spf)

        spf = self.graph1.spf("z", "s")
        self.assertEqual((["s"], math.inf), spf)

    def testSpf1(self):
        spf = self.graph1.spf("s", "v")
        self.assertEqual((["s", "x", "u", "v"], 9), spf)

        # Make sure spf can be run multiple times on the same graph
        spf = self.graph1.spf("u", "s")
        self.assertEqual((["u", "x", "y", "s"], 11), spf)
