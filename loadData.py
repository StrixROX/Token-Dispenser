from DatabaseConnector import DatabaseConnector
import os

db = DatabaseConnector('engineering_practicum.db')
db.loadDataFolder()