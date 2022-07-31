from unittest import TestCase, mock

import colorama

from wave_function_collapse.exceptions import WaveFunctionCollapseException
from wave_function_collapse.space import Space
from wave_function_collapse.tile import RuleDirection, RuleMatchingType, Tile


class SpaceUnitTests(TestCase):
    def setUp(self):
        self.tile1 = Tile(
            "Test Tile 1",
            color=colorama.Fore.CYAN,
            frequency=10,
            rules={
                RuleDirection.ALL: (
                    {
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": ("test-1", "test-2"),
                    }
                )
            },
            symbol="A",
            tags=("test-1",),
        )
        self.tile2 = Tile(
            "Test Tile 2",
            color=colorama.Fore.RED,
            frequency=5,
            rules={
                RuleDirection.ALL: (
                    {
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": ("test-1", "test_2"),
                    }
                )
            },
            symbol="B",
            tags=("test-2",),
        )
        self.tiles = [self.tile1, self.tile2]

    def test_init_possible_tiles(self):
        space = Space((1, 2), possible_tiles=self.tiles)
        self.assertEqual(space.coords, (1, 2))
        self.assertEqual(space.possible_tiles, self.tiles)
        self.assertIsNone(space.tile)

    def test_init_tile(self):
        space = Space((1, 2), tile=self.tile1)
        self.assertEqual(space.coords, (1, 2))
        self.assertEqual(space.tile, self.tile1)
        self.assertIsNone(space.possible_tiles)

    def test_init_cannot_assign_tile_and_possible_tiles(self):
        with self.assertRaises(ValueError) as context:
            Space((1, 2), possible_tiles=self.tiles, tile=self.tile1)

        self.assertEqual(
            str(context.exception), "Cannot assign possible tiles and tile."
        )

    def test_init_must_assign_tile_or_possible_tiles(self):
        with self.assertRaises(ValueError) as context:
            Space((1, 2))

        self.assertEqual(
            str(context.exception),
            "Must assign either possible tiles or tile.",
        )

    @mock.patch("wave_function_collapse.space.shannon_entropy")
    def test_entropy_for_possible_tiles(self, entropy_mock):
        entropy_mock.return_value = 0.987654321
        space = Space((1, 2), possible_tiles=self.tiles)
        self.assertEqual(space.entropy, 0.987654321)
        entropy_mock.assert_called_once_with(
            self.tile1.frequency, self.tile2.frequency
        )

    @mock.patch("wave_function_collapse.space.shannon_entropy")
    def test_entropy_zero_if_assigned_tile(self, entropy_mock):
        entropy_mock.return_value = 0.987654321
        space = Space((1, 2), tile=self.tile1)
        self.assertEqual(space.entropy, 0)
        entropy_mock.assert_not_called()

    def test_neighbors(self):
        space = Space((1, 2), possible_tiles=self.tiles)
        self.assertEqual(
            space.neighbors,
            {
                RuleDirection.NORTH: (1, 1),
                RuleDirection.EAST: (2, 2),
                RuleDirection.SOUTH: (1, 3),
                RuleDirection.WEST: (0, 2),
            },
        )

    @mock.patch("wave_function_collapse.space.random.uniform")
    def test_assign_first_tile(self, random_uniform_mock):
        random_uniform_mock.return_value = 8

        space = Space((1, 2), possible_tiles=self.tiles)
        space.assign_tile()

        self.assertIsNone(space.possible_tiles)
        self.assertEqual(space.tile, self.tile1)
        random_uniform_mock.assert_called_once_with(0, 15)

    @mock.patch("wave_function_collapse.space.random.uniform")
    def test_assign_second_tile(self, random_uniform_mock):
        random_uniform_mock.return_value = 12

        space = Space((1, 2), possible_tiles=self.tiles)
        space.assign_tile()

        self.assertIsNone(space.possible_tiles)
        self.assertEqual(space.tile, self.tile2)
        random_uniform_mock.assert_called_once_with(0, 15)

    @mock.patch("wave_function_collapse.space.random.uniform")
    def test_assign_tile_raise_if_already_collapsed(self, random_uniform_mock):
        space = Space((1, 2), tile=self.tile1)

        with self.assertRaises(WaveFunctionCollapseException) as context:
            space.assign_tile()

        self.assertEqual(
            str(context.exception),
            "This space has already been assigned a tile.",
        )
        random_uniform_mock.assert_not_called()

    @mock.patch("wave_function_collapse.space.random.uniform")
    def test_assign_tile_no_random_number_if_one_option(
        self, random_uniform_mock
    ):
        space = Space((1, 2), possible_tiles=[self.tile1])
        space.assign_tile()

        self.assertIsNone(space.possible_tiles)
        self.assertEqual(space.tile, self.tile1)
        random_uniform_mock.assert_not_called()

    def test_set_tile(self):
        space = Space((1, 2), possible_tiles=self.tiles)
        space.set_tile(self.tiles[0])

        self.assertEqual(space.tile, self.tiles[0])
        self.assertIsNone(space.possible_tiles)
        self.assertIsNone(space.frequencies)

    def test_set_possible_tiles(self):
        space = Space((1, 2), possible_tiles=self.tiles)
        space.set_possible_tiles(self.tiles[:-1])

        self.assertEqual(space.possible_tiles, self.tiles[:-1])

    def test_set_possible_tiles_raise_exception_if_empty(self):
        space = Space((1, 2), possible_tiles=self.tiles)

        with self.assertRaises(WaveFunctionCollapseException) as context:
            space.set_possible_tiles([])

        self.assertEqual(
            str(context.exception),
            "No options remaining for this space. This should not happen. "
            "Please check the rules.",
        )

    def test_set_frequencies(self):
        space = Space((1, 2), possible_tiles=self.tiles)
        space.set_frequencies([5, 10])

        self.assertEqual(space.frequencies, [5, 10])

    def test_set_frequencies_remove_if_zero(self):
        space = Space((1, 2), possible_tiles=self.tiles)
        space.set_frequencies([5, 0])

        self.assertEqual(space.frequencies, [5])
        self.assertEqual(space.possible_tiles, [self.tile1])

    def test_set_frequencies_exception_if_all_zero(self):
        space = Space((1, 2), possible_tiles=self.tiles)

        with self.assertRaises(WaveFunctionCollapseException) as context:
            space.set_frequencies([0, 0])

        self.assertEqual(
            str(context.exception),
            "No options remaining for this space. This should not happen. "
            "Please check the rules.",
        )
