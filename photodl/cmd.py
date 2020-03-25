import crayons

SUCCESS = crayons.green("✔  Success :)")
FATAL = crayons.red("✖  Oh no   :(")
ERROR = crayons.yellow("✜  Oops    :)")
INFO = crayons.blue("❖  FYI       ")


def printout(text, status):
    print("{0}\t{1}".format(status, text))


def tellme(text):
    return input(crayons.white("➤  Your turn!\t{0} ".format(text), bold=True))
