import os
import sys
import subprocess


def parser_proc(command, file, proc_id=None):
    proc = subprocess.Popen(
        [command], stdout=subprocess.PIPE, shell=True, encoding='utf-8')
    while True:
        line = proc.stdout.readline()
        if line:
            sys.stdout.write(line)
            sys.stdout.flush()
            with open(file, 'a') as out:
                out.write('{}'.format(line))
        if line.__len__() == 0 and proc.poll() is not None:
            break


def get_process_id():
    return None


def main():
    file = 'output.log'
    command = '. {}/generator.sh'.format(os.getcwd())
    proc_id = get_process_id()
    parser_proc(command, file)


if __name__ == '__main__':
    main()
