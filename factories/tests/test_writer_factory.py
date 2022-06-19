import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from factories.writer_factory import WriterFactory
from modules.writer import Writer


class TestWriterFactory(unittest.TestCase):
    def test_MakeWriter(self):
        self.assertEqual(WriterFactory.MakeWriter(1, [1, 2, 3], {"Writer 1": Writer(id=1), "Writer 2": Writer(id=1)}),
                         None,
                         msg="Return value should be None!")
        self.assertEqual(WriterFactory.MakeWriter(1, [], {}), None, msg="Return value should be None!")


if __name__ == '__main__':
    unittest.main()
