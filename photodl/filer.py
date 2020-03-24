from hashlib import blake2b
from pathlib import Path
from shutil import copyfile


class Sync():
    bufsize = 262144

    def __init__(self, files, dest):
        self.filestosort = files
        self.dest = dest

    def sort(self):
        self.sorted = {}

        for file in self.filestosort:
            y = str(file["year"])
            u = "{0}-{1:02d}-{2:02d}".format(file["year"],
                                             file["month"],
                                             file["day"])

            if y in self.sorted and u in self.sorted[y]:
                self.sorted[y][u] += [file]
            elif y in self.sorted and u not in self.sorted[y]:
                self.sorted[y][u] = [file]
            else:
                self.sorted[y] = {u: [file]}

    def hashfile(self, file):
        hasher = blake2b()

        with open(file, "rb") as f:
            while True:
                data = f.read(self.bufsize)
                if not data:
                    break
                hasher.update(data)

        return hasher.hexdigest()

    def dedupe(self):
        realfilestosort = []

        for file in self.filestosort:
            file["blake2b"] = self.hashfile(file["url"])

        self.destdbdumppath = Path(self.dest) / Path(".hash.db")

        if self.destdbdumppath.exists():
            with open(self.destdbdumppath.resolve(), "r") as destdbdump:
                self.destdb = destdbdump.read().splitlines()

            for file in self.filestosort:
                if file["blake2b"] not in self.destdb:
                    realfilestosort.append(file)

            self.filestosort = realfilestosort

    def copy(self):
        for year in self.sorted:
            for dirprefix in self.sorted[year]:
                eventtitle = input("Event name for {0}: ".format(dirprefix))
                for file in self.sorted[year][dirprefix]:
                    oldp = Path(file["url"])
                    if eventtitle != "":
                        prefix = dirprefix + "_" + eventtitle
                    else:
                        prefix = dirprefix
                    name = prefix + "_" + oldp.name
                    newdir = Path(self.dest)\
                        / Path(year)\
                        / Path(prefix)\
                        / Path("RAW")
                    newdir.mkdir(parents=True, exist_ok=True)
                    newp = newdir / Path(name)
                    copyfile(file["url"], str(newp.resolve()))

    def dumpdb(self):
        with open(self.destdbdumppath.resolve(), "a") as destdbdump:
            for file in self.filestosort:
                destdbdump.write("{0}\n".format(str(file["blake2b"])))

    def go(self):
        self.dedupe()
        self.sort()
        self.copy()
        self.dumpdb()
