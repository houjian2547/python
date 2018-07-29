/*
SQLyog Ultimate v8.32 
MySQL - 5.6.25-log : Database - python_test
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`python_test` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `python_test`;

/*Table structure for table `first_url_type` */

DROP TABLE IF EXISTS `first_url_type`;

CREATE TABLE `first_url_type` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL COMMENT '一级地址',
  `type_name` varchar(255) DEFAULT NULL COMMENT '电影类型名字',
  `type_code` int(50) DEFAULT NULL COMMENT '电影类型code',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8 COMMENT='一级地址和电影类型表';

/*Table structure for table `second_url_film_name` */

DROP TABLE IF EXISTS `second_url_film_name`;

CREATE TABLE `second_url_film_name` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `second_url` varchar(255) DEFAULT NULL COMMENT '二级访问地址',
  `film_name` varchar(255) DEFAULT NULL COMMENT '电影名字',
  `type_code` int(50) DEFAULT NULL COMMENT '电影类型code',
  `download_ftp_url` varchar(255) DEFAULT NULL COMMENT '下载地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15041 DEFAULT CHARSET=utf8 COMMENT='二级地址和电影地址';

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
