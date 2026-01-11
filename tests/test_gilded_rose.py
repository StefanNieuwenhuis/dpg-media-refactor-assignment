# -*- coding: utf-8 -*-
import pytest

from constants import MIN_QUALITY, MAX_QUALITY, SULFURAS_QUALITY, AGED_BRIE, SULFURAS, BACKSTAGE_PASS, DEXTERITY_VEST
from models import Item
from gilded_rose import GildedRose

# --------------------------------------------------
# Test Constants
# --------------------------------------------------

NORMAL_DEGRADE = 1
EXPIRED_DEGRADE = 2

AGED_BRIE_INCREASE = 1
AGED_BRIE_EXPIRED_INCREASE = 2

BACKSTAGE_INCREASE_NORMAL = 1
BACKSTAGE_INCREASE_MEDIUM = 2
BACKSTAGE_INCREASE_HIGH = 3

# --------------------------------------------------
# Test helper functions
# --------------------------------------------------
def update(item: Item) -> Item:
    """Receives a single Item, adds it to the inventory, and updates it conform business rules"""
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()

    return gilded_rose.items[0]

# --------------------------------------------------
# Unit Tests
# --------------------------------------------------

class TestGildedRose:
    class TestGenerics:
        def test_quality_is_never_negative(self) -> None:
            item = Item(name="Standard Item", sell_in=5, quality=MIN_QUALITY)
            updated = update(item)

            assert updated.quality == MIN_QUALITY

        def test_quality_never_exceeds_maximum(self) -> None:
            item = Item(name=AGED_BRIE, sell_in=5, quality=MAX_QUALITY)

            updated = update(item)

            assert updated.quality == MAX_QUALITY

    class TestStandardItems:
        def test_standard_item_before_sell_date(self) -> None:
            item = Item(name=DEXTERITY_VEST, sell_in=10, quality=20)

            updated = update(item)

            assert updated.sell_in == 9
            assert updated.quality == 20 - NORMAL_DEGRADE

        def test_standard_item_on_sell_date(self) -> None:
            item = Item(name=DEXTERITY_VEST, sell_in=0, quality=20)

            updated = update(item)

            assert updated.sell_in == -1
            assert updated.quality == 20 - EXPIRED_DEGRADE

        def test_standard_item_after_sell_date(self) -> None:
            item = Item(name=DEXTERITY_VEST, sell_in=-5, quality=20)

            updated = update(item)

            assert updated.quality == 20 - EXPIRED_DEGRADE

        def test_standard_item_sell_in_decrements(self) -> None:
            item = Item(name="Standard item", sell_in=1, quality=10)

            updated = update(item)

            assert updated.sell_in == 0

    class TestAgedBrie:
        def test_aged_brie_increases_quality(self) -> None:
            item = Item(name=AGED_BRIE, sell_in=5, quality=10)

            updated = update(item)

            assert updated.quality == 10 + AGED_BRIE_INCREASE

        def test_aged_brie_after_sell_date_increases_twice_as_fast(self) -> None:
            """
            This case surprised me, since the description in GuildedRoseRequirements was quite vague on this.
            """
            item = Item(name=AGED_BRIE, sell_in=0, quality=10)

            updated = update(item)

            assert updated.quality == 10 + AGED_BRIE_EXPIRED_INCREASE

    class TestLegendaryItems:
        def test_sulfuras_never_changes(self) -> None:
            item = Item(name=SULFURAS, sell_in=0, quality=SULFURAS_QUALITY)

            updated = update(item)

            assert updated.sell_in == 0
            assert updated.quality == SULFURAS_QUALITY

    class TestBackstagePass:
        def test_backstage_pass_increases_quality(self) -> None:
            item = Item(name=BACKSTAGE_PASS, sell_in=15, quality=20)

            updated = update(item)

            assert updated.quality == 20 + BACKSTAGE_INCREASE_NORMAL

        def test_backstage_pass_sell_in_decrements(self) -> None:
            item = Item(name=BACKSTAGE_PASS, sell_in=5, quality=20)

            updated = update(item)

            assert updated.sell_in == 4

        def test_backstage_pass_10_days_or_less(self) -> None:
            item = Item(name=BACKSTAGE_PASS, sell_in=10, quality=20)

            updated = update(item)

            assert updated.quality == 20 + BACKSTAGE_INCREASE_MEDIUM

        def test_backstage_pass_5_days_or_less(self) -> None:
            item = Item(name=BACKSTAGE_PASS, sell_in=5, quality=20)

            updated = update(item)

            assert updated.quality == 20 + BACKSTAGE_INCREASE_HIGH

        def test_backstage_pass_after_concert(self) -> None:
            item = Item(name=BACKSTAGE_PASS, sell_in=0, quality=20)

            updated = update(item)

            assert updated.quality == MIN_QUALITY

        def test_backstage_pass_quality_capped_at_maximum(self) -> None:
            item = Item(name=BACKSTAGE_PASS, sell_in=5, quality=MAX_QUALITY - 1)

            updated = update(item)

            assert updated.quality == MAX_QUALITY
