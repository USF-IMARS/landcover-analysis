"""
example unit test for ExampleClass
list of unittest assert methods:
https://docs.python.org/3/library/unittest.html#assert-methods
"""

# std modules:
from unittest import TestCase
import numpy as np

from landcover_classify.read_bands_at import read_bands_at


class Test_read_bands_at(TestCase):

    def test_read_one_point(self):
        """ Read one point from middle of the image """
        result = read_bands_at(
            '16FEB12162517-M1BS-_RB_Rrs.tiff',
            [[25.932147, -81.735270]],
            longformat=False
        )
        print(result)
        np.testing.assert_almost_equal(
            result,
            [[
                0.083664, 0.160671, 0.209449, 0.186279, 0.170908, 0.086403,
                0.045154, 0.017258
            ]],
            decimal=5
        )

    def test_read_point_out_of_frame(self):
        """ Read one point from outside of the image """
        result = read_bands_at(
            '16FEB12162517-M1BS-_RB_Rrs.tiff',
            [[-89.735270, 20.932147]],
            longformat=False
        )
        print(result)
        np.testing.assert_almost_equal(
            result,
            [[
                0.083664, 0.160671, 0.209449, 0.186279, 0.170908, 0.086403,
                0.045154, 0.017258
            ]],
            decimal=5
        )

    def test_read_one_point_longformat(self):
        """ Read one point from middle of the image """
        result = read_bands_at(
            '16FEB12162517-M1BS-_RB_Rrs.tiff',
            [[25.932147, -81.735270]],
            longformat=True
        )
        print('*'*40)
        print(result)
        print('*'*40)
        np.testing.assert_almost_equal(
            result['band_n'].array,
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        )
        np.testing.assert_almost_equal(
            result['pixel_value'].array,
            [
                    0.083664, 0.160671, 0.209449, 0.186279, 0.170908,
                    0.086403, 0.045154, 0.017258
            ],
            decimal=5
        )
