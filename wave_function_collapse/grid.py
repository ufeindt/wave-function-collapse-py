import random
from copy import copy
from typing import List, Tuple

from wave_function_collapse.constants import ADJACENT_BORDERS
from wave_function_collapse.exceptions import WaveFunctionCollapseException
from wave_function_collapse.space import Space
from wave_function_collapse.tile import Tile


class Grid:
    """Grid of spaces.

    Attributes:
        tileset: List of tiles to be used, will be resorted by name.
            Tile names must be unique.
        size: Size of the grid (width x height, default: 20x20).
    """

    def __init__(self, tileset: List[Tile], size: Tuple[int] = (20, 20)):
        self.tileset = sorted(tileset, key=lambda t: t.name)
        self.size = size
        self.spaces = {
            (x, y): Space((x, y), possible_tiles=copy(self.tileset))
            for x in range(self.size[0])
            for y in range(self.size[1])
        }

    def __str__(self):
        lines = []
        for y in range(self.size[1]):
            line = ""
            for x in range(self.size[0]):
                if tile := self.spaces[(x, y)].tile:
                    line += str(tile)
                else:
                    line += " "
            lines.append(line)

        return "\n".join(lines)

    @property
    def lowest_entropy_spaces(self):
        non_zero_entropy_spaces = [
            space.entropy
            for space in self.spaces.values()
            if space.entropy > 0
        ]
        if not non_zero_entropy_spaces:
            return []

        min_entropy = min(non_zero_entropy_spaces)

        return sorted(
            [
                coords
                for coords, space in self.spaces.items()
                if space.entropy == min_entropy
            ]
        )

    def assign_next_tile(self):
        """Assgins a tile to the next space.

        Raises:
            WaveFunctionCollapseException if not spaces left.
        """
        if not (coords := self.lowest_entropy_spaces):
            raise WaveFunctionCollapseException(
                "All spaces have been assigned a tile."
            )

        coord = coords[random.randrange(len(coords))]
        self.spaces[coord].assign_tile()

        coords_checked = []
        coords_to_check = [
            coord
            for coord in self.spaces[coord].neighbors.values()
            if coord in self.spaces and self.spaces[coord].possible_tiles
        ]
        random.shuffle(coords_to_check)

        while coords_to_check:
            coord = coords_to_check.pop(0)
            space = self.spaces[coord]
            neighbors = {
                ADJACENT_BORDERS[d_]: c_
                for d_, c_ in space.neighbors.items()
                if c_ in self.spaces
            }
            original_possible_tiles = copy(space.possible_tiles)

            for direction, neighbor_coord in neighbors.items():
                neighbor = self.spaces[neighbor_coord]
                if neighbor.tile:
                    tiles_to_check = [neighbor.tile]
                else:
                    tiles_to_check = neighbor.possible_tiles

                space.possible_tiles = [
                    t_
                    for t_ in space.possible_tiles
                    if any(
                        tile.check_rules(t_, direction)
                        for tile in tiles_to_check
                    )
                ]

            if not space.possible_tiles:
                raise WaveFunctionCollapseException(
                    "No options remaining for this space. "
                    "This should not happen. "
                    "Please check the rules."
                )

            if len(space.possible_tiles) == 1:
                space.assign_tile()

            if space.possible_tiles != original_possible_tiles:
                new_coords_to_check = [
                    c_
                    for c_ in space.neighbors.values()
                    if c_ in self.spaces
                    and c_ not in coords_to_check
                    and c_ not in coords_checked
                    and self.spaces[c_].possible_tiles
                ]
                random.shuffle(new_coords_to_check)
                coords_to_check.extend(new_coords_to_check)

    def assign_all_tiles(self):
        """Assigns tiles to spaces until there are none left."""
        while self.lowest_entropy_spaces:
            self.assign_next_tile()
