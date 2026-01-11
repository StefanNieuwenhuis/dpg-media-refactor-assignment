import pytest

from constants import MAX_QUALITY, SULFURAS_QUALITY
from models import Item
from update_strategies import update_standard_item, update_aged_brie, update_sulfuras, update_backstage_pass, \
    get_update_strategy


class TestUpdateStrategies:
    class TestStandardItemsUpdateStrategy:
        def test_update_standard_item_before_expiry(self) -> None:
            item = Item("Standard Item", sell_in=5, quality=10)
            updated = update_standard_item(item)

            assert updated.sell_in == 4
            assert updated.quality == 9

        def test_update_standard_item_after_expiry(self)-> None:
            item = Item("Standard Item", sell_in=-1, quality=10)
            updated = update_standard_item(item)

            assert updated.sell_in == -2
            assert updated.quality == 8  # quality degrades twice as fast

    class TestAgedBrieUpdateStrategy:
        def test_update_aged_brie_increases(self) -> None:
            item = Item("Aged Brie", sell_in=5, quality=10)
            updated = update_aged_brie(item)

            assert updated.quality == 11

        def test_update_aged_brie_after_expiry(self) -> None:
            item = Item("Aged Brie", sell_in=-1, quality=10)
            updated = update_aged_brie(item)

            assert updated.quality == 12 # quality increases twice as fast

        def test_update_aged_brie_max_quality(self)-> None:
            item = Item("Aged Brie", sell_in=5, quality=MAX_QUALITY)
            updated = update_aged_brie(item)

            assert updated.quality == MAX_QUALITY

    class TestSulfurasUpdateStrategy:
        def test_update_sulfuras_unchanged(self) -> None:
            item = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=SULFURAS_QUALITY)
            updated = update_sulfuras(item)

            assert updated.sell_in == 0
            assert updated.quality == SULFURAS_QUALITY
            assert updated is item

    class TestBackStagePageUpdateStrategy:
        def test_update_backstage_pass_far_from_concert(self) -> None:
            item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=10)
            updated = update_backstage_pass(item)

            assert updated.quality == 11

        def test_update_backstage_pass_10_days(self) -> None:
            item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=10)
            updated = update_backstage_pass(item)

            assert updated.sell_in == 9
            assert updated.quality == 12

        def test_update_backstage_pass_5_days(self) -> None:
            item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10)
            updated = update_backstage_pass(item)

            assert updated.sell_in == 4
            assert updated.quality == 13

        def test_update_backstage_pass_after_concert(self) -> None:
            item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)
            updated = update_backstage_pass(item)

            assert updated.sell_in == -1
            assert updated.quality == 0

    class TestUpdateStrategySelector:
        def test_get_strategy_standard_item(self):
            item = Item("Standard Item", sell_in=5, quality=10)
            strategy = get_update_strategy(item)
            assert strategy == update_standard_item

        def test_get_strategy_aged_brie(self):
            item = Item("Aged Brie", sell_in=5, quality=MAX_QUALITY)
            strategy = get_update_strategy(item)
            assert strategy == update_aged_brie

        def test_get_strategy_sulfuras(self):
            item = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=SULFURAS_QUALITY)
            strategy = get_update_strategy(item)
            assert strategy == update_sulfuras

        def test_get_strategy_backstage_pass(self):
            item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=10)
            strategy = get_update_strategy(item)
            assert strategy == update_backstage_pass