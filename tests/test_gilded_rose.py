# -*- coding: utf-8 -*-
import pytest

from gilded_rose import GildedRose, Item

# --------------------------------------------------
# Test Constants
# --------------------------------------------------

MIN_QUALITY = 0
MAX_QUALITY = 50

# --------------------------------------------------
# Test helper functions
# --------------------------------------------------
def update(item: Item) -> Item:
    """
    Receives a single Item, adds it to inventory, and updates it conform business rules

    :param item: (Item) Item added to inventory and to be updated
    :return: updated Item
    """

    items = [item]
    GildedRose(items).update_quality()

    return items[0]

# --------------------------------------------------
# Unit Tests
# --------------------------------------------------
class TestGildedRose:
    class TestGenerics:
        def test_quality_is_never_negative(self) -> None:
            item = Item("Standard Item", sell_in=5, quality=MIN_QUALITY)
            updated = update(item)

            assert updated.quality == MIN_QUALITY

        def test_quality_never_exceeds_maximum(self) -> None:
            item = Item("Aged Brie", sell_in=5, quality=MAX_QUALITY)

            updated = update(item)

            assert updated.quality == MAX_QUALITY
