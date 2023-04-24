from typing import Union
import sqlite3
import os

# TODO: implement the functions
class DatabaseConnector:
  def __init__(self) -> None:
    pass

  def loadDataFolder(self) -> None:
    print('Loading data...')

    db_path = os.path.join(os.getcwd(), "engineering_practicum.db")
    self.conn = sqlite3.connect(db_path)
    self.cursor = self.conn.cursor()

    if not os.path.exists('data'):
      os.mkdir('data')

    for filename in os.listdir('data'):
      with open(f'data/{filename}', 'r') as f:
        sql = f.read()
        self.cursor.execute(sql)
        print(f"Executed SQL command from the file {filename}")

    self.conn.commit()

  def getTable(self, tableName:str) -> Union[list, None]:
    # returns list of table rows
    # or None if table doesn't exist
    return None
  
  def query(self, query:str) -> Union[list, None]:
    pass

db = DatabaseConnector()
db.loadDataFolder()
