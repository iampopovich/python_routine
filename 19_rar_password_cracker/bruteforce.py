import rarfile
import zipfile
import datetime
from threading import Thread
import optparse
import itertools

rarfile.UNRAR_TOOL = "unrar"


def bruteforce(charset, minlength, maxlength):
    return (''.join(candidate)
            for candidate in itertools.chain.from_iterable(
                itertools.product(charset, repeat=i)
                for i in range(minlength, maxlength + 1)))


def extractFile(arFile, attempt):
    try:
        arFile.extractall(pwd=attempt)
        print "Password found! password is %s" % attempt
        exit(0)
    except Exception, e:
        pass
    if datetime.datetime.now().second % 20 == 0:
        print 'At %s' % attempt


def main():
    parser = optparse.OptionParser(
        "usage%prog --fr <rarfile> -c <charset> -n <size> -n_min <min_size>")
    parser.add_option('--fr', dest='rname', type='string',
                      help='specify rar file')
    parser.add_option('--fz', dest='zname', type='string',
                      help='specify zip file')
    parser.add_option('-c', dest='charset', type='string',
                      help='specify charset')
    parser.add_option('-n', dest='size', type='string',
                      help='size of password')
    parser.add_option('--nmin', dest='minSize', type='int',
                      help='min size of password')
    (options, args) = parser.parse_args()
    cond_1 = options.rname == None and options.zname == None
    cond_2 = options.charset == None
    cond_3 = options.size == None
    cond_4 = options.minSize == None or int(options.minSize) < 0
    if cond_1 or cond_2 or cond_3:
        print parser.usage
        exit(0)
    else:
        if options.rname:
            arname = options.rname
            arFile = rarfile.RarFile(arname)
        else:
            arname = options.zname
            arFile = zipfile.ZipFile(arname)
        charset = options.charset
        size = options.size
        minSize = options.minSize

    size = int(size)
    for attempt in bruteforce(charset, minSize, size):
        # match it against your password, or whatever
        extractFile(arFile, attempt)

        # uncomment below lines if you want to use multiple threads
        #t = Thread(target=extractFile, args=(arFile,attempt))
        # t.start()


if __name__ == '__main__':
    main()
