from dataclasses import replace

from constants import MIN_QUALITY, MAX_QUALITY
from models import Item


def clamp_quality(quality: int) -> int:
    """Clamp quality between MIN_QUALITY and MAX_QUALITY"""
    return max(MIN_QUALITY, min(MAX_QUALITY, quality))

def is_expired(sell_in: int) -> bool:
    """Check if the sell_in date has passed"""
    return sell_in <= 0

def decrease_sell_in(item: Item) -> Item:
    """Decrease sell in by 1"""
    return replace(item, sell_in=item.sell_in - 1)

def adjust_quality(item: Item, delta: int) -> Item:
    """Return a new Item with quality adjusted by delta"""
    adjusted_quality = clamp_quality(item.quality + delta)
    return replace(item, quality=adjusted_quality)