from typing import Union
import sqlite3
import os
import datetime

import helpers
from ..Scanner.definitions import StudentQR

class DatabaseConnector:
  def __init__(self, dbName:str) -> None:
    self.is_connected = False
    self.__db = None
    self.__cur = None

    if os.path.exists(helpers.getAbsolutePath(dbName)):
      try:
        self.__db = sqlite3.connect(os.path.join(os.getcwd(), dbName))
        self.__cur = self.__db.cursor()
      except sqlite3.Error as err:
        Exception(f"Error while connecting to database: {dbName}.")
    else:
      raise Exception(f"Database does not exist: {dbName}.")

  def loadDataFolder(self) -> None:
    print('Loading data from data folder...')

    if not os.path.exists(helpers.getAbsolutePath('data')):
      os.mkdir(helpers.getAbsolutePath('data'))

    dataFiles = os.listdir(helpers.getAbsolutePath('data'))
    
    if len(dataFiles) == 0:
      print("No files to load.")
      quit()

    for file in dataFiles:
      print(f"Loading {file}...")
      with open(helpers.getAbsolutePath(f"data/{file}"), 'r') as f:
        sqlScript = f.read()
        try:
          self.__cur.executescript(sqlScript)
        except sqlite3.Error as err:
          print(f"Error while loading {file}.")

    self.__db.commit()

  def getTable(self, tableName:str) -> Union[list, None]:
    # returns list of table rows
    # or None if table doesn't exist

    # Check if the table exists
    self.__cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'")
    if not self.__cur.fetchone():
        print(f"Table does not exist in the database: '{tableName}'.")
        return None

    # Retrieve all rows from the table
    self.__cur.execute(f"SELECT * FROM {tableName}")
    rows = self.__cur.fetchall()

    # Get the column names from the table's PRAGMA statement
    self.__cur.execute(f"PRAGMA table_info({tableName})")
    tableInfo = self.__cur.fetchall()
    colNames = [x[1] for x in tableInfo]

    # Combine the column names with the rows to create a list of dictionaries
    tableData = [dict(zip(colNames, row)) for row in rows]

    return tableData

  # def createTable(self, query:str) -> None:
  #     #Creates a new table in the database
  #     self.__cur.execute(query)
  #     self.__db.commit()

  # def executeSelectQuery(self, query:str) -> list:
  #     #retrieves all necessary data if it exists
  #     #returns empty list otherwise
  #     self.__cur.execute(query)
  #     rows = self.__cur.fetchall()
  #     result = [list(row) for row in rows]
  #     self.__db.commit()
  #     return result

  # def executeQuery(self, query:str) -> None:
  #     # Inserts/Updates/Deletes from a table
  #     self.__cur.execute(query)
  #     self.__db.commit()
  
  def scanIsLogged(self, qr:StudentQR) -> bool:
    # check if QR code exists in the table
    self.__cur.execute(f"SELECT * FROM meal_attendance WHERE qrcode='{qr.hash}'")
    res = self.__cur.fetchone()
    if len(res) != 0:
        print("QR code already scanned.")
        return True
    
    return False
  
  def logScan(self, qr:StudentQR, scanTime:datetime.time) -> bool:
    # insert scan data into the meal_attendance table
    try:
      self.__cur.execute(f"INSERT INTO meal_attendance (roll_no, qrcode, timestamp) VALUES ({qr.roll_no}, '{qr.hash}', '{scanTime}')")
      self.__db.commit()
      
      return True
    except sqlite3.Error:
      return False