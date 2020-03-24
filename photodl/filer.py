class Sync():
    def __init__(self, files):
        self.filestosort = files
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

        return self.sorted
