CREATE TABLE mess_scans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  scan_datetime DATETIME NOT NULL,
  mess_number TEXT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES registered_students(id)
);