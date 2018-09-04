from src.html_line_parser import HTMLReader
import unittest

class TestExecutor(unittest.TestCase):
    def test_get_top_left(self):
        html_line_parser = HTMLReader()
        style_list = [
            'top:1141.0159pt;left:1107.771pt;line-height:21.542969pt;font-family:GlyphLessFont;font-size:43.0pt;width:92.57153pt;',
            'top:733.7009pt;left:1560.343pt;line-height:21.54303pt;font-family:GlyphLessFont;font-size:43.0pt;width:133.71521pt;',
            'top:1141.0159pt;left:1493.4849pt;line-height:21.542969pt;font-family:GlyphLessFont;font-size:43.0pt;width:22.628784pt;']
        result = html_line_parser.get_top_left(style_list)
        self.assertEqual(result,'top:1141.0159pt;left:1107.771pt')

    def test_get_bottom_right(self):
        html_line_parser = HTMLReader()
        style_list = [
            'top:1141.0159pt;left:1107.771pt;line-height:21.542969pt;font-family:GlyphLessFont;font-size:43.0pt;width:92.57153pt;',
            'top:733.7009pt;left:1560.343pt;line-height:21.54303pt;font-family:GlyphLessFont;font-size:43.0pt;width:133.71521pt;',
            'top:1141.0159pt;left:1493.4849pt;line-height:21.542969pt;font-family:GlyphLessFont;font-size:43.0pt;width:22.628784pt;']
        result = html_line_parser.get_bottom_right(style_list)
        self.assertEqual(result, 'top:1141.0159pt;left:1493.4849pt')

if __name__ == '__main__':
    unittest.main()