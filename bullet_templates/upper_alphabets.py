from bullet_templates.abstract_template import AbstractBulletIdentifier


class UpperAlphaBulletsIdentifier(AbstractBulletIdentifier):
    def _get_bullet_identifier_regex(self):
        return '^\([A-Z]{1}\)'

    def get_bullet_regex(self):
        return '\([A-Z]{1}\)'


if __name__ == '__main__':
    text = '''(A) This section says about all Articles in 3(B) sections'''
    bullet_finder = UpperAlphaBulletsIdentifier()
    print(bullet_finder.getName())
    print(bullet_finder.find_bullets(text))
    print(bullet_finder.is_bullet_present(text))
