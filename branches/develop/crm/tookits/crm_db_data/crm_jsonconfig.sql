-- MySQL dump 10.13  Distrib 5.6.28, for debian-linux-gnu (x86_64)
--
-- Host: 192.168.162.103    Database: crm
-- ------------------------------------------------------
-- Server version	5.5.15-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `crm_jsonconfig`
--

DROP TABLE IF EXISTS `crm_jsonconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crm_jsonconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `value` longtext NOT NULL,
  `create_time` datetime NOT NULL,
  `description` longtext NOT NULL,
  `modify_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crm_jsonconfig`
--

LOCK TABLES `crm_jsonconfig` WRITE;
/*!40000 ALTER TABLE `crm_jsonconfig` DISABLE KEYS */;
INSERT INTO `crm_jsonconfig` VALUES (1,'no-test','[\"TelecomCheck\"]','2016-03-09 16:42:38','交付申请中，不支持测试期的模块','2016-03-17 14:09:21'),(2,'web-modules','[\"RuleSpecialList\", \"RuleApplyLoan\", \"ApplyLoan\", \"TelecomCheck\", \"Stability_c\", \"PayConsumption\", \"AccountchangeMonth\"]','2016-03-09 16:43:53','风险罗盘web版支持的模块','2016-03-22 10:55:35'),(3,'enabled-modules','[\"RuleSpecialList\", \"RuleApplyLoan\", \"SpecialList_c\", \"ApplyLoan\", \"TelecomCheck\", \"Location\", \"Stability_c\", \"Consumption_c\", \"Media_c\", \"PayConsumption\", \"AirTravel\", \"Stability\", \"Authentication\", \"Consumption\", \"Media\", \"brcreditpoint\", \"scorep2p\", \"scorebank\", \"scorecf\", \"ScoreCust\", \"DataCust\", \"Title\", \"Assets\", \"Brand\", \"AccountchangeMonth\"]','2016-03-18 18:49:03','','2016-03-18 18:49:03');
/*!40000 ALTER TABLE `crm_jsonconfig` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-24 11:03:34
