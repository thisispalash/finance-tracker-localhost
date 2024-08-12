-- `receipts` table
CREATE TABLE IF NOT EXISTS receipts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  img_hash TEXT NOT NULL UNIQUE,
  store TEXT NOT NULL,
  date TEXT NOT NULL,
  time TEXT,
  count INTEGER NOT NULL,
  total REAL NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- `items` table
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  receipt_id INTEGER NOT NULL,
  item TEXT NOT NULL,
  price REAL NOT NULL,
  FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
);