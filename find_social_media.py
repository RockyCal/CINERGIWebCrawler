__author__ = 'Anoushka'
from build_title import build_title
from socialMediaKnown import socialMediaKnown

def find_social_media(url):
    title = build_title(url)
    ret_statement = ""
    if title is not None:
        for soc in socialMediaKnown:
            if soc in title:
                return soc
    else:
        return ret_statement