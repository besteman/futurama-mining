DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS miner;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE miner (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name INTEGER NOT NULL,
  enabled BOOLEAN NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user (username, password)
VALUES( 'besteman' , 123);

INSERT INTO miner (name, enabled) 
VALUES ( 'this', 1 );

INSERT INTO miner (name, enabled) 
VALUES ( 'that', 0 );