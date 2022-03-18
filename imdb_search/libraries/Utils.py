import os
# from time import time

from robot.libraries.BuiltIn import BuiltIn

# browser_lib = BuiltIn().get_library_instance("RPA.Browser.Selenium.Selenium")


def log_to_console(message: str) -> None:

    BuiltIn().log_to_console(f"\n{message}")


def is_local():
    try:
        return os.environ["ENVIRONMENT"] == "LOCAL"
    except:
        return False


def is_dev():
    try:
        return os.environ["ENVIRONMENT"] == "DEV"
    except:
        return False


def is_our_uat():
    try:
        return os.environ["ENVIRONMENT"] == "OUR_UAT"
    except:
        return False


def is_client_uat():
    try:
        return os.environ["ENVIRONMENT"] == "CLIENT_UAT"
    except:
        return False


def is_production():
    try:
        return os.environ["ENVIRONMENT"] == "PRODUCTION"
    except:
        return False


def get_identifier():

    try:
        if os.environ["LOCAL_TO_DEV_SERVER"] == "True":
            return "d847ffb1-a803-4ede-ab57-f44776257b69"
    except:
        pass

    identifier = BuiltIn().get_variable_value("${identifier}")
    return identifier


def get_base_url():
    try:
        if os.environ["LOCAL_TO_DEV_SERVER"] == "True":
            return "http://13.58.117.7:8000/api/v1"
    except:
        pass

    if is_local():
        return "http://localhost:8000/api/v1"

    elif is_dev():
        return "http://13.58.117.7:8000/api/v1"

    elif is_our_uat():
        return "http://18.224.145.213:8000/api/v1"

    elif is_client_uat():
        return "<client_uat_url>:8000/api/v1"

    elif is_production():
        return "<production_url>:8000/api/v1"

    else:
        return "http://localhost:8000/api/v1"


def get_runitem(
    started_at, status, report_data, is_ticket=True, screenshot=False, **kwargs
):

    logger = BuiltIn().get_library_instance("BotLogger")
    completed_at = BuiltIn().get_time()
    log_text = logger.get_log_contents()

    def get_attachment():
        data = open("output/error.png", "rb").read()
        encoded_image = base64.b64encode(data)
        decoded_image = "data:image/png;base64," + \
            encoded_image.decode("UTF-8")
        return [decoded_image]

    notification = {
        "data": {"Reason": kwargs.get("error_reason")},
        "subject": "Warning! DRC bot has closed during execution",
        "subject": kwargs.get("subject"),
        "attachments": get_attachment() if screenshot else None,
    }

    run_item = {
        "started_at": started_at,
        "completed_at": completed_at,
        "status": status,
        "report_data": report_data if report_data else {},
        "log_text": log_text,
        "is_ticket": is_ticket,
        "notification": notification,
    }

    return run_item


# def wait_and_click(xpath, timeout):
#    browser_lib.wait_until_element_is_visible(locator=xpath, timeout=timeout)
#    browser_lib.click_element(locator=xpath)
