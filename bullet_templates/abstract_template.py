import abc
import re


class AbstractBulletIdentifier(metaclass=abc.ABCMeta):
    def find_bullets(self, text):
        matches = list()
        regex = self._get_bullet_identifier_regex()
        pattern = re.compile(regex)
        for match in pattern.findall(text):
            matches.append(match)
        return matches

    def is_bullet_present(self, text):
        regex = self._get_bullet_identifier_regex()
        pattern = re.compile(regex)
        if pattern.search(text) is not None:
            return True
        else:
            return False

    def getName(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def _get_bullet_identifier_regex(self):
        pass

    @abc.abstractmethod
    def get_bullet_regex(self):
        pass


