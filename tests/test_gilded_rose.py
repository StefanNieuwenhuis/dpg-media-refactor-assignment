# -*- coding: utf-8 -*-
import pytest

from gilded_rose import GildedRose, Item

# --------------------------------------------------
# Test Constants
# --------------------------------------------------

MIN_QUALITY = 0
MAX_QUALITY = 50

NORMAL_DEGRADE = 1
EXPIRED_DEGRADE = 2

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

    class TestStandardItems:
        def test_standard_item_before_sell_date(self) -> None:
            item = Item("+5 Dexterity Vest", sell_in=10, quality=20)

            updated = update(item)

            assert updated.sell_in == 9
            assert updated.quality == 20 - NORMAL_DEGRADE

        def test_standard_item_on_sell_date(self) -> None:
            item = Item("+5 Dexterity Vest", sell_in=0, quality=20)

            updated = update(item)

            assert updated.sell_in == -1
            assert updated.quality == 20 - EXPIRED_DEGRADE

        def test_standard_item_after_sell_date(self) -> None:
            item = Item("+5 Dexterity Vest", sell_in=-5, quality=20)

            updated = update(item)

            assert updated.quality == 20 - EXPIRED_DEGRADE

        def test_standard_item_sell_in_decrements(self) -> None:
            item = Item("Standard item", sell_in=1, quality=10)

            updated = update(item)

            assert updated.sell_in == 0

# --------------------------------------------------
# Test Runner
# --------------------------------------------------
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])