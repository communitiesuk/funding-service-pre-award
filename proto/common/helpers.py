import re


def make_url_slug(sentence):
    no_apostrophes = re.sub(r"""['"]""", "", sentence)
    normalised_sentence = re.sub(r"[^A-Za-z0-9]+", "-", no_apostrophes)
    slug = re.sub(r"-+", "-", normalised_sentence)
    return slug
