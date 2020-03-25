def main():
    import argparse
    from pathlib import Path
    from photodl import metadata
    from photodl import filer

    parser = argparse.ArgumentParser(prog="photodl",
                                     description="A simple python package to d"
                                                 "ownload, sort and backup pho"
                                                 "tos from an SD card.")

    parser.add_argument("paths", metavar="path", type=str, nargs="+",
                        help="Path(s) to download, sort and backup.")

    parser.add_argument("dest", type=str, nargs=1,
                        help="Path to copy sorted files to.")

    parser.add_argument("--backup", type=str, help="Path to backup files to.")

    args = parser.parse_args()
    files = []

    for path in args.paths:
        p = Path(path).glob("**/*")
        files += [str(x.resolve()) for x in p if x.is_file()]

    d = metadata.Dater(files)
    d.date()

    s = filer.Sync(d.db, args.dest[0])
    s.go()

    print(args)

    if args.backup is not None:
        b = filer.Backup(d.db, args.backup)
        b.zip()


if __name__ == "__main__":
    main()
