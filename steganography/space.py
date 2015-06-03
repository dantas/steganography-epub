import fileinput
import os
import sys


class Space(object):
    SELECT_FILES = ('.html', '.css')
    ZERO = '\n'
    ONE = '\r\n'

    def __init__(self, epub):
        self._files = []
        self._lines = []

        for dirpath, dirnames, filenames in os.walk(epub.work_dir):
            for name in filenames:
                if name.endswith(self.SELECT_FILES):
                    self._files.append(os.path.join(dirpath, name))

        self._files = sorted(self._files)

        for line_in_file in fileinput.input(self._files):
            if line_in_file[-2:] == self.ONE:
                self._lines.append(1)
            else:
                self._lines.append(0)

    def __setitem__(self, pos, value):
        self._lines[pos] = 1 if value else 0

    def __getitem__(self, pos):
        return self._lines[pos]

    def __len__(self):
        return len(self._lines)

    def commit(self):
        pos = 0
        for line_in_file in fileinput.input(self._files, inplace=True):
            sys.stdout.write(self._strip(line_in_file))
            if self._lines[pos] == 1:
                sys.stdout.write(self.ONE)
            else:
                sys.stdout.write(self.ZERO)

            pos += 1

    @classmethod
    def _strip(cls, line):
        if line[-2:] == cls.ONE:
            return line[:-2]
        elif line[-1:] == cls.ZERO:
            return line[:-1]
        else:
            return line
