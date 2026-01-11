from dataclasses import replace
from typing import Callable

from constants import MIN_QUALITY, AGED_BRIE, BACKSTAGE_PASS, SULFURAS, CONJURED_PREFIX, CONJURED_DEGRADATION
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

def update_conjured_item(item: Item) -> Item:
    """Update strategy for conjured items"""
    item = decrease_sell_in(item)

    quality_delta = -(CONJURED_DEGRADATION * 2) if is_expired(item.sell_in) else -CONJURED_DEGRADATION

    return adjust_quality(item, quality_delta)

def get_update_strategy(item: Item) -> Callable[[Item], Item]:
    """Apply the correct update strategy based on an item's name"""
    if item.name.startswith(CONJURED_PREFIX):
        return update_conjured_item

    return {
        AGED_BRIE: update_aged_brie,
        BACKSTAGE_PASS: update_backstage_pass,
        SULFURAS: update_sulfuras,
    }.get(item.name, update_standard_item)


def update_item(item: Item) -> Item:
    """Select and apply the appropriate strategy"""
    strategy = get_update_strategy(item)

    return strategy(item)