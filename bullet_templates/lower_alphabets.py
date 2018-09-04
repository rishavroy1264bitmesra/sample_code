from bullet_templates.abstract_template import AbstractBulletIdentifier


class LowerAlphaBulletsIdentifier(AbstractBulletIdentifier):
    def _get_bullet_identifier_regex(self):
        return '^\([a-h j-s]{1}\)'

    def get_bullet_regex(self):
        return '\([a-h j-s]{1}\)'


if __name__ == '__main__':
    text = '''(j) This section says about all Articles in 3(B) sections'''
    bullet_finder = LowerAlphaBulletsIdentifier()
    print(bullet_finder.getName())
    print(bullet_finder.find_bullets(text))
    print(bullet_finder.is_bullet_present(text))
