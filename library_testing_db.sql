-- Bos Library database schema and seed data
-- Run after pulling DB changes: mysql -u root -p < library_testing_db.sql
CREATE DATABASE IF NOT EXISTS `bos_library`;
USE `bos_library`;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS borrows;
DROP TABLE IF EXISTS book_copies;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS users;
-- genres
CREATE TABLE genres (
  idGenre int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (idGenre)
);
INSERT INTO genres
VALUES (1, 'Non-fiction'),
  (2, 'Fiction'),
  (3, 'Romance'),
  (4, 'Thriller'),
  (5, 'Self-Help');
-- books
CREATE TABLE books (
  ISBN varchar(14) NOT NULL,
  Title varchar(200) DEFAULT NULL,
  Author varchar(100) DEFAULT NULL,
  Age_Restricted int DEFAULT NULL,
  idGenre int DEFAULT NULL,
  PRIMARY KEY (ISBN),
  KEY idGenre (idGenre),
  CONSTRAINT books_ibfk_1 FOREIGN KEY (idGenre) REFERENCES genres (idGenre) ON DELETE
  SET NULL
);
INSERT INTO books
VALUES (
    '9780008533571',
    'Watching You',
    'Helen Fields',
    18,
    4
  ),
  (
    '9780435232818',
    'The Crucible',
    'Arthur Miller',
    18,
    1
  ),
  (
    '9781398519732',
    'All Your Perfects',
    'Colleen Hoover',
    18,
    3
  ),
  (
    '9781405807050',
    'Carol Ann Duffy Selected Poems',
    'Michael.J.Woods',
    16,
    2
  ),
  (
    '9781847941831',
    'Atomic Habits',
    'James Clear',
    18,
    5
  );
-- book_copies
CREATE TABLE book_copies (
  copy_id int NOT NULL,
  copy_status varchar(45) DEFAULT NULL,
  copy_ISBN varchar(14) NOT NULL,
  PRIMARY KEY (copy_id, copy_ISBN),
  KEY copy_ISBN (copy_ISBN),
  CONSTRAINT book_copies_ibfk_1 FOREIGN KEY (copy_ISBN) REFERENCES books (ISBN) ON DELETE CASCADE
);
INSERT INTO book_copies
VALUES (1, 'Available', '9780008533571'),
  (1, 'Available', '9781398519732'),
  (1, 'Available', '9781405807050'),
  (1, 'Available', '9781847941831'),
  (2, 'Borrowed', '9780008533571'),
  (2, 'Borrowed', '9781398519732'),
  (2, 'Borrowed', '9781405807050'),
  (2, 'Borrowed', '9781847941831');
-- users
CREATE TABLE users (
  idUser int NOT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  DOB date DEFAULT NULL,
  user_role varchar(20) DEFAULT NULL,
  PRIMARY KEY (idUser)
);
INSERT INTO users
VALUES (
    1,
    'Apichapat',
    'Temboonsarun',
    '2009-09-27',
    'Student'
  ),
  (2, 'Anh', 'Nguyen', '2008-06-20', 'Student'),
  (3, 'Whalley', 'Andy', '1980-01-01', 'Teacher'),
  (4, 'Shang Min', 'Lee', '2010-10-19', 'Student'),
  (5, 'Esther', 'Taylor', '1984-05-05', 'Teacher');
-- borrows
CREATE TABLE borrows (
  idBorrow int NOT NULL,
  borrow_date date DEFAULT NULL,
  return_date date DEFAULT NULL,
  due_date date DEFAULT NULL,
  idUser int DEFAULT NULL,
  book_copy_id int DEFAULT NULL,
  book_copy_ISBN varchar(14) DEFAULT NULL,
  PRIMARY KEY (idBorrow),
  KEY idUser (idUser),
  KEY book_copy_id (book_copy_id),
  KEY book_copy_ISBN (book_copy_ISBN),
  CONSTRAINT borrows_ibfk_1 FOREIGN KEY (idUser) REFERENCES users (idUser) ON DELETE CASCADE,
  CONSTRAINT borrows_ibfk_2 FOREIGN KEY (book_copy_id) REFERENCES book_copies (copy_id) ON DELETE CASCADE,
  CONSTRAINT borrows_ibfk_3 FOREIGN KEY (book_copy_ISBN) REFERENCES books (ISBN) ON DELETE CASCADE
);
INSERT INTO borrows
VALUES (
    1,
    '2026-05-17',
    NULL,
    '2026-05-31',
    1,
    1,
    '9781405807050'
  ),
  (
    2,
    '2026-05-17',
    NULL,
    '2026-05-31',
    1,
    1,
    '9781405807050'
  );
SET FOREIGN_KEY_CHECKS = 1;