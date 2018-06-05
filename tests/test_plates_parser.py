"""License plate parser for cars registered in Poland."""

import unittest
from vroom import plates_parser

class ParserTest(unittest.TestCase):
    """Test Case for Parser"""

    def test_search_plates(self):
        """
        Test for search_plates method.
        Method should return True if plate is found in string.
        """

        parser = plates_parser.Parser()
        self.assertTrue(parser.search_plates("Plate number SY 12345"))
        self.assertFalse(parser.search_plates("This string contains no plates."))

    def test_findall_plates(self):
        """
        Test for findall_plates method.
        Method should return a set of found plates.
        """

        parser = plates_parser.Parser()
        plates_string = "List of plates: SY 12345, WR0NG12, STY1A234, SZ 1AA23"
        plates_list = {"SY 12345", "SZ 1AA23", "STY1A234"}
        self.assertEqual(parser.findall_plates(plates_string), plates_list)

    def test_match_plate(self):
        """
        Test for match_plate method.
        Method should return a PlateDetails namedtuple if plate is found.
        """

        parser = plates_parser.Parser()
        plates_details = plates_parser.PlateDetails('SY 12345', 'Bytom', 'śląskie')
        self.assertEqual(parser.match_plate("SY 12345"), plates_details)
        self.assertIsNone(parser.match_plate("HEJ 12345"))

if __name__ == '__main__':
    unittest.main()
