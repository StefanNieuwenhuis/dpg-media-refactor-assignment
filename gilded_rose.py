# -*- coding: utf-8 -*-
from helpers import is_expired, decrease_sell_in, adjust_quality


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for i, item in enumerate(self.items):
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item = adjust_quality(item, -1)
            else:
                if item.quality < 50:
                    item = adjust_quality(item, 1)
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item = adjust_quality(item, 1)
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item = adjust_quality(item, 1)
            if item.name != "Sulfuras, Hand of Ragnaros":
                item = decrease_sell_in(item)
            if is_expired(item.sell_in):
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item = adjust_quality(item, -1)
                    else:
                        item = adjust_quality(item, -item.quality)
                else:
                    if item.quality < 50:
                        item = adjust_quality(item, 1)

            self.items[i] = item
