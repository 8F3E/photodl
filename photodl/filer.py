from pathlib import Path
from shutil import copyfile


class Sync():
    def __init__(self, files, dest):
        self.filestosort = files
        self.dest = dest
        self.sorted = {}

    def sort(self):
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

    # def dedupe(self):
    #     for year in self.sorted:
    #         for dirprefix in self.sorted[year]:
    #             p = Path(self.dest) / Path(year) / Path(dirprefix)
    #             if p.exists() and p.isdir():
    #                 self.sorted[year].pop(dirprefix, None)

    def go(self):
        self.sort()
        # self.dedupe()

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
