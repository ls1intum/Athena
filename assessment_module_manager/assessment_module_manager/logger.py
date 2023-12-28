from logging import getLogger, DEBUG, Formatter, StreamHandler
import sys

logger = getLogger(__name__)
# debug to stdout
logger.setLevel(DEBUG)
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - [assessment_module_manager] - %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
