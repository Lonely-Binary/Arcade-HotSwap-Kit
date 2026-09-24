"""Watch COIN (BCM26) and COUNTER (BCM24) and print each pulse group.

See which line your acceptor pulses. Never add the two counts together.
"""
from collections import deque
from threading import Lock
from time import monotonic, sleep
from gpiozero import DigitalInputDevice


class CoinProbe:
    def __init__(self, bcm):
        self.bcm = bcm
        self.lock = Lock()
        self.last = None
        self.count = 0
        self.ready = deque()
        self.device = DigitalInputDevice(bcm, pull_up=True, bounce_time=None)
        self.device.when_activated = self.edge

    def edge(self):
        with self.lock:
            now = monotonic()
            if self.last is not None and now - self.last < 0.060:
                return
            if self.count and now - self.last >= 0.200:
                self.ready.append(self.count)
                self.count = 0
            self.last = now
            self.count += 1

    def poll(self):
        with self.lock:
            if self.ready:
                return self.ready.popleft()
            if self.count and monotonic() - self.last >= 0.200:
                count, self.count = self.count, 0
                return count
            return 0

    def close(self):
        self.device.when_activated = None
        self.device.close()


def main():
    probes = []
    try:
        for bcm in (26, 24):
            probes.append(CoinProbe(bcm))
        print("Coin probe ready. Insert one learned coin, then wait.")
        while True:
            for probe in probes:
                count = probe.poll()
                if count:
                    print("%s BCM%d: %d pulse(s)" % ("COIN" if probe.bcm == 26 else "COUNTER", probe.bcm, count))
            sleep(0.005)
    except KeyboardInterrupt:
        pass
    finally:
        for probe in probes:
            probe.close()


if __name__ == "__main__":
    main()
