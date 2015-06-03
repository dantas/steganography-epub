import os
import shutil
import zipfile


class Epub(object):
    def __init__(self):
        self.work_dir = 'tmp'

    def expand(self, path):
        self.cleanup()
        zfile = zipfile.ZipFile(path)
        zfile.extractall(self.work_dir)
        zfile.close()

    def contract(self, path):
        zipobj = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)

        fn_files = []
        for base, dirs, files in os.walk(self.work_dir):
            for name in files:
                fn = os.path.join(base, name)
                if name == 'mimetype':
                    fn_files.insert(0, fn)
                else:
                    fn_files.append(fn)

        rootlen = len(self.work_dir) + 1

        zipobj.write(fn_files[0], fn_files[0][rootlen:], zipfile.ZIP_STORED)

        for i in range(1, len(fn_files)):
            zipobj.write(fn_files[i], fn_files[i][rootlen:])

        self.cleanup()

    def cleanup(self):
        try:
            shutil.rmtree(self.work_dir)
        except:
            pass
