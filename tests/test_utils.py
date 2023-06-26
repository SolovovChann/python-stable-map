import unittest

from stable_map.utils import mutate


def add_100_to(sequence: list[int]) -> None:
    sequence.append(100)


class TestMutate(unittest.TestCase):
    def test_mutate(self) -> None:
        sequence = [[item] for item in range(5)]
        reference = [
            [*item, 100]
            for item in sequence
        ]

        mutate(add_100_to, sequence, [])

        self.assertSequenceEqual(sequence, reference)
