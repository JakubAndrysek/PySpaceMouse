import unittest
import re

def reg(input, input2):
    raise Exception("asd")

class raiseTest(unittest.TestCase):
    def testraiseRegex(self):
        self.assertRaisesRegexp(Exception, "a", reg, "Point", "TutorialsPoint")


if __name__ == '__main__':
    unittest.main()