import sys
import os
import io


class LoggerOut:
    def __init__(self, filename, hidden=False):
        self.terminal = sys.stdout
        self.filename = filename
        self.hidden = hidden

    def write(self, message):
        self.terminal.write(message)  # standard output to console
        if my_log == log_methods[0]:  # logging to StringIO object
            self.filename.write(message)
        else:  # logging straight to default file
            with open(self.filename, "a") as file:
                print(message, file=file, flush=True, end='')
            if not self.hidden:
                self.hide_default()  # hide default log file

    def hide_default(self):
        os.system(f'attrib +h {log_methods[1]}')
        self.hidden = True

    def flush(self):
        pass


class LoggerIn:
    def __init__(self, filename):
        self.terminal = sys.stdin
        self.filename = filename

    def readline(self):
        entry = self.terminal.readline()
        if my_log == log_methods[0]:
            self.filename.write(entry)
        else:
            with open(self.filename, "a") as file:
                print(entry.rstrip(), file=file, flush=True)
        return entry


# logging method via memory (StringIO) or
# directly to file (file creation upon start up)
log_methods = [io.StringIO(), 'default.txt']
my_log = log_methods[0]
