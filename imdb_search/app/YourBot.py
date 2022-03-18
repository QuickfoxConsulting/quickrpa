from libraries.SetupError import setup_error
from robot.libraries.BuiltIn import BuiltIn
# from libraries.Communicate import RunItem
from libraries.Utils import log_to_console
from libraries.Bot import Bot

logger = BuiltIn().get_library_instance("BotLogger")
browser = BuiltIn().get_library_instance("RPA.Browser.Selenium")


class YourBot(Bot):
    def __init__(self, browser):
        self.browser = browser

    def run(self):
        try:
            log_to_console("Running robot")

        except Exception as e:
            setup_error(e, "main entry point error")
