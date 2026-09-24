"""Observe GP28 after configuring the acceptor. No currency assumptions."""
from time import sleep_ms
from arcade import CoinInput

coin = CoinInput(28)
print("Coin probe ready. Insert one learned coin, then wait.")
try:
    while True:
        pulses = coin.poll()
        if pulses == -1:
            print("Input queue overflow; group discarded. Repeat the test.")
        elif pulses:
            print("GP28:", pulses if pulses <= 10 else ">10", "pulse(s)")
        sleep_ms(1)
finally:
    coin.close()
