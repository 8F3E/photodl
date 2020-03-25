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
            datetimestr = self.img.datetime
        except AttributeError:
            print("{0} does not contain EXIF datetime data.".format(self.url))
            return []

        try:
            datetimeobj = datetime.strptime(datetimestr, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            print("Could not parse datetime from {0}.".format(self.url))
            return []

        return {"url": self.url,
                "year": datetimeobj.year,
                "month": datetimeobj.month,
                "day": datetimeobj.day}


class Dater:
    def __init__(self, urls):
        self.urls = urls
        self.db = []

    def date(self):
        for url in self.urls:
            carbondater = CarbonDating(url)
            dated = carbondater.date()

            if len(dated) > 0:
                self.db.append(dated)
