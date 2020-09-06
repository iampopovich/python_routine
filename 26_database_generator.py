import sys
import os
import string
import random
from datetime import datetime


def genName(size=30, chars=string.ascii_letters + string.digits + " "):
    return "".join(random.choice(chars) for i in range(random.randint(5, size)))


def genPhoneNumber(size=15, chars=string.digits):
    return "".join(random.choice(chars) for i in range(random.randint(9, size)))


def genEmail(size=10, chars=string.ascii_letters + string.digits):
    name = "".join(random.choice(chars)
                   for i in range(random.randint(5, size)))
    domain = "".join(random.choice(chars)
                     for i in range(random.randint(5, size)))
    region = "".join(random.choice(string.ascii_letters)
                     for i in range(random.randint(2, 3)))
    return "{0}@{1}.{2}".format(name, domain, region)


def genCardNum(size=16, chars=string.digits):
    return "".join(random.choice(chars) for i in range(size))


def genPoints():
    return(random.randint(0, 1000000))


def genBirthDate():
    currentTimestamp = int(datetime.now().timestamp())
    timestamp = random.randint(0, currentTimestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")


def main(args):
    delim = args[2]
    if os.path.isfile("deg.csv"):
        os.unlink("deg.csv")
    with open("deg.csv", "a") as out:
        for i in range(int(args[1])):
            name = genName()
            number = genPhoneNumber()
            email = genEmail()
            card = genCardNum()
            points = genPoints()
            bday = genBirthDate()
            out.write(delim.join(
                map(str, [name, number, email, card, points, bday]))+"\n")


if __name__ == "__main__":
    main(sys.argv)
