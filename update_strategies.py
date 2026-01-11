from dataclasses import replace
from typing import Callable

from constants import MIN_QUALITY
from helpers import adjust_quality, decrease_sell_in, is_expired
from models import Item


def update_sulfuras(item: Item) -> Item:
    """Updating Sulfuras is quite simple: Nothing changes, since it's a Legendary Item"""
    return item

def update_standard_item(item: Item) -> Item:
    """Update strategy for standard items that conform to the default set of business rules"""
    item = decrease_sell_in(item)
    quality_delta = -2 if is_expired(item.sell_in) else -1

    return adjust_quality(item, quality_delta)

def update_aged_brie(item: Item) -> Item:
    """Update strategy for aged brie"""
    item = decrease_sell_in(item)
    quality_delta = 2 if is_expired(item.sell_in) else 1

    return adjust_quality(item, quality_delta)

def update_backstage_pass(item: Item) -> Item:
    """Update strategy for aged brie"""
    item = decrease_sell_in(item)

    if is_expired(item.sell_in):
        return replace(item, quality=MIN_QUALITY)

    quality_delta = 1
    if item.sell_in < 5:
        quality_delta = 3
    elif item.sell_in < 10:
        quality_delta = 2

    return adjust_quality(item, quality_delta)

def get_update_strategy(item: Item) -> Callable[[Item], Item]:
    """Apply the correct update strategy based on an item's name"""
    return {
        "Aged Brie": update_aged_brie,
        "Backstage passes to a TAFKAL80ETC concert": update_backstage_pass,
        "Sulfuras, Hand of Ragnaros": update_sulfuras,
    }.get(item.name, update_standard_item)