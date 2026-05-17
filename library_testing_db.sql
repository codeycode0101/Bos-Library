-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: bos_library
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book_copies`
--

DROP TABLE IF EXISTS book_copies;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE book_copies (
  copy_id int NOT NULL,
  copy_status varchar(45) DEFAULT NULL,
  copy_ISBN varchar(14) NOT NULL,
  PRIMARY KEY (copy_id,copy_ISBN),
  KEY copy_ISBN (copy_ISBN),
  CONSTRAINT book_copies_ibfk_1 FOREIGN KEY (copy_ISBN) REFERENCES books (ISBN) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_copies`
--

LOCK TABLES book_copies WRITE;
/*!40000 ALTER TABLE book_copies DISABLE KEYS */;
INSERT INTO book_copies VALUES (1,'Available','9780008533571'),(1,'Available','9781398519732'),(1,'Available','9781405807050'),(1,'Available','9781847941831'),(2,'Borrowed','9780008533571'),(2,'Borrowed','9781398519732'),(2,'Borrowed','9781405807050'),(2,'Borrowed','9781847941831');
/*!40000 ALTER TABLE book_copies ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS books;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE books (
  ISBN varchar(14) NOT NULL,
  Title varchar(200) DEFAULT NULL,
  Author varchar(100) DEFAULT NULL,
  Age_Restricted int DEFAULT NULL,
  idGenre int DEFAULT NULL,
  PRIMARY KEY (ISBN),
  KEY idGenre (idGenre),
  CONSTRAINT books_ibfk_1 FOREIGN KEY (idGenre) REFERENCES genres (idGenre) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES books WRITE;
/*!40000 ALTER TABLE books DISABLE KEYS */;
INSERT INTO books VALUES ('9780008533571','Watching You','Helen Fields',18,4),('9780435232818','The Crucible','Arthur Miller',18,1),('9781398519732','All Your Perfects','Colleen Hoover',18,3),('9781405807050','Carol Ann Duffy Selected Poems','Michael.J.Woods',16,2),('9781847941831','Atomic Habits','James Clear',18,5);
/*!40000 ALTER TABLE books ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `borrows`
--

DROP TABLE IF EXISTS borrows;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrows`
--

LOCK TABLES borrows WRITE;
/*!40000 ALTER TABLE borrows DISABLE KEYS */;
INSERT INTO borrows VALUES (1,'2026-05-17',NULL,'2026-05-31',1,1,'9781405807050'),(2,'2026-05-17',NULL,'2026-05-31',1,1,'9781405807050');
/*!40000 ALTER TABLE borrows ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS genres;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE genres (
  idGenre int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (idGenre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES genres WRITE;
/*!40000 ALTER TABLE genres DISABLE KEYS */;
INSERT INTO genres VALUES (1,'Non-fiction'),(2,'Fiction'),(3,'Romance'),(4,'Thriller'),(5,'Self-Help');
/*!40000 ALTER TABLE genres ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS users;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE users (
  idUser int NOT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  DOB date DEFAULT NULL,
  user_role varchar(20) DEFAULT NULL,
  PRIMARY KEY (idUser)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES users WRITE;
/*!40000 ALTER TABLE users DISABLE KEYS */;
INSERT INTO users VALUES (1,'Apichapat','Temboonsarun','2009-09-27','Student'),(2,'Anh','Nguyen','2008-06-20','Student'),(3,'Whalley','Andy','1980-01-01','Teacher'),(4,'Shang Min','Lee','2010-10-19','Student'),(5,'Esther','Taylor','1984-05-05','Teacher');
/*!40000 ALTER TABLE users ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-17 14:05:06
