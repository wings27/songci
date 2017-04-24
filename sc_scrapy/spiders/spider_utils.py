import re


def ignore_case_re(pattern_format):
    return re.compile(pattern_format, flags=re.UNICODE + re.IGNORECASE)
