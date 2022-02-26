import os

LOGFILE_PATH='logs/scraper.log'

BASE_DIR = os.path.join(os.path.dirname(__file__), '../')
OUTPUT_DIRNAME='outputs'
OUTPUT_DIR = os.path.join(BASE_DIR, OUTPUT_DIRNAME)

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
