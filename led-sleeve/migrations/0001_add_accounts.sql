PRAGMA user_version=1;

CREATE TABLE accounts (
  provider TEXT,
  id TEXT,
  credentials TEXT,
  sort_order INT UNIQUE,
  UNIQUE(provider, id)
);
