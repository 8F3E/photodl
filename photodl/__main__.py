import argparse
from pathlib import Path
from photodl import metadata


parser = argparse.ArgumentParser(prog="photodl",
                                 description="A simple python package to d"
                                             "ownload, sort and backup pho"
                                             "tos from an SD card.")

parser.add_argument("paths", metavar="path", type=str, nargs="+",
                    help="A path to download, sort and backup.")

args = parser.parse_args()
files = []

for path in args.paths:
    p = Path(path).glob("**/*")
    files += [str(x.resolve()) for x in p if x.is_file()]

d = metadata.Dater(files)
d.date()
print(str(d.db))
