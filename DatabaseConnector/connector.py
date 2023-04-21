from typing import Union

# TODO: implement the functions
class DatabaseConnector:
  def __init__(self) -> None:
    pass

  def loadDataFolder(self) -> None:
    print('Loading data...')
    pass

  def getTable(self, tableName:str) -> Union[list, None]:
    # returns disctionaty of table rows
    # or None if table doesn't exist
    return None
  
  def query(self, query:str) -> Union[list, None]:
    pass