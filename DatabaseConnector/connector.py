from typing import Union, List
import sqlite3
import os

# TODO: implement the functions
class DatabaseConnector:
  def __init__(self) -> None:
    db_path = os.path.join(os.getcwd(), "engineering_practicum.db")
    self.conn = sqlite3.connect(db_path)
    self.cursor = self.conn.cursor()

  def loadDataFolder(self) -> None:
    print('Loading data...')

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

    # Check if the table exists
    self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'")
    if not self.cursor.fetchone():
        print(f"The table '{tableName}' does not exist in the database.")
        return None

    # Retrieve all rows from the table
    self.cursor.execute(f"SELECT * FROM {tableName}")
    rows = self.cursor.fetchall()

    # Get the column names from the table's PRAGMA statement
    self.cursor.execute(f"PRAGMA table_info({tableName})")
    column_names = [column[1] for column in self.cursor.fetchall()]

    # Combine the column names with the rows to create a list of dictionaries
    table_data = [dict(zip(column_names, row)) for row in rows]

    return table_data
