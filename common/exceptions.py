"""
See (this guide)[https://github.com/HackSoftware/Django-Styleguide#approach-2---hacksofts-proposed-way]
for more details.
"""


class TokenError(Exception):
    pass


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}
