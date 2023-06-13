READ_FILE_OPEN_MODE = 'r'
APPEND_FILE_OPEN_MODE = 'a'
REWRITE_FILE_OPEN_MODE = 'w'

def write_text_file(file, text, mode = APPEND_FILE_OPEN_MODE):
    with open(file, mode) as file_stream:
        try:
            file_stream.write(text)
        except:
            print(write_text_file.__name__ + '() Error: occures when write text in file')
            print(file)
            print(text)
        file_stream.close()

def append_text_file(file, text):
    write_text_file(file, text, APPEND_FILE_OPEN_MODE)

def rewrite_text_file(file, text):
    write_text_file(file, text, REWRITE_FILE_OPEN_MODE)

def read_text_file(file, mode = READ_FILE_OPEN_MODE):
    with open(file, mode) as file_stream:
        text = file_stream.read()
        file_stream.close()
        return text