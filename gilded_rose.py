# -*- coding: utf-8 -*-
from update_strategies import update_item


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        self.items = list(map(update_item, self.items))
