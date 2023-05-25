def write_text_file(file, text, mode = 'a'):
    with open(file, mode) as file_stream:
        file_stream.write(text)
        file_stream.close()

def append_text_file(file, text):
    write_text_file(file, text, 'a')

def rewrite_text_file(file, text, mode = 'a'):
    write_text_file(file, text, 'w')

def read_text_file(file, mode = 'r'):
    with open(file, mode) as file_stream:
        text = file_stream.read()
        file_stream.close()
        return text