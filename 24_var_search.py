import sys
import re


def parse_variable(file, variable):
    variable_val = []
    print(variable)
    with open(file, 'r') as f:
        for line in f:
            if not variable_val:
                if re.search('char %s\[\] =' %variable, line):
                    variable_val.append(re.search(".*", line).group(0)[1:-1])
                continue
            if re.search(r'".*"', line):
                variable_val.append(re.search(r'".*"', line).group(0)[1:-1])
                continue
            if variable_val and not re.search(r'".*"', line):
                break
    print ''.join(variable_val[1:])


def main(args):
    parse_variable(args[1], args[2])

if __name__ == '__main__':
    main(sys.argv)
