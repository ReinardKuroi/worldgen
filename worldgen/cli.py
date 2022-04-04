import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dimensions', action='store',
                    help='Space or comma-separated XYZ dimensions of the generated object.')
parser.add_argument('-s', '--scale', action='store',
                    help='Generated object scale (like zooming in on a map)')


def parse_args() -> argparse.Namespace:
    return parser.parse_args()
