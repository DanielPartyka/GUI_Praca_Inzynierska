from unittest import TestCase

from praca_inzynierska import MovableBlock
from uamf import BlockMeta
from uamf.ds import Size, Point

class TestMovableBlock(TestCase):
    def test_block_id(self):
        # example objects
        obj = MovableBlock(100,200,300,400,5)
        obj1 = MovableBlock(100,200,300,400,35)
        obj2 = MovableBlock(100,200,300,400,-3)
        # possible range of block id's (1-48)
        possible_id = [value for value in range(49) if value > 0]
        # test id
        self.assertTrue(obj.get_id() and obj1.get_id() in possible_id)
        self.assertFalse(obj2.get_id() in possible_id)

    def test_changing_position(self):
        # example object
        obj = MovableBlock(100, 200, 300, 400, 5)
        # (x0 = 100, y0 = 200, width = 300, height = 400, 5 = blockid)
        # testing changing postition of block
        obj.setPos(0,0)
        # x0
        self.assertEqual(0,obj.x())
        # y0
        self.assertEqual(0,obj.y())

    def test_width_height(self):
        # example object
        obj = MovableBlock(100, 200, 300, 400, 5)
        # checking width and height
        # x1 = x0 + width, y1 = y0 + height
        # x1
        self.assertEqual(400, obj.x() + obj.get_w())
        # y1
        self.assertEqual(600, obj.y() + obj.get_h())

class TestUamf(TestCase):
    def test_uamf(self):
        # Block structure
        # BlockMeta = ("mat_path", size_of_block, amount_of_rows, amount_of_columns, amount_of_spots,
        # math_path, cords (xo, yo) of block, list or dictionary of spots)
        block = BlockMeta('/mat_path', Size(100,100), 10, 15, "/math_path", Point(100,100), list)
        # check dimensions of block structure
        self.assertEqual(100, block.height)
        # Check if list of spots is not empty
        self.assertIsNotNone(block.spots)
        # Check amount of rows
        self.assertEqual(10, block.rows_number)
        # Check amount of columns
        self.assertEqual(15,block.columns_number)


# Unfortunately cannot create an instance of Numeration of Spots class, so we are unable to test it

# class TestNumerationOfSpot(TestCase):
#     def test_block_numeration_id(self):
#         # example object
#         numerastion2 = NumerationOfSpot(5)
#         numeration1 = NumerationOfSpot(1)
#         # # possible id's
#         # possible_id = [value for value in range(49) if value > 0]
#         # # test id
#         # self.assertFalse(obj1.get_id() in possible_id)
#         # self.assertTrue(obj.get_id() in possible_id)




