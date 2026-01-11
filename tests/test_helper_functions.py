import pytest

from models import Item
from constants import MAX_QUALITY, MIN_QUALITY
from helpers import clamp_quality, adjust_quality


class TestHelperFunctions:
    class TestClampQuality:
        def test_clamp_quality_within_range(self) -> None:
            assert clamp_quality(25) == 25

        def test_clamp_quality_below_zero(self) -> None:
            assert clamp_quality(-5) == 0

        def test_clamp_quality_above_fifty(self) -> None:
            assert clamp_quality(75) == MAX_QUALITY

        def test_clamp_quality_boundaries(self) -> None:
            assert clamp_quality(MIN_QUALITY) == MIN_QUALITY
            assert clamp_quality(MAX_QUALITY) == MAX_QUALITY

    class TestAdjustQuality:
        def test_adjust_quality_respects_bounds(self):
            item = Item("Test", sell_in=5, quality=5)

            # Can't go below 0
            result = adjust_quality(item, -10)
            assert result.quality == 0

            # Can't go above 50
            item2 = Item("Test", sell_in=5, quality=48)
            result2 = adjust_quality(item2, 10)
            assert result2.quality == 50