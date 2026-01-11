import pytest

from models import Item
from helpers import decrease_sell_in, adjust_quality


class TestImmutability:
    def test_item_is_immutable(self) -> None:
        item = Item("Test", sell_in=5, quality=10)

        with pytest.raises(Exception): # FrozenInstanceError
            # noinspection PyDataclass
            item.quality = 15

    def test_decrease_sell_in_immutable(self) -> None:
        original = Item("Test", sell_in=5, quality=10)
        updated = decrease_sell_in(original)

        assert original.sell_in == 5  # the original is not changed
        assert updated.sell_in == 4  # new instance of Item
        assert original is not updated

    def test_adjust_quality_immutable(self):
        original = Item("Test", sell_in=5, quality=10)
        updated = adjust_quality(original, -3)

        assert original.quality == 10  # the original is not changed
        assert updated.quality == 7  # new instance of Item
