import pytest

from decision_games_with_ai.games.utils.coords_formatters import CoordsFormatter


@pytest.fixture
def coords_formatters():
    pass


def test_translate_from_xy_to_uci(coords_formatters):
    expected = 'b1'
    result = CoordsFormatter.translate_from_xy_to_uci(1, 0)

    assert expected == result


def test_translate_from_uci_to_xy(coords_formatters):
    expected = 2, 3
    result = CoordsFormatter.translate_from_uci_to_xy('c4')

    assert expected == result