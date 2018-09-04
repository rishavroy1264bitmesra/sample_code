from bullet_templates.alpha_numeric_bullets import AlphaNumericBulletsIdentifier
from bullet_templates.float_numerical_bullets import FloatNumericalBulletsIdentifier
from bullet_templates.lower_alphabets import LowerAlphaBulletsIdentifier
from bullet_templates.numerical_bullets import NumericBulletsIdentifier
from bullet_templates.roman_bullets import RomanBulletsIdentifier
from bullet_templates.upper_alphabets import UpperAlphaBulletsIdentifier


class TestExecutor(object):
    def test_alpha_numeric_bullets(self):
        text = '''2(A) This section says about all Articles in 3(B) sections'''
        identifier = AlphaNumericBulletsIdentifier()
        bullets_found = identifier.find_bullets(text)
        assert len(bullets_found) > 0

    def test_float_numeric_bullets(self):
        text = '''2.11 This section says about all Articles in 3(B) sections'''
        identifier = FloatNumericalBulletsIdentifier()
        bullets_found = identifier.find_bullets(text)
        assert len(bullets_found) > 0

    def test_lower_alpha_bullets(self):
        text = '''(a) This section says about all Articles in 3(B) sections'''
        identifier = LowerAlphaBulletsIdentifier()
        bullets_found = identifier.find_bullets(text)
        assert len(bullets_found) > 0

    def test_numeric_bullets(self):
        text = '''2. This section says about all Articles in 3(B) sections'''
        identifier = NumericBulletsIdentifier()
        bullets_found = identifier.find_bullets(text)
        assert len(bullets_found) > 0

    def test_roman_bullets(self):
        text = '''(vi) This section says about all Articles in 3(B) sections'''
        identifier = RomanBulletsIdentifier()
        bullets_found = identifier.find_bullets(text)
        assert len(bullets_found) > 0

    def test_upper_alpha_bullets(self):
        text = '''(A) This section says about all Articles in 3(B) sections'''
        identifier = UpperAlphaBulletsIdentifier()
        bullets_found = identifier.find_bullets(text)
        assert len(bullets_found) > 0
