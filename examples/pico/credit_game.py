"""Insert a coin, press KEY1, then score with KEY2 for ten seconds."""
from time import ticks_ms, ticks_diff, sleep_ms
from arcade import Button, CoinInput

# #region config
CREDITS_BY_PULSES = {1: 1}  # pulse group -> credits. {3: 1}: three pulses buy one credit.
ROUND_MS = 10_000
USE_DISPLAY = False
# #endregion


class Game:
    def __init__(self):
        self.credits = 0
        self.score = 0
        self.playing = False
        self.started = 0

    def update(self, now, pulses=0, start=False, hit=False):
        messages = []
        if pulses:
            credit = CREDITS_BY_PULSES.get(pulses, 0)
            if credit:
                self.credits += credit
                messages.append("Credits: %d" % self.credits)
            else:
                messages.append("Unknown pulse group ignored: %d" % pulses)
        # Expiry comes before scoring: a press at the deadline is too late.
        if self.playing and ticks_diff(now, self.started) >= ROUND_MS:
            self.playing = False
            messages.append("Time up! Score: %d" % self.score)
            return messages
        if start and not self.playing:
            if not self.credits:
                messages.append("Insert a coin")
            else:
                self.credits -= 1
                self.score = 0
                self.started = now
                self.playing = True
                messages.append("GO! Press KEY2 for %d seconds" % (ROUND_MS // 1000))
                return messages
        if hit and self.playing:
            self.score += 1
            messages.append("Score: %d" % self.score)
        return messages


def main():
    display = None
    if USE_DISPLAY:
        from arcade import make_display
        display = make_display()
        display.draw_text8("HotSwap Arcade", 8, 8, 0x07E0)
    start, hit = Button(16), Button(17)
    coin = CoinInput(28)
    game = Game()
    previous_rows = (None, None, None)
    status = "Insert a coin. KEY1 starts; KEY2 scores."
    print(status)
    try:
        while True:
            pulses = coin.poll()
            messages = game.update(ticks_ms(), pulses,
                                   start.poll() == 1, hit.poll() == 1)
            for message in messages:
                print(message)
                status = message
            if display:
                rows = ("Credits: %d" % game.credits,
                        "Score: %d" % game.score, status)
                for row, text in enumerate(rows):
                    if text != previous_rows[row]:
                        # Fixed-width padding clears the previous row in one draw.
                        display.draw_text8(text[:56].ljust(56), 8, 32 + row * 20)
                previous_rows = rows
            sleep_ms(1)
    finally:
        coin.close()


if __name__ == "__main__":
    main()
