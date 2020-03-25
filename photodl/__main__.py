import sys


def main():
    import argparse
    from pathlib import Path
    from photodl import filer

    parser = argparse.ArgumentParser(prog="photodl",
                                     description="A simple python package to d"
                                                 "ownload, sort and backup pho"
                                                 "tos from an SD card.")

    parser.add_argument("paths", metavar="path", type=str, nargs="+",
                        help="Path(s) to download, sort and backup from.")

    parser.add_argument("dest", type=str, nargs=1,
                        help="Path to copy sorted files to.")

    parser.add_argument("--backup", type=str, help="Path to backup files to. "
                                                   "(You really should...)")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    files = []

    for path in args.paths:
        p = Path(path).glob("**/*")
        files += [str(x.resolve()) for x in p if x.is_file()]

    f = filer.Filer(files, args.dest[0], args.backup)
    f.go()
    sys.exit(0)


if __name__ == "__main__":
    main()
