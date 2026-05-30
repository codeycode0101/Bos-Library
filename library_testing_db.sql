-- Clean MySQL dump for library_testing_db
CREATE DATABASE IF NOT EXISTS `bos_library`;
USE `bos_library`;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `borrows`;
DROP TABLE IF EXISTS `book_copies`;
DROP TABLE IF EXISTS `books`;
DROP TABLE IF EXISTS `genres`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `genres` (
  `idGenre` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idGenre`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
CREATE TABLE `books` (
  `ISBN` varchar(14) NOT NULL,
  `Title` varchar(200) DEFAULT NULL,
  `Author` varchar(100) DEFAULT NULL,
  `Age_Restricted` int DEFAULT NULL,
  `idGenre` int DEFAULT NULL,
  PRIMARY KEY (`ISBN`),
  KEY `idGenre` (`idGenre`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`idGenre`) REFERENCES `genres` (`idGenre`) ON DELETE
  SET NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
CREATE TABLE `book_copies` (
  `copy_id` int NOT NULL,
  `copy_status` varchar(45) DEFAULT NULL,
  `copy_ISBN` varchar(14) NOT NULL,
  PRIMARY KEY (`copy_id`, `copy_ISBN`),
  KEY `copy_ISBN` (`copy_ISBN`),
  CONSTRAINT `book_copies_ibfk_1` FOREIGN KEY (`copy_ISBN`) REFERENCES `books` (`ISBN`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
CREATE TABLE `users` (
  `idUser` int NOT NULL,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `user_role` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
CREATE TABLE `borrows` (
  `idBorrow` int NOT NULL AUTO_INCREMENT,
  `borrow_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `idUser` int DEFAULT NULL,
  `book_copy_id` int DEFAULT NULL,
  `book_copy_ISBN` varchar(14) DEFAULT NULL,
  `late` tinyint(1) DEFAULT '0',
  `returned` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`idBorrow`),
  KEY `idUser` (`idUser`),
  KEY `book_copy_id` (`book_copy_id`),
  KEY `book_copy_ISBN` (`book_copy_ISBN`),
  KEY `book_copy_id_book_copy_ISBN` (`book_copy_id`, `book_copy_ISBN`),
  CONSTRAINT `borrows_ibfk_1` FOREIGN KEY (`idUser`) REFERENCES `users` (`idUser`) ON DELETE CASCADE,
  CONSTRAINT `borrows_ibfk_2` FOREIGN KEY (`book_copy_id`, `book_copy_ISBN`) REFERENCES `book_copies` (`copy_id`, `copy_ISBN`) ON DELETE CASCADE,
  CONSTRAINT `borrows_ibfk_3` FOREIGN KEY (`book_copy_ISBN`) REFERENCES `books` (`ISBN`) ON DELETE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
INSERT INTO `genres` (`idGenre`, `name`)
VALUES (1, 'Non-fiction'),
  (2, 'Fiction'),
  (3, 'Romance'),
  (4, 'Thriller'),
  (5, 'Self-Help');
INSERT INTO `books` (
    `ISBN`,
    `Title`,
    `Author`,
    `Age_Restricted`,
    `idGenre`
  )
VALUES ('1001', 'Watching You', 'Helen Fields', 18, 4),
  ('1002', 'The Crucible', 'Arthur Miller', 18, 1),
  (
    '1003',
    'All Your Perfects',
    'Colleen Hoover',
    18,
    3
  ),
  (
    '1004',
    'Carol Ann Duffy Selected Poems',
    'Michael.J.Woods',
    16,
    2
  ),
  ('1005', 'Atomic Habits', 'James Clear', 18, 5);
INSERT INTO `book_copies` (`copy_id`, `copy_status`, `copy_ISBN`)
VALUES (1, 'Borrowed', '1001'),
  (2, 'Available', '1001'),
  (1, 'Borrowed', '1002'),
  (2, 'Available', '1002'),
  (1, 'Available', '1003'),
  (2, 'Available', '1003'),
  (1, 'Available', '1004'),
  (2, 'Borrowed', '1004'),
  (1, 'Available', '1005'),
  (2, 'Available', '1005');
INSERT INTO `users` (
    `idUser`,
    `first_name`,
    `last_name`,
    `DOB`,
    `user_role`
  )
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
INSERT INTO `borrows` (
    `borrow_date`,
    `return_date`,
    `due_date`,
    `idUser`,
    `book_copy_id`,
    `book_copy_ISBN`,
    `late`,
    `returned`
  )
VALUES (
    '2026-05-17',
    NULL,
    '2026-05-31',
    1,
    1,
    '1001',
    0,
    NULL
  ),
  (
    '2026-05-18',
    NULL,
    '2026-05-31',
    2,
    1,
    '1002',
    0,
    NULL
  ),
  (
    '2026-05-23',
    NULL,
    '2026-06-06',
    3,
    2,
    '1004',
    0,
    NULL
  );
SET FOREIGN_KEY_CHECKS = 1;