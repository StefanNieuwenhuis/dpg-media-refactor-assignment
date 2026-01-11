# -*- coding: utf-8 -*-

from update_strategies import get_update_strategy


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for i, item in enumerate(self.items):
            strategy = get_update_strategy(item)
            self.items[i] = strategy(item)
