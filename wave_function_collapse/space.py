import random
from typing import List, Tuple

from wave_function_collapse.exceptions import WaveFunctionCollapseException
from wave_function_collapse.tile import RuleDirection, Tile
from wave_function_collapse.utils import shannon_entropy


class Space:
    """Square space with either a list of possible tiles and an assigned
    tile.

    Attributes:
        coords: The space's coordinates (x, y). (The x-axis points east,
            y-axis south.)
        possible_tiles: List of possible tiles that could be assigned.
            Mutually exclusive with tile.
        tile: Tile assigned to the space. Mutually exclusive with tile.

    Properties:
        entropy: Shannon entropy of the space based on the possibles
            tiles' frequencies.
        neighbors: List of neighboring coordingates.
    """

    def __init__(
        self,
        coords: Tuple[int],
        possible_tiles: List[Tile] = None,
        tile: Tile = None,
    ):
        if possible_tiles and tile:
            raise ValueError("Cannot assign possible tiles and tile.")

        if not possible_tiles and not tile:
            raise ValueError("Must assign either possible tiles or tile.")

        self.coords = coords
        self.possible_tiles = possible_tiles
        self.tile = tile

    @property
    def entropy(self):
        """Shannon entropy."""
        if self.possible_tiles:
            return shannon_entropy(
                *[tile.frequency for tile in self.possible_tiles]
            )

        return 0

    @property
    def neighbors(self):
        """Neighboring coordinates."""
        return {
            RuleDirection.NORTH: (self.coords[0], self.coords[1] - 1),
            RuleDirection.EAST: (self.coords[0] + 1, self.coords[1]),
            RuleDirection.SOUTH: (self.coords[0], self.coords[1] + 1),
            RuleDirection.WEST: (self.coords[0] - 1, self.coords[1]),
        }

    def assign_tile(self):
        """Assigns a tile to the space based on the tiles' frequencies.

        Raises:
            WaveFunctionCollapseException if already assigned.
        """
        if not self.possible_tiles:
            raise WaveFunctionCollapseException(
                "This space has already been assigned a tile."
            )
        elif len(self.possible_tiles) == 1:
            self.tile = self.possible_tiles[0]
            self.possible_tiles = None
            return

        random_number = random.uniform(
            0, sum(tile.frequency for tile in self.possible_tiles)
        )

        cumulative_frequency = 0
        for tile in self.possible_tiles:
            cumulative_frequency += tile.frequency
            if random_number < cumulative_frequency:
                self.tile = tile
                self.possible_tiles = None
                break
