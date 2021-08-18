import unittest

import config as cfg
import common as cmn


class MyTestCase(unittest.TestCase):
    def setUp(self):
        cfg.N = 4

    def tearDown(self):
        cfg.N = 30

    def test_get_fence_node_idx_(self):
        self.assertEqual(cmn.get_fence_node_idx(2, 3), 13)
        self.assertEqual(cmn.get_fence_node_idx(3, 3), 18)
        self.assertEqual(cmn.get_fence_node_idx(4, 4), 24)

    def test_get_fence_node_dirs(self):
        self.assertEqual(cmn.get_fence_node_dirs(13), (2, 3))
        self.assertEqual(cmn.get_fence_node_dirs(18), (3, 3))
        self.assertEqual(cmn.get_fence_node_dirs(24), (4, 4))

    def test_fence_border(self):
        self.assertCountEqual(cmn.fence_border(0), [cmn.Directions.Up, cmn.Directions.Left])
        self.assertCountEqual(cmn.fence_border(2), [cmn.Directions.Up])
        self.assertCountEqual(cmn.fence_border(2), [cmn.Directions.Up])

if __name__ == '__main__':
    unittest.main()
