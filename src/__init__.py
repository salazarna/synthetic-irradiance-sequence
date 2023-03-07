# Warnings
import warnings
warnings.filterwarnings(action='ignore')

# Logging
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('numexpr').setLevel(logging.WARNING)

# Scripts
from src import methods
from src import metrics
from src import utils
from src import version

if __name__ == '__main__':
    print(f'Successfully executed {__name__}.')