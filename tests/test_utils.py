import unittest
import nuheat.util as util


class TestUtils(unittest.TestCase):

    def test_fahrenheit_to_celsius(self):
        tests = [
            [32, 0],
            [72, 22],
            [212, 100]
        ]
        for test in tests:
            celsius = util.fahrenheit_to_celsius(test[0])
            self.assertEqual(celsius, test[1])

    def test_celsius_to_fahrenheit(self):
        tests = [
            [32, 0],
            [72, 22],
            [212, 100]
        ]
        for test in tests:
            fahrenheit = util.celsius_to_fahrenheit(test[1])
            self.assertEqual(fahrenheit, test[0])

    def test_fahrenheit_to_nuheat(self):
        tests = [
            [41, 481],  # min
            [72, 2217],
            [157, 6977]  # max
        ]
        for test in tests:
            temp = util.fahrenheit_to_nuheat(test[0])
            self.assertEqual(temp, test[1])

    def test_celsius_to_nuheat(self):
        tests = [
            [5, 481],  # min
            [22, 2217],
            [69, 6921]  # max
        ]
        for test in tests:
            temp = util.celsius_to_nuheat(test[0])
            self.assertEqual(temp, test[1])

    def test_nuheat_to_fahrenheit(self):
        tests = [
            [500, 41],  # min
            [2222, 72],
            [7000, 157]  # max
        ]
        for test in tests:
            fahrenheit = util.nuheat_to_fahrenheit(test[0])
            self.assertEqual(fahrenheit, test[1])

    def test_nuheat_to_celsius(self):
        tests = [
            [500, 5],  # min
            [2222, 22],
            [7000, 69]  # max
        ]
        for test in tests:
            celsius = util.nuheat_to_celsius(test[0])
            self.assertEqual(celsius, test[1])
