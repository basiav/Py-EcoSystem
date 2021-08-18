import unittest

import sys
sys.path.append('../')

import config as cfg
import common as cmn
import fence


class MyTestCase(unittest.TestCase):
    def setUp(self):
        cfg.N = 4  # All the tests below performed with N = 4

    def tearDown(self):
        cfg.N = 30

    def test_get_fence_node_idx_(self):
        self.assertEqual(fence.get_fence_node_idx(2, 3), 13)
        self.assertEqual(fence.get_fence_node_idx(3, 3), 18)
        self.assertEqual(fence.get_fence_node_idx(4, 4), 24)

    def test_get_fence_node_dirs(self):
        self.assertEqual(fence.get_fence_node_dirs(13), (2, 3))
        self.assertEqual(fence.get_fence_node_dirs(18), (3, 3))
        self.assertEqual(fence.get_fence_node_dirs(24), (4, 4))

    def test_fence_border(self):
        self.assertCountEqual(fence.fence_border(0), [cmn.Directions.Up, cmn.Directions.Left])
        self.assertCountEqual(fence.fence_border(2), [cmn.Directions.Up])
        self.assertCountEqual(fence.fence_border(4), [cmn.Directions.Up, cmn.Directions.Right])
        self.assertCountEqual(fence.fence_border(14), [cmn.Directions.Right])
        self.assertCountEqual(fence.fence_border(24), [cmn.Directions.Right, cmn.Directions.Down])
        self.assertCountEqual(fence.fence_border(21), [cmn.Directions.Down])
        self.assertCountEqual(fence.fence_border(20), [cmn.Directions.Down, cmn.Directions.Left])
        self.assertCountEqual(fence.fence_border(5), [cmn.Directions.Left])

    def test_node_neighbours(self):
        self.assertIsNone(fence.get_node_neighbours(cmn.Directions.Up, 0, 0))
        self.assertIsNone(fence.get_node_neighbours(cmn.Directions.Right, 0, 4))
        self.assertIsNone(fence.get_node_neighbours(cmn.Directions.Down, 4, 4))
        self.assertIsNone(fence.get_node_neighbours(cmn.Directions.Left, 4, 0))

        self.assertEqual(fence.get_node_neighbours(cmn.Directions.Up, 4, 3), 18)
        self.assertEqual(fence.get_node_neighbours(cmn.Directions.Right, 1, 3), 9)
        self.assertEqual(fence.get_node_neighbours(cmn.Directions.Down, 3, 2), 22)
        self.assertEqual(fence.get_node_neighbours(cmn.Directions.Left, 3, 2), 16)

        with self.assertRaises(NameError):
            fence.get_node_neighbours(cmn.Directions.Left, -1, -1)


if __name__ == '__main__':
    unittest.main()
