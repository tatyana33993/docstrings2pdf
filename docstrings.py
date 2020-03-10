#!/usr/bin/env python3
import re


def get_docstrings(filename):
    f = open(filename, 'r', encoding='utf-8')
    d = {}
    current_class = ''
    current_def = ''
    current_comm = ''
    comm = False
    for line in f:
        current_class, current_def = get_current_class(line, current_class,
                                                       current_def)
        current_def = get_current_def(line, current_def)
        comm, current_comm, d = get_current_comm(line, current_class,
                                                 current_def, comm,
                                                 current_comm, d)
    f.close()
    return d


def get_current_class(line, current_class, current_def):
    if re.match(r'class', line.lstrip()):
        current_class = line[line.find('class') + 6:line.find(':')]
        current_def = ''
    return (current_class, current_def)


def get_current_def(line, current_def):
    if re.match(r'def', line.lstrip()):
        current_def = line[line.find('def') + 4:line.find('(')]
    return current_def


def get_current_comm(line, current_class, current_def, comm, current_comm, d):
    if re.match(r'"""|\'\'\'', line.lstrip()) and not comm:
        comm = True
    elif re.match(r'"""|\'\'\'', line.lstrip()) and comm:
        comm = False
        d["{0}.{1}".format(current_class, current_def)] = current_comm
        current_comm = ''
    elif comm:
        current_comm += line
    else:
        pass
    return (comm, current_comm, d)


if __name__ == '__main__':
    get_docstrings('example.txt')
