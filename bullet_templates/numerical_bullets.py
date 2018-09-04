from bullet_templates.abstract_template import AbstractBulletIdentifier


class NumericBulletsIdentifier(AbstractBulletIdentifier):
    def _get_bullet_identifier_regex(self):
        return '^[0-9]{1,3}\s?(?!\.[0-9])'

    def get_bullet_regex(self):
        return '[0-9]{1,3}\s?(?!\.[0-9])'


if __name__ == '__main__':
    text = '''3678. EFFECTIVENESS, TERMINATION AND SUSPENSION'''
    bullet_finder = NumericBulletsIdentifier()
    print(bullet_finder.getName())
    print(bullet_finder.find_bullets(text))
    print(bullet_finder.is_bullet_present(text))
