import logging
import io


class BotLogger(object):
    def __init__(self, logger_name="IMDB_logger") -> None:
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.log_capture_string = io.StringIO()
        ch = logging.StreamHandler(self.log_capture_string)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def get_log_contents(self):
        return self.log_capture_string.getvalue()

    def clear_logs(self):
        self.log_capture_string.truncate(0)
        self.log_capture_string.seek(0)

    def close_logger(self):
        self.log_capture_string.close()
