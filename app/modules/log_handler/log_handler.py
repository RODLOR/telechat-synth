import os

class log_handler():
    def __init__(self, log_path: str): # Iniciarlizar el log
        self.log_path = log_path
        log_directory = os.path.dirname(self.log_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                f.write('~* Log Init *~\n')

    def log_write(self, texto : str):
        with open(self.log_path, 'a') as f:
            f.write(f'\n{texto}')
    
    def fn_block(self):
        with open(self.log_path, 'a') as f:
            f.write(f'\n~* Exit *~\n')
    def fn_by_err(self, err_info : str):
        write = f'Date: err~ User: err~ Bot: err~ Bot error: {err_info}. '
        self.log_write(write)
        self.fn_block()