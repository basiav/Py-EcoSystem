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
        cfg.N = 30  # Clean-Up

    def test_get_fence_node_idx_(self):
        self.assertEqual(fence.get_fence_node_idx(2, 3), 13)
        self.assertEqual(fence.get_fence_node_idx(3, 3), 18)
        self.assertEqual(fence.get_fence_node_idx(4, 4), 24)

    def test_get_fence_node_dirs(self):
        self.assertEqual(fence.get_fence_node_dirs(13), (2, 3))
        self.assertEqual(fence.get_fence_node_dirs(18), (3, 3))
        self.assertEqual(fence.get_fence_node_dirs(24), (4, 4))

        self.assertEqual(fence.get_fence_node_dirs(13)[0], 2)
        self.assertEqual(fence.get_fence_node_dirs(13)[1], 3)

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
        self.assertIsNone(fence.get_node_neighbour(cmn.Directions.Up, 0, 0))
        self.assertIsNone(fence.get_node_neighbour(cmn.Directions.Right, 0, 4))
        self.assertIsNone(fence.get_node_neighbour(cmn.Directions.Down, 4, 4))
        self.assertIsNone(fence.get_node_neighbour(cmn.Directions.Left, 4, 0))

        self.assertEqual(fence.get_node_neighbour(cmn.Directions.Up, 4, 3), 18)
        self.assertEqual(fence.get_node_neighbour(cmn.Directions.Right, 1, 3), 9)
        self.assertEqual(fence.get_node_neighbour(cmn.Directions.Down, 3, 2), 22)
        self.assertEqual(fence.get_node_neighbour(cmn.Directions.Left, 3, 2), 16)

        with self.assertRaises(NameError):
            fence.get_node_neighbour(cmn.Directions.Left, -1, -1)

    def test_check_if_wall_exists(self):
        self.assertFalse(fence.check_if_wall_exists(6, 11))
        self.assertFalse(fence.check_if_wall_exists(11, 6))
        fence.build_vertex(6, 11)
        self.assertTrue(fence.check_if_wall_exists(6, 11))
        self.assertTrue(fence.check_if_wall_exists(11, 6))
        fence.build_vertex(6, 11)
        self.assertTrue(fence.check_if_wall_exists(6, 11))
        fence.build_vertex(16, 11)
        self.assertTrue(fence.check_if_wall_exists(11, 16))

    def test_neighbour_relationships(self):
        self.assertEqual(fence.neighbours_relations(13, 8), cmn.Directions.Up)
        self.assertEqual(fence.neighbours_relations(13, 14), cmn.Directions.Right)
        self.assertEqual(fence.neighbours_relations(13, 18), cmn.Directions.Down)
        self.assertEqual(fence.neighbours_relations(13, 12), cmn.Directions.Left)
        self.assertIsNone(fence.neighbours_relations(13, 20), None)

    def test_get_move_directions(self):
        self.assertEqual(fence.get_move_direction(0, 1), cmn.Directions.Up)
        self.assertEqual(fence.get_move_direction(1, 1), cmn.Directions.Up_Right)
        self.assertEqual(fence.get_move_direction(1, 0), cmn.Directions.Right)
        self.assertEqual(fence.get_move_direction(1, -1), cmn.Directions.Down_Right)
        self.assertEqual(fence.get_move_direction(0, -1), cmn.Directions.Down)
        self.assertEqual(fence.get_move_direction(-1, -1), cmn.Directions.Down_Left)
        self.assertEqual(fence.get_move_direction(-1, 0), cmn.Directions.Left)
        self.assertEqual(fence.get_move_direction(-1, 1), cmn.Directions.Up_Left)

    def test_can_make_move(self):
        left, neutral, right, up, down = -1, 0, 1, 1, -1

        # Given, when, then
        self.assertTrue(fence.can_make_move(1, 1, right, up))
        self.assertTrue(fence.can_make_move(3, 1, neutral, up))
        self.assertTrue(fence.can_make_move(0, 3, neutral, down))
        self.assertTrue(fence.can_make_move(3, 0, right, neutral))
        self.assertTrue(fence.can_make_move(0, 3, left, down))
        self.assertFalse(fence.can_make_move(3, 1, neutral, down))
        self.assertFalse(fence.can_make_move(0, 3, right, down))

        # Given, when, then
        for row_move, col_move in zip(range(-1, 1), range(-1, 1)):
            if row_move != 0 and col_move != 0:
                self.assertTrue(fence.can_make_move(2, 2, col_move, row_move))
            else:
                self.assertFalse(fence.can_make_move(2, 2, col_move, row_move))  # Cannot stay in the same place

        # Given, when
        fence.build_vertex(11, 12)
        fence.build_vertex(7, 12)
        # Then
        self.assertTrue(fence.can_make_move(2, 1, right, up))
        # When
        fence.build_vertex(12, 17)
        # Then
        self.assertFalse(fence.can_make_move(2, 1, right, up))
        self.assertFalse(fence.can_make_move(2, 2, left, up))
        self.assertFalse(fence.can_make_move(2, 2, left, neutral))
        self.assertTrue(fence.can_make_move(2, 2, neutral, up))

        # Given, when
        fence.build_vertex(12, 13)
        fence.build_vertex(17, 18)
        fence.build_vertex(13, 18)
        # Then
        for row_move, col_move in zip(range(-1, 1), range(-1, 1)):
            self.assertFalse(fence.can_make_move(2, 2, col_move, row_move))


if __name__ == '__main__':
    unittest.main()
