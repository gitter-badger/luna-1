# coding=utf8

"""
Configure the exceptions at here.
"""


class ErrorCode(object):
    " 0 ~ 1000 System Error "
    UNAUTH = 401
    PAGE_NOT_FOUND = 404

    ARGS_PARSED_ERROR = 800


class TranslateCode(object):
    translate = {
        ErrorCode.UNAUTH: 'Unauthorization Request.',
        ErrorCode.PAGE_NOT_FOUND: 'Page Not Found',

        ErrorCode.ARGS_PARSED_ERROR: 'Arguments Parse Error',
    }

    def __init__(self, code):
        pass

    def __new__(self, code):
        return self.translate.get(code, None)
