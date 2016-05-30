import logging


class ArubaLog(object):
    def __init__(self, level=logging.DEBUG, dst_file='debug.log', name=__name__, log_to_file=False,
                 log_to_stdout=True):
        """
        Initialize Logging System

        :param level: Debugging level.
        :param dst_file: Log destination file.
        :param name: the name of the debugger.
        :param log_to_file: boolean, True in case logs must be placed on file too.
        """
        self.level = level
        self.dst_file = dst_file
        self.log = logging.getLogger(name)
        self.log.setLevel(level)
        self.name = name

        formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

        if log_to_file is True:
            file_handler = logging.FileHandler(dst_file, "a")
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.log.addHandler(file_handler)

        elif log_to_stdout is True:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)
            self.log.addHandler(stream_handler)
        else:
            raise ValueError("No Stream Handler Specified.")

    def debug(self, msg):
        self.log.debug(msg)

    def critical(self, msg):
        self.log.critical(msg)

    def warning(self, msg):
        self.log.warning(msg)

    def info(self, msg):
        self.log.info(msg)

    def error(self, error):
        self.log.error(error)
