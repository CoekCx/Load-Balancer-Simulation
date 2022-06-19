import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from utils.object_parser import ObjectParser
from modules.writer import Writer
from modules.worker import Worker


class TestObjectParser(unittest.TestCase):
    def test_GetObjectNames(self):
        self.assertEqual(ObjectParser.GetObjectNames([Writer(id=1), Writer(id=2)]), ['Writer 1', 'Writer 2'],
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetObjectNames([Worker(id=1), Worker(id=2)]), ['Worker 1', 'Worker 2'],
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetObjectNames([]), [],
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetObjectNames({}), [],
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetObjectNames([1, 2, 3]), ['1', '2', '3'],
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetObjectNames([Writer(id=1), Writer(id=2)], True),
                         [{'name': 'Writer 1'}, {'name': 'Writer 2'}],
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetObjectNames([Worker(id=1), Worker(id=2)], True),
                         [{'name': 'Worker 1'}, {'name': 'Worker 2'}],
                         msg="Return value should be None!")

    def test_GetClassObjectByName(self):
        self.assertEqual(ObjectParser.GetClassObjectByName([], None), None, msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetClassObjectByName([Writer(id=1), Writer(id=2)], "wrong name"), None,
                         msg="Return value should be None!")
        self.assertEqual(ObjectParser.GetClassObjectByName([Worker(id=1), Worker(id=2)], "wrong name"), None,
                         msg="Return value should be None!")
        writer = Writer(id=2)
        self.assertEqual(ObjectParser.GetClassObjectByName([Writer(id=1), writer], "Writer 2"), writer,
                         msg="Return value should be None!")
        worker = Worker(id=1)
        self.assertEqual(ObjectParser.GetClassObjectByName([worker, Worker(id=2)], "Worker 1"), worker,
                         msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
