from unittest import TestCase

import colorama

from wave_function_collapse.tile import RuleDirection, RuleMatchingType, Tile


class TileUnitTests(TestCase):
    def test_init(self):
        tile = Tile(
            "Test Tile",
            color=colorama.Fore.CYAN,
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "test",
                    },
                )
            },
            symbol="A",
            tags=("test",),
        )
        self.assertEqual(tile.name, "Test Tile")
        self.assertEqual(tile.color, colorama.Fore.CYAN)
        self.assertEqual(
            tile.rules,
            {
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "test",
                    },
                )
            },
        )
        self.assertEqual(tile.symbol, "A")
        self.assertEqual(tile.tags, ("test",))

    def test_symbol_must_be_single_character(self):
        with self.assertRaises(ValueError) as context:
            Tile("Test Tile", symbol="ABC")

        self.assertEqual(
            str(context.exception), "Symbol must be a single character."
        )

    def test_symbol_defaults_to_block(self):
        tile = Tile("Test Tile")
        self.assertEqual(tile.symbol, "█")

    def test_default_color_none(self):
        tile = Tile("Test Tile")
        self.assertIsNone(tile.color)

    def test_str(self):
        tile = Tile("Test Tile", symbol="A", color=colorama.Fore.CYAN)
        self.assertEqual(
            str(tile), f"{colorama.Fore.CYAN}A{colorama.Style.RESET_ALL}"
        )

    def test_str_no_color(self):
        tile = Tile("Test Tile", symbol="A")
        self.assertEqual(str(tile), "A")

    def test_get_adjacency_frequency(self):
        tile1 = Tile(
            "Test Tile 1",
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "test",
                    },
                ),
            },
            tags=("test",),
        )

        tile2 = Tile(
            "Test Tile 2",
            tags=("test",),
        )

        self.assertEqual(
            tile1.get_adjacency_frequency(tile2, RuleDirection.NORTH), 1
        )

    def test_check_rules_wrong_direction(self):
        tile1 = Tile(
            "Test Tile 1",
            rules={
                RuleDirection.WEST: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "test",
                    },
                ),
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "test-2",
                    },
                ),
            },
            tags=("test",),
        )

        tile2 = Tile(
            "Test Tile 2",
            tags=("test",),
        )

        self.assertEqual(
            tile1.get_adjacency_frequency(tile2, RuleDirection.NORTH), 0
        )

    def test_check_rules_wrong_tag(self):
        tile1 = Tile(
            "Test Tile 1",
            rules={
                RuleDirection.ALL: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_value": "test-2",
                    },
                )
            },
            tags=("test",),
        )

        tile2 = Tile(
            "Test Tile 2",
            tags=("test",),
        )

        self.assertEqual(
            tile1.get_adjacency_frequency(tile2, RuleDirection.NORTH), 0
        )

    def test_check_rules_false_if_no_rules(self):
        tile1 = Tile(
            "Test Tile 1",
            rules={
                RuleDirection.WEST: (
                    {
                        "frequency": 1,
                        "matching_type": RuleMatchingType.TAGS,
                        "matching_values": "test-2",
                    },
                )
            },
            tags=("test",),
        )

        tile2 = Tile(
            "Test Tile 2",
            tags=("test",),
        )

        self.assertEqual(
            tile1.get_adjacency_frequency(tile2, RuleDirection.NORTH), 0
        )
