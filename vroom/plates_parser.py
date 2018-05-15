"""License plate parser for cars registered in Poland."""

import json
import re


def load_area_codes():
    """
    Loads and returns area codes dictionary.
    """
    with open("area_codes.json", "r") as file:
        area_dict = json.load(file)
    return area_dict

def load_regex_patterns():
    """
    Loads and returns regex patterns dictionary.
    """
    with open("regex_patterns.json", "r") as file:
        regex_patterns = json.load(file)
    return regex_patterns


class RegexPattern(object):
    """
    Class representing regex pattern. It contains compiled regex
    and information about matching administrative unit.
    """

    def __init__(self, area_code, pattern, unit_dict, ignore_case):
        self.pattern = pattern
        self.regexp = self.compile(ignore_case)
        self.area_code = area_code
        self.unit = unit_dict['unit']
        self.voivodeship = unit_dict['voivodeship']

    def compile(self, ignore_case):
        """
        Compiles regex pattern with flags.
        """
        if ignore_case:
            return re.compile(self.pattern, flags=re.IGNORECASE)
        else:
            return re.compile(self.pattern)


class Parser(object):
    """
    Main parser class.
    """

    AREA_CODES = load_area_codes()
    REGEX_PATTERNS = load_regex_patterns()


    def __init__(self, force_space=False, ignore_case=False):
        self.force_space = force_space
        self.ignore_case = ignore_case
        self.regexes = self.construct_regexes(self.force_space, self.ignore_case)


    def construct_regexes(self, force_space=False, ignore_case=False):
        """
        Constructs a list of regex patterns.
        """
        regexes = []

        for area_code, unit_dict in self.AREA_CODES.items():
            #load all possible patterns for signature length
            patterns = self.REGEX_PATTERNS[str(len(area_code))]

            #Construct base regex string
            if force_space:
                regex_base = r"\b{} {}\b"
            else:
                regex_base = r"\b{} ?{}\b"

            regexes.extend([RegexPattern(area_code,
                                         regex_base.format(area_code, pattern),
                                         unit_dict,
                                         ignore_case
                                        ) for pattern in patterns])
        return regexes

    def search_plates(self, text):
        """
        Searches text for license plates, returns True if any matches found.
        """
        found = False
        for regex in self.regexes:
            if re.search(regex.regexp, text):
                found = True
                break
        return found

    def findall_plates(self, text, return_units=False):
        """
        Searches text for license plates, returns all matches.
        """

        found_plates = []
        for regex in self.regexes:
            result = re.findall(regex.regexp, text)
            if result:
                if return_units:
                    result_units = [self.build_plate_dict(res,
                                                          regex.unit,
                                                          regex.voivodeship
                                                         ) for res in result]
                    found_plates.extend(result_units)
                else:
                    found_plates.extend(result)
        if found_plates:
            return found_plates

    def match_plate(self, text):
        """
        Checks if text matches license plate pattern and returns dictionary
        with administrative unit information.
        """

        for regex in self.regexes:
            if re.match(regex.regexp, text):
                return self.build_plate_dict(text, regex.unit, regex.voivodeship)

    @staticmethod
    def build_plate_dict(plate, unit, voivodeship):
        """
        Helper function for returning plate administrative info dictionary.
        """
        plate_dict = {
            'plate': plate,
            'unit': unit,
            'voivodeship': voivodeship
        }
        return plate_dict

