from configparser import ConfigParser
from keyboards import ListOfButtons


config = ConfigParser()
config.read("config.ini")

TOKEN = config['tokens']['TOKEN']