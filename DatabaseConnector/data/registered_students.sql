CREATE TABLE IF NOT EXISTS registered_students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  roll_number TEXT NOT NULL,
  qrcode TEXT NOT NULL
);
