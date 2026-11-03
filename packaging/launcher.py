"""Punto d'ingresso dell'app macOS: avvia il pannello (e il browser, salvo --no-browser)."""
import sys

from mix3d.server import serve

if __name__ == "__main__":
    serve(open_browser="--no-browser" not in sys.argv)
