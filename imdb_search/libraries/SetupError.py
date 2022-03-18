from robot.libraries.BuiltIn import BuiltIn
import traceback


def setup_error(exception=None, error_reason="Unknown Error"):
    logger = BuiltIn().get_library_instance("BotLogger")
    logger.logger.error(error_reason)

    if exception:
        trace = traceback.format_exc()
        logger.logger.error(trace)
        BuiltIn().log_to_console(logger.get_log_contents())
        logger.close_logger()
        raise exception
    else:
        BuiltIn().log_to_console(logger.get_log_contents())
        logger.close_logger()
        raise Exception(error_reason)


def setup_success():
    logger = BuiltIn().get_library_instance("BotLogger")
    logger.logger.info("Setup Successful")
    BuiltIn().log_to_console(logger.get_log_contents())
    logger.clear_logs()
