-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: ecom
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addition`
--

DROP TABLE IF EXISTS `addition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addition` (
  `itemid` varchar(30) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `discription` longtext,
  `qty` varchar(20) DEFAULT NULL,
  `category` enum('electronics','grocery','fashion','home') DEFAULT NULL,
  `price` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`itemid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addition`
--

LOCK TABLES `addition` WRITE;
/*!40000 ALTER TABLE `addition` DISABLE KEYS */;
INSERT INTO `addition` VALUES ('C0gX5n','samsung_galaxy','A-15','1','electronics','18599'),('D7tT9n','iPhone_14_Pro_Max','iphone','1','electronics','120599'),('D7vM0z','tomato','veg','1','grocery','99'),('F4iI8x','Black_Jean','The best fit for everyone','1','fashion','999'),('G2eX3c','Ear-Buds-1','works on bluetooth','1','electronics','1599'),('G2lH7g','Durian_juice','juice','1','grocery','150'),('G4yK8h','Shirt','Best Fit','1','fashion','1699'),('I8fA5o','tech_watch','watch','1','electronics','4599'),('J5vR2s','Victus','16d305','1','electronics','7099'),('J6vX9e','Roots','red','1','grocery','99'),('J9yM4h','T-shirt','The best fit for everyone','1','fashion','1500'),('K7iQ5y','Eggs','eggs','1','grocery','120'),('L4hN9b','headset','red','1','electronics','6599'),('M4eO4e','ketchup','Tomato','1','grocery','89'),('M8kO5c','T-shirt_Red','The best fit for everyone','1','fashion','1599'),('N3qU2x','mac_book','apple products','1','electronics','130099'),('O0gD8h','Dell','gaming laptop','1','electronics','68599'),('O5aX4i','Milk','Fresh one','1','grocery','39'),('O8kS5w','T-shirt','The best fit for everyone','1','fashion','1599'),('P6nS6x','T-shirt_Leaf','The best fit for everyone','1','fashion','1599'),('P6uK3q','Green_peas','peas','1','grocery','49'),('R1vY4j','blog_header_','mobile','1','electronics','20599'),('R3dQ7v','Patch_fire','The best fit for everyone','1','fashion','1599'),('T1rI4x','T-shirt_Black','The best fit for everyone','1','fashion','1599'),('T2lZ3i','Potato_chips','chips','1','grocery','99'),('T4yH1u','Boat_set','headset','1','electronics','6599'),('U4cK3e','Dal','red_dal','1','grocery','49'),('V4aI6p','T-shirt_Nrml','The best fit for everyone','1','fashion','1599'),('Y3nD6d','Shirt-Blue','Best Fit','1','fashion','1699'),('Y8xL6m','Korolina','berries','1','grocery','99');
/*!40000 ALTER TABLE `addition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `name` varchar(40) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('Janardhan','9963558417','janardhanyelusuri58233@gmail.com','Frds@1234');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `username` varchar(50) NOT NULL,
  `productname` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  `price` int NOT NULL,
  `totalprice` int NOT NULL,
  PRIMARY KEY (`username`,`productname`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`username`) REFERENCES `signup` (`name`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` bigint NOT NULL AUTO_INCREMENT,
  `item_id` varchar(30) NOT NULL,
  `item_name` longtext NOT NULL,
  `qty` int DEFAULT NULL,
  `total_price` bigint DEFAULT NULL,
  `user` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user` (`user`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user`) REFERENCES `signup` (`name`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `addition` (`itemid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'C0gX5n','samsung_galaxy',1,18599,'janardhan');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signup`
--

DROP TABLE IF EXISTS `signup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `signup` (
  `name` varchar(40) NOT NULL,
  `mobile` varchar(12) DEFAULT NULL,
  `email` varchar(75) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `password` text,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signup`
--

LOCK TABLES `signup` WRITE;
/*!40000 ALTER TABLE `signup` DISABLE KEYS */;
INSERT INTO `signup` VALUES ('Janardhan','09963558417','janardhanyelusuri58233@gmail.com','2-37,Vedullanarava','Frds@1234'),('kartik','9963558417','kartikcuze543@gmail.com','2-37,Vedullanarava','Frds@1234');
/*!40000 ALTER TABLE `signup` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-23 15:14:16
