import pytest
from helpers import clamp_quality
from constants import MAX_QUALITY, MIN_QUALITY

class TestHelperFunctions:
    class TestClampQuality:
        def test_clamp_quality_within_range(self) -> None:
            assert clamp_quality(25) == 25

        def test_clamp_quality_below_zero(self):
            assert clamp_quality(-5) == 0

        def test_clamp_quality_above_fifty(self):
            assert clamp_quality(75) == MAX_QUALITY

        def test_clamp_quality_boundaries(self):
            assert clamp_quality(MIN_QUALITY) == MIN_QUALITY
            assert clamp_quality(MAX_QUALITY) == MAX_QUALITY