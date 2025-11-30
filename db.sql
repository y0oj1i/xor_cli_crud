-- MySQL dump for xor_crud app
CREATE DATABASE IF NOT EXISTS `xor_crud` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `xor_crud`;

CREATE TABLE `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nonce` varchar(64) NOT NULL,
  `data_enc` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
