import sys

sys.path.append("C:/Users/Milos/Documents/FAKULTET/3 godina/6_semestar/RES/Python/"
                "python-project-main-final/python-project-main")

import unittest
from utils.validation import Validate


class TestValidate(unittest.TestCase):
    def test_ValidateIntValue(self):
        self.assertEqual(Validate.ValidateIntValue("non int"), False, msg="Should make an exception and return False!")
        self.assertEqual(Validate.ValidateIntValue("1"), True, msg="Should cast to int and return True!")
        self.assertEqual(Validate.ValidateIntValue("1", less_than=True, limit=5), True,
                         msg="Should check if value is less than limit and return True!")
        self.assertEqual(Validate.ValidateIntValue("1", less_than=True, limit=0), False,
                         msg="Should check if value is less than limit and return False!")
        self.assertEqual(Validate.ValidateIntValue("1", more_than=True, limit=5), False,
                         msg="Should check if value is higher than limit and return False!")
        self.assertEqual(Validate.ValidateIntValue("1", more_than=True, limit=0), True,
                         msg="Should check if value is higher than limit and return True!")

    def test_ValidateExistenceOfIntValue(self):
        self.assertEqual(Validate.ValidateExistenceOfIntValue("non int", [1, 2, 3]), False,
                         msg="Should check if value exists and return False!")
        self.assertEqual(Validate.ValidateExistenceOfIntValue(1, [1, 2, 3]), False,
                         msg="Should check if value exists, determine that it does exist and return False!")
        self.assertEqual(Validate.ValidateExistenceOfIntValue(0, [1, 2, 3]), True,
                         msg="Should check if value exists, determine that it doesn't exist and return True!")


if __name__ == '__main__':
    unittest.main()
