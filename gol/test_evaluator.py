#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    sys.path.append('..')

from rules_parser.rules_parser import Selector, SelectorOperator, Comparison, \
    BoolOperator

GRID = [
    'ccc',
    'bbb',
    'aaa',
]


def _test_evaluator():
    assert Selector('aaaaaaaaa')(GRID, (1, 1), {}) == 3
    assert Selector('aaaaaaaaa')(GRID, (0, 1), {}) == 2
    assert Selector('*********')(GRID, (1, 1), {}) == 9
    assert Selector('*********')(GRID, (0, 1), {}) == 6
    # TODO: add more tests


def _test_selector_evaluator():
    assert SelectorOperator('+', [1, 1])(GRID, (0, 0), {}) == 2
    assert SelectorOperator('-', [1, 2])(GRID, (0, 0), {}) == -1
    assert SelectorOperator('*', [2, 2])(GRID, (0, 0), {}) == 4
    assert SelectorOperator('/', [6, 2])(GRID, (0, 0), {}) == 3
    assert SelectorOperator('%', [5, 2])(GRID, (0, 0), {}) == 1

    assert SelectorOperator('+', [1, 1, 1])(GRID, (0, 0), {}) == 3
    assert SelectorOperator('-', [5, 2, 2])(GRID, (0, 0), {}) == 1

    assert SelectorOperator('*', [Selector('aaaaaaaaa'), 2])\
        (GRID, (1, 1), {}) == 6
    # TODO: add more tests


def _test_comparison_evaluator():
    assert Comparison(5, '<', 10)(GRID, (0, 0), {}) is True
    assert Comparison(5, '>', 10)(GRID, (0, 0), {}) is False
    assert Comparison(Selector('cccaaaaaa'), '>=', 6)(GRID, (1, 1), {}) is True
    assert Comparison(Selector('cccaaaaaa'), '>=', 5)(GRID, (1, 1), {}) is True
    assert Comparison(Selector('cccaaaaaa'), '>=', 7)(GRID, (1, 1), {}) is False
    assert Comparison(Selector('cccaaaaaa'), '>', 6)(GRID, (1, 1), {}) is False

    # TODO: add all operators & some SelectorOperators


def _test_bool_op_evaluator():
    assert BoolOperator('and', [Comparison(5, '<', 10), Comparison(0, '<', 1)]) is True
    assert BoolOperator('and', [Comparison(5, '<', 10), Comparison(1, '<', 1)]) is False
    assert BoolOperator('or', [Comparison(5, '<', 10), Comparison(0, '<', 1)]) is True
    assert BoolOperator('or', [Comparison(5, '<', 10), Comparison(1, '<', 1)]) is True
    assert BoolOperator('or', [Comparison(5, '>', 10), Comparison(1, '<', 1)]) is True


if __name__ == '__main__':
    _test_evaluator()
    _test_selector_evaluator()
    _test_comparison_evaluator()
