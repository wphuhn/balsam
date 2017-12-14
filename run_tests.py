import sys
import os
import django
import tempfile
import unittest


def set_permissions(top):
    os.chmod(top, 0o755)
    for root,subdirs,files in os.walk(top):
        for dir in (os.path.join(root, s) for s in subdirs):
            os.chmod(dir, 0o755)
        for file in (os.path.join(root, f) for f in files):
            os.chmod(file, 0o644)

if __name__ == "__main__":
    tempdir = tempfile.TemporaryDirectory(dir=os.getcwd(), prefix="testdata_")
    
    os.environ['BALSAM_TEST_DIRECTORY'] = tempdir.name
    os.environ['BALSAM_TEST']='1'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'argobalsam.settings'
    django.setup()

    set_permissions(tempdir.name)

    loader = unittest.defaultTestLoader
    if len(sys.argv) > 1:
        names = sys.argv[1:]
        suite = loader.loadTestsFromNames(names)
    else:
        suite = loader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(suite)
