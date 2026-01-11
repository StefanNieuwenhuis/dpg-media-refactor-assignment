# -*- coding: utf-8 -*-

from src.models import Item
from src.constants import MIN_QUALITY, MAX_QUALITY, SULFURAS_QUALITY, AGED_BRIE, SULFURAS, BACKSTAGE_PASS, ELIXER_MONGOOSE, \
    DEXTERITY_VEST
from src.gilded_rose import GildedRose


class TestIntegration:
    def test_update_integration(self) -> None:
        items = [
            Item(name=DEXTERITY_VEST, sell_in=10, quality=20),
            Item(name=AGED_BRIE, sell_in=2, quality=0),
            Item(name=ELIXER_MONGOOSE, sell_in=5, quality=7),
            Item(name=SULFURAS, sell_in=0, quality=80),
            Item(name=BACKSTAGE_PASS, sell_in=15, quality=20),
        ]

        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert gilded_rose.items[0].quality == 19
        assert gilded_rose.items[1].quality == 1
        assert gilded_rose.items[2].quality == 6
        assert gilded_rose.items[3].quality == 80
        assert gilded_rose.items[4].quality == 21

    def test_30_day_simulation(self) -> None:
        items = [
            Item(name="Standard Item", sell_in=10, quality=20),
            Item(name=AGED_BRIE, sell_in=5, quality=10),
            Item(name=SULFURAS, sell_in=0, quality=80),
            Item(name=BACKSTAGE_PASS, sell_in=15, quality=20),
        ]

        days = 30

        gilded_rose = GildedRose(items)

        for day in range(days):
            gilded_rose.update_quality()

        # Standard item should degrade to minimum quality (i.e. zero)
        assert gilded_rose.items[0].quality == MIN_QUALITY

        # Aged Brie quality should increase to maximum quality (i.e. fifty)
        assert gilded_rose.items[1].quality == MAX_QUALITY

        # Sulfuras quality should remain the same
        assert gilded_rose.items[2].quality == SULFURAS_QUALITY

        # Backstage pass quality should be zero after a concert
        assert gilded_rose.items[3].quality == MIN_QUALITY
