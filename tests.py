import unittest
import text_functions

class TestTT(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_line_date(self):
        self.assertEqual(text_functions.is_line_date('2014/11/03(junk)').group(1),
                '2014/11/03')

    def test_is_line_chat_get_user(self):
        line = '21:11	Casey	And now I prepare work it seems'
        self.assertEqual(text_functions.is_line_chat(line).group(2), 'Casey')

    def test_is_line_chat_get_text(self):
        line = '21:11	Casey	And now I prepare work it seems'
        self.assertEqual(text_functions.is_line_chat(line).group(3),
                'And now I prepare work it seems')

    def test_parse_link_check_against_dateline(self):
        line = '2014/11/03(junk)'
        parsed_line = text_functions.parse_line(line)
        self.assertEqual(parsed_line.date, '2014/11/03')

    def test_parse_link_check_against_chatline_user(self):
        line = '21:11	Casey	And now I prepare work it seems'
        parsed_line = text_functions.parse_line(line)
        self.assertEqual(parsed_line.user, 'Casey')

    def test_parse_link_check_against_chatline_text(self):
        line = '21:11	Casey	And now I prepare work it seems'
        parsed_line = text_functions.parse_line(line)
        self.assertEqual(parsed_line.text, 'And now I prepare work it seems')

if __name__ == '__main__':
    unittest.main()
