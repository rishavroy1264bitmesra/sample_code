from bullet_templates.abstract_template import AbstractBulletIdentifier


class UpperRomanBulletsIdentifier(AbstractBulletIdentifier):
    def _get_bullet_identifier_regex(self):
        return '^\(?(II?I?|I?I?VI?I?I?|I?I?XI?I?I?)\)?\.?'

    def get_bullet_regex(self):
        return '^\(?(II?I?|I?I?VI?I?I?|I?I?XI?I?I?)\)?\.?'


if __name__ == '__main__':
    text = '''(X) This section says about all Articles in 3(B) sections'''
    bullet_finder = UpperRomanBulletsIdentifier()
    print(bullet_finder.getName())
    print(bullet_finder.find_bullets(text))
    print(bullet_finder.is_bullet_present(text))
