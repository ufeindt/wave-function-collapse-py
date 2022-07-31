import random
from copy import copy
from typing import List, Tuple

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

    def check_tile_possible(self, coords: Tuple[int], tile: Tile) -> bool:
        """Checks if a tile is allowed at the given coordinates.

        Arguments:
            coords: A space's coordinates.
            tile: The tile to be checked.

        Returns:
            Boolean flag whether the tile is allowed.
        """
        space = self.spaces[coords]

        for direction, neighbor_coords in space.neighbors.items():
            if neighbor_coords not in self.spaces:
                continue

            neighbor = self.spaces[neighbor_coords]
            if neighbor.tile:
                tiles_to_check = [neighbor.tile]
            else:
                tiles_to_check = neighbor.possible_tiles

            if not any(
                tile.get_adjacency_frequency(t_, direction)
                for t_ in tiles_to_check
            ):
                return False

        return True

    def update_possible_tiles_for_single_space(
        self, coords: Tuple[int]
    ) -> bool:
        """Updates the possible tiles for a space.

        Arguments:
            coords: The space's coordinates.

        Returns:
            Boolean flag whether any fields were updated.

        Raises:
            WaveFunctionCollapseException if a tile is already assigned.
        """
        space = self.spaces[coords]
        original_possible_tiles = copy(space.possible_tiles)

        space.possible_tiles = [
            tile
            for tile in space.possible_tiles
            if self.check_tile_possible(coords, tile)
        ]

        if not space.possible_tiles:
            raise WaveFunctionCollapseException(
                "No options remaining for this space. "
                "This should not happen. "
                "Please check the rules."
            )

        if len(space.possible_tiles) == 1:
            space.assign_tile()

        return space.possible_tiles != original_possible_tiles

    def update_possible_tiles(
        self,
        coords_to_check: List[Tuple[int]],
        check_further: bool = True,
        shuffle_list: bool = True,
    ):
        """Updates the possible tiles for a list of spaces.

        Arguments:
            coords_to_check: List of space coordinates to check.
            check_further: Flag whether the neighbors of checked spaces
                that changed should also be checked (default: True).
            shuffle_list: Flag whether to shuffle the list of
                coordinates (default: True).

        Raises:
            WaveFunctionCollapseException if a tile is already assigned.
        """
        coords_checked = []
        if shuffle_list:
            random.shuffle(coords_to_check)

        while coords_to_check:
            coords = coords_to_check.pop(0)
            updated = self.update_possible_tiles_for_single_space(coords)

            if updated and check_further:
                new_coords_to_check = [
                    c_
                    for c_ in self.spaces[coords].neighbors.values()
                    if c_ in self.spaces
                    and c_ not in coords_to_check
                    and c_ not in coords_checked
                    and self.spaces[c_].possible_tiles
                ]
                if shuffle_list:
                    random.shuffle(new_coords_to_check)
                coords_to_check.extend(new_coords_to_check)

    def assign_next_tile(self):
        """Assgins a tile to the next space.

        Raises:
            WaveFunctionCollapseException if not spaces left.
        """
        if not (low_entropy_spaces := self.lowest_entropy_spaces):
            raise WaveFunctionCollapseException(
                "All spaces have been assigned a tile."
            )

        coords = low_entropy_spaces[random.randrange(len(low_entropy_spaces))]
        self.spaces[coords].assign_tile()

        coords_to_check = [
            coord
            for coord in self.spaces[coords].neighbors.values()
            if coord in self.spaces and self.spaces[coord].possible_tiles
        ]
        self.update_possible_tiles(coords_to_check)

    def assign_all_tiles(self):
        """Assigns tiles to spaces until there are none left."""
        while self.lowest_entropy_spaces:
            self.assign_next_tile()
