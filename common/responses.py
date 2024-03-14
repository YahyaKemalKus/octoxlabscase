from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, data, status=200, template_name=None, headers=None, exception=False, content_type=None):
        data = {
            'success': True,
            'data': data
        }
        super().__init__(data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        data = {
            'success': False,
            'error': data,
            'data': None
        }
        super().__init__(data, status, template_name, headers, exception, content_type)

    def __call__(self, data):
        self.data["error"] = data
        return self