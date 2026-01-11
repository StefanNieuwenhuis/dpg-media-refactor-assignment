# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    sell_in: int
    quality: int
