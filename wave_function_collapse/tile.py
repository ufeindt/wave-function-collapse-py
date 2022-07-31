from __future__ import annotations

from enum import Enum
from typing import Dict, Tuple, TypedDict

import colorama


class RuleDirection(str, Enum):
    ALL = "ALL"
    EAST = "E"
    NORTH = "N"
    # NORTHEAST = "NE"
    # NORTHWEST = "NW"
    SOUTH = "S"
    # SOUTHEAST = "SE"
    # SOUTHWEST = "SW"
    WEST = "W"


class RuleMatchingType(str, Enum):
    # BORDER = "BORDER"
    # NOT_TAGS = "NOT TAGS"
    TAGS = "TAGS"


class TileRule(TypedDict):
    frequency: float
    matching_type: RuleMatchingType
    matching_value: str


class Tile:
    """Class representing a tile with the methods for drawing it.

    Attributes:
        name: Tile name, used in rules for specific tiles.
        color: ANSI color string for terminal output (default: None).
        frequency: Integer frequency of the tiles occurence (default: 1)
        rules: Dictionary of rules for adjacent tiles with directions as
            keys,  (default: None).
        symbol: String symbol representation for terminal output
            (default: █).
        tags: List of string tags, used for rules for tagged tiles
            (default: None).
    """

    def __init__(
        self,
        name: str,
        color: str = None,
        frequency: float = 1,
        rules: Dict[RuleDirection, Tuple[TileRule]] = None,
        symbol: str = "█",
        tags: Tuple[str] = None,
    ) -> None:
        if not symbol:
            self.symbol = "█"
        elif len(symbol) != 1:
            raise ValueError("Symbol must be a single character.")
        else:
            self.symbol = symbol

        if frequency < 1:
            raise ValueError("Frequency must be > 0.")

        self.name = name
        self.color = color
        self.frequency = frequency
        self.rules = rules
        self.tags = tags

    def __str__(self, **kwargs):
        if self.color:
            return f"{self.color}{self.symbol}{colorama.Style.RESET_ALL}"

        return self.symbol

    def get_adjacency_frequency(
        self, tile: Tile, direction: RuleDirection
    ) -> float:
        """Get the frewuency of a certain tile occuring adjacent to this
        tile in the given direction.

        Argument:
            tile: Another tile.
            direction: The direction, in which that tile may be placed.

        Returns:
            Frequency of this tile occuring.
        """
        if not (rules := self.rules.get(direction)):
            if not (rules := self.rules.get(RuleDirection.ALL)):
                return False

        frequency = 0
        for rule in rules:
            if rule["matching_type"] == RuleMatchingType.TAGS:
                if rule["matching_value"] in tile.tags:
                    frequency += rule["frequency"]

        return max(0, frequency)
