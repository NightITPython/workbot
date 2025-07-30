from dotenv import load_dotenv
from os import getenv
import logging


data = {}
status_link = {}
logger = logging.getLogger(__name__)
ADMIN_ID = [7471183111]
bot_id = 8070109537
bots = {}
domain = "https://ds7zck-8000.cs-ide.io"
logging.basicConfig(
    level=logging.DEBUG,
    format="🌐 [%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)


load_dotenv()


TOKEN = getenv("TOKEN")
DB = "/home/user/night/database.db"


