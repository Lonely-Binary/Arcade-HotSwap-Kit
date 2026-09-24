"""Host-side tests for Pico debounce, pulse groups and game rules."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PERIOD = 1 << 30
now = 0


def ticks_diff(a, b):
    return ((a - b + PERIOD // 2) % PERIOD) - PERIOD // 2


class Pin:
    IN, PULL_DOWN, PULL_UP, IRQ_FALLING = range(4)

    def __init__(self, gpio, mode=None, pull=None):
        self.level = 1 if pull == self.PULL_UP else 0
        self.handler = None

    def value(self):
        return self.level

    def irq(self, trigger=None, handler=None, hard=False):
        self.handler = handler


clock = types.SimpleNamespace(ticks_ms=lambda: now, ticks_diff=ticks_diff,
                              sleep_ms=lambda _: None)
machine = types.SimpleNamespace(Pin=Pin, disable_irq=lambda: 0, enable_irq=lambda _: None)
micropython = types.SimpleNamespace(alloc_emergency_exception_buf=lambda _: None)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


with patch.dict(sys.modules, {"time": clock, "machine": machine, "micropython": micropython}):
    arcade = load("arcade", "examples/pico/arcade.py")
    with patch.dict(sys.modules, {"arcade": arcade}):
        game = load("credit_game", "examples/pico/credit_game.py")


def at(value):
    global now
    now = value % PERIOD


class Inputs(unittest.TestCase):
    def setUp(self):
        at(0)

    def test_bounce_and_held_button(self):
        button = arcade.Button(16)
        button.pin.level = 1
        at(10); self.assertEqual(button.poll(), 0)
        button.pin.level = 0
        at(15); self.assertEqual(button.poll(), 0)
        button.pin.level = 1
        at(20); self.assertEqual(button.poll(), 0)
        at(49); self.assertEqual(button.poll(), 0)
        at(50); self.assertEqual(button.poll(), 1)
        at(500); self.assertEqual(button.poll(), 0)
        button.pin.level = 0
        at(510); self.assertEqual(button.poll(), 0)
        at(540); self.assertEqual(button.poll(), -1)

    def test_two_pulses_and_bounce_form_one_group(self):
        coin = arcade.CoinInput()
        for t in (10, 15, 110):
            at(t); coin._edge(coin.pin)
        at(309); self.assertEqual(coin.poll(), 0)
        at(310); self.assertEqual(coin.poll(), 2)
        self.assertEqual(coin.poll(), 0)

    def test_new_coin_before_loop_resumes_preserves_both(self):
        coin = arcade.CoinInput()
        at(10); coin._edge(coin.pin)
        at(310); coin._edge(coin.pin)
        at(510)
        self.assertEqual(coin.poll(), 1)
        self.assertEqual(coin.poll(), 1)
        self.assertEqual(coin.poll(), 0)

    def test_timer_wrap(self):
        coin = arcade.CoinInput()
        at(PERIOD - 50); coin._edge(coin.pin)
        at(50); coin._edge(coin.pin)
        at(250); self.assertEqual(coin.poll(), 2)

    def test_excessive_pulses_are_not_a_valid_small_group(self):
        coin = arcade.CoinInput()
        for i in range(15):
            at(10 + i * 100); coin._edge(coin.pin)
        at(1610); self.assertEqual(coin.poll(), 11)

    def test_queue_overflow_is_reported(self):
        coin = arcade.CoinInput()
        for i in range(10):
            at(i * 300); coin._edge(coin.pin)
        self.assertEqual(coin.poll(), -1)
        self.assertEqual(coin.poll(), 0)


class GameRules(unittest.TestCase):
    def test_start_requires_credit(self):
        state = game.Game()
        self.assertEqual(state.update(0, start=True), ["Insert a coin"])
        self.assertFalse(state.playing)

    def test_one_credit_one_round_and_no_restart(self):
        state = game.Game()
        state.update(0, pulses=1)
        state.update(100, start=True)
        state.update(200, start=True)
        self.assertEqual(state.credits, 0)
        self.assertEqual(state.started, 100)
        self.assertTrue(state.playing)

    def test_unknown_groups_do_not_award_credit(self):
        state = game.Game()
        for n in (2, 3, 11, -1):
            state.update(0, pulses=n)
        self.assertEqual(state.credits, 0)

    def test_deadline_precedes_score(self):
        state = game.Game()
        state.update(0, pulses=1, start=True)
        state.update(9999, hit=True)
        state.update(10000, hit=True)
        state.update(10001, hit=True)
        self.assertEqual(state.score, 1)
        self.assertFalse(state.playing)

    def test_coin_during_round_is_saved(self):
        state = game.Game()
        state.update(0, pulses=1, start=True)
        state.update(100, pulses=1)
        self.assertEqual(state.credits, 1)

    def test_round_timer_wrap(self):
        state = game.Game()
        state.update(PERIOD - 5000, pulses=1, start=True)
        state.update(5000, hit=True)
        self.assertFalse(state.playing)
        self.assertEqual(state.score, 0)


if __name__ == "__main__":
    unittest.main()
