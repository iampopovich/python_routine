# from pyzbar.pyzbar import decode
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import os
import sys
import csv


def recognize_and_rock(args):
    for root, dirs, files in os.walk(args[1]):
        for file in files:
            decoded_code = None
            try:
                # print (decode(Image.open(os.path.join(args[1], file))))
                code = decode(Image.open(os.path.join(args[1], file)))[0].data.decode('utf8')
            except:
                code = 'an error accured , try to scan manually'
            with open('result.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                    quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([file,code])


if __name__ == '__main__':
    recognize_and_rock(sys.argv)