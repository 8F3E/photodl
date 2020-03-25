from hashlib import blake2b
from pathlib import Path
from shutil import copyfile
from datetime import datetime
import os
import zipfile
from photodl import metadata


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
                destdb = destdbdump.read().splitlines()

            for file in self.filestosort:
                if file["blake2b"] not in destdb:
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


class Backup():
    def __init__(self, filelist, dest):
        self.files = filelist
        self.dest = dest

    def namer(self):
        date = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")
        name = input("Name this backup: ")

        if name != "":
            filename = "{0}_{1}.zip".format(date, name)
        else:
            filename = "{0}.zip".format(date)

        return Path(self.dest) / Path(filename)

    def zip(self):
        file = self.namer()
        file.parent.mkdir(parents=True, exist_ok=True)
        urls = [x["url"] for x in self.files]
        common = os.path.commonpath(urls)
        with zipfile.ZipFile(file.resolve(),
                             "a",
                             compression=zipfile.ZIP_STORED,
                             compresslevel=9) as zf:
            for f in self.files:
                zf.write(f["url"], arcname=f["url"][len(common):])


class Filer():
    def __init__(self, files, dest, backup):
        self.files = files
        self.dest = dest
        self.backup = backup

    def go(self):
        d = metadata.Dater(self.files)
        d.date()

        s = Sync(d.db, self.dest)
        s.go()

        if self.backup is not None:
            b = Backup(d.db, self.backup)
            b.zip()
