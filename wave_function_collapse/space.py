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
        frequencies: List of floats of the same length as possible_tiles
            representing the tile's frequencies.
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

        if possible_tiles:
            self.frequencies = [1 for tile in possible_tiles]
        else:
            self.frequencies = None

    @property
    def entropy(self):
        """Shannon entropy."""
        if self.frequencies:
            return shannon_entropy(
                *[frequency for frequency in self.frequencies]
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

    def set_tile(self, tile):
        """Set the tile attribute and resets possible_tiles and
        frequencies.
        """
        self.tile = tile
        self.possible_tiles = None
        self.frequencies = None

    def set_possible_tiles(self, possible_tiles: List[Tile]):
        """Sets the possible_tiles property.

        Raises:
            WaveFunctionCollapseException if no tiles remain as this
            should not happen.
        """
        if not possible_tiles:
            raise WaveFunctionCollapseException(
                "No options remaining for this space. "
                "This should not happen. "
                "Please check the rules."
            )

        self.possible_tiles = possible_tiles

    def set_frequencies(self, frequencies: List[float]):
        if 0 in frequencies:
            self.set_possible_tiles(
                [
                    tile
                    for frequency, tile in zip(
                        frequencies, self.possible_tiles
                    )
                    if frequency
                ]
            )
            frequencies = [frequency for frequency in frequencies if frequency]

        self.frequencies = frequencies

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
            self.set_tile(self.possible_tiles[0])
            return

        random_number = random.uniform(0, sum(self.frequencies))

        cumulative_frequency = 0
        for tile, frequency in zip(self.possible_tiles, self.frequencies):
            cumulative_frequency += frequency
            if random_number < cumulative_frequency:
                self.set_tile(tile)
                break
