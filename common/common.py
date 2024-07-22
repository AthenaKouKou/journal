import os

JOURNAL_CODE = 'JOURNAL_CODE'

journal_code = None


def get_journal():
    global journal_code
    journal_code = os.getenv(JOURNAL_CODE)
    return journal_code


def get_collect_name(base_name):
    global journal_code
    if not journal_code:
        get_journal()
    return f'{journal_code}_{base_name}'
