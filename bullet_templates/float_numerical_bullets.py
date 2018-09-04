from bullet_templates.abstract_template import AbstractBulletIdentifier


class FloatNumericalBulletsIdentifier(AbstractBulletIdentifier):
    def _get_bullet_identifier_regex(self):
        return '^\d{1,2}\s?\.\s?\d{1,2}'

    def get_bullet_regex(self):
        return '\d{1,2}\.\d{1,2}'


if __name__ == '__main__':
    text = '''2.11 This section says about all Articles in 31.1 sections'''
    bullet_finder = FloatNumericalBulletsIdentifier()
    print(bullet_finder.getName())
    print(bullet_finder.find_bullets(text))
    print(bullet_finder.is_bullet_present(text))
