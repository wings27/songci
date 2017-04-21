ping_ze_def = {
    'PING': 'A',
    'ZE': 'B',
    'PING_YUN': 'C',
    'ZE_YUN': 'D',
    'ANY': 'X',
}


def is_yun(chars: str is not None) -> bool:
    return chars.endswith('C') or chars.endswith('D')


def to_tones_regex(chars: str is not None) -> str:
    to_tones_regex_mapping = {
        'A': '(1|2)',
        'C': '(1|2)',
        'B': '(3|4)',
        'D': '(3|4)',
        'X': '.',
    }
    return chars.translate(str.maketrans(to_tones_regex_mapping))
