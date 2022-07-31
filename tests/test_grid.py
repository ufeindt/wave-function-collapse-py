from unittest import TestCase, mock

import colorama

from wave_function_collapse.exceptions import WaveFunctionCollapseException
from wave_function_collapse.grid import Grid
from wave_function_collapse.tile import RuleDirection, RuleMatchingType, Tile


class GridUnitTests(TestCase):
    def setUp(self):
        self.tile1 = Tile(
            "Mountain",
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "mountain",
                    },
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "hill",
                    },
                )
            },
            symbol="M",
            tags=("mountain",),
        )
        self.tile2 = Tile(
            "Hill",
            color=colorama.Fore.GREEN,
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "mountain",
                    },
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "hill",
                    },
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "grassland",
                    },
                )
            },
            symbol="H",
            tags=("hill",),
        )
        self.tile3 = Tile(
            "Grassland",
            color=colorama.Fore.LIGHTGREEN_EX,
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "hill",
                    },
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "grassland",
                    },
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "sea",
                    },
                )
            },
            symbol="G",
            tags=("grassland",),
        )
        self.tile4 = Tile(
            "Sea",
            color=colorama.Fore.BLUE,
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "grassland",
                    },
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "sea",
                    },
                )
            },
            symbol="S",
            tags=("sea",),
        )
        self.tiles = [self.tile1, self.tile2, self.tile3, self.tile4]
        self.tiles_sorted = sorted(self.tiles, key=lambda t: t.name)

    def test_init(self):
        grid = Grid(self.tiles, size=(2, 2))
        self.assertEqual(grid.size, (2, 2))
        self.assertEqual(grid.tileset, self.tiles_sorted)

        for x in range(2):
            for y in range(2):
                self.assertIn((x, y), grid.spaces)
                space = grid.spaces[(x, y)]
                self.assertEqual(
                    space.possible_tiles,
                    self.tiles_sorted,
                )
                self.assertIsNone(space.tile)

    def test_str_initial(self):
        grid = Grid(self.tiles, size=(2, 2))
        self.assertEqual(str(grid), "  \n  ")

    def test_lowest_entropy_spaces(self):
        grid = Grid(self.tiles, size=(2, 2))
        self.assertEqual(
            grid.lowest_entropy_spaces,
            [(x, y) for x in range(2) for y in range(2)],
        )

        grid.spaces[(0, 0)].possible_tiles.pop()
        grid.spaces[(0, 0)].frequencies.pop()
        self.assertEqual(
            grid.lowest_entropy_spaces,
            [(0, 0)],
        )

    def test_lowest_entropy_spaces_all_assigned(self):
        grid = Grid(self.tiles, size=(2, 2))
        for space in grid.spaces.values():
            space.set_tile(space.possible_tiles[0])

        self.assertEqual(
            grid.lowest_entropy_spaces,
            [],
        )

    def test_check_tile_possible(self):
        grid = Grid(self.tiles, size=(2, 2))
        grid.spaces[(0, 0)].tile = self.tile1
        grid.spaces[(0, 0)].possible_tiles = None

        grid.update_possible_tiles([(0, 1), (1, 0)])

        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile1), 3)
        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile2), 4)
        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile3), 0)
        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile4), 0)

        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile1), 3)
        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile2), 4)
        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile3), 0)
        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile4), 0)

        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile1), 4)
        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile2), 4)
        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile3), 2)
        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile4), 0)

    def test_check_tile_possible_directional_rules(self):
        # Do not allow hills east of mountains/mountains west of hills.
        self.tiles[0].rules[RuleDirection.EAST] = (
            {
                "frequency": 1,
                "matching_type": RuleMatchingType.TAGS,
                "matching_value": "mountain",
            },
        )
        self.tiles[1].rules[RuleDirection.WEST] = (
            {
                "frequency": 1,
                "matching_type": RuleMatchingType.TAGS,
                "matching_value": "hill",
            },
            {
                "frequency": 1,
                "matching_type": RuleMatchingType.TAGS,
                "matching_value": "grassland",
            },
        )

        grid = Grid(self.tiles, size=(2, 2))
        grid.spaces[(0, 0)].tile = self.tiles[0]
        grid.spaces[(0, 0)].possible_tiles = None

        grid.update_possible_tiles([(0, 1), (1, 0)])

        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile1), 2)
        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile2), 3)
        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile3), 0)
        self.assertEqual(grid.get_tile_frequency((0, 1), self.tile4), 0)

        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile1), 3)
        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile2), 0)
        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile3), 0)
        self.assertEqual(grid.get_tile_frequency((1, 0), self.tile4), 0)

        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile1), 3)
        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile2), 2)
        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile3), 0)
        self.assertEqual(grid.get_tile_frequency((1, 1), self.tile4), 0)

    def test_update_possible_tiles_for_single_space(self):
        grid = Grid(self.tiles, size=(2, 2))
        grid.spaces[(0, 0)].tile = self.tile1
        grid.spaces[(0, 0)].possible_tiles = None

        grid.update_possible_tiles_for_single_space((0, 1))

        self.assertEqual(
            [tile.name for tile in grid.spaces[(0, 1)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 0)].possible_tiles],
            ["Grassland", "Hill", "Mountain", "Sea"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 1)].possible_tiles],
            ["Grassland", "Hill", "Mountain", "Sea"],
        )

    def test_update_possible_tiles(self):
        grid = Grid(self.tiles, size=(2, 2))
        grid.spaces[(0, 0)].tile = self.tile1
        grid.spaces[(0, 0)].possible_tiles = None

        grid.update_possible_tiles([(0, 1), (1, 0)])

        self.assertEqual(
            [tile.name for tile in grid.spaces[(0, 1)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 0)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 1)].possible_tiles],
            ["Grassland", "Hill", "Mountain"],
        )

    def test_update_possible_tiles_do_not_check_further(self):
        grid = Grid(self.tiles, size=(2, 2))
        grid.spaces[(0, 0)].tile = self.tile1
        grid.spaces[(0, 0)].possible_tiles = None

        grid.update_possible_tiles([(0, 1), (1, 0)], check_further=False)

        self.assertEqual(
            [tile.name for tile in grid.spaces[(0, 1)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 0)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 1)].possible_tiles],
            ["Grassland", "Hill", "Mountain", "Sea"],
        )

    @mock.patch("wave_function_collapse.space.random.uniform")
    @mock.patch("wave_function_collapse.grid.random.randrange")
    def test_assign_next_tile(
        self, random_randrange_mock, random_uniform_mock
    ):
        random_randrange_mock.return_value = 0
        random_uniform_mock.return_value = 12.5

        grid = Grid(self.tiles, size=(2, 2))
        grid.assign_next_tile()

        random_randrange_mock.assert_called_once_with(4)
        random_uniform_mock.assert_called_once_with(0, 20)

        self.assertEqual(grid.spaces[(0, 0)].tile.name, "Mountain")
        self.assertIsNone(grid.spaces[(0, 0)].possible_tiles)

        self.assertEqual(
            [tile.name for tile in grid.spaces[(0, 1)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 0)].possible_tiles],
            ["Hill", "Mountain"],
        )
        self.assertEqual(
            [tile.name for tile in grid.spaces[(1, 1)].possible_tiles],
            ["Grassland", "Hill", "Mountain"],
        )

        self.assertEqual(str(grid), f"{self.tile1} \n  ")

    @mock.patch("wave_function_collapse.space.random.uniform")
    @mock.patch("wave_function_collapse.grid.random.randrange")
    def test_assign_next_space_exception_if_all_assigned(
        self, random_randrange_mock, random_uniform_mock
    ):
        grid = Grid(self.tiles, size=(2, 2))
        for space in grid.spaces.values():
            space.set_tile(space.possible_tiles[0])

        with self.assertRaises(WaveFunctionCollapseException) as context:
            grid.assign_next_tile()

        self.assertEqual(
            str(context.exception), "All spaces have been assigned a tile."
        )

        random_randrange_mock.assert_not_called()
        random_uniform_mock.ssert_not_called()

    @mock.patch("wave_function_collapse.space.random.uniform")
    @mock.patch("wave_function_collapse.grid.random.randrange")
    def test_assign_next_space_auto_assign_zero_entropy(
        self, random_randrange_mock, random_uniform_mock
    ):
        random_randrange_mock.return_value = 0
        random_uniform_mock.return_value = 2.5

        self.tile1.rules[RuleDirection.ALL] = (
            {
                "frequency": 1,
                "matching_type": RuleMatchingType.TAGS,
                "matching_value": "mountain",
            },
        )
        self.tile2.rules[RuleDirection.ALL] = (
            {
                "frequency": 1,
                "matching_type": RuleMatchingType.TAGS,
                "matching_value": "hill",
            },
        )

        grid = Grid([self.tile1, self.tile2], size=(2, 2))
        grid.assign_next_tile()

        random_randrange_mock.assert_called_once_with(4)
        random_uniform_mock.assert_called_once_with(0, 4)

        for x in range(2):
            for y in range(2):
                self.assertEqual(grid.spaces[(x, y)].tile.name, "Mountain")
                self.assertIsNone(grid.spaces[(x, y)].possible_tiles)

        self.assertEqual(
            str(grid), f"{self.tile1}{self.tile1}\n{self.tile1}{self.tile1}"
        )

    @mock.patch("wave_function_collapse.space.random.uniform")
    @mock.patch("wave_function_collapse.grid.random.randrange")
    def test_assign_all_tiles(
        self, random_randrange_mock, random_uniform_mock
    ):
        random_randrange_mock.return_value = 0
        random_uniform_mock.side_effect = [12.5, 4.5, 4.5, 3.5]

        grid = Grid(self.tiles, size=(2, 2))
        grid.assign_all_tiles()

        random_randrange_mock.assert_has_calls(
            [mock.call(4), mock.call(2), mock.call(2), mock.call(1)],
            any_order=False,
        )
        random_uniform_mock.assert_has_calls(
            [
                mock.call(0, 20),
                mock.call(0, 7),
                mock.call(0, 6),
                mock.call(0, 4),
            ],
            any_order=False,
        )

        for x in range(2):
            for y in range(2):
                self.assertEqual(grid.spaces[(x, y)].tile.name, "Mountain")
                self.assertIsNone(grid.spaces[(x, y)].possible_tiles)

        self.assertEqual(
            str(grid), f"{self.tile1}{self.tile1}\n{self.tile1}{self.tile1}"
        )
