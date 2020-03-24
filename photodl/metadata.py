from datetime import datetime
from exif import Image


class CarbonDating:
    def __init__(self, url):
        self.url = url
        with open(self.url, "rb") as imgfile:
            self.img = Image(imgfile)

    def date(self):
        if not self.img.has_exif:
            print("{0} does not contain EXIF data.".format(self.url))
            return False

        try:
            self.datetimestr = self.img.datetime
        except AttributeError:
            print("{0} does not contain EXIF datetime data.".format(self.url))

        try:
            self.datetimeobj = datetime.strptime(self.datetimestr,
                                                 "%Y:%m:%d %H:%M:%S")
        except ValueError:
            print("Could not parse datetime from {0}.".format(self.url))

        self.year = self.datetimeobj.year
        self.month = self.datetimeobj.month
        self.day = self.datetimeobj.day

        return [self.url, self.year, self.month, self.day]
