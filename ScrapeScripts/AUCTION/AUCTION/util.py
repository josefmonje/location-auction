"""Module that contains helper class(es)"""
import re
import unicodedata

class Formatter(object):
    """class contains some utility functions"""
    @staticmethod
    def format_data(data):
        """Unicode character handling"""
        return data.replace(u"\u2028", "").replace(u"\u201c", "\"").replace(u"\u201d", "\"").replace(u"\xa0'", " ").replace(u"\u2018", "'").replace(u"\u2019", "'")
    @staticmethod
    def get_array_value(arr):
        """Get the first index value of array if it is not an empty array"""
        if len(arr) > 0:
            return arr[0].replace(u'\u2019', '').replace(u'\u201c', '').replace(u'\u201d', '').replace(u'\u2013', '-').replace(u"\xa0'", " ").replace(u'\u2022', '-')
        else:
            return ''
    @staticmethod
    def replace_unicodes(string):
        "remove unicode characters"
        return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
    @staticmethod
    def remove_tags(text):
        """removes html tags"""
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub('', text)
    @staticmethod
    def find_digits(string):
        """returns the array of digits found in the given string"""
        return re.findall(r'\d+', string)
    @staticmethod
    def remove_spaces(string):
        """remove extra space from string"""
        return string.replace('\n', '').replace('\r', '').replace('\t', '').replace('\f', '').replace('&amp;', '&').strip(' ')
    