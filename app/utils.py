import re
import os
import sys
import datetime
import yaml
import logging
from logging.handlers import RotatingFileHandler


CONFIGFILE = os.environ['CONFIGPATH']
# CONFIGPATH = CONFIGFILE.replace('config.yml', '')


def remove_bracketed_text(text, brackets="()[]{}"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars).strip()


def upperescape(string):
    """Uppercase and Escape string. Used to help with YT-DL regex match.
    - ``string``: string to manipulate

    returns:
        ``string``: str new string
    """
    # UPPERCASE as YTDL is case insensitive for ease.
    string = string.upper()
    # Remove quote characters as YTDL converts these.
    string = string.replace('’',"'")
    string = string.replace('“','"')
    string = string.replace('”','"')
    # Remove anything between braces, making it optional
    string = remove_bracketed_text(string)
    # Treat any non-letter character as an optional non-letter wildcard
    string = re.sub(r'[^A-Z]','[^A-Z]*', string)
    # Make it look for and as whole or ampersands
    string = string.replace('\\ AND\\ ','\\ (AND|&)\\ ')
    return string


def checkconfig():
    """Checks if config files exist in config path
    If no config available, will copy template to config folder and exit script

    returns:

        `cfg`: dict containing configuration values
    """
    logger = logging.getLogger('sonarr-ytdl')
    config_template = os.path.abspath(CONFIGFILE + '.template')
    config_template_exists = os.path.exists(os.path.abspath(config_template))
    config_file = os.path.abspath(CONFIGFILE)
    config_file_exists = os.path.exists(os.path.abspath(config_file))
    if not config_file_exists:
        logger.critical('Configuration file not found.')  # print('Configuration file not found.')
        if not config_template_exists:
            os.system('cp /app/config.yml.template ' + config_template)
        logger.critical("Create a config.yml using config.yml.template as an example.")  # sys.exit("Create a config.yml using config.yml.template as an example.")
        sys.exit()
    else:
        logger.info('Configuration Found. Loading file.')  # print('Configuration Found. Loading file.')
        with open(
            config_file,
            "r"
        ) as ymlfile:
            cfg = yaml.load(
                ymlfile,
                Loader=yaml.BaseLoader
            )
        return cfg


def offsethandler(airdate, offset):
    """Adjusts an episodes airdate
    - ``airdate``: Airdate from sonarr # (datetime)
    - ``offset``: Offset from series config.yml # (dict)

    returns:
        ``airdate``: datetime updated original airdate
    """
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    if 'weeks' in offset:
        weeks = int(offset['weeks'])
    if 'days' in offset:
        days = int(offset['days'])
    if 'hours' in offset:
        hours = int(offset['hours'])
    if 'minutes' in offset:
        minutes = int(offset['minutes'])
    airdate = airdate + datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
    return airdate


class YoutubeDLLogger(object):

    def __init__(self):
        self.logger = logging.getLogger('sonarr-ytdl')

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)


def ytdl_hooks_debug(d):
    logger = logging.getLogger('sonarr-ytdl')
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        logger.info("      Done downloading {}".format(file_tuple[1]))  # print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        progress = "      {} - {} - {}".format(d['filename'], d['_percent_str'], d['_eta_str'])
        logger.debug(progress)


def ytdl_hooks(d):
    logger = logging.getLogger('sonarr-ytdl')
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        logger.info("      Downloaded - {}".format(file_tuple[1]))

def setup_logging(lf_enabled=True, lc_enabled=True, debugging=False):
    log_level = logging.INFO
    log_level = logging.DEBUG if debugging == True else log_level
    logger = logging.getLogger('sonarr-ytdl')
    logger.setLevel(log_level)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if lf_enabled:
        # setup logfile
        log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
        log_file = os.path.abspath(log_file + '/sonarr-ytdl.log')
        loggerfile = RotatingFileHandler(
            log_file,
            maxBytes=5000000,
            backupCount=5
        )
        loggerfile.setLevel(log_level)
        loggerfile.set_name('FileHandler')
        loggerfile.setFormatter(log_format)
        logger.addHandler(loggerfile)

    if lc_enabled:
        # setup console log
        loggerconsole = logging.StreamHandler()
        loggerconsole.setLevel(log_level)
        loggerconsole.set_name('StreamHandler')
        loggerconsole.setFormatter(log_format)
        logger.addHandler(loggerconsole)

    return logger
