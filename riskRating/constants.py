import os
import dotenv

envPath = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(envPath):
    print("loading dot env...")
    dotenv.load_dotenv()

ORACLE_USERNAME = os.environ['ORACLE_USERNAME']
ORACLE_PASSWORD = os.environ['ORACLE_PASSWORD']
ORACLE_TNS_NAME = os.environ['ORACLE_TNS_NAME']
ORACLE_DRIVER_NAME = os.environ['ORACLE_DRIVER_NAME']
DATA_PATH = os.environ['DATA_PATH']