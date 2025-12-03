import unittest


def reg(input, input2):
    raise Exception("asd")


class raiseTest(unittest.TestCase):
    def testraiseRegex(self):
        self.assertRaisesRegex(Exception, "a", reg, "Point", "TutorialsPoint")


if __name__ == "__main__":
    unittest.main()
