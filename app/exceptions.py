class CustomExceptionA(Exception):
    def __init__(self, message: str = "Incorrect request condition"):
        self.message = message
        self.status_code = 400
        self.error_code = "CUSTOM_A"


class CustomExceptionB(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        self.status_code = 404
        self.error_code = "CUSTOM_B"
