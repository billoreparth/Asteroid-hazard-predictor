import sys

class custom_exception(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.line_no=exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"the error has occured in file :{self.file_name} in line number : {self.line_no} and error message is {self.error_message}"
        

