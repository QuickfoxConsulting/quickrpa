from YourBot import YourBot
from libraries.Bot import Bot
from robot.libraries.BuiltIn import BuiltIn


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    browser = BuiltIn().get_library_instance("RPA.Browser.Selenium.Browser")
    app = YourBot(browser)
    browser.close_all_browsers()
