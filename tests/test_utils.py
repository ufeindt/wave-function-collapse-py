from unittest import TestCase

from wave_function_collapse.utils import shannon_entropy


class ShannonEntropyTests(TestCase):
    def test_entropy_zero_for_single_case(self):
        self.assertEqual(shannon_entropy(1), 0)
        self.assertEqual(shannon_entropy(10), 0)

    def test_entropy_one_for_two_equal_frequencies(self):
        self.assertEqual(shannon_entropy(1, 1), 1)

    def test_different_frequencies(self):
        self.assertEqual(shannon_entropy(1, 1, 1, 1), 2)
        self.assertEqual(shannon_entropy(1, 1, 2), 1.5)
        self.assertEqual(shannon_entropy(1, 1, 2, 4), 1.75)
