from constants import MIN_QUALITY, MAX_QUALITY
from models import Item


def clamp_quality(quality: int) -> int:
    """Clamp quality between MIN_QUALITY and MAX_QUALITY"""
    return max(MIN_QUALITY, min(MAX_QUALITY, quality))

def is_expired(sell_in: int) -> bool:
    """Check if the sell_in date has passed"""
    return sell_in <= 0

def decrease_sell_in(item: Item) -> None:
    """Decrease sell in by 1"""
    item.sell_in -= 1