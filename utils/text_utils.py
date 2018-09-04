import re

def remove_space(text):
    return re.sub('\s+|\n+|\r+','',text)
