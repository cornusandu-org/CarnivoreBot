from .dependencies import logging, colorama
from datetime import datetime

logging.getLogger("werkzeug").setLevel(logging.ERROR);

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS");

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: f"{colorama.Style.DIM}{colorama.Fore.RESET}",
        logging.INFO: f"{colorama.Style.RESET_ALL}",
        SUCCESS: f"{colorama.Fore.GREEN}",
        logging.WARNING: f"{colorama.Fore.YELLOW}",
        logging.ERROR: f"{colorama.Fore.RED}",
        logging.CRITICAL: f"{colorama.Style.BRIGHT}{colorama.Fore.RED}",
    }

    RESET = colorama.Style.RESET_ALL

    def format(self, record):
        timestamp = datetime.fromtimestamp(
            record.created
        ).astimezone().isoformat(timespec="milliseconds")

        color = self.COLORS.get(record.levelno, "")

        output = (
            f"{color}"
            f"{timestamp}\t"
            f"[{record.levelname.center(8)}]\t"
            f"{record.threadName}: "
            f"{record.name}: "
            f"{record.getMessage()}"
            f"{self.RESET}"
        )

        if record.exc_info:
            output += f"\n {colorama.Style.RESET_ALL}{colorama.Style.DIM}#{color}{colorama.Style.NORMAL} " + self.formatException(record.exc_info).replace('\n', f"\n {colorama.Style.RESET_ALL}{colorama.Style.DIM}#{color}{colorama.Style.NORMAL} ")

        if record.stack_info:
            output += f"\n {colorama.Style.RESET_ALL}{colorama.Style.DIM}#{colorama.Style.RESET_ALL} " + self.formatStack(record.stack_info).replace('\n', f"\n {colorama.Style.DIM}#{colorama.Style.RESET_ALL} ")

        return output
    
def getLogger(name: str):
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(ColorFormatter())

    logger = logging.getLogger(name)
    logger.addHandler(handler)

    def success(message, *args, **kwargs):
        if logger.isEnabledFor(SUCCESS):
            logger._log(SUCCESS, message, args, **kwargs)

    logger.success = success
    logger.setLevel(logging.DEBUG)

    return logger
