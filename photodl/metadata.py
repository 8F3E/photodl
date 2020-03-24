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
            return []

        try:
            self.datetimestr = self.img.datetime
        except AttributeError:
            print("{0} does not contain EXIF datetime data.".format(self.url))
            return []

        try:
            self.datetimeobj = datetime.strptime(self.datetimestr,
                                                 "%Y:%m:%d %H:%M:%S")
        except ValueError:
            print("Could not parse datetime from {0}.".format(self.url))
            return []

        return {"url": self.url,
                "year": self.datetimeobj.year,
                "month": self.datetimeobj.month,
                "day": self.datetimeobj.day}


class Dater:
    def __init__(self, urls):
        self.urls = urls
        self.db = []
        self.carbondater = None

    def date(self):
        for url in self.urls:
            self.carbondater = CarbonDating(url)
            dated = self.carbondater.date()

            if len(dated) > 0:
                self.db.append(dated)
