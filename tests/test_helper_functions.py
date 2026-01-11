# -*- coding: utf-8 -*-

from src.models import Item
from src.constants import MAX_QUALITY, MIN_QUALITY
from src.helpers import clamp_quality, adjust_quality


class TestHelperFunctions:
    class TestClampQuality:
        def test_clamp_quality_within_range(self) -> None:
            assert clamp_quality(25) == 25

        def test_clamp_quality_below_zero(self) -> None:
            assert clamp_quality(-5) == MIN_QUALITY

        def test_clamp_quality_above_fifty(self) -> None:
            assert clamp_quality(75) == MAX_QUALITY

        def test_clamp_quality_boundaries(self) -> None:
            assert clamp_quality(MIN_QUALITY) == MIN_QUALITY
            assert clamp_quality(MAX_QUALITY) == MAX_QUALITY

    class TestAdjustQuality:
        def test_adjust_quality_respects_bounds(self):
            item = Item("Test", sell_in=5, quality=5)

            # The quality cannot go below the minimum
            result = adjust_quality(item, -10)
            assert result.quality == MIN_QUALITY

            # The quality cannot go above the maximum
            item2 = Item("Test", sell_in=5, quality=48)
            result2 = adjust_quality(item2, 10)
            assert result2.quality == MAX_QUALITY