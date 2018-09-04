from bullet_templates.abstract_template import AbstractBulletIdentifier


class LowerRomanBulletsIdentifier(AbstractBulletIdentifier):
    def _get_bullet_identifier_regex(self):
        return '^\((ii?i?|i?i?vi?i?i?|i?i?xi?i?i?)\)'

    def get_bullet_regex(self):
        return '^\((ii?i?|i?i?vi?i?i?|i?i?xi?i?i?)\)'


if __name__ == '__main__':
    text = '''(x) This section says about all Articles in 3(B) sections'''
    bullet_finder = LowerRomanBulletsIdentifier()
    print(bullet_finder.getName())
    print(bullet_finder.find_bullets(text))
    print(bullet_finder.is_bullet_present(text))
