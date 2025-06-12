from dotenv import load_dotenv
import os

load_dotenv()

# SuiteCRM configuration
SUITECRM_URL = os.getenv('SUITECRM_URL', 'http://localhost/SuiteCRM-7.14.6/service/v4_1/rest.php')
USERNAME = os.getenv('SUITECRM_USERNAME', 'admin')
PASSWORD = os.getenv('SUITECRM_PASSWORD', 'Admin@123')