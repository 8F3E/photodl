import crayons

SUCCESS = crayons.green("✔  Success :)")
FATAL = crayons.red("✖  Oh no   :(")
ERROR = crayons.yellow("✜  Oops    :)")
INFO = crayons.blue("❖  FYI       ")


def title():
    print(crayons.white("photodl v1.0.0", bold=True))
    print()


def printout(text, status):
    print("{0}\t{1}".format(status, text))


def tellme(text):
    return input(crayons.white("➤  Your turn!\t{0}  ".format(text), bold=True))
