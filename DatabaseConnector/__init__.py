from .connector import DatabaseConnector

if __name__ == "__main__":
  db = DatabaseConnector()
  db.loadDataFolder()
  quit()
