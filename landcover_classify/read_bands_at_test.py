"""
example unit test for ExampleClass
list of unittest assert methods:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

# std modules:
from unittest import TestCase

from landcover_classify.read_bands_at import read_bands_at


class Test_read_bands_at(TestCase):

    def test_read_one_point(self):
        """ Read one point from middle of the image """
        result = read_bands_at(
            '16FEB12162517-M1BS-_RB_Rrs.tiff',
            [[-81.735270, 25.932147]],
            longformat=False
        )
        print(result)
        self.assertEqual(
            result,
            [[
                0.08366379, 0.16067146, 0.2094495, 0.18627913,
                0.17090823, 0.08640266, 0.04515372, 0.01725759
            ]]
        )
