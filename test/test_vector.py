import unittest

from vector import Vector


class TestVector(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Vector(5, 10) + Vector(6, 3), Vector(11, 13))

    def test_subtract(self):
        self.assertEqual(Vector(12, 7) - Vector(3, 3), Vector(9, 4))

    def test_multiply(self):
        self.assertEqual(Vector(3, 7) * 5, Vector(15, 35))

if __name__ == '__main__':
    unittest.main()
