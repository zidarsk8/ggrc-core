-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: db    Database: ggrcdev
-- ------------------------------------------------------
-- Server version	5.6.36-log

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
-- Table structure for table `access_control_list`
--

DROP TABLE IF EXISTS `access_control_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_control_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `ac_role_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `parent_id_nn` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_access_control_list` (`person_id`,`ac_role_id`,`object_id`,`object_type`,`parent_id_nn`),
  KEY `ac_role_id` (`ac_role_id`),
  KEY `fk_access_control_list_contexts` (`context_id`),
  KEY `ix_access_control_list_updated_at` (`updated_at`),
  KEY `idx_object_type_object_idx` (`object_type`,`object_id`),
  KEY `fk_access_control_list_parent_id` (`parent_id`),
  KEY `ix_person_object` (`person_id`,`object_type`,`object_id`),
  KEY `idx_object_type_object_id_parent_id_nn` (`object_type`,`object_id`,`parent_id_nn`),
  CONSTRAINT `access_control_list_ibfk_1` FOREIGN KEY (`ac_role_id`) REFERENCES `access_control_roles` (`id`),
  CONSTRAINT `access_control_list_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `access_control_list_ibfk_3` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),
  CONSTRAINT `fk_access_control_list_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `access_control_list` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_control_list`
--

LOCK TABLES `access_control_list` WRITE;
/*!40000 ALTER TABLE `access_control_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_control_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `access_control_roles`
--

DROP TABLE IF EXISTS `access_control_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_control_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `object_type` varchar(250) DEFAULT NULL,
  `tooltip` varchar(250) DEFAULT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '1',
  `update` tinyint(1) NOT NULL DEFAULT '1',
  `delete` tinyint(1) NOT NULL DEFAULT '1',
  `my_work` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `mandatory` tinyint(1) NOT NULL DEFAULT '0',
  `default_to_current_user` tinyint(1) NOT NULL DEFAULT '0',
  `non_editable` tinyint(1) NOT NULL DEFAULT '0',
  `internal` tinyint(1) NOT NULL DEFAULT '0',
  `notify_about_proposal` tinyint(1) NOT NULL DEFAULT '0',
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`object_type`),
  KEY `fk_access_control_roles_contexts` (`context_id`),
  KEY `ix_access_control_roles_updated_at` (`updated_at`),
  KEY `fk_access_control_roles_parent_id` (`parent_id`),
  CONSTRAINT `access_control_roles_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_access_control_roles_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `access_control_roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3926 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_control_roles`
--

LOCK TABLES `access_control_roles` WRITE;
/*!40000 ALTER TABLE `access_control_roles` DISABLE KEYS */;
INSERT INTO `access_control_roles` VALUES (1,'Primary Contacts','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(2,'Secondary Contacts','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(3,'Primary Contacts','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(4,'Secondary Contacts','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(5,'Primary Contacts','Clause',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(6,'Secondary Contacts','Clause',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(7,'Primary Contacts','Contract',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(8,'Secondary Contacts','Contract',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(9,'Primary Contacts','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,1,NULL),(10,'Secondary Contacts','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(11,'Principal Assignees','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(12,'Secondary Assignees','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(13,'Primary Contacts','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(14,'Secondary Contacts','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(15,'Primary Contacts','Facility',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(16,'Secondary Contacts','Facility',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(17,'Primary Contacts','Issue',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(18,'Secondary Contacts','Issue',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(19,'Primary Contacts','Market',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(20,'Secondary Contacts','Market',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(21,'Primary Contacts','Objective',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(22,'Secondary Contacts','Objective',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(23,'Primary Contacts','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(24,'Secondary Contacts','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(25,'Primary Contacts','Policy',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(26,'Secondary Contacts','Policy',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(27,'Primary Contacts','Process',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(28,'Secondary Contacts','Process',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(29,'Primary Contacts','Product',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(30,'Secondary Contacts','Product',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(31,'Primary Contacts','Project',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(32,'Secondary Contacts','Project',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(33,'Primary Contacts','Program',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(34,'Secondary Contacts','Program',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(35,'Primary Contacts','Regulation',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(36,'Secondary Contacts','Regulation',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(37,'Primary Contacts','Requirement',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(38,'Secondary Contacts','Requirement',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(39,'Primary Contacts','Standard',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(40,'Secondary Contacts','Standard',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(41,'Primary Contacts','System',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(42,'Secondary Contacts','System',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(43,'Primary Contacts','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(44,'Secondary Contacts','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0,NULL),(45,'Admin','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(46,'Admin','Clause',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(47,'Admin','Comment',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(48,'Admin','Contract',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(49,'Admin','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,1,NULL),(50,'Admin','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(51,'Admin','Document',NULL,1,1,0,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(52,'Admin','Facility',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(53,'Admin','Issue',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(54,'Admin','Market',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(55,'Admin','Objective',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(56,'Admin','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(57,'Admin','Policy',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(58,'Admin','Process',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(59,'Admin','Product',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(60,'Admin','Project',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(61,'Admin','Regulation',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(62,'Admin','Risk',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,1,NULL),(63,'Admin','Requirement',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(64,'Admin','Standard',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(65,'Admin','System',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(66,'Admin','Threat',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(67,'Admin','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0,NULL),(68,'Verifiers Document Mapped','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0,NULL),(69,'Verifiers Mapped','Assessment',NULL,1,0,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0,NULL),(70,'Creators Document Mapped','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0,NULL),(71,'Creators Mapped','Assessment',NULL,1,0,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0,NULL),(72,'Assignees','Assessment',NULL,1,1,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,1,0,1,0,0,NULL),(73,'Verifiers','Assessment',NULL,1,1,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,0,0,NULL),(74,'Assignees Mapped','Assessment',NULL,1,0,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0,NULL),(75,'Assignees Document Mapped','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0,NULL),(76,'Creators','Assessment',NULL,1,1,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,1,0,1,0,0,NULL),(77,'ProposalReader','Proposal',NULL,1,0,0,1,'2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL,0,0,1,1,0,NULL),(78,'ProposalEditor','Proposal',NULL,1,1,0,1,'2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL,0,0,1,1,0,NULL),(303,'Admin','Evidence',NULL,1,1,0,1,'2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL,1,1,1,0,0,NULL),(909,'Primary Contacts','Metric',NULL,1,1,1,1,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,0,0,NULL),(910,'Secondary Contacts','Metric',NULL,1,1,1,1,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,0,0,NULL),(911,'Admin','Metric',NULL,1,1,1,1,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,1,1,1,0,0,NULL),(912,'Admin*56*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,56),(913,'Admin*56*912*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,912),(914,'Admin*56*912*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,912),(915,'Admin*56*912*914*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,914),(916,'Admin*56*912*914*915*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,915),(917,'Primary Contacts*23*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,23),(918,'Primary Contacts*23*917*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,917),(919,'Primary Contacts*23*917*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,917),(920,'Primary Contacts*23*917*919*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,919),(921,'Primary Contacts*23*917*919*920*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,920),(922,'Secondary Contacts*24*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,24),(923,'Secondary Contacts*24*922*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,922),(924,'Secondary Contacts*24*922*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,922),(925,'Secondary Contacts*24*922*924*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,924),(926,'Secondary Contacts*24*922*924*925*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,925),(927,'Admin*63*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,63),(928,'Admin*63*927*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,927),(929,'Admin*63*927*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,927),(930,'Admin*63*927*929*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,929),(931,'Admin*63*927*929*930*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,930),(932,'Primary Contacts*37*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,37),(933,'Primary Contacts*37*932*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,932),(934,'Primary Contacts*37*932*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,932),(935,'Primary Contacts*37*932*934*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,934),(936,'Primary Contacts*37*932*934*935*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,935),(937,'Secondary Contacts*38*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,38),(938,'Secondary Contacts*38*937*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,937),(939,'Secondary Contacts*38*937*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,937),(940,'Secondary Contacts*38*937*939*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,939),(941,'Secondary Contacts*38*937*939*940*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,940),(942,'Admin*45*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,45),(943,'Admin*45*942*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,942),(944,'Admin*45*942*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,942),(945,'Admin*45*942*944*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,944),(946,'Admin*45*942*944*945*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,945),(947,'Primary Contacts*1*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1),(948,'Primary Contacts*1*947*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,947),(949,'Primary Contacts*1*947*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,947),(950,'Primary Contacts*1*947*949*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,949),(951,'Primary Contacts*1*947*949*950*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,950),(952,'Secondary Contacts*2*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,2),(953,'Secondary Contacts*2*952*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,952),(954,'Secondary Contacts*2*952*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,952),(955,'Secondary Contacts*2*952*954*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,954),(956,'Secondary Contacts*2*952*954*955*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,955),(957,'Admin*65*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,65),(958,'Admin*65*957*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,957),(959,'Admin*65*957*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,957),(960,'Admin*65*957*959*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,959),(961,'Admin*65*957*959*960*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,960),(962,'Primary Contacts*41*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,41),(963,'Primary Contacts*41*962*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,962),(964,'Primary Contacts*41*962*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,962),(965,'Primary Contacts*41*962*964*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,964),(966,'Primary Contacts*41*962*964*965*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,965),(967,'Secondary Contacts*42*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,42),(968,'Secondary Contacts*42*967*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,967),(969,'Secondary Contacts*42*967*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,967),(970,'Secondary Contacts*42*967*969*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,969),(971,'Secondary Contacts*42*967*969*970*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,970),(972,'Admin*55*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,55),(973,'Admin*55*972*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,972),(974,'Admin*55*972*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,972),(975,'Admin*55*972*974*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,974),(976,'Admin*55*972*974*975*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,975),(977,'Primary Contacts*21*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,21),(978,'Primary Contacts*21*977*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,977),(979,'Primary Contacts*21*977*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,977),(980,'Primary Contacts*21*977*979*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,979),(981,'Primary Contacts*21*977*979*980*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,980),(982,'Secondary Contacts*22*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,22),(983,'Secondary Contacts*22*982*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,982),(984,'Secondary Contacts*22*982*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,982),(985,'Secondary Contacts*22*982*984*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,984),(986,'Secondary Contacts*22*982*984*985*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,985),(987,'Admin*61*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,61),(988,'Admin*61*987*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,987),(989,'Admin*61*987*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,987),(990,'Admin*61*987*989*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,989),(991,'Admin*61*987*989*990*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,990),(992,'Primary Contacts*35*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,35),(993,'Primary Contacts*35*992*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,992),(994,'Primary Contacts*35*992*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,992),(995,'Primary Contacts*35*992*994*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,994),(996,'Primary Contacts*35*992*994*995*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,995),(997,'Secondary Contacts*36*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,36),(998,'Secondary Contacts*36*997*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,997),(999,'Secondary Contacts*36*997*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,997),(1000,'Secondary Contacts*36*997*999*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,999),(1001,'Secondary Contacts*36*997*999*1000*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1000),(1002,'Admin*57*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,57),(1003,'Admin*57*1002*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1002),(1004,'Admin*57*1002*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1002),(1005,'Admin*57*1002*1004*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1004),(1006,'Admin*57*1002*1004*1005*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1005),(1007,'Primary Contacts*25*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,25),(1008,'Primary Contacts*25*1007*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1007),(1009,'Primary Contacts*25*1007*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1007),(1010,'Primary Contacts*25*1007*1009*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1009),(1011,'Primary Contacts*25*1007*1009*1010*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1010),(1012,'Secondary Contacts*26*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,26),(1013,'Secondary Contacts*26*1012*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1012),(1014,'Secondary Contacts*26*1012*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1012),(1015,'Secondary Contacts*26*1012*1014*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1014),(1016,'Secondary Contacts*26*1012*1014*1015*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1015),(1017,'Admin*51*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,51),(1018,'Admin*51*1017*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1017),(1019,'Admin*53*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,53),(1020,'Admin*53*1019*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1019),(1021,'Admin*53*1019*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1019),(1022,'Admin*53*1019*1021*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1021),(1023,'Admin*53*1019*1021*1022*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1022),(1024,'Primary Contacts*17*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,17),(1025,'Primary Contacts*17*1024*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1024),(1026,'Primary Contacts*17*1024*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1024),(1027,'Primary Contacts*17*1024*1026*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1026),(1028,'Primary Contacts*17*1024*1026*1027*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1027),(1029,'Secondary Contacts*18*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,18),(1030,'Secondary Contacts*18*1029*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1029),(1031,'Secondary Contacts*18*1029*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1029),(1032,'Secondary Contacts*18*1029*1031*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1031),(1033,'Secondary Contacts*18*1029*1031*1032*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1032),(1034,'Admin*59*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,59),(1035,'Admin*59*1034*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1034),(1036,'Admin*59*1034*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1034),(1037,'Admin*59*1034*1036*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1036),(1038,'Admin*59*1034*1036*1037*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1037),(1039,'Primary Contacts*29*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,29),(1040,'Primary Contacts*29*1039*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1039),(1041,'Primary Contacts*29*1039*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1039),(1042,'Primary Contacts*29*1039*1041*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1041),(1043,'Primary Contacts*29*1039*1041*1042*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1042),(1044,'Secondary Contacts*30*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,30),(1045,'Secondary Contacts*30*1044*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1044),(1046,'Secondary Contacts*30*1044*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1044),(1047,'Secondary Contacts*30*1044*1046*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1046),(1048,'Secondary Contacts*30*1044*1046*1047*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1047),(1049,'Admin*67*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,67),(1050,'Admin*67*1049*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1049),(1051,'Admin*67*1049*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1049),(1052,'Admin*67*1049*1051*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1051),(1053,'Admin*67*1049*1051*1052*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1052),(1054,'Primary Contacts*43*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,43),(1055,'Primary Contacts*43*1054*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1054),(1056,'Primary Contacts*43*1054*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1054),(1057,'Primary Contacts*43*1054*1056*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1056),(1058,'Primary Contacts*43*1054*1056*1057*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1057),(1059,'Secondary Contacts*44*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,44),(1060,'Secondary Contacts*44*1059*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1059),(1061,'Secondary Contacts*44*1059*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1059),(1062,'Secondary Contacts*44*1059*1061*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1061),(1063,'Secondary Contacts*44*1059*1061*1062*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1062),(1064,'Assignees*72*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,72),(1065,'Assignees*72*1064*','Audit',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1064),(1066,'Assignees*72*1064*1065*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1065),(1067,'Assignees*72*1064*1065*1066*','Evidence',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1066),(1068,'Assignees*72*1064*1065*1066*1067*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1067),(1069,'Assignees*72*1064*1065*1066*1067*1068*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1068),(1070,'Assignees*72*1064*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1064),(1071,'Assignees*72*1064*1070*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1070),(1072,'Assignees*72*1064*1070*1071*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1071),(1073,'Assignees*72*1064*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1064),(1074,'Assignees*72*1064*1073*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1073),(1075,'Assignees*72*1064*1073*1074*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1074),(1076,'Assignees*72*1064*','Issue',NULL,1,1,1,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1064),(1077,'Assignees*72*1064*1076*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1076),(1078,'Assignees*72*1064*1076*1077*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1077),(1079,'Assignees*72*1064*1076*1077*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1077),(1080,'Assignees*72*1064*1076*1077*1079*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1079),(1081,'Assignees*72*1064*1076*1077*1079*1080*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1080),(1082,'Assignees*72*1064*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1064),(1083,'Creators*76*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,76),(1084,'Creators*76*1083*','Audit',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1083),(1085,'Creators*76*1083*1084*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1084),(1086,'Creators*76*1083*1084*1085*','Evidence',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1085),(1087,'Creators*76*1083*1084*1085*1086*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1086),(1088,'Creators*76*1083*1084*1085*1086*1087*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1087),(1089,'Creators*76*1083*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1083),(1090,'Creators*76*1083*1089*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1089),(1091,'Creators*76*1083*1089*1090*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1090),(1092,'Creators*76*1083*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1083),(1093,'Creators*76*1083*1092*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1092),(1094,'Creators*76*1083*1092*1093*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1093),(1095,'Creators*76*1083*','Issue',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1083),(1096,'Creators*76*1083*1095*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1095),(1097,'Creators*76*1083*1095*1096*','Document',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1096),(1098,'Creators*76*1083*1095*1096*1097*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1097),(1099,'Creators*76*1083*1095*1096*1097*1098*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1098),(1100,'Creators*76*1083*1095*1096*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1096),(1101,'Creators*76*1083*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1083),(1102,'Verifiers*73*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,73),(1103,'Verifiers*73*1102*','Audit',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1102),(1104,'Verifiers*73*1102*1103*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1103),(1105,'Verifiers*73*1102*1103*1104*','Evidence',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1104),(1106,'Verifiers*73*1102*1103*1104*1105*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1105),(1107,'Verifiers*73*1102*1103*1104*1105*1106*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1106),(1108,'Verifiers*73*1102*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1102),(1109,'Verifiers*73*1102*1108*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1108),(1110,'Verifiers*73*1102*1108*1109*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1109),(1111,'Verifiers*73*1102*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1102),(1112,'Verifiers*73*1102*1111*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1111),(1113,'Verifiers*73*1102*1111*1112*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1112),(1114,'Verifiers*73*1102*','Issue',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1102),(1115,'Verifiers*73*1102*1114*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1114),(1116,'Verifiers*73*1102*1114*1115*','Document',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1115),(1117,'Verifiers*73*1102*1114*1115*1116*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1116),(1118,'Verifiers*73*1102*1114*1115*1116*1117*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1117),(1119,'Verifiers*73*1102*1114*1115*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1115),(1120,'Verifiers*73*1102*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1102),(1121,'Admin*64*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,64),(1122,'Admin*64*1121*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1121),(1123,'Admin*64*1121*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1121),(1124,'Admin*64*1121*1123*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1123),(1125,'Admin*64*1121*1123*1124*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1124),(1126,'Primary Contacts*39*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,39),(1127,'Primary Contacts*39*1126*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1126),(1128,'Primary Contacts*39*1126*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1126),(1129,'Primary Contacts*39*1126*1128*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1128),(1130,'Primary Contacts*39*1126*1128*1129*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1129),(1131,'Secondary Contacts*40*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,40),(1132,'Secondary Contacts*40*1131*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1131),(1133,'Secondary Contacts*40*1131*','Document',NULL,1,1,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1131),(1134,'Secondary Contacts*40*1131*1133*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1133),(1135,'Secondary Contacts*40*1131*1133*1134*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL,0,0,1,1,0,1134),(1136,'Admin*48*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,48),(1137,'Admin*48*1136*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1136),(1138,'Admin*48*1136*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1136),(1139,'Admin*48*1136*1138*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1138),(1140,'Admin*48*1136*1138*1139*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1139),(1141,'Primary Contacts*7*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,7),(1142,'Primary Contacts*7*1141*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1141),(1143,'Primary Contacts*7*1141*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1141),(1144,'Primary Contacts*7*1141*1143*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1143),(1145,'Primary Contacts*7*1141*1143*1144*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1144),(1146,'Secondary Contacts*8*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,8),(1147,'Secondary Contacts*8*1146*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1146),(1148,'Secondary Contacts*8*1146*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1146),(1149,'Secondary Contacts*8*1146*1148*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1148),(1150,'Secondary Contacts*8*1146*1148*1149*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1149),(1151,'Admin*60*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,60),(1152,'Admin*60*1151*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1151),(1153,'Admin*60*1151*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1151),(1154,'Admin*60*1151*1153*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1153),(1155,'Admin*60*1151*1153*1154*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1154),(1156,'Primary Contacts*31*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,31),(1157,'Primary Contacts*31*1156*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1156),(1158,'Primary Contacts*31*1156*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1156),(1159,'Primary Contacts*31*1156*1158*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1158),(1160,'Primary Contacts*31*1156*1158*1159*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1159),(1161,'Secondary Contacts*32*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,32),(1162,'Secondary Contacts*32*1161*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1161),(1163,'Secondary Contacts*32*1161*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1161),(1164,'Secondary Contacts*32*1161*1163*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1163),(1165,'Secondary Contacts*32*1161*1163*1164*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1164),(1166,'Admin*50*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,50),(1167,'Admin*50*1166*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1166),(1168,'Admin*50*1166*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1166),(1169,'Admin*50*1166*1168*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1168),(1170,'Admin*50*1166*1168*1169*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1169),(1171,'Primary Contacts*13*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,13),(1172,'Primary Contacts*13*1171*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1171),(1173,'Primary Contacts*13*1171*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1171),(1174,'Primary Contacts*13*1171*1173*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1173),(1175,'Primary Contacts*13*1171*1173*1174*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1174),(1176,'Secondary Contacts*14*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,14),(1177,'Secondary Contacts*14*1176*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1176),(1178,'Secondary Contacts*14*1176*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1176),(1179,'Secondary Contacts*14*1176*1178*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1178),(1180,'Secondary Contacts*14*1176*1178*1179*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1179),(1181,'Admin*49*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,49),(1182,'Admin*49*1181*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1181),(1183,'Admin*49*1181*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1181),(1184,'Admin*49*1181*1183*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1183),(1185,'Admin*49*1181*1183*1184*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1184),(1186,'Admin*49*1181*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1181),(1187,'Primary Contacts*9*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,9),(1188,'Primary Contacts*9*1187*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1187),(1189,'Primary Contacts*9*1187*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1187),(1190,'Primary Contacts*9*1187*1189*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1189),(1191,'Primary Contacts*9*1187*1189*1190*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1190),(1192,'Primary Contacts*9*1187*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1187),(1193,'Secondary Contacts*10*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,10),(1194,'Secondary Contacts*10*1193*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1193),(1195,'Secondary Contacts*10*1193*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1193),(1196,'Secondary Contacts*10*1193*1195*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1195),(1197,'Secondary Contacts*10*1193*1195*1196*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1196),(1198,'Secondary Contacts*10*1193*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1193),(1199,'Principal Assignees*11*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,11),(1200,'Principal Assignees*11*1199*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1199),(1201,'Principal Assignees*11*1199*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1199),(1202,'Principal Assignees*11*1199*1201*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1201),(1203,'Principal Assignees*11*1199*1201*1202*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1202),(1204,'Principal Assignees*11*1199*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1199),(1205,'Secondary Assignees*12*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,12),(1206,'Secondary Assignees*12*1205*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1205),(1207,'Secondary Assignees*12*1205*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1205),(1208,'Secondary Assignees*12*1205*1207*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1207),(1209,'Secondary Assignees*12*1205*1207*1208*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1208),(1210,'Secondary Assignees*12*1205*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1205),(1211,'Admin*52*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,52),(1212,'Admin*52*1211*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1211),(1213,'Admin*52*1211*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1211),(1214,'Admin*52*1211*1213*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1213),(1215,'Admin*52*1211*1213*1214*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1214),(1216,'Primary Contacts*15*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,15),(1217,'Primary Contacts*15*1216*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1216),(1218,'Primary Contacts*15*1216*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1216),(1219,'Primary Contacts*15*1216*1218*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1218),(1220,'Primary Contacts*15*1216*1218*1219*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1219),(1221,'Secondary Contacts*16*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,16),(1222,'Secondary Contacts*16*1221*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1221),(1223,'Secondary Contacts*16*1221*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1221),(1224,'Secondary Contacts*16*1221*1223*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1223),(1225,'Secondary Contacts*16*1221*1223*1224*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1224),(1226,'Admin*58*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,58),(1227,'Admin*58*1226*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1226),(1228,'Admin*58*1226*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1226),(1229,'Admin*58*1226*1228*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1228),(1230,'Admin*58*1226*1228*1229*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1229),(1231,'Primary Contacts*27*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,27),(1232,'Primary Contacts*27*1231*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1231),(1233,'Primary Contacts*27*1231*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1231),(1234,'Primary Contacts*27*1231*1233*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1233),(1235,'Primary Contacts*27*1231*1233*1234*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1234),(1236,'Secondary Contacts*28*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,28),(1237,'Secondary Contacts*28*1236*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1236),(1238,'Secondary Contacts*28*1236*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1236),(1239,'Secondary Contacts*28*1236*1238*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1238),(1240,'Secondary Contacts*28*1236*1238*1239*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1239),(1241,'Admin*46*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,46),(1242,'Admin*46*1241*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1241),(1243,'Admin*46*1241*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1241),(1244,'Admin*46*1241*1243*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1243),(1245,'Admin*46*1241*1243*1244*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1244),(1246,'Primary Contacts*5*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,5),(1247,'Primary Contacts*5*1246*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1246),(1248,'Primary Contacts*5*1246*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1246),(1249,'Primary Contacts*5*1246*1248*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1248),(1250,'Primary Contacts*5*1246*1248*1249*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1249),(1251,'Secondary Contacts*6*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,6),(1252,'Secondary Contacts*6*1251*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1251),(1253,'Secondary Contacts*6*1251*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1251),(1254,'Secondary Contacts*6*1251*1253*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1253),(1255,'Secondary Contacts*6*1251*1253*1254*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1254),(1256,'Admin*911*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,911),(1257,'Admin*911*1256*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1256),(1258,'Admin*911*1256*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1256),(1259,'Admin*911*1256*1258*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1258),(1260,'Admin*911*1256*1258*1259*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1259),(1261,'Primary Contacts*909*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,909),(1262,'Primary Contacts*909*1261*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1261),(1263,'Primary Contacts*909*1261*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1261),(1264,'Primary Contacts*909*1261*1263*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1263),(1265,'Primary Contacts*909*1261*1263*1264*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1264),(1266,'Secondary Contacts*910*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,910),(1267,'Secondary Contacts*910*1266*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1266),(1268,'Secondary Contacts*910*1266*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1266),(1269,'Secondary Contacts*910*1266*1268*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1268),(1270,'Secondary Contacts*910*1266*1268*1269*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1269),(1271,'Admin*303*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,303),(1272,'Admin*303*1271*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1271),(1273,'Admin*54*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,54),(1274,'Admin*54*1273*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1273),(1275,'Admin*54*1273*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1273),(1276,'Admin*54*1273*1275*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1275),(1277,'Admin*54*1273*1275*1276*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1276),(1278,'Primary Contacts*19*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,19),(1279,'Primary Contacts*19*1278*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1278),(1280,'Primary Contacts*19*1278*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1278),(1281,'Primary Contacts*19*1278*1280*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1280),(1282,'Primary Contacts*19*1278*1280*1281*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1281),(1283,'Secondary Contacts*20*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,20),(1284,'Secondary Contacts*20*1283*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1283),(1285,'Secondary Contacts*20*1283*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1283),(1286,'Secondary Contacts*20*1283*1285*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1285),(1287,'Secondary Contacts*20*1283*1285*1286*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1286),(1288,'Primary Contacts','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1289,'Secondary Contacts','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1290,'Admin','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,1,1,1,0,0,NULL),(1291,'Admin*1290*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1290),(1292,'Admin*1290*1291*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1291),(1293,'Admin*1290*1291*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1291),(1294,'Admin*1290*1291*1293*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1293),(1295,'Admin*1290*1291*1293*1294*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1294),(1296,'Primary Contacts*1288*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1288),(1297,'Primary Contacts*1288*1296*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1296),(1298,'Primary Contacts*1288*1296*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1296),(1299,'Primary Contacts*1288*1296*1298*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1298),(1300,'Primary Contacts*1288*1296*1298*1299*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1299),(1301,'Secondary Contacts*1289*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1289),(1302,'Secondary Contacts*1289*1301*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1301),(1303,'Secondary Contacts*1289*1301*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1301),(1304,'Secondary Contacts*1289*1301*1303*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1303),(1305,'Secondary Contacts*1289*1301*1303*1304*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1304),(1306,'Primary Contacts','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1307,'Secondary Contacts','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1308,'Admin','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,1,1,1,0,0,NULL),(1309,'Admin*1308*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1308),(1310,'Admin*1308*1309*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1309),(1311,'Admin*1308*1309*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1309),(1312,'Admin*1308*1309*1311*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1311),(1313,'Admin*1308*1309*1311*1312*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1312),(1314,'Primary Contacts*1306*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1306),(1315,'Primary Contacts*1306*1314*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1314),(1316,'Primary Contacts*1306*1314*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1314),(1317,'Primary Contacts*1306*1314*1316*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1316),(1318,'Primary Contacts*1306*1314*1316*1317*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1317),(1319,'Secondary Contacts*1307*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1307),(1320,'Secondary Contacts*1307*1319*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1319),(1321,'Secondary Contacts*1307*1319*','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1319),(1322,'Secondary Contacts*1307*1319*1321*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1321),(1323,'Secondary Contacts*1307*1319*1321*1322*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,1322),(1324,'Admin','BackgroundTask',NULL,1,1,1,0,'2018-08-24 09:33:20',NULL,'2018-08-24 09:33:20',NULL,0,0,1,0,0,NULL),(1325,'Audit Captains Mapped','Audit',NULL,1,1,1,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1326,'Auditors Assessment Mapped','Assessment',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1327,'Auditors','Audit',NULL,1,0,0,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1328,'Audit Captains','Audit',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,1,1,1,0,0,NULL),(1329,'Auditors Mapped','Audit',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1330,'Auditors Snapshot Mapped','Snapshot',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1331,'Auditors Issue Mapped','Issue',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1332,'Auditors Document Mapped','Document',NULL,1,1,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1333,'Program Managers','Program',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,1,1,1,0,0,NULL),(1334,'Program Editors','Program',NULL,1,1,1,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1335,'Program Readers','Program',NULL,1,0,0,1,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,0,0,NULL),(1336,'Program Managers Mapped','Program',NULL,1,1,1,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1337,'Program Editors Mapped','Program',NULL,1,1,1,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(1338,'Program Readers Mapped','Program',NULL,1,0,0,0,'2018-08-24 09:33:19',NULL,'2018-08-24 09:33:19',NULL,0,0,1,1,0,NULL),(2905,'Auditors*1327*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,1327),(2906,'Auditors*1327*2905*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2905),(2907,'Auditors*1327*2905*2906*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2906),(2908,'Auditors*1327*2905*2906*2907*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2907),(2909,'Auditors*1327*2905*','AssessmentTemplate',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2905),(2910,'Auditors*1327*2905*','Issue',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2905),(2911,'Auditors*1327*2905*2910*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2910),(2912,'Auditors*1327*2905*2910*2911*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2911),(2913,'Auditors*1327*2905*2910*2911*2912*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2912),(2914,'Auditors*1327*2905*2910*2911*2912*2913*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2913),(2915,'Auditors*1327*2905*2910*2911*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2911),(2916,'Auditors*1327*2905*','Assessment',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2905),(2917,'Auditors*1327*2905*2916*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2916),(2918,'Auditors*1327*2905*2916*2917*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2917),(2919,'Auditors*1327*2905*2916*2917*2918*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2918),(2920,'Auditors*1327*2905*2916*2917*2918*2919*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2919),(2921,'Auditors*1327*2905*2916*2917*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2917),(2922,'Auditors*1327*2905*','Snapshot',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2905),(2923,'Audit Captains*1328*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,1328),(2924,'Audit Captains*1328*2923*','Assessment',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2923),(2925,'Audit Captains*1328*2923*2924*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2924),(2926,'Audit Captains*1328*2923*2924*2925*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2925),(2927,'Audit Captains*1328*2923*2924*2925*2926*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2926),(2928,'Audit Captains*1328*2923*2924*2925*2926*2927*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2927),(2929,'Audit Captains*1328*2923*2924*2925*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2925),(2930,'Audit Captains*1328*2923*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2923),(2931,'Audit Captains*1328*2923*2930*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2930),(2932,'Audit Captains*1328*2923*2930*2931*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2931),(2933,'Audit Captains*1328*2923*','Snapshot',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2923),(2934,'Audit Captains*1328*2923*','Issue',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2923),(2935,'Audit Captains*1328*2923*2934*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2934),(2936,'Audit Captains*1328*2923*2934*2935*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2935),(2937,'Audit Captains*1328*2923*2934*2935*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2935),(2938,'Audit Captains*1328*2923*2934*2935*2937*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2937),(2939,'Audit Captains*1328*2923*2934*2935*2937*2938*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2938),(2940,'Audit Captains*1328*2923*','AssessmentTemplate',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2923),(2941,'Program Managers*1333*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,1333),(2942,'Program Managers*1333*2941*','Control',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2943,'Program Managers*1333*2941*2942*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2942),(2944,'Program Managers*1333*2941*2942*2943*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2943),(2945,'Program Managers*1333*2941*2942*2943*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2943),(2946,'Program Managers*1333*2941*2942*2943*2945*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2945),(2947,'Program Managers*1333*2941*2942*2943*2945*2946*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2946),(2948,'Program Managers*1333*2941*2942*2943*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2943),(2949,'Program Managers*1333*2941*','Risk',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2950,'Program Managers*1333*2941*2949*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2949),(2951,'Program Managers*1333*2941*2949*2950*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2950),(2952,'Program Managers*1333*2941*2949*2950*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2950),(2953,'Program Managers*1333*2941*2949*2950*2952*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2952),(2954,'Program Managers*1333*2941*2949*2950*2952*2953*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2953),(2955,'Program Managers*1333*2941*2949*2950*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2950),(2956,'Program Managers*1333*2941*','AccessGroup',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2957,'Program Managers*1333*2941*2956*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2956),(2958,'Program Managers*1333*2941*2956*2957*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2957),(2959,'Program Managers*1333*2941*2956*2957*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2957),(2960,'Program Managers*1333*2941*2956*2957*2959*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2959),(2961,'Program Managers*1333*2941*2956*2957*2959*2960*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2960),(2962,'Program Managers*1333*2941*','Clause',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2963,'Program Managers*1333*2941*2962*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2962),(2964,'Program Managers*1333*2941*2962*2963*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2963),(2965,'Program Managers*1333*2941*2962*2963*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2963),(2966,'Program Managers*1333*2941*2962*2963*2965*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2965),(2967,'Program Managers*1333*2941*2962*2963*2965*2966*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2966),(2968,'Program Managers*1333*2941*','Contract',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2969,'Program Managers*1333*2941*2968*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2968),(2970,'Program Managers*1333*2941*2968*2969*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2969),(2971,'Program Managers*1333*2941*2968*2969*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2969),(2972,'Program Managers*1333*2941*2968*2969*2971*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2971),(2973,'Program Managers*1333*2941*2968*2969*2971*2972*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2972),(2974,'Program Managers*1333*2941*','DataAsset',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2975,'Program Managers*1333*2941*2974*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2974),(2976,'Program Managers*1333*2941*2974*2975*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2975),(2977,'Program Managers*1333*2941*2974*2975*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2975),(2978,'Program Managers*1333*2941*2974*2975*2977*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2977),(2979,'Program Managers*1333*2941*2974*2975*2977*2978*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2978),(2980,'Program Managers*1333*2941*','Facility',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2981,'Program Managers*1333*2941*2980*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2980),(2982,'Program Managers*1333*2941*2980*2981*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2981),(2983,'Program Managers*1333*2941*2980*2981*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2981),(2984,'Program Managers*1333*2941*2980*2981*2983*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2983),(2985,'Program Managers*1333*2941*2980*2981*2983*2984*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2984),(2986,'Program Managers*1333*2941*','Issue',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2987,'Program Managers*1333*2941*2986*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2986),(2988,'Program Managers*1333*2941*2986*2987*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2987),(2989,'Program Managers*1333*2941*2986*2987*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2987),(2990,'Program Managers*1333*2941*2986*2987*2989*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2989),(2991,'Program Managers*1333*2941*2986*2987*2989*2990*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2990),(2992,'Program Managers*1333*2941*','Market',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2993,'Program Managers*1333*2941*2992*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2992),(2994,'Program Managers*1333*2941*2992*2993*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2993),(2995,'Program Managers*1333*2941*2992*2993*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2993),(2996,'Program Managers*1333*2941*2992*2993*2995*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2995),(2997,'Program Managers*1333*2941*2992*2993*2995*2996*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2996),(2998,'Program Managers*1333*2941*','Objective',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(2999,'Program Managers*1333*2941*2998*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2998),(3000,'Program Managers*1333*2941*2998*2999*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2999),(3001,'Program Managers*1333*2941*2998*2999*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2999),(3002,'Program Managers*1333*2941*2998*2999*3001*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3001),(3003,'Program Managers*1333*2941*2998*2999*3001*3002*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3002),(3004,'Program Managers*1333*2941*','OrgGroup',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3005,'Program Managers*1333*2941*3004*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3004),(3006,'Program Managers*1333*2941*3004*3005*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3005),(3007,'Program Managers*1333*2941*3004*3005*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3005),(3008,'Program Managers*1333*2941*3004*3005*3007*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3007),(3009,'Program Managers*1333*2941*3004*3005*3007*3008*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3008),(3010,'Program Managers*1333*2941*','Policy',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3011,'Program Managers*1333*2941*3010*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3010),(3012,'Program Managers*1333*2941*3010*3011*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3011),(3013,'Program Managers*1333*2941*3010*3011*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3011),(3014,'Program Managers*1333*2941*3010*3011*3013*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3013),(3015,'Program Managers*1333*2941*3010*3011*3013*3014*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3014),(3016,'Program Managers*1333*2941*','Process',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3017,'Program Managers*1333*2941*3016*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3016),(3018,'Program Managers*1333*2941*3016*3017*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3017),(3019,'Program Managers*1333*2941*3016*3017*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3017),(3020,'Program Managers*1333*2941*3016*3017*3019*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3019),(3021,'Program Managers*1333*2941*3016*3017*3019*3020*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3020),(3022,'Program Managers*1333*2941*','Product',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3023,'Program Managers*1333*2941*3022*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3022),(3024,'Program Managers*1333*2941*3022*3023*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3023),(3025,'Program Managers*1333*2941*3022*3023*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3023),(3026,'Program Managers*1333*2941*3022*3023*3025*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3025),(3027,'Program Managers*1333*2941*3022*3023*3025*3026*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3026),(3028,'Program Managers*1333*2941*','Project',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3029,'Program Managers*1333*2941*3028*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3028),(3030,'Program Managers*1333*2941*3028*3029*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3029),(3031,'Program Managers*1333*2941*3028*3029*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3029),(3032,'Program Managers*1333*2941*3028*3029*3031*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3031),(3033,'Program Managers*1333*2941*3028*3029*3031*3032*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3032),(3034,'Program Managers*1333*2941*','Regulation',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3035,'Program Managers*1333*2941*3034*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3034),(3036,'Program Managers*1333*2941*3034*3035*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3035),(3037,'Program Managers*1333*2941*3034*3035*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3035),(3038,'Program Managers*1333*2941*3034*3035*3037*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3037),(3039,'Program Managers*1333*2941*3034*3035*3037*3038*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3038),(3040,'Program Managers*1333*2941*','RiskAssessment',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3041,'Program Managers*1333*2941*3040*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3040),(3042,'Program Managers*1333*2941*3040*3041*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3041),(3043,'Program Managers*1333*2941*3040*3041*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3041),(3044,'Program Managers*1333*2941*3040*3041*3043*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3043),(3045,'Program Managers*1333*2941*3040*3041*3043*3044*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3044),(3046,'Program Managers*1333*2941*','Requirement',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3047,'Program Managers*1333*2941*3046*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3046),(3048,'Program Managers*1333*2941*3046*3047*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3047),(3049,'Program Managers*1333*2941*3046*3047*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3047),(3050,'Program Managers*1333*2941*3046*3047*3049*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3049),(3051,'Program Managers*1333*2941*3046*3047*3049*3050*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3050),(3052,'Program Managers*1333*2941*','Standard',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3053,'Program Managers*1333*2941*3052*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3052),(3054,'Program Managers*1333*2941*3052*3053*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3053),(3055,'Program Managers*1333*2941*3052*3053*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3053),(3056,'Program Managers*1333*2941*3052*3053*3055*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3055),(3057,'Program Managers*1333*2941*3052*3053*3055*3056*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3056),(3058,'Program Managers*1333*2941*','System',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3059,'Program Managers*1333*2941*3058*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3058),(3060,'Program Managers*1333*2941*3058*3059*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3059),(3061,'Program Managers*1333*2941*3058*3059*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3059),(3062,'Program Managers*1333*2941*3058*3059*3061*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3061),(3063,'Program Managers*1333*2941*3058*3059*3061*3062*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3062),(3064,'Program Managers*1333*2941*','Metric',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3065,'Program Managers*1333*2941*3064*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3064),(3066,'Program Managers*1333*2941*3064*3065*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3065),(3067,'Program Managers*1333*2941*3064*3065*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3065),(3068,'Program Managers*1333*2941*3064*3065*3067*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3067),(3069,'Program Managers*1333*2941*3064*3065*3067*3068*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3068),(3070,'Program Managers*1333*2941*','Threat',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3071,'Program Managers*1333*2941*3070*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3070),(3072,'Program Managers*1333*2941*3070*3071*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3071),(3073,'Program Managers*1333*2941*3070*3071*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3071),(3074,'Program Managers*1333*2941*3070*3071*3073*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3073),(3075,'Program Managers*1333*2941*3070*3071*3073*3074*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3074),(3076,'Program Managers*1333*2941*','Vendor',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3077,'Program Managers*1333*2941*3076*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3076),(3078,'Program Managers*1333*2941*3076*3077*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3077),(3079,'Program Managers*1333*2941*3076*3077*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3077),(3080,'Program Managers*1333*2941*3076*3077*3079*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3079),(3081,'Program Managers*1333*2941*3076*3077*3079*3080*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3080),(3082,'Program Managers*1333*2941*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3083,'Program Managers*1333*2941*','Audit',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3084,'Program Managers*1333*2941*3083*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3083),(3085,'Program Managers*1333*2941*3083*3084*','Assessment',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3084),(3086,'Program Managers*1333*2941*3083*3084*3085*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3085),(3087,'Program Managers*1333*2941*3083*3084*3085*3086*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3086),(3088,'Program Managers*1333*2941*3083*3084*3085*3086*3087*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3087),(3089,'Program Managers*1333*2941*3083*3084*3085*3086*3087*3088*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3088),(3090,'Program Managers*1333*2941*3083*3084*3085*3086*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3086),(3091,'Program Managers*1333*2941*3083*3084*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3084),(3092,'Program Managers*1333*2941*3083*3084*3091*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3091),(3093,'Program Managers*1333*2941*3083*3084*3091*3092*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3092),(3094,'Program Managers*1333*2941*3083*3084*','Snapshot',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3084),(3095,'Program Managers*1333*2941*3083*3084*','Issue',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3084),(3096,'Program Managers*1333*2941*3083*3084*3095*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3095),(3097,'Program Managers*1333*2941*3083*3084*3095*3096*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3096),(3098,'Program Managers*1333*2941*3083*3084*3095*3096*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3096),(3099,'Program Managers*1333*2941*3083*3084*3095*3096*3098*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3098),(3100,'Program Managers*1333*2941*3083*3084*3095*3096*3098*3099*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3099),(3101,'Program Managers*1333*2941*3083*3084*','AssessmentTemplate',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3084),(3102,'Program Managers*1333*2941*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3103,'Program Managers*1333*2941*3102*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3102),(3104,'Program Managers*1333*2941*3102*3103*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3103),(3105,'Program Editors*1334*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,1334),(3106,'Program Editors*1334*3105*','Control',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3107,'Program Editors*1334*3105*3106*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3106),(3108,'Program Editors*1334*3105*3106*3107*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3107),(3109,'Program Editors*1334*3105*3106*3107*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3107),(3110,'Program Editors*1334*3105*3106*3107*3109*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3109),(3111,'Program Editors*1334*3105*3106*3107*3109*3110*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3110),(3112,'Program Editors*1334*3105*3106*3107*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3107),(3113,'Program Editors*1334*3105*','Risk',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3114,'Program Editors*1334*3105*3113*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3113),(3115,'Program Editors*1334*3105*3113*3114*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3114),(3116,'Program Editors*1334*3105*3113*3114*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3114),(3117,'Program Editors*1334*3105*3113*3114*3116*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3116),(3118,'Program Editors*1334*3105*3113*3114*3116*3117*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3117),(3119,'Program Editors*1334*3105*3113*3114*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3114),(3120,'Program Editors*1334*3105*','AccessGroup',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3121,'Program Editors*1334*3105*3120*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3120),(3122,'Program Editors*1334*3105*3120*3121*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3121),(3123,'Program Editors*1334*3105*3120*3121*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3121),(3124,'Program Editors*1334*3105*3120*3121*3123*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3123),(3125,'Program Editors*1334*3105*3120*3121*3123*3124*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3124),(3126,'Program Editors*1334*3105*','Clause',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3127,'Program Editors*1334*3105*3126*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3126),(3128,'Program Editors*1334*3105*3126*3127*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3127),(3129,'Program Editors*1334*3105*3126*3127*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3127),(3130,'Program Editors*1334*3105*3126*3127*3129*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3129),(3131,'Program Editors*1334*3105*3126*3127*3129*3130*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3130),(3132,'Program Editors*1334*3105*','Contract',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3133,'Program Editors*1334*3105*3132*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3132),(3134,'Program Editors*1334*3105*3132*3133*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3133),(3135,'Program Editors*1334*3105*3132*3133*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3133),(3136,'Program Editors*1334*3105*3132*3133*3135*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3135),(3137,'Program Editors*1334*3105*3132*3133*3135*3136*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3136),(3138,'Program Editors*1334*3105*','DataAsset',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3139,'Program Editors*1334*3105*3138*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3138),(3140,'Program Editors*1334*3105*3138*3139*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3139),(3141,'Program Editors*1334*3105*3138*3139*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3139),(3142,'Program Editors*1334*3105*3138*3139*3141*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3141),(3143,'Program Editors*1334*3105*3138*3139*3141*3142*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3142),(3144,'Program Editors*1334*3105*','Facility',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3145,'Program Editors*1334*3105*3144*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3144),(3146,'Program Editors*1334*3105*3144*3145*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3145),(3147,'Program Editors*1334*3105*3144*3145*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3145),(3148,'Program Editors*1334*3105*3144*3145*3147*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3147),(3149,'Program Editors*1334*3105*3144*3145*3147*3148*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3148),(3150,'Program Editors*1334*3105*','Issue',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3151,'Program Editors*1334*3105*3150*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3150),(3152,'Program Editors*1334*3105*3150*3151*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3151),(3153,'Program Editors*1334*3105*3150*3151*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3151),(3154,'Program Editors*1334*3105*3150*3151*3153*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3153),(3155,'Program Editors*1334*3105*3150*3151*3153*3154*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3154),(3156,'Program Editors*1334*3105*','Market',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3157,'Program Editors*1334*3105*3156*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3156),(3158,'Program Editors*1334*3105*3156*3157*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3157),(3159,'Program Editors*1334*3105*3156*3157*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3157),(3160,'Program Editors*1334*3105*3156*3157*3159*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3159),(3161,'Program Editors*1334*3105*3156*3157*3159*3160*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3160),(3162,'Program Editors*1334*3105*','Objective',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3163,'Program Editors*1334*3105*3162*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3162),(3164,'Program Editors*1334*3105*3162*3163*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3163),(3165,'Program Editors*1334*3105*3162*3163*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3163),(3166,'Program Editors*1334*3105*3162*3163*3165*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3165),(3167,'Program Editors*1334*3105*3162*3163*3165*3166*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3166),(3168,'Program Editors*1334*3105*','OrgGroup',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3169,'Program Editors*1334*3105*3168*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3168),(3170,'Program Editors*1334*3105*3168*3169*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3169),(3171,'Program Editors*1334*3105*3168*3169*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3169),(3172,'Program Editors*1334*3105*3168*3169*3171*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3171),(3173,'Program Editors*1334*3105*3168*3169*3171*3172*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3172),(3174,'Program Editors*1334*3105*','Policy',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3175,'Program Editors*1334*3105*3174*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3174),(3176,'Program Editors*1334*3105*3174*3175*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3175),(3177,'Program Editors*1334*3105*3174*3175*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3175),(3178,'Program Editors*1334*3105*3174*3175*3177*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3177),(3179,'Program Editors*1334*3105*3174*3175*3177*3178*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3178),(3180,'Program Editors*1334*3105*','Process',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3181,'Program Editors*1334*3105*3180*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3180),(3182,'Program Editors*1334*3105*3180*3181*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3181),(3183,'Program Editors*1334*3105*3180*3181*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3181),(3184,'Program Editors*1334*3105*3180*3181*3183*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3183),(3185,'Program Editors*1334*3105*3180*3181*3183*3184*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3184),(3186,'Program Editors*1334*3105*','Product',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3187,'Program Editors*1334*3105*3186*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3186),(3188,'Program Editors*1334*3105*3186*3187*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3187),(3189,'Program Editors*1334*3105*3186*3187*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3187),(3190,'Program Editors*1334*3105*3186*3187*3189*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3189),(3191,'Program Editors*1334*3105*3186*3187*3189*3190*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3190),(3192,'Program Editors*1334*3105*','Project',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3193,'Program Editors*1334*3105*3192*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3192),(3194,'Program Editors*1334*3105*3192*3193*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3193),(3195,'Program Editors*1334*3105*3192*3193*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3193),(3196,'Program Editors*1334*3105*3192*3193*3195*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3195),(3197,'Program Editors*1334*3105*3192*3193*3195*3196*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3196),(3198,'Program Editors*1334*3105*','Regulation',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3199,'Program Editors*1334*3105*3198*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3198),(3200,'Program Editors*1334*3105*3198*3199*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3199),(3201,'Program Editors*1334*3105*3198*3199*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3199),(3202,'Program Editors*1334*3105*3198*3199*3201*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3201),(3203,'Program Editors*1334*3105*3198*3199*3201*3202*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3202),(3204,'Program Editors*1334*3105*','RiskAssessment',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3205,'Program Editors*1334*3105*3204*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3204),(3206,'Program Editors*1334*3105*3204*3205*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3205),(3207,'Program Editors*1334*3105*3204*3205*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3205),(3208,'Program Editors*1334*3105*3204*3205*3207*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3207),(3209,'Program Editors*1334*3105*3204*3205*3207*3208*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3208),(3210,'Program Editors*1334*3105*','Requirement',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3211,'Program Editors*1334*3105*3210*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3210),(3212,'Program Editors*1334*3105*3210*3211*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3211),(3213,'Program Editors*1334*3105*3210*3211*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3211),(3214,'Program Editors*1334*3105*3210*3211*3213*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3213),(3215,'Program Editors*1334*3105*3210*3211*3213*3214*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3214),(3216,'Program Editors*1334*3105*','Standard',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3217,'Program Editors*1334*3105*3216*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3216),(3218,'Program Editors*1334*3105*3216*3217*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3217),(3219,'Program Editors*1334*3105*3216*3217*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3217),(3220,'Program Editors*1334*3105*3216*3217*3219*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3219),(3221,'Program Editors*1334*3105*3216*3217*3219*3220*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3220),(3222,'Program Editors*1334*3105*','System',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3223,'Program Editors*1334*3105*3222*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3222),(3224,'Program Editors*1334*3105*3222*3223*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3223),(3225,'Program Editors*1334*3105*3222*3223*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3223),(3226,'Program Editors*1334*3105*3222*3223*3225*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3225),(3227,'Program Editors*1334*3105*3222*3223*3225*3226*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3226),(3228,'Program Editors*1334*3105*','Metric',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3229,'Program Editors*1334*3105*3228*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3228),(3230,'Program Editors*1334*3105*3228*3229*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3229),(3231,'Program Editors*1334*3105*3228*3229*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3229),(3232,'Program Editors*1334*3105*3228*3229*3231*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3231),(3233,'Program Editors*1334*3105*3228*3229*3231*3232*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3232),(3234,'Program Editors*1334*3105*','Threat',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3235,'Program Editors*1334*3105*3234*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3234),(3236,'Program Editors*1334*3105*3234*3235*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3235),(3237,'Program Editors*1334*3105*3234*3235*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3235),(3238,'Program Editors*1334*3105*3234*3235*3237*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3237),(3239,'Program Editors*1334*3105*3234*3235*3237*3238*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3238),(3240,'Program Editors*1334*3105*','Vendor',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3241,'Program Editors*1334*3105*3240*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3240),(3242,'Program Editors*1334*3105*3240*3241*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3241),(3243,'Program Editors*1334*3105*3240*3241*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3241),(3244,'Program Editors*1334*3105*3240*3241*3243*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3243),(3245,'Program Editors*1334*3105*3240*3241*3243*3244*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3244),(3246,'Program Editors*1334*3105*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3247,'Program Editors*1334*3105*','Audit',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3248,'Program Editors*1334*3105*3247*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3247),(3249,'Program Editors*1334*3105*3247*3248*','Issue',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3248),(3250,'Program Editors*1334*3105*3247*3248*3249*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3249),(3251,'Program Editors*1334*3105*3247*3248*3249*3250*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3250),(3252,'Program Editors*1334*3105*3247*3248*3249*3250*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3250),(3253,'Program Editors*1334*3105*3247*3248*3249*3250*3252*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3252),(3254,'Program Editors*1334*3105*3247*3248*3249*3250*3252*3253*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3253),(3255,'Program Editors*1334*3105*3247*3248*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3248),(3256,'Program Editors*1334*3105*3247*3248*3255*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3255),(3257,'Program Editors*1334*3105*3247*3248*3255*3256*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3256),(3258,'Program Editors*1334*3105*3247*3248*','Snapshot',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3248),(3259,'Program Editors*1334*3105*3247*3248*','Assessment',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3248),(3260,'Program Editors*1334*3105*3247*3248*3259*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3259),(3261,'Program Editors*1334*3105*3247*3248*3259*3260*','Evidence',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3260),(3262,'Program Editors*1334*3105*3247*3248*3259*3260*3261*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3261),(3263,'Program Editors*1334*3105*3247*3248*3259*3260*3261*3262*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3262),(3264,'Program Editors*1334*3105*3247*3248*3259*3260*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3260),(3265,'Program Editors*1334*3105*3247*3248*','AssessmentTemplate',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3248),(3266,'Program Editors*1334*3105*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3267,'Program Editors*1334*3105*3266*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3266),(3268,'Program Editors*1334*3105*3266*3267*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3267),(3269,'Program Readers*1335*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,1335),(3270,'Program Readers*1335*3269*','Audit',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3271,'Program Readers*1335*3269*3270*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3270),(3272,'Program Readers*1335*3269*3270*3271*','Assessment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3271),(3273,'Program Readers*1335*3269*3270*3271*3272*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3272),(3274,'Program Readers*1335*3269*3270*3271*3272*3273*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3273),(3275,'Program Readers*1335*3269*3270*3271*3272*3273*','Evidence',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3273),(3276,'Program Readers*1335*3269*3270*3271*3272*3273*3275*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3275),(3277,'Program Readers*1335*3269*3270*3271*3272*3273*3275*3276*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3276),(3278,'Program Readers*1335*3269*3270*3271*','Snapshot',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3271),(3279,'Program Readers*1335*3269*3270*3271*','AssessmentTemplate',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3271),(3280,'Program Readers*1335*3269*3270*3271*','Issue',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3271),(3281,'Program Readers*1335*3269*3270*3271*3280*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3280),(3282,'Program Readers*1335*3269*3270*3271*3280*3281*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3281),(3283,'Program Readers*1335*3269*3270*3271*3280*3281*3282*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3282),(3284,'Program Readers*1335*3269*3270*3271*3280*3281*3282*3283*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3283),(3285,'Program Readers*1335*3269*3270*3271*3280*3281*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3281),(3286,'Program Readers*1335*3269*3270*3271*','Evidence',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3271),(3287,'Program Readers*1335*3269*3270*3271*3286*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3286),(3288,'Program Readers*1335*3269*3270*3271*3286*3287*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3287),(3289,'Program Readers*1335*3269*','Control',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3290,'Program Readers*1335*3269*3289*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3289),(3291,'Program Readers*1335*3269*3289*3290*','Proposal',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3290),(3292,'Program Readers*1335*3269*3289*3290*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3290),(3293,'Program Readers*1335*3269*3289*3290*3292*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3292),(3294,'Program Readers*1335*3269*3289*3290*3292*3293*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3293),(3295,'Program Readers*1335*3269*3289*3290*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3290),(3296,'Program Readers*1335*3269*','Risk',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3297,'Program Readers*1335*3269*3296*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3296),(3298,'Program Readers*1335*3269*3296*3297*','Proposal',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3297),(3299,'Program Readers*1335*3269*3296*3297*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3297),(3300,'Program Readers*1335*3269*3296*3297*3299*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3299),(3301,'Program Readers*1335*3269*3296*3297*3299*3300*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3300),(3302,'Program Readers*1335*3269*3296*3297*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3297),(3303,'Program Readers*1335*3269*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3304,'Program Readers*1335*3269*3303*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3303),(3305,'Program Readers*1335*3269*3303*3304*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3304),(3306,'Program Readers*1335*3269*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3307,'Program Readers*1335*3269*','AccessGroup',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3308,'Program Readers*1335*3269*3307*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3307),(3309,'Program Readers*1335*3269*3307*3308*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3308),(3310,'Program Readers*1335*3269*3307*3308*3309*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3309),(3311,'Program Readers*1335*3269*3307*3308*3309*3310*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3310),(3312,'Program Readers*1335*3269*3307*3308*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3308),(3313,'Program Readers*1335*3269*','Clause',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3314,'Program Readers*1335*3269*3313*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3313),(3315,'Program Readers*1335*3269*3313*3314*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3314),(3316,'Program Readers*1335*3269*3313*3314*3315*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3315),(3317,'Program Readers*1335*3269*3313*3314*3315*3316*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3316),(3318,'Program Readers*1335*3269*3313*3314*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3314),(3319,'Program Readers*1335*3269*','Contract',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3320,'Program Readers*1335*3269*3319*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3319),(3321,'Program Readers*1335*3269*3319*3320*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3320),(3322,'Program Readers*1335*3269*3319*3320*3321*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3321),(3323,'Program Readers*1335*3269*3319*3320*3321*3322*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3322),(3324,'Program Readers*1335*3269*3319*3320*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3320),(3325,'Program Readers*1335*3269*','DataAsset',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3326,'Program Readers*1335*3269*3325*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3325),(3327,'Program Readers*1335*3269*3325*3326*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3326),(3328,'Program Readers*1335*3269*3325*3326*3327*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3327),(3329,'Program Readers*1335*3269*3325*3326*3327*3328*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3328),(3330,'Program Readers*1335*3269*3325*3326*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3326),(3331,'Program Readers*1335*3269*','Facility',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3332,'Program Readers*1335*3269*3331*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3331),(3333,'Program Readers*1335*3269*3331*3332*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3332),(3334,'Program Readers*1335*3269*3331*3332*3333*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3333),(3335,'Program Readers*1335*3269*3331*3332*3333*3334*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3334),(3336,'Program Readers*1335*3269*3331*3332*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3332),(3337,'Program Readers*1335*3269*','Issue',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3338,'Program Readers*1335*3269*3337*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3337),(3339,'Program Readers*1335*3269*3337*3338*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3338),(3340,'Program Readers*1335*3269*3337*3338*3339*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3339),(3341,'Program Readers*1335*3269*3337*3338*3339*3340*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3340),(3342,'Program Readers*1335*3269*3337*3338*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3338),(3343,'Program Readers*1335*3269*','Market',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3344,'Program Readers*1335*3269*3343*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3343),(3345,'Program Readers*1335*3269*3343*3344*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3344),(3346,'Program Readers*1335*3269*3343*3344*3345*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3345),(3347,'Program Readers*1335*3269*3343*3344*3345*3346*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3346),(3348,'Program Readers*1335*3269*3343*3344*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3344),(3349,'Program Readers*1335*3269*','Objective',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3350,'Program Readers*1335*3269*3349*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3349),(3351,'Program Readers*1335*3269*3349*3350*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3350),(3352,'Program Readers*1335*3269*3349*3350*3351*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3351),(3353,'Program Readers*1335*3269*3349*3350*3351*3352*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3352),(3354,'Program Readers*1335*3269*3349*3350*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3350),(3355,'Program Readers*1335*3269*','OrgGroup',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3356,'Program Readers*1335*3269*3355*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3355),(3357,'Program Readers*1335*3269*3355*3356*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3356),(3358,'Program Readers*1335*3269*3355*3356*3357*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3357),(3359,'Program Readers*1335*3269*3355*3356*3357*3358*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3358),(3360,'Program Readers*1335*3269*3355*3356*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3356),(3361,'Program Readers*1335*3269*','Policy',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3362,'Program Readers*1335*3269*3361*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3361),(3363,'Program Readers*1335*3269*3361*3362*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3362),(3364,'Program Readers*1335*3269*3361*3362*3363*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3363),(3365,'Program Readers*1335*3269*3361*3362*3363*3364*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3364),(3366,'Program Readers*1335*3269*3361*3362*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3362),(3367,'Program Readers*1335*3269*','Process',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3368,'Program Readers*1335*3269*3367*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3367),(3369,'Program Readers*1335*3269*3367*3368*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3368),(3370,'Program Readers*1335*3269*3367*3368*3369*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3369),(3371,'Program Readers*1335*3269*3367*3368*3369*3370*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3370),(3372,'Program Readers*1335*3269*3367*3368*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3368),(3373,'Program Readers*1335*3269*','Product',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3374,'Program Readers*1335*3269*3373*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3373),(3375,'Program Readers*1335*3269*3373*3374*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3374),(3376,'Program Readers*1335*3269*3373*3374*3375*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3375),(3377,'Program Readers*1335*3269*3373*3374*3375*3376*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3376),(3378,'Program Readers*1335*3269*3373*3374*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3374),(3379,'Program Readers*1335*3269*','Project',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3380,'Program Readers*1335*3269*3379*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3379),(3381,'Program Readers*1335*3269*3379*3380*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3380),(3382,'Program Readers*1335*3269*3379*3380*3381*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3381),(3383,'Program Readers*1335*3269*3379*3380*3381*3382*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3382),(3384,'Program Readers*1335*3269*3379*3380*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3380),(3385,'Program Readers*1335*3269*','Regulation',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3386,'Program Readers*1335*3269*3385*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3385),(3387,'Program Readers*1335*3269*3385*3386*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3386),(3388,'Program Readers*1335*3269*3385*3386*3387*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3387),(3389,'Program Readers*1335*3269*3385*3386*3387*3388*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3388),(3390,'Program Readers*1335*3269*3385*3386*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3386),(3391,'Program Readers*1335*3269*','RiskAssessment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3392,'Program Readers*1335*3269*3391*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3391),(3393,'Program Readers*1335*3269*3391*3392*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3392),(3394,'Program Readers*1335*3269*3391*3392*3393*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3393),(3395,'Program Readers*1335*3269*3391*3392*3393*3394*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3394),(3396,'Program Readers*1335*3269*3391*3392*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3392),(3397,'Program Readers*1335*3269*','Requirement',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3398,'Program Readers*1335*3269*3397*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3397),(3399,'Program Readers*1335*3269*3397*3398*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3398),(3400,'Program Readers*1335*3269*3397*3398*3399*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3399),(3401,'Program Readers*1335*3269*3397*3398*3399*3400*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3400),(3402,'Program Readers*1335*3269*3397*3398*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3398),(3403,'Program Readers*1335*3269*','Standard',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3404,'Program Readers*1335*3269*3403*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3403),(3405,'Program Readers*1335*3269*3403*3404*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3404),(3406,'Program Readers*1335*3269*3403*3404*3405*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3405),(3407,'Program Readers*1335*3269*3403*3404*3405*3406*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3406),(3408,'Program Readers*1335*3269*3403*3404*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3404),(3409,'Program Readers*1335*3269*','System',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3410,'Program Readers*1335*3269*3409*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3409),(3411,'Program Readers*1335*3269*3409*3410*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3410),(3412,'Program Readers*1335*3269*3409*3410*3411*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3411),(3413,'Program Readers*1335*3269*3409*3410*3411*3412*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3412),(3414,'Program Readers*1335*3269*3409*3410*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3410),(3415,'Program Readers*1335*3269*','Metric',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3416,'Program Readers*1335*3269*3415*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3415),(3417,'Program Readers*1335*3269*3415*3416*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3416),(3418,'Program Readers*1335*3269*3415*3416*3417*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3417),(3419,'Program Readers*1335*3269*3415*3416*3417*3418*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3418),(3420,'Program Readers*1335*3269*3415*3416*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3416),(3421,'Program Readers*1335*3269*','Threat',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3422,'Program Readers*1335*3269*3421*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3421),(3423,'Program Readers*1335*3269*3421*3422*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3422),(3424,'Program Readers*1335*3269*3421*3422*3423*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3423),(3425,'Program Readers*1335*3269*3421*3422*3423*3424*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3424),(3426,'Program Readers*1335*3269*3421*3422*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3422),(3427,'Program Readers*1335*3269*','Vendor',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3428,'Program Readers*1335*3269*3427*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3427),(3429,'Program Readers*1335*3269*3427*3428*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3428),(3430,'Program Readers*1335*3269*3427*3428*3429*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3429),(3431,'Program Readers*1335*3269*3427*3428*3429*3430*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3430),(3432,'Program Readers*1335*3269*3427*3428*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3428),(3433,'Secondary Contacts*34*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,34),(3434,'Secondary Contacts*34*3433*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3433),(3435,'Secondary Contacts*34*3433*3434*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3434),(3436,'Secondary Contacts*34*3433*3434*3435*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3435),(3437,'Secondary Contacts*34*3433*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3433),(3438,'Primary Contacts*33*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,33),(3439,'Primary Contacts*33*3438*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3438),(3440,'Primary Contacts*33*3438*3439*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3439),(3441,'Primary Contacts*33*3438*3439*3440*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3440),(3442,'Primary Contacts*33*3438*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3438),(3443,'Program Managers*1333*2941*','TechnologyEnvironment',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3444,'Program Managers*1333*2941*3443*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3443),(3445,'Program Managers*1333*2941*3443*3444*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3444),(3446,'Program Managers*1333*2941*3443*3444*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3444),(3447,'Program Managers*1333*2941*3443*3444*3446*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3446),(3448,'Program Managers*1333*2941*3443*3444*3446*3447*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3447),(3449,'Program Editors*1334*3105*','TechnologyEnvironment',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3450,'Program Editors*1334*3105*3449*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3449),(3451,'Program Editors*1334*3105*3449*3450*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3450),(3452,'Program Editors*1334*3105*3449*3450*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3450),(3453,'Program Editors*1334*3105*3449*3450*3452*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3452),(3454,'Program Editors*1334*3105*3449*3450*3452*3453*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3453),(3455,'Program Readers*1335*3269*','TechnologyEnvironment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3456,'Program Readers*1335*3269*3455*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3455),(3457,'Program Readers*1335*3269*3455*3456*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3456),(3458,'Program Readers*1335*3269*3455*3456*3457*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3457),(3459,'Program Readers*1335*3269*3455*3456*3457*3458*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3458),(3460,'Program Readers*1335*3269*3455*3456*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3456),(3461,'Program Managers*1333*2941*','ProductGroup',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,2941),(3462,'Program Managers*1333*2941*3461*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3461),(3463,'Program Managers*1333*2941*3461*3462*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3462),(3464,'Program Managers*1333*2941*3461*3462*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3462),(3465,'Program Managers*1333*2941*3461*3462*3464*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3464),(3466,'Program Managers*1333*2941*3461*3462*3464*3465*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3465),(3467,'Program Editors*1334*3105*','ProductGroup',NULL,1,1,1,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3105),(3468,'Program Editors*1334*3105*3467*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3467),(3469,'Program Editors*1334*3105*3467*3468*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3468),(3470,'Program Editors*1334*3105*3467*3468*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3468),(3471,'Program Editors*1334*3105*3467*3468*3470*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3470),(3472,'Program Editors*1334*3105*3467*3468*3470*3471*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3471),(3473,'Program Readers*1335*3269*','ProductGroup',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3269),(3474,'Program Readers*1335*3269*3473*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3473),(3475,'Program Readers*1335*3269*3473*3474*','Document',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3474),(3476,'Program Readers*1335*3269*3473*3474*3475*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3475),(3477,'Program Readers*1335*3269*3473*3474*3475*3476*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3476),(3478,'Program Readers*1335*3269*3473*3474*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3474),(3479,'Product Managers','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3480,'Technical Leads','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3481,'Technical / Program Managers','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3482,'Legal Counsels','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3483,'System Owners','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3484,'Product Managers','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3485,'Technical Leads','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3486,'Technical / Program Managers','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3487,'Legal Counsels','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3488,'System Owners','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3489,'Product Managers','Facility',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3490,'Technical Leads','Facility',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3491,'Technical / Program Managers','Facility',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3492,'Legal Counsels','Facility',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3493,'System Owners','Facility',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3494,'Product Managers','Market',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3495,'Technical Leads','Market',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3496,'Technical / Program Managers','Market',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3497,'Legal Counsels','Market',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3498,'System Owners','Market',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3499,'Product Managers','Metric',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3500,'Technical Leads','Metric',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3501,'Technical / Program Managers','Metric',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3502,'Legal Counsels','Metric',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3503,'System Owners','Metric',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3504,'Product Managers','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3505,'Technical Leads','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3506,'Technical / Program Managers','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3507,'Legal Counsels','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3508,'System Owners','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3509,'Product Managers','Process',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3510,'Technical Leads','Process',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3511,'Technical / Program Managers','Process',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3512,'Legal Counsels','Process',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3513,'System Owners','Process',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3514,'Product Managers','Product',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3515,'Technical Leads','Product',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3516,'Technical / Program Managers','Product',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3517,'Legal Counsels','Product',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3518,'System Owners','Product',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3519,'Product Managers','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3520,'Technical Leads','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3521,'Technical / Program Managers','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3522,'Legal Counsels','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3523,'System Owners','ProductGroup',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3524,'Product Managers','Project',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3525,'Technical Leads','Project',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3526,'Technical / Program Managers','Project',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3527,'Legal Counsels','Project',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3528,'System Owners','Project',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3529,'Product Managers','System',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3530,'Technical Leads','System',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3531,'Technical / Program Managers','System',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3532,'Legal Counsels','System',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3533,'System Owners','System',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3534,'Product Managers','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3535,'Technical Leads','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3536,'Technical / Program Managers','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3537,'Legal Counsels','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3538,'System Owners','TechnologyEnvironment',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3539,'Product Managers','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3540,'Technical Leads','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3541,'Technical / Program Managers','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3542,'Legal Counsels','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3543,'System Owners','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:21',1,'2018-08-24 09:33:21',NULL,0,0,1,0,0,NULL),(3544,'Technical / Program Managers*3536*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3536),(3545,'Technical / Program Managers*3536*3544*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3544),(3546,'Technical / Program Managers*3536*3544*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3544),(3547,'Technical / Program Managers*3536*3544*3546*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3546),(3548,'Technical / Program Managers*3536*3544*3546*3547*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3547),(3549,'Technical Leads*3535*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3535),(3550,'Technical Leads*3535*3549*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3549),(3551,'Technical Leads*3535*3549*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3549),(3552,'Technical Leads*3535*3549*3551*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3551),(3553,'Technical Leads*3535*3549*3551*3552*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3552),(3554,'System Owners*3538*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3538),(3555,'System Owners*3538*3554*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3554),(3556,'System Owners*3538*3554*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3554),(3557,'System Owners*3538*3554*3556*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3556),(3558,'System Owners*3538*3554*3556*3557*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3557),(3559,'Product Managers*3534*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3534),(3560,'Product Managers*3534*3559*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3559),(3561,'Product Managers*3534*3559*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3559),(3562,'Product Managers*3534*3559*3561*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3561),(3563,'Product Managers*3534*3559*3561*3562*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3562),(3564,'Legal Counsels*3537*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3537),(3565,'Legal Counsels*3537*3564*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3564),(3566,'Legal Counsels*3537*3564*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3564),(3567,'Legal Counsels*3537*3564*3566*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3566),(3568,'Legal Counsels*3537*3564*3566*3567*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3567),(3569,'Technical / Program Managers*3506*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3506),(3570,'Technical / Program Managers*3506*3569*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3569),(3571,'Technical / Program Managers*3506*3569*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3569),(3572,'Technical / Program Managers*3506*3569*3571*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3571),(3573,'Technical / Program Managers*3506*3569*3571*3572*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3572),(3574,'Technical Leads*3505*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3505),(3575,'Technical Leads*3505*3574*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3574),(3576,'Technical Leads*3505*3574*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3574),(3577,'Technical Leads*3505*3574*3576*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3576),(3578,'Technical Leads*3505*3574*3576*3577*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3577),(3579,'System Owners*3508*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3508),(3580,'System Owners*3508*3579*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3579),(3581,'System Owners*3508*3579*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3579),(3582,'System Owners*3508*3579*3581*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3581),(3583,'System Owners*3508*3579*3581*3582*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3582),(3584,'Product Managers*3504*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3504),(3585,'Product Managers*3504*3584*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3584),(3586,'Product Managers*3504*3584*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3584),(3587,'Product Managers*3504*3584*3586*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3586),(3588,'Product Managers*3504*3584*3586*3587*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3587),(3589,'Legal Counsels*3507*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3507),(3590,'Legal Counsels*3507*3589*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3589),(3591,'Legal Counsels*3507*3589*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3589),(3592,'Legal Counsels*3507*3589*3591*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3591),(3593,'Legal Counsels*3507*3589*3591*3592*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3592),(3594,'Technical / Program Managers*3481*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3481),(3595,'Technical / Program Managers*3481*3594*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3594),(3596,'Technical / Program Managers*3481*3594*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3594),(3597,'Technical / Program Managers*3481*3594*3596*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3596),(3598,'Technical / Program Managers*3481*3594*3596*3597*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3597),(3599,'Technical Leads*3480*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3480),(3600,'Technical Leads*3480*3599*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3599),(3601,'Technical Leads*3480*3599*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3599),(3602,'Technical Leads*3480*3599*3601*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3601),(3603,'Technical Leads*3480*3599*3601*3602*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3602),(3604,'System Owners*3483*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3483),(3605,'System Owners*3483*3604*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3604),(3606,'System Owners*3483*3604*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3604),(3607,'System Owners*3483*3604*3606*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3606),(3608,'System Owners*3483*3604*3606*3607*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3607),(3609,'Product Managers*3479*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3479),(3610,'Product Managers*3479*3609*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3609),(3611,'Product Managers*3479*3609*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3609),(3612,'Product Managers*3479*3609*3611*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3611),(3613,'Product Managers*3479*3609*3611*3612*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3612),(3614,'Legal Counsels*3482*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3482),(3615,'Legal Counsels*3482*3614*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3614),(3616,'Legal Counsels*3482*3614*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3614),(3617,'Legal Counsels*3482*3614*3616*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3616),(3618,'Legal Counsels*3482*3614*3616*3617*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3617),(3619,'Technical / Program Managers*3531*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3531),(3620,'Technical / Program Managers*3531*3619*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3619),(3621,'Technical / Program Managers*3531*3619*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3619),(3622,'Technical / Program Managers*3531*3619*3621*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3621),(3623,'Technical / Program Managers*3531*3619*3621*3622*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3622),(3624,'Technical Leads*3530*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3530),(3625,'Technical Leads*3530*3624*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3624),(3626,'Technical Leads*3530*3624*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3624),(3627,'Technical Leads*3530*3624*3626*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3626),(3628,'Technical Leads*3530*3624*3626*3627*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3627),(3629,'System Owners*3533*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3533),(3630,'System Owners*3533*3629*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3629),(3631,'System Owners*3533*3629*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3629),(3632,'System Owners*3533*3629*3631*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3631),(3633,'System Owners*3533*3629*3631*3632*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3632),(3634,'Product Managers*3529*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3529),(3635,'Product Managers*3529*3634*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3634),(3636,'Product Managers*3529*3634*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3634),(3637,'Product Managers*3529*3634*3636*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3636),(3638,'Product Managers*3529*3634*3636*3637*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3637),(3639,'Legal Counsels*3532*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3532),(3640,'Legal Counsels*3532*3639*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3639),(3641,'Legal Counsels*3532*3639*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3639),(3642,'Legal Counsels*3532*3639*3641*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3641),(3643,'Legal Counsels*3532*3639*3641*3642*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3642),(3644,'Technical / Program Managers*3521*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3521),(3645,'Technical / Program Managers*3521*3644*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3644),(3646,'Technical / Program Managers*3521*3644*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3644),(3647,'Technical / Program Managers*3521*3644*3646*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3646),(3648,'Technical / Program Managers*3521*3644*3646*3647*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3647),(3649,'Technical Leads*3520*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3520),(3650,'Technical Leads*3520*3649*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3649),(3651,'Technical Leads*3520*3649*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3649),(3652,'Technical Leads*3520*3649*3651*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3651),(3653,'Technical Leads*3520*3649*3651*3652*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3652),(3654,'System Owners*3523*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3523),(3655,'System Owners*3523*3654*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3654),(3656,'System Owners*3523*3654*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3654),(3657,'System Owners*3523*3654*3656*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3656),(3658,'System Owners*3523*3654*3656*3657*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3657),(3659,'Product Managers*3519*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3519),(3660,'Product Managers*3519*3659*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3659),(3661,'Product Managers*3519*3659*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3659),(3662,'Product Managers*3519*3659*3661*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3661),(3663,'Product Managers*3519*3659*3661*3662*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3662),(3664,'Legal Counsels*3522*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3522),(3665,'Legal Counsels*3522*3664*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3664),(3666,'Legal Counsels*3522*3664*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3664),(3667,'Legal Counsels*3522*3664*3666*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3666),(3668,'Legal Counsels*3522*3664*3666*3667*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3667),(3669,'Technical / Program Managers*3526*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3526),(3670,'Technical / Program Managers*3526*3669*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3669),(3671,'Technical / Program Managers*3526*3669*','Document',NULL,1,1,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3669),(3672,'Technical / Program Managers*3526*3669*3671*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3671),(3673,'Technical / Program Managers*3526*3669*3671*3672*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:21',NULL,'2018-08-24 09:33:21',NULL,0,0,1,1,0,3672),(3674,'Technical Leads*3525*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3525),(3675,'Technical Leads*3525*3674*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3674),(3676,'Technical Leads*3525*3674*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3674),(3677,'Technical Leads*3525*3674*3676*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3676),(3678,'Technical Leads*3525*3674*3676*3677*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3677),(3679,'System Owners*3528*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3528),(3680,'System Owners*3528*3679*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3679),(3681,'System Owners*3528*3679*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3679),(3682,'System Owners*3528*3679*3681*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3681),(3683,'System Owners*3528*3679*3681*3682*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3682),(3684,'Product Managers*3524*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3524),(3685,'Product Managers*3524*3684*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3684),(3686,'Product Managers*3524*3684*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3684),(3687,'Product Managers*3524*3684*3686*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3686),(3688,'Product Managers*3524*3684*3686*3687*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3687),(3689,'Legal Counsels*3527*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3527),(3690,'Legal Counsels*3527*3689*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3689),(3691,'Legal Counsels*3527*3689*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3689),(3692,'Legal Counsels*3527*3689*3691*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3691),(3693,'Legal Counsels*3527*3689*3691*3692*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3692),(3694,'Technical / Program Managers*3486*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3486),(3695,'Technical / Program Managers*3486*3694*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3694),(3696,'Technical / Program Managers*3486*3694*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3694),(3697,'Technical / Program Managers*3486*3694*3696*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3696),(3698,'Technical / Program Managers*3486*3694*3696*3697*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3697),(3699,'Technical Leads*3485*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3485),(3700,'Technical Leads*3485*3699*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3699),(3701,'Technical Leads*3485*3699*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3699),(3702,'Technical Leads*3485*3699*3701*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3701),(3703,'Technical Leads*3485*3699*3701*3702*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3702),(3704,'System Owners*3488*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3488),(3705,'System Owners*3488*3704*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3704),(3706,'System Owners*3488*3704*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3704),(3707,'System Owners*3488*3704*3706*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3706),(3708,'System Owners*3488*3704*3706*3707*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3707),(3709,'Product Managers*3484*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3484),(3710,'Product Managers*3484*3709*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3709),(3711,'Product Managers*3484*3709*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3709),(3712,'Product Managers*3484*3709*3711*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3711),(3713,'Product Managers*3484*3709*3711*3712*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3712),(3714,'Legal Counsels*3487*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3487),(3715,'Legal Counsels*3487*3714*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3714),(3716,'Legal Counsels*3487*3714*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3714),(3717,'Legal Counsels*3487*3714*3716*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3716),(3718,'Legal Counsels*3487*3714*3716*3717*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3717),(3719,'Technical / Program Managers*3516*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3516),(3720,'Technical / Program Managers*3516*3719*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3719),(3721,'Technical / Program Managers*3516*3719*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3719),(3722,'Technical / Program Managers*3516*3719*3721*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3721),(3723,'Technical / Program Managers*3516*3719*3721*3722*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3722),(3724,'Technical Leads*3515*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3515),(3725,'Technical Leads*3515*3724*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3724),(3726,'Technical Leads*3515*3724*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3724),(3727,'Technical Leads*3515*3724*3726*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3726),(3728,'Technical Leads*3515*3724*3726*3727*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3727),(3729,'System Owners*3518*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3518),(3730,'System Owners*3518*3729*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3729),(3731,'System Owners*3518*3729*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3729),(3732,'System Owners*3518*3729*3731*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3731),(3733,'System Owners*3518*3729*3731*3732*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3732),(3734,'Product Managers*3514*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3514),(3735,'Product Managers*3514*3734*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3734),(3736,'Product Managers*3514*3734*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3734),(3737,'Product Managers*3514*3734*3736*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3736),(3738,'Product Managers*3514*3734*3736*3737*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3737),(3739,'Legal Counsels*3517*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3517),(3740,'Legal Counsels*3517*3739*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3739),(3741,'Legal Counsels*3517*3739*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3739),(3742,'Legal Counsels*3517*3739*3741*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3741),(3743,'Legal Counsels*3517*3739*3741*3742*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3742),(3744,'Technical / Program Managers*3541*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3541),(3745,'Technical / Program Managers*3541*3744*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3744),(3746,'Technical / Program Managers*3541*3744*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3744),(3747,'Technical / Program Managers*3541*3744*3746*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3746),(3748,'Technical / Program Managers*3541*3744*3746*3747*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3747),(3749,'Technical Leads*3540*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3540),(3750,'Technical Leads*3540*3749*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3749),(3751,'Technical Leads*3540*3749*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3749),(3752,'Technical Leads*3540*3749*3751*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3751),(3753,'Technical Leads*3540*3749*3751*3752*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3752),(3754,'System Owners*3543*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3543),(3755,'System Owners*3543*3754*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3754),(3756,'System Owners*3543*3754*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3754),(3757,'System Owners*3543*3754*3756*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3756),(3758,'System Owners*3543*3754*3756*3757*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3757),(3759,'Product Managers*3539*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3539),(3760,'Product Managers*3539*3759*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3759),(3761,'Product Managers*3539*3759*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3759),(3762,'Product Managers*3539*3759*3761*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3761),(3763,'Product Managers*3539*3759*3761*3762*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3762),(3764,'Legal Counsels*3542*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3542),(3765,'Legal Counsels*3542*3764*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3764),(3766,'Legal Counsels*3542*3764*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3764),(3767,'Legal Counsels*3542*3764*3766*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3766),(3768,'Legal Counsels*3542*3764*3766*3767*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3767),(3769,'Technical / Program Managers*3491*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3491),(3770,'Technical / Program Managers*3491*3769*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3769),(3771,'Technical / Program Managers*3491*3769*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3769),(3772,'Technical / Program Managers*3491*3769*3771*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3771),(3773,'Technical / Program Managers*3491*3769*3771*3772*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3772),(3774,'Technical Leads*3490*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3490),(3775,'Technical Leads*3490*3774*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3774),(3776,'Technical Leads*3490*3774*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3774),(3777,'Technical Leads*3490*3774*3776*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3776),(3778,'Technical Leads*3490*3774*3776*3777*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3777),(3779,'System Owners*3493*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3493),(3780,'System Owners*3493*3779*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3779),(3781,'System Owners*3493*3779*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3779),(3782,'System Owners*3493*3779*3781*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3781),(3783,'System Owners*3493*3779*3781*3782*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3782),(3784,'Product Managers*3489*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3489),(3785,'Product Managers*3489*3784*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3784),(3786,'Product Managers*3489*3784*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3784),(3787,'Product Managers*3489*3784*3786*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3786),(3788,'Product Managers*3489*3784*3786*3787*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3787),(3789,'Legal Counsels*3492*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3492),(3790,'Legal Counsels*3492*3789*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3789),(3791,'Legal Counsels*3492*3789*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3789),(3792,'Legal Counsels*3492*3789*3791*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3791),(3793,'Legal Counsels*3492*3789*3791*3792*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3792),(3794,'Technical / Program Managers*3511*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3511),(3795,'Technical / Program Managers*3511*3794*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3794),(3796,'Technical / Program Managers*3511*3794*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3794),(3797,'Technical / Program Managers*3511*3794*3796*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3796),(3798,'Technical / Program Managers*3511*3794*3796*3797*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3797),(3799,'Technical Leads*3510*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3510),(3800,'Technical Leads*3510*3799*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3799),(3801,'Technical Leads*3510*3799*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3799),(3802,'Technical Leads*3510*3799*3801*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3801),(3803,'Technical Leads*3510*3799*3801*3802*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3802),(3804,'System Owners*3513*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3513),(3805,'System Owners*3513*3804*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3804),(3806,'System Owners*3513*3804*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3804),(3807,'System Owners*3513*3804*3806*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3806),(3808,'System Owners*3513*3804*3806*3807*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3807),(3809,'Product Managers*3509*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3509),(3810,'Product Managers*3509*3809*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3809),(3811,'Product Managers*3509*3809*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3809),(3812,'Product Managers*3509*3809*3811*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3811),(3813,'Product Managers*3509*3809*3811*3812*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3812),(3814,'Legal Counsels*3512*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3512),(3815,'Legal Counsels*3512*3814*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3814),(3816,'Legal Counsels*3512*3814*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3814),(3817,'Legal Counsels*3512*3814*3816*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3816),(3818,'Legal Counsels*3512*3814*3816*3817*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3817),(3819,'Technical / Program Managers*3501*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3501),(3820,'Technical / Program Managers*3501*3819*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3819),(3821,'Technical / Program Managers*3501*3819*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3819),(3822,'Technical / Program Managers*3501*3819*3821*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3821),(3823,'Technical / Program Managers*3501*3819*3821*3822*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3822),(3824,'Technical Leads*3500*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3500),(3825,'Technical Leads*3500*3824*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3824),(3826,'Technical Leads*3500*3824*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3824),(3827,'Technical Leads*3500*3824*3826*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3826),(3828,'Technical Leads*3500*3824*3826*3827*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3827),(3829,'System Owners*3503*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3503),(3830,'System Owners*3503*3829*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3829),(3831,'System Owners*3503*3829*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3829),(3832,'System Owners*3503*3829*3831*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3831),(3833,'System Owners*3503*3829*3831*3832*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3832),(3834,'Product Managers*3499*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3499),(3835,'Product Managers*3499*3834*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3834),(3836,'Product Managers*3499*3834*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3834),(3837,'Product Managers*3499*3834*3836*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3836),(3838,'Product Managers*3499*3834*3836*3837*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3837),(3839,'Legal Counsels*3502*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3502),(3840,'Legal Counsels*3502*3839*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3839),(3841,'Legal Counsels*3502*3839*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3839),(3842,'Legal Counsels*3502*3839*3841*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3841),(3843,'Legal Counsels*3502*3839*3841*3842*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3842),(3844,'Technical / Program Managers*3496*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3496),(3845,'Technical / Program Managers*3496*3844*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3844),(3846,'Technical / Program Managers*3496*3844*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3844),(3847,'Technical / Program Managers*3496*3844*3846*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3846),(3848,'Technical / Program Managers*3496*3844*3846*3847*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3847),(3849,'Technical Leads*3495*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3495),(3850,'Technical Leads*3495*3849*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3849),(3851,'Technical Leads*3495*3849*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3849),(3852,'Technical Leads*3495*3849*3851*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3851),(3853,'Technical Leads*3495*3849*3851*3852*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3852),(3854,'System Owners*3498*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3498),(3855,'System Owners*3498*3854*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3854),(3856,'System Owners*3498*3854*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3854),(3857,'System Owners*3498*3854*3856*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3856),(3858,'System Owners*3498*3854*3856*3857*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3857),(3859,'Product Managers*3494*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3494),(3860,'Product Managers*3494*3859*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3859),(3861,'Product Managers*3494*3859*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3859),(3862,'Product Managers*3494*3859*3861*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3861),(3863,'Product Managers*3494*3859*3861*3862*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3862),(3864,'Legal Counsels*3497*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3497),(3865,'Legal Counsels*3497*3864*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3864),(3866,'Legal Counsels*3497*3864*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3864),(3867,'Legal Counsels*3497*3864*3866*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3866),(3868,'Legal Counsels*3497*3864*3866*3867*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3867),(3869,'Primary Contacts','Risk',NULL,1,1,1,1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,0,0,NULL),(3870,'Secondary Contacts','Risk',NULL,1,1,1,1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,0,0,NULL),(3871,'Primary Contacts','Threat',NULL,1,1,1,1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,0,0,NULL),(3872,'Secondary Contacts','Threat',NULL,1,1,1,1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,0,0,NULL),(3885,'Admin*62*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,62),(3886,'Admin*62*3885*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3885),(3887,'Admin*62*3885*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3885),(3888,'Admin*62*3885*3887*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3887),(3889,'Admin*62*3885*3887*3888*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3888),(3890,'Admin*62*3885*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3885),(3891,'Primary Contacts*3869*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3869),(3892,'Primary Contacts*3869*3891*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3891),(3893,'Primary Contacts*3869*3891*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3891),(3894,'Primary Contacts*3869*3891*3893*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3893),(3895,'Primary Contacts*3869*3891*3893*3894*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3894),(3896,'Primary Contacts*3869*3891*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3891),(3897,'Secondary Contacts*3870*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3870),(3898,'Secondary Contacts*3870*3897*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3897),(3899,'Secondary Contacts*3870*3897*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3897),(3900,'Secondary Contacts*3870*3897*3899*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3899),(3901,'Secondary Contacts*3870*3897*3899*3900*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3900),(3902,'Secondary Contacts*3870*3897*','Proposal',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3897),(3903,'Admin*66*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,66),(3904,'Admin*66*3903*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3903),(3905,'Admin*66*3903*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3903),(3906,'Admin*66*3903*3905*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3905),(3907,'Admin*66*3903*3905*3906*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3906),(3908,'Primary Contacts*3871*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3871),(3909,'Primary Contacts*3871*3908*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3908),(3910,'Primary Contacts*3871*3908*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3908),(3911,'Primary Contacts*3871*3908*3910*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3910),(3912,'Primary Contacts*3871*3908*3910*3911*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3911),(3913,'Secondary Contacts*3872*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3872),(3914,'Secondary Contacts*3872*3913*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3913),(3915,'Secondary Contacts*3872*3913*','Document',NULL,1,1,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3913),(3916,'Secondary Contacts*3872*3913*3915*','Relationship',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3915),(3917,'Secondary Contacts*3872*3913*3915*3916*','Comment',NULL,1,0,0,0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL,0,0,1,1,0,3916),(3918,'Task Assignees','TaskGroupTask',NULL,1,1,0,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,1,0,1,0,0,NULL),(3919,'Task Assignees','CycleTaskGroupObjectTask',NULL,1,1,0,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,1,0,1,0,0,NULL),(3920,'Admin','Workflow',NULL,1,1,1,1,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,1,1,1,0,0,NULL),(3921,'Admin Mapped','Workflow',NULL,1,1,1,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,0,0,1,1,0,NULL),(3922,'Workflow Member','Workflow',NULL,1,0,0,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,0,0,1,0,0,NULL),(3923,'Workflow Member Mapped','Workflow',NULL,1,0,0,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,0,0,1,1,0,NULL),(3924,'Task Secondary Assignees','TaskGroupTask',NULL,1,1,0,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,0,0,1,0,0,NULL),(3925,'Task Secondary Assignees','CycleTaskGroupObjectTask',NULL,1,1,0,0,'2018-08-24 09:33:23',NULL,'2018-08-24 09:33:23',NULL,0,0,1,0,0,NULL);
/*!40000 ALTER TABLE `access_control_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `access_groups`
--

DROP TABLE IF EXISTS `access_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `notes` text NOT NULL,
  `description` text NOT NULL,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_access_groups` (`slug`),
  UNIQUE KEY `uq_t_access_groups` (`title`),
  KEY `fk_access_groups_contexts` (`context_id`),
  KEY `ix_access_groups_updated_at` (`updated_at`),
  CONSTRAINT `access_groups_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_groups`
--

LOCK TABLES `access_groups` WRITE;
/*!40000 ALTER TABLE `access_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acl_copy`
--

DROP TABLE IF EXISTS `acl_copy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acl_copy` (
  `id` int(11) NOT NULL DEFAULT '0',
  `person_id` int(11) NOT NULL,
  `ac_role_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acl_copy`
--

LOCK TABLES `acl_copy` WRITE;
/*!40000 ALTER TABLE `acl_copy` DISABLE KEYS */;
/*!40000 ALTER TABLE `acl_copy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acr_copy`
--

DROP TABLE IF EXISTS `acr_copy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acr_copy` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(250) NOT NULL,
  `object_type` varchar(250) DEFAULT NULL,
  `tooltip` varchar(250) DEFAULT NULL,
  `read` tinyint(1) NOT NULL DEFAULT '1',
  `update` tinyint(1) NOT NULL DEFAULT '1',
  `delete` tinyint(1) NOT NULL DEFAULT '1',
  `my_work` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `mandatory` tinyint(1) NOT NULL DEFAULT '0',
  `default_to_current_user` tinyint(1) NOT NULL DEFAULT '0',
  `non_editable` tinyint(1) NOT NULL DEFAULT '0',
  `internal` tinyint(1) NOT NULL DEFAULT '0',
  `notify_about_proposal` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acr_copy`
--

LOCK TABLES `acr_copy` WRITE;
/*!40000 ALTER TABLE `acr_copy` DISABLE KEYS */;
INSERT INTO `acr_copy` VALUES (1,'Primary Contacts','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(2,'Secondary Contacts','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(3,'Primary Contacts','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(4,'Secondary Contacts','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(5,'Primary Contacts','Clause',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(6,'Secondary Contacts','Clause',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(7,'Primary Contacts','Contract',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(8,'Secondary Contacts','Contract',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(9,'Primary Contacts','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,1),(10,'Secondary Contacts','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(11,'Principal Assignees','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(12,'Secondary Assignees','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(13,'Primary Contacts','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(14,'Secondary Contacts','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(15,'Primary Contacts','Facility',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(16,'Secondary Contacts','Facility',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(17,'Primary Contacts','Issue',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(18,'Secondary Contacts','Issue',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(19,'Primary Contacts','Market',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(20,'Secondary Contacts','Market',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(21,'Primary Contacts','Objective',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(22,'Secondary Contacts','Objective',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(23,'Primary Contacts','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(24,'Secondary Contacts','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(25,'Primary Contacts','Policy',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(26,'Secondary Contacts','Policy',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(27,'Primary Contacts','Process',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(28,'Secondary Contacts','Process',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(29,'Primary Contacts','Product',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(30,'Secondary Contacts','Product',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(31,'Primary Contacts','Project',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(32,'Secondary Contacts','Project',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(33,'Primary Contacts','Program',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(34,'Secondary Contacts','Program',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(35,'Primary Contacts','Regulation',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(36,'Secondary Contacts','Regulation',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(37,'Primary Contacts','Requirement',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(38,'Secondary Contacts','Requirement',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(39,'Primary Contacts','Standard',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(40,'Secondary Contacts','Standard',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(41,'Primary Contacts','System',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(42,'Secondary Contacts','System',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(43,'Primary Contacts','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(44,'Secondary Contacts','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,0,0,1,0,0),(45,'Admin','AccessGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(46,'Admin','Clause',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(47,'Admin','Comment',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(48,'Admin','Contract',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(49,'Admin','Control',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,1),(50,'Admin','DataAsset',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(51,'Admin','Document',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(52,'Admin','Facility',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(53,'Admin','Issue',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(54,'Admin','Market',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(55,'Admin','Objective',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(56,'Admin','OrgGroup',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(57,'Admin','Policy',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(58,'Admin','Process',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(59,'Admin','Product',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(60,'Admin','Project',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(61,'Admin','Regulation',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(62,'Admin','Risk',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,1),(63,'Admin','Requirement',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(64,'Admin','Standard',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(65,'Admin','System',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(66,'Admin','Threat',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(67,'Admin','Vendor',NULL,1,1,1,1,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL,1,1,1,0,0),(68,'Verifiers Document Mapped','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0),(69,'Verifiers Mapped','Assessment',NULL,1,0,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0),(70,'Creators Document Mapped','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0),(71,'Creators Mapped','Assessment',NULL,1,0,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0),(72,'Assignees','Assessment',NULL,1,1,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,1,0,1,0,0),(73,'Verifiers','Assessment',NULL,1,1,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,0,0),(74,'Assignees Mapped','Assessment',NULL,1,0,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0),(75,'Assignees Document Mapped','Assessment',NULL,1,1,1,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,0,0,1,1,0),(76,'Creators','Assessment',NULL,1,1,0,1,'2018-08-24 09:33:16',NULL,'2018-08-24 09:33:16',NULL,1,0,1,0,0),(77,'ProposalReader','Proposal',NULL,1,0,0,1,'2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL,0,0,1,1,0),(78,'ProposalEditor','Proposal',NULL,1,1,0,1,'2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL,0,0,1,1,0);
/*!40000 ALTER TABLE `acr_copy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessment_templates`
--

DROP TABLE IF EXISTS `assessment_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assessment_templates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template_object_type` varchar(250) DEFAULT NULL,
  `test_plan_procedure` tinyint(1) NOT NULL DEFAULT '1',
  `procedure_description` text NOT NULL,
  `default_people` text NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `audit_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `context_id` (`context_id`),
  KEY `fk_assessment_template_audits` (`audit_id`),
  CONSTRAINT `assessment_templates_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_assessment_template_audits` FOREIGN KEY (`audit_id`) REFERENCES `audits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_templates`
--

LOCK TABLES `assessment_templates` WRITE;
/*!40000 ALTER TABLE `assessment_templates` DISABLE KEYS */;
/*!40000 ALTER TABLE `assessment_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessments`
--

DROP TABLE IF EXISTS `assessments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assessments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `design` varchar(250) NOT NULL DEFAULT '',
  `operationally` varchar(250) NOT NULL DEFAULT '',
  `os_state` varchar(250) NOT NULL,
  `test_plan` text NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `status` enum('Not Started','In Progress','In Review','Verified','Completed','Deprecated','Rework Needed') NOT NULL DEFAULT 'Not Started',
  `notes` text NOT NULL,
  `description` text NOT NULL,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `finished_date` datetime DEFAULT NULL,
  `verified_date` datetime DEFAULT NULL,
  `recipients` varchar(250) DEFAULT 'Assessor,Creator,Verifier',
  `send_by_default` tinyint(1) DEFAULT '1',
  `audit_id` int(11) NOT NULL,
  `assessment_type` varchar(250) NOT NULL DEFAULT 'Control',
  `label` enum('Needs Discussion','Needs Rework','Followup','Auditor pulls evidence') DEFAULT NULL,
  `test_plan_procedure` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_control_assessments` (`slug`),
  KEY `context_id` (`context_id`),
  KEY `fk_assessments_audits` (`audit_id`),
  KEY `fk_assessments_label` (`label`),
  CONSTRAINT `assessments_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_assessments_audits` FOREIGN KEY (`audit_id`) REFERENCES `audits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessments`
--

LOCK TABLES `assessments` WRITE;
/*!40000 ALTER TABLE `assessments` DISABLE KEYS */;
/*!40000 ALTER TABLE `assessments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attribute_definitions`
--

DROP TABLE IF EXISTS `attribute_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attribute_definitions` (
  `attribute_definition_id` int(11) NOT NULL AUTO_INCREMENT,
  `attribute_type_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `namespace_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`attribute_definition_id`),
  KEY `attribute_type_id` (`attribute_type_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  KEY `namespace_id` (`namespace_id`),
  CONSTRAINT `attribute_definitions_ibfk_1` FOREIGN KEY (`attribute_type_id`) REFERENCES `attribute_types` (`attribute_type_id`),
  CONSTRAINT `attribute_definitions_ibfk_2` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attribute_definitions_ibfk_3` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attribute_definitions_ibfk_4` FOREIGN KEY (`namespace_id`) REFERENCES `namespaces` (`namespace_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute_definitions`
--

LOCK TABLES `attribute_definitions` WRITE;
/*!40000 ALTER TABLE `attribute_definitions` DISABLE KEYS */;
INSERT INTO `attribute_definitions` VALUES (1,1,'last_assessment_date','Last Assessment Date',NULL,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL),(2,2,'last_comment','Last Comment',NULL,'2018-08-24 09:33:17','2018-08-24 09:33:17',NULL,NULL);
/*!40000 ALTER TABLE `attribute_definitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attribute_templates`
--

DROP TABLE IF EXISTS `attribute_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attribute_templates` (
  `attribute_template_id` int(11) NOT NULL AUTO_INCREMENT,
  `attribute_definition_id` int(11) DEFAULT NULL,
  `object_template_id` int(11) DEFAULT NULL,
  `namespace_id` int(11) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `mandatory` tinyint(1) DEFAULT NULL,
  `unique` tinyint(1) DEFAULT NULL,
  `help_text` text NOT NULL,
  `options` text NOT NULL,
  `default_value` text NOT NULL,
  `read_only` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`attribute_template_id`),
  KEY `attribute_definition_id` (`attribute_definition_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  KEY `namespace_id` (`namespace_id`),
  KEY `object_template_id` (`object_template_id`),
  CONSTRAINT `attribute_templates_ibfk_1` FOREIGN KEY (`attribute_definition_id`) REFERENCES `attribute_definitions` (`attribute_definition_id`),
  CONSTRAINT `attribute_templates_ibfk_2` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attribute_templates_ibfk_3` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attribute_templates_ibfk_4` FOREIGN KEY (`namespace_id`) REFERENCES `namespaces` (`namespace_id`),
  CONSTRAINT `attribute_templates_ibfk_5` FOREIGN KEY (`object_template_id`) REFERENCES `object_templates` (`object_template_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute_templates`
--

LOCK TABLES `attribute_templates` WRITE;
/*!40000 ALTER TABLE `attribute_templates` DISABLE KEYS */;
INSERT INTO `attribute_templates` VALUES (1,1,1,NULL,1,NULL,NULL,'','','',1,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL),(2,1,2,NULL,1,NULL,NULL,'','','',1,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL),(3,2,3,NULL,1,NULL,NULL,'','','',1,'2018-08-24 09:33:17','2018-08-24 09:33:17',NULL,NULL);
/*!40000 ALTER TABLE `attribute_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attribute_types`
--

DROP TABLE IF EXISTS `attribute_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attribute_types` (
  `attribute_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `field_type` varchar(255) NOT NULL,
  `db_column_name` varchar(50) NOT NULL,
  `computed` tinyint(1) NOT NULL,
  `aggregate_function` text NOT NULL,
  `namespace_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`attribute_type_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  KEY `namespace_id` (`namespace_id`),
  CONSTRAINT `attribute_types_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attribute_types_ibfk_2` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attribute_types_ibfk_3` FOREIGN KEY (`namespace_id`) REFERENCES `namespaces` (`namespace_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute_types`
--

LOCK TABLES `attribute_types` WRITE;
/*!40000 ALTER TABLE `attribute_types` DISABLE KEYS */;
INSERT INTO `attribute_types` VALUES (1,'Computed attribute for last assessment date','computed_assessment_finished_date','computed_assessment_finished_date',1,'Assessment finished_date max',NULL,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL),(2,'Computed attribute for last comment','value_string','last_comment',1,'Comment description last',NULL,'2018-08-24 09:33:17','2018-08-24 09:33:17',NULL,NULL);
/*!40000 ALTER TABLE `attribute_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attributes`
--

DROP TABLE IF EXISTS `attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attributes` (
  `attribute_id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) DEFAULT NULL,
  `object_type` varchar(250) DEFAULT NULL,
  `attribute_definition_id` int(11) DEFAULT NULL,
  `attribute_template_id` int(11) DEFAULT NULL,
  `value_string` text NOT NULL,
  `value_integer` int(11) DEFAULT NULL,
  `value_datetime` datetime DEFAULT NULL,
  `source_type` varchar(250) DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `source_attr` varchar(250) DEFAULT NULL,
  `namespace_id` int(11) DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`attribute_id`),
  UNIQUE KEY `uq_attributes` (`object_id`,`object_type`,`attribute_definition_id`,`attribute_template_id`),
  KEY `attribute_definition_id` (`attribute_definition_id`),
  KEY `attribute_template_id` (`attribute_template_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  KEY `namespace_id` (`namespace_id`),
  KEY `ix_source` (`source_type`,`source_id`,`source_attr`),
  KEY `ix_value_datetime` (`value_datetime`),
  KEY `ix_value_integer` (`value_integer`),
  CONSTRAINT `attributes_ibfk_1` FOREIGN KEY (`attribute_definition_id`) REFERENCES `attribute_definitions` (`attribute_definition_id`),
  CONSTRAINT `attributes_ibfk_2` FOREIGN KEY (`attribute_template_id`) REFERENCES `attribute_templates` (`attribute_template_id`),
  CONSTRAINT `attributes_ibfk_3` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attributes_ibfk_4` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `attributes_ibfk_5` FOREIGN KEY (`namespace_id`) REFERENCES `namespaces` (`namespace_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attributes`
--

LOCK TABLES `attributes` WRITE;
/*!40000 ALTER TABLE `attributes` DISABLE KEYS */;
/*!40000 ALTER TABLE `attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audits`
--

DROP TABLE IF EXISTS `audits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `report_start_date` date DEFAULT NULL,
  `report_end_date` date DEFAULT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Planned',
  `gdrive_evidence_folder` varchar(250) DEFAULT NULL,
  `program_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `audit_firm_id` int(11) DEFAULT NULL,
  `object_type` varchar(250) NOT NULL,
  `secondary_contact_id` int(11) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL DEFAULT '0',
  `folder` text NOT NULL,
  `last_deprecated_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_t_audits` (`title`),
  KEY `program_id` (`program_id`),
  KEY `fk_audits_contact` (`contact_id`),
  KEY `fk_audits_contexts` (`context_id`),
  KEY `ix_audits_updated_at` (`updated_at`),
  KEY `fk_audits_secondary_contact` (`secondary_contact_id`),
  CONSTRAINT `audits_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `audits_ibfk_3` FOREIGN KEY (`program_id`) REFERENCES `programs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audits`
--

LOCK TABLES `audits` WRITE;
/*!40000 ALTER TABLE `audits` DISABLE KEYS */;
/*!40000 ALTER TABLE `audits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `automappings`
--

DROP TABLE IF EXISTS `automappings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `automappings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `relationship_id` int(11) DEFAULT NULL,
  `source_id` int(11) NOT NULL,
  `source_type` varchar(250) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `destination_type` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_automappings_contexts` (`context_id`),
  KEY `ix_automappings_updated_at` (`updated_at`),
  CONSTRAINT `automappings_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `automappings`
--

LOCK TABLES `automappings` WRITE;
/*!40000 ALTER TABLE `automappings` DISABLE KEYS */;
/*!40000 ALTER TABLE `automappings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `background_tasks`
--

DROP TABLE IF EXISTS `background_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `background_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  `parameters` mediumblob,
  `result` mediumblob,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  KEY `fk_background_tasks_contexts` (`context_id`),
  KEY `ix_background_tasks_updated_at` (`updated_at`),
  CONSTRAINT `background_tasks_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `background_tasks`
--

LOCK TABLES `background_tasks` WRITE;
/*!40000 ALTER TABLE `background_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `background_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `lft` int(11) DEFAULT NULL,
  `rgt` int(11) DEFAULT NULL,
  `scope_id` int(11) DEFAULT NULL,
  `depth` int(11) DEFAULT NULL,
  `required` tinyint(1) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `type` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_categories_contexts` (`context_id`),
  KEY `ix_categories_updated_at` (`updated_at`),
  CONSTRAINT `fk_categories_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (37,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Confidentiality',NULL,NULL,102,NULL,NULL,NULL,'ControlAssertion'),(38,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Integrity',NULL,NULL,102,NULL,NULL,NULL,'ControlAssertion'),(39,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Availability',NULL,NULL,102,NULL,NULL,NULL,'ControlAssertion'),(40,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Security',NULL,NULL,102,NULL,NULL,NULL,'ControlAssertion'),(41,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Privacy',NULL,NULL,102,NULL,NULL,NULL,'ControlAssertion'),(42,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Org and Admin/Governance',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(43,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Training',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(44,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Policies & Procedures',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(45,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','HR',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(46,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Logical Access/ Access Control',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(47,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Access Management',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(48,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Authorization',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(49,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Authentication',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(50,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Change Management',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(51,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Segregation of Duties',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(52,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Configuration Management',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(53,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Package Verification and Code release',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(54,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Incident Management',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(55,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Monitoring ',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(56,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Process',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(57,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Business Continuity',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(58,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Disaster Recovery',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(59,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Restoration Tests',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(60,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Backup Logs ',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(61,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Replication',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(62,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Data Protection and Retention',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(63,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Physical Security',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(64,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Data Centers',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory'),(65,NULL,'2016-05-03 10:37:03','2016-05-03 10:37:03','Sites',NULL,NULL,100,NULL,NULL,NULL,'ControlCategory');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorizations`
--

DROP TABLE IF EXISTS `categorizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categorizations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `category_id` int(11) NOT NULL,
  `categorizable_id` int(11) DEFAULT NULL,
  `categorizable_type` varchar(250) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `category_type` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `fk_categorizations_contexts` (`context_id`),
  KEY `ix_categorizations_updated_at` (`updated_at`),
  CONSTRAINT `categorizations_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `fk_categorizations_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorizations`
--

LOCK TABLES `categorizations` WRITE;
/*!40000 ALTER TABLE `categorizations` DISABLE KEYS */;
/*!40000 ALTER TABLE `categorizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clauses`
--

DROP TABLE IF EXISTS `clauses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clauses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `na` tinyint(1) NOT NULL,
  `notes` text NOT NULL,
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `description` text NOT NULL,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_clauses` (`slug`),
  UNIQUE KEY `uq_t_clauses` (`title`),
  KEY `context_id` (`context_id`),
  CONSTRAINT `clauses_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clauses`
--

LOCK TABLES `clauses` WRITE;
/*!40000 ALTER TABLE `clauses` DISABLE KEYS */;
/*!40000 ALTER TABLE `clauses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `assignee_type` text NOT NULL,
  `revision_id` int(11) DEFAULT NULL,
  `custom_attribute_definition_id` int(11) DEFAULT NULL,
  `initiator_instance_id` int(11) DEFAULT NULL,
  `initiator_instance_type` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `context_id` (`context_id`),
  KEY `fk_comments_revisions` (`revision_id`),
  KEY `fk_comments_custom_attribute_definitions` (`custom_attribute_definition_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_comments_custom_attribute_definitions` FOREIGN KEY (`custom_attribute_definition_id`) REFERENCES `custom_attribute_definitions` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_comments_revisions` FOREIGN KEY (`revision_id`) REFERENCES `revisions` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `context_implications`
--

DROP TABLE IF EXISTS `context_implications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `context_implications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `context_id` int(11) DEFAULT NULL,
  `source_context_id` int(11) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `context_scope` varchar(128) DEFAULT NULL,
  `source_context_scope` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_context_implications_contexts` (`context_id`),
  KEY `ix_context_implications_updated_at` (`updated_at`),
  KEY `ix_context_implications_source_id` (`source_context_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `context_implications`
--

LOCK TABLES `context_implications` WRITE;
/*!40000 ALTER TABLE `context_implications` DISABLE KEYS */;
INSERT INTO `context_implications` VALUES (1,NULL,NULL,NULL,'2018-08-24 09:33:20','2018-08-24 09:33:20',NULL,NULL);
/*!40000 ALTER TABLE `context_implications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contexts`
--

DROP TABLE IF EXISTS `contexts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contexts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `description` text NOT NULL,
  `related_object_id` int(11) DEFAULT NULL,
  `related_object_type` varchar(128) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_contexts_contexts` (`context_id`),
  KEY `ix_context_related_object` (`related_object_type`,`related_object_id`),
  KEY `ix_contexts_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contexts`
--

LOCK TABLES `contexts` WRITE;
/*!40000 ALTER TABLE `contexts` DISABLE KEYS */;
INSERT INTO `contexts` VALUES (0,'System Administration','Context for super-user permissions.',NULL,NULL,NULL,'2018-08-24 09:33:19','2018-08-24 09:33:19',NULL),(1,'Administration','Context for Administrative resources.',NULL,NULL,0,'2018-08-24 09:33:15','2018-08-24 09:33:15',1);
/*!40000 ALTER TABLE `contexts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controls`
--

DROP TABLE IF EXISTS `controls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `directive_id` int(11) DEFAULT NULL,
  `kind_id` int(11) DEFAULT NULL,
  `means_id` int(11) DEFAULT NULL,
  `version` varchar(250) DEFAULT NULL,
  `verify_frequency_id` int(11) DEFAULT NULL,
  `fraud_related` tinyint(1) DEFAULT NULL,
  `key_control` tinyint(1) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `notes` text NOT NULL,
  `company_control` tinyint(1) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `test_plan` text NOT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_controls` (`slug`),
  UNIQUE KEY `uq_t_controls` (`title`),
  KEY `directive_id` (`directive_id`),
  KEY `fk_controls_contexts` (`context_id`),
  KEY `ix_controls_updated_at` (`updated_at`),
  CONSTRAINT `controls_ibfk_1` FOREIGN KEY (`directive_id`) REFERENCES `directives` (`id`),
  CONSTRAINT `fk_controls_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controls`
--

LOCK TABLES `controls` WRITE;
/*!40000 ALTER TABLE `controls` DISABLE KEYS */;
/*!40000 ALTER TABLE `controls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_attribute_definitions`
--

DROP TABLE IF EXISTS `custom_attribute_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_attribute_definitions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `title` varchar(250) NOT NULL,
  `helptext` varchar(250) DEFAULT NULL,
  `placeholder` varchar(250) DEFAULT NULL,
  `definition_type` varchar(250) NOT NULL,
  `attribute_type` varchar(250) NOT NULL,
  `multi_choice_options` text,
  `mandatory` tinyint(1) DEFAULT NULL,
  `definition_id` int(11) DEFAULT NULL,
  `multi_choice_mandatory` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_custom_attribute` (`definition_type`,`definition_id`,`title`),
  KEY `ix_custom_attributes_title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_attribute_definitions`
--

LOCK TABLES `custom_attribute_definitions` WRITE;
/*!40000 ALTER TABLE `custom_attribute_definitions` DISABLE KEYS */;
INSERT INTO `custom_attribute_definitions` VALUES (1,NULL,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','Type','Assessment Category',NULL,'assessment','Dropdown','Documentation,Interview',0,NULL,NULL);
/*!40000 ALTER TABLE `custom_attribute_definitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_attribute_values`
--

DROP TABLE IF EXISTS `custom_attribute_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_attribute_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `custom_attribute_id` int(11) NOT NULL,
  `attributable_id` int(11) DEFAULT NULL,
  `attributable_type` varchar(250) DEFAULT NULL,
  `attribute_value` text NOT NULL,
  `attribute_object_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_custom_attribute_value` (`custom_attribute_id`,`attributable_id`),
  KEY `custom_attribute_values_ibfk_1` (`custom_attribute_id`),
  KEY `ix_custom_attributes_attributable` (`attributable_id`,`attributable_type`),
  CONSTRAINT `custom_attribute_values_ibfk_1` FOREIGN KEY (`custom_attribute_id`) REFERENCES `custom_attribute_definitions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_attribute_values`
--

LOCK TABLES `custom_attribute_values` WRITE;
/*!40000 ALTER TABLE `custom_attribute_values` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_attribute_values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cycle_task_entries`
--

DROP TABLE IF EXISTS `cycle_task_entries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cycle_task_entries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cycle_task_group_object_task_id` int(11) NOT NULL,
  `description` text,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `cycle_id` int(11) NOT NULL,
  `_is_declining_review` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cycle_task_entries_contexts` (`context_id`),
  KEY `ix_cycle_task_entries_updated_at` (`updated_at`),
  KEY `cycle_task_entries_cycle` (`cycle_id`),
  KEY `cycle_task_entries_ibfk_2` (`cycle_task_group_object_task_id`),
  CONSTRAINT `cycle_task_entries_cycle` FOREIGN KEY (`cycle_id`) REFERENCES `cycles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cycle_task_entries_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `cycle_task_entries_ibfk_2` FOREIGN KEY (`cycle_task_group_object_task_id`) REFERENCES `cycle_task_group_object_tasks` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cycle_task_entries`
--

LOCK TABLES `cycle_task_entries` WRITE;
/*!40000 ALTER TABLE `cycle_task_entries` DISABLE KEYS */;
/*!40000 ALTER TABLE `cycle_task_entries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cycle_task_group_object_tasks`
--

DROP TABLE IF EXISTS `cycle_task_group_object_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cycle_task_group_object_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_group_task_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `description` text,
  `title` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `sort_index` varchar(250) NOT NULL,
  `cycle_id` int(11) NOT NULL,
  `response_options` text NOT NULL,
  `selected_response_options` text NOT NULL,
  `task_type` varchar(250) NOT NULL,
  `cycle_task_group_id` int(11) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `finished_date` datetime DEFAULT NULL,
  `verified_date` datetime DEFAULT NULL,
  `last_deprecated_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_slug` (`slug`),
  KEY `task_group_task_id` (`task_group_task_id`),
  KEY `fk_cycle_task_group_object_tasks_contexts` (`context_id`),
  KEY `ix_cycle_task_group_object_tasks_updated_at` (`updated_at`),
  KEY `cycle_task_group_object_tasks_cycle` (`cycle_id`),
  KEY `cycle_task_group_id` (`cycle_task_group_id`),
  CONSTRAINT `cycle_task_group_id` FOREIGN KEY (`cycle_task_group_id`) REFERENCES `cycle_task_groups` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cycle_task_group_object_tasks_cycle` FOREIGN KEY (`cycle_id`) REFERENCES `cycles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cycle_task_group_object_tasks_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cycle_task_group_object_tasks`
--

LOCK TABLES `cycle_task_group_object_tasks` WRITE;
/*!40000 ALTER TABLE `cycle_task_group_object_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `cycle_task_group_object_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cycle_task_groups`
--

DROP TABLE IF EXISTS `cycle_task_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cycle_task_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cycle_id` int(11) NOT NULL,
  `task_group_id` int(11) DEFAULT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `description` text,
  `title` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `sort_index` varchar(250) NOT NULL,
  `next_due_date` date DEFAULT NULL,
  `secondary_contact_id` int(11) DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_slug` (`slug`),
  KEY `task_group_id` (`task_group_id`),
  KEY `fk_cycle_task_groups_contact` (`contact_id`),
  KEY `fk_cycle_task_groups_contexts` (`context_id`),
  KEY `ix_cycle_task_groups_updated_at` (`updated_at`),
  KEY `fk_cycle_task_groups_secondary_contact` (`secondary_contact_id`),
  KEY `cycle_task_groups_ibfk_3` (`cycle_id`),
  CONSTRAINT `cycle_task_groups_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `people` (`id`),
  CONSTRAINT `cycle_task_groups_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `cycle_task_groups_ibfk_3` FOREIGN KEY (`cycle_id`) REFERENCES `cycles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cycle_task_groups`
--

LOCK TABLES `cycle_task_groups` WRITE;
/*!40000 ALTER TABLE `cycle_task_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `cycle_task_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cycles`
--

DROP TABLE IF EXISTS `cycles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cycles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `description` text,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `is_current` tinyint(1) NOT NULL,
  `next_due_date` date DEFAULT NULL,
  `secondary_contact_id` int(11) DEFAULT NULL,
  `is_verification_needed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cycles` (`slug`),
  KEY `fk_cycles_contact` (`contact_id`),
  KEY `fk_cycles_contexts` (`context_id`),
  KEY `ix_cycles_updated_at` (`updated_at`),
  KEY `fk_cycles_secondary_contact` (`secondary_contact_id`),
  KEY `cycles_ibfk_3` (`workflow_id`),
  CONSTRAINT `cycles_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `people` (`id`),
  CONSTRAINT `cycles_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `cycles_ibfk_3` FOREIGN KEY (`workflow_id`) REFERENCES `workflows` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cycles`
--

LOCK TABLES `cycles` WRITE;
/*!40000 ALTER TABLE `cycles` DISABLE KEYS */;
/*!40000 ALTER TABLE `cycles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_assets`
--

DROP TABLE IF EXISTS `data_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_data_assets` (`slug`),
  UNIQUE KEY `uq_t_data_assets` (`title`),
  KEY `fk_data_assets_contexts` (`context_id`),
  KEY `ix_data_assets_updated_at` (`updated_at`),
  CONSTRAINT `fk_data_assets_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_assets`
--

LOCK TABLES `data_assets` WRITE;
/*!40000 ALTER TABLE `data_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directives`
--

DROP TABLE IF EXISTS `directives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `directives` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `version` varchar(250) DEFAULT NULL,
  `organization` varchar(250) DEFAULT NULL,
  `scope` text NOT NULL,
  `kind_id` int(11) DEFAULT NULL,
  `audit_start_date` datetime DEFAULT NULL,
  `audit_frequency_id` int(11) DEFAULT NULL,
  `audit_duration_id` int(11) DEFAULT NULL,
  `kind` varchar(250) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `meta_kind` varchar(250) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_directives` (`slug`),
  UNIQUE KEY `uq_t_directives` (`title`),
  KEY `fk_directives_contexts` (`context_id`),
  KEY `ix_directives_meta_kind` (`meta_kind`),
  KEY `ix_directives_updated_at` (`updated_at`),
  CONSTRAINT `fk_directives_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directives`
--

LOCK TABLES `directives` WRITE;
/*!40000 ALTER TABLE `directives` DISABLE KEYS */;
/*!40000 ALTER TABLE `directives` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `title` varchar(250) NOT NULL,
  `link` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `kind` enum('FILE','REFERENCE_URL') NOT NULL DEFAULT 'REFERENCE_URL',
  `source_gdrive_id` varchar(250) NOT NULL DEFAULT '',
  `gdrive_id` varchar(250) NOT NULL DEFAULT '',
  `slug` varchar(250) NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Active',
  `recipients` varchar(250) NOT NULL DEFAULT 'Admin',
  `send_by_default` tinyint(1) NOT NULL DEFAULT '1',
  `last_deprecated_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_control_document` (`slug`),
  KEY `fk_documents_contexts` (`context_id`),
  KEY `ix_documents_updated_at` (`updated_at`),
  KEY `idx_gdrive_id` (`gdrive_id`),
  CONSTRAINT `fk_documents_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `action` enum('POST','PUT','DELETE','BULK','GET') NOT NULL,
  `resource_id` int(11) DEFAULT NULL,
  `resource_type` varchar(250) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `events_modified_by` (`modified_by_id`),
  KEY `ix_events_updated_at` (`updated_at`),
  CONSTRAINT `events_modified_by` FOREIGN KEY (`modified_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,1,'2018-08-24 09:33:18','BULK',NULL,'Document','2018-08-24 09:33:18');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evidence`
--

DROP TABLE IF EXISTS `evidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evidence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(250) NOT NULL,
  `source_gdrive_id` varchar(250) NOT NULL,
  `gdrive_id` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `kind` enum('URL','FILE') NOT NULL,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `last_deprecated_date` date DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Active',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_control_evidence` (`slug`),
  KEY `fk_evidence_contexts` (`context_id`),
  KEY `ix_evidence_updated_at` (`updated_at`),
  CONSTRAINT `evidence_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evidence`
--

LOCK TABLES `evidence` WRITE;
/*!40000 ALTER TABLE `evidence` DISABLE KEYS */;
/*!40000 ALTER TABLE `evidence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities`
--

DROP TABLE IF EXISTS `facilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `facilities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_facilities` (`slug`),
  UNIQUE KEY `uq_t_facilities` (`title`),
  KEY `fk_facilities_contexts` (`context_id`),
  KEY `ix_facilities_updated_at` (`updated_at`),
  CONSTRAINT `fk_facilities_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities`
--

LOCK TABLES `facilities` WRITE;
/*!40000 ALTER TABLE `facilities` DISABLE KEYS */;
/*!40000 ALTER TABLE `facilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fulltext_record_properties`
--

DROP TABLE IF EXISTS `fulltext_record_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fulltext_record_properties` (
  `key` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(64) NOT NULL,
  `tags` varchar(250) DEFAULT NULL,
  `property` varchar(250) NOT NULL,
  `content` text NOT NULL,
  `subproperty` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`key`,`type`,`property`,`subproperty`),
  KEY `ix_fulltext_record_properties_key` (`key`),
  KEY `ix_fulltext_record_properties_tags` (`tags`),
  KEY `ix_fulltext_record_properties_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fulltext_record_properties`
--

LOCK TABLES `fulltext_record_properties` WRITE;
/*!40000 ALTER TABLE `fulltext_record_properties` DISABLE KEYS */;
/*!40000 ALTER TABLE `fulltext_record_properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `import_exports`
--

DROP TABLE IF EXISTS `import_exports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `import_exports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_type` enum('Import','Export') NOT NULL,
  `status` enum('Not Started','Analysis','Blocked','Analysis Failed','Stopped','Failed','Finished','In Progress') NOT NULL,
  `description` text,
  `created_at` datetime NOT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `created_by_id` int(11) NOT NULL,
  `results` longtext,
  `title` text,
  `content` longtext,
  `gdrive_metadata` text,
  PRIMARY KEY (`id`),
  KEY `created_by_id` (`created_by_id`),
  CONSTRAINT `import_exports_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `import_exports`
--

LOCK TABLES `import_exports` WRITE;
/*!40000 ALTER TABLE `import_exports` DISABLE KEYS */;
/*!40000 ALTER TABLE `import_exports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issues`
--

DROP TABLE IF EXISTS `issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `test_plan` text NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `notes` text NOT NULL,
  `description` text NOT NULL,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `audit_id` int(11) DEFAULT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `folder` text NOT NULL,
  `due_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_issues` (`slug`),
  UNIQUE KEY `uq_t_issues` (`title`),
  KEY `context_id` (`context_id`),
  KEY `fk_issues_audits` (`audit_id`),
  CONSTRAINT `fk_issues_audits` FOREIGN KEY (`audit_id`) REFERENCES `audits` (`id`),
  CONSTRAINT `issues_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issues`
--

LOCK TABLES `issues` WRITE;
/*!40000 ALTER TABLE `issues` DISABLE KEYS */;
/*!40000 ALTER TABLE `issues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issuetracker_issues`
--

DROP TABLE IF EXISTS `issuetracker_issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issuetracker_issues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  `title` varchar(250) DEFAULT NULL,
  `component_id` varchar(50) DEFAULT NULL,
  `hotlist_id` varchar(50) DEFAULT NULL,
  `issue_type` varchar(50) DEFAULT NULL,
  `issue_priority` varchar(50) DEFAULT NULL,
  `issue_severity` varchar(50) DEFAULT NULL,
  `assignee` varchar(250) DEFAULT NULL,
  `cc_list` text NOT NULL,
  `issue_id` varchar(50) DEFAULT NULL,
  `issue_url` varchar(250) DEFAULT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_object_id_object_type` (`object_type`,`object_id`),
  KEY `context_id` (`context_id`),
  CONSTRAINT `issuetracker_issues_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issuetracker_issues`
--

LOCK TABLES `issuetracker_issues` WRITE;
/*!40000 ALTER TABLE `issuetracker_issues` DISABLE KEYS */;
/*!40000 ALTER TABLE `issuetracker_issues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labels`
--

DROP TABLE IF EXISTS `labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `object_type` varchar(250) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`object_type`),
  KEY `context_id` (`context_id`),
  CONSTRAINT `labels_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labels`
--

LOCK TABLES `labels` WRITE;
/*!40000 ALTER TABLE `labels` DISABLE KEYS */;
INSERT INTO `labels` VALUES (1,'Needs Discussion','Assessment','2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL),(2,'Needs Rework','Assessment','2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL),(3,'Followup','Assessment','2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL),(4,'Auditor Pulls Evidence','Assessment','2018-08-24 09:33:17',NULL,'2018-08-24 09:33:17',NULL);
/*!40000 ALTER TABLE `labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance`
--

DROP TABLE IF EXISTS `maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `maintenance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `under_maintenance` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance`
--

LOCK TABLES `maintenance` WRITE;
/*!40000 ALTER TABLE `maintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `markets`
--

DROP TABLE IF EXISTS `markets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `markets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_markets` (`slug`),
  UNIQUE KEY `uq_t_markets` (`title`),
  KEY `fk_markets_contexts` (`context_id`),
  KEY `ix_markets_updated_at` (`updated_at`),
  CONSTRAINT `fk_markets_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `markets`
--

LOCK TABLES `markets` WRITE;
/*!40000 ALTER TABLE `markets` DISABLE KEYS */;
/*!40000 ALTER TABLE `markets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metrics`
--

DROP TABLE IF EXISTS `metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metrics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `notes` text NOT NULL,
  `slug` varchar(250) NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `test_plan` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_metrics` (`slug`),
  UNIQUE KEY `uq_t_metrics` (`title`),
  KEY `fk_metrics_contexts` (`context_id`),
  KEY `ix_metrics_updated_at` (`updated_at`),
  CONSTRAINT `metrics_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metrics`
--

LOCK TABLES `metrics` WRITE;
/*!40000 ALTER TABLE `metrics` DISABLE KEYS */;
/*!40000 ALTER TABLE `metrics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migration_log`
--

DROP TABLE IF EXISTS `migration_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `migration_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `down_version_num` varchar(50) DEFAULT NULL,
  `version_num` varchar(50) DEFAULT NULL,
  `is_migration_complete` tinyint(1) NOT NULL,
  `log` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migration_log`
--

LOCK TABLES `migration_log` WRITE;
/*!40000 ALTER TABLE `migration_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `migration_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `namespaces`
--

DROP TABLE IF EXISTS `namespaces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `namespaces` (
  `namespace_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`namespace_id`),
  UNIQUE KEY `name` (`name`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  CONSTRAINT `namespaces_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `namespaces_ibfk_2` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `namespaces`
--

LOCK TABLES `namespaces` WRITE;
/*!40000 ALTER TABLE `namespaces` DISABLE KEYS */;
/*!40000 ALTER TABLE `namespaces` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_configs`
--

DROP TABLE IF EXISTS `notification_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_configs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `enable_flag` tinyint(1) DEFAULT NULL,
  `notif_type` varchar(250) DEFAULT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_notif_configs_person_id_notif_type` (`person_id`,`notif_type`),
  KEY `fk_notification_configs_contexts` (`context_id`),
  KEY `ix_notification_configs_updated_at` (`updated_at`),
  CONSTRAINT `notification_configs_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `notification_configs_ibfk_2` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_configs`
--

LOCK TABLES `notification_configs` WRITE;
/*!40000 ALTER TABLE `notification_configs` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_types`
--

DROP TABLE IF EXISTS `notification_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `description` varchar(250) DEFAULT NULL,
  `advance_notice` int(11) DEFAULT NULL,
  `template` varchar(250) NOT NULL,
  `instant` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `modified_by_id` (`modified_by_id`),
  CONSTRAINT `notification_types_ibfk_1` FOREIGN KEY (`modified_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_types`
--

LOCK TABLES `notification_types` WRITE;
/*!40000 ALTER TABLE `notification_types` DISABLE KEYS */;
INSERT INTO `notification_types` VALUES (1,'request_open','Notify all assignees Requesters Assignees and Verifiers that a new request has been created.',0,'request_open',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(2,'request_declined','Notify Requester that a request has been declined.',0,'request_declined',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(3,'request_manual','Send a manual notification to the Requester.',0,'request_manual',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(4,'assessment_open','Send an open assessment notification to Assessors, Assignees and Verifiers.',0,'assessment_open',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(5,'assessment_declined','Notify Assessor that an assessment was declined.',0,'assessment_declined',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(6,'assessment_manual','Send a manual notification to the Requester.',0,'assessment_manual',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(7,'assessment_assignees_reminder','Notify all Assessors that they should take a look at the assessment.',0,'',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(8,'comment_created','Notify selected users that a comment has been created',0,'comment_created',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(9,'assessment_updated','Send an Assessment updated notification to Assessors, Creators and Verifiers.',0,'assessment_updated',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(10,'assessment_completed','Notify Assessors, Creators and Verifiers that an Assessment has been completed.',0,'assessment_completed',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(11,'assessment_ready_for_review','Notify Assessors, Creators and Verifiers that an Assessment is ready for review.',0,'assessment_ready_for_review',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(12,'assessment_verified','Notify Assessors, Creators and Verifiers that an Assessment has been verified.',0,'assessment_verified',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(13,'assessment_reopened','Notify Assessors, Creators and Verifiers that an Assessment has been reopened.',0,'assessment_reopened',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(14,'assessment_started','Notify the people assigned to an Assessment that the latter has moved to In Progress.',0,'assessment_started',0,'2018-08-24 09:33:15',NULL,'2018-08-24 09:33:15',NULL),(15,'cycle_created','Notify workflow members that a one time workflow has been started and send them their assigned tasks.',0,'cycle_created',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(16,'manual_cycle_created','Notify workflow members that a one time workflow has been started and send them their assigned tasks.',0,'manual_cycle_created',1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(17,'cycle_task_due_in','Notify task assignee his task is due in X days',1,'cycle_task_due_in',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(18,'one_time_cycle_task_due_in','Notify task assignee his task is due in X days',1,'cycle_task_due_in',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(19,'week_cycle_task_due_in','Notify task assignee his task is due in X days',1,'cycle_task_due_in',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(20,'month_cycle_task_due_in','Notify task assignee his task is due in X days',1,'cycle_task_due_in',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(23,'cycle_task_due_today','Notify task assignee his task is due today',0,'cycle_task_due_today',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(24,'cycle_task_reassigned','Notify task assignee his task is due today',0,'cycle_task_due_today',1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(25,'task_group_assignee_change','Email owners on task group assignee change.',0,'task_group_assignee_change',1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(26,'cycle_task_declined','Notify task assignee his task is due today',0,'cycle_task_due_today',1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(27,'all_cycle_tasks_completed','Notify workflow owner when all cycle tasks in one cycle have been completed and verified',0,'weekly_workflow_starts_in',1,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(28,'week_workflow_starts_in','Advanced notification for a recurring workflow.',1,'week_workflow_starts_in',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(29,'month_workflow_starts_in','Advanced notification for a recurring workflow.',3,'month_workflow_starts_in',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(32,'cycle_start_failed','Notify workflow owners that a cycle has failed tostart for a recurring workflow',-1,'cycle_start_failed',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(33,'cycle_task_overdue','Notify a task assignee that a task is overdue.',-1,'cycle_task_overdue',0,'2018-08-24 09:33:22',NULL,'2018-08-24 09:33:22',NULL),(34,'day_cycle_task_due_in','Notify task assignee his task is due in X days',1,'cycle_task_due_in',0,'0000-00-00 00:00:00',NULL,'0000-00-00 00:00:00',NULL),(35,'day_workflow_starts_in','Advanced notification for a recurring workflow.',1,'day_workflow_starts_in',0,'0000-00-00 00:00:00',NULL,'0000-00-00 00:00:00',NULL);
/*!40000 ALTER TABLE `notification_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `notification_type_id` int(11) NOT NULL,
  `send_on` datetime NOT NULL,
  `sent_at` datetime DEFAULT NULL,
  `custom_message` text NOT NULL,
  `force_notifications` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `repeating` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `modified_by_id` (`modified_by_id`),
  KEY `fk_notification_type_id` (`notification_type_id`),
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`notification_type_id`) REFERENCES `notification_types` (`id`),
  CONSTRAINT `notifications_ibfk_3` FOREIGN KEY (`modified_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_history`
--

DROP TABLE IF EXISTS `notifications_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `notification_type_id` int(11) NOT NULL,
  `send_on` datetime NOT NULL,
  `sent_at` datetime DEFAULT NULL,
  `custom_message` text NOT NULL,
  `force_notifications` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `repeating` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `notification_type_id` (`notification_type_id`),
  KEY `modified_by_id` (`modified_by_id`),
  CONSTRAINT `notifications_history_ibfk_1` FOREIGN KEY (`notification_type_id`) REFERENCES `notification_types` (`id`),
  CONSTRAINT `notifications_history_ibfk_2` FOREIGN KEY (`modified_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_history`
--

LOCK TABLES `notifications_history` WRITE;
/*!40000 ALTER TABLE `notifications_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_labels`
--

DROP TABLE IF EXISTS `object_labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `label_id` (`label_id`,`object_id`,`object_type`),
  KEY `context_id` (`context_id`),
  CONSTRAINT `object_labels_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `object_labels_ibfk_2` FOREIGN KEY (`label_id`) REFERENCES `labels` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_labels`
--

LOCK TABLES `object_labels` WRITE;
/*!40000 ALTER TABLE `object_labels` DISABLE KEYS */;
/*!40000 ALTER TABLE `object_labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_people`
--

DROP TABLE IF EXISTS `object_people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `role` varchar(250) DEFAULT NULL,
  `notes` text NOT NULL,
  `person_id` int(11) NOT NULL,
  `personable_id` int(11) NOT NULL,
  `personable_type` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_object_people` (`person_id`,`personable_id`,`personable_type`),
  KEY `fk_object_people_contexts` (`context_id`),
  KEY `ix_person_id` (`person_id`),
  KEY `ix_object_people_updated_at` (`updated_at`),
  CONSTRAINT `fk_object_people_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `object_people_ibfk_1` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_people`
--

LOCK TABLES `object_people` WRITE;
/*!40000 ALTER TABLE `object_people` DISABLE KEYS */;
/*!40000 ALTER TABLE `object_people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_templates`
--

DROP TABLE IF EXISTS `object_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_templates` (
  `object_template_id` int(11) NOT NULL AUTO_INCREMENT,
  `object_type_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `namespace_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_template_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  KEY `namespace_id` (`namespace_id`),
  KEY `object_type_id` (`object_type_id`),
  CONSTRAINT `object_templates_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `object_templates_ibfk_2` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `object_templates_ibfk_3` FOREIGN KEY (`namespace_id`) REFERENCES `namespaces` (`namespace_id`),
  CONSTRAINT `object_templates_ibfk_4` FOREIGN KEY (`object_type_id`) REFERENCES `object_types` (`object_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_templates`
--

LOCK TABLES `object_templates` WRITE;
/*!40000 ALTER TABLE `object_templates` DISABLE KEYS */;
INSERT INTO `object_templates` VALUES (1,1,'Control','Control',NULL,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL),(2,1,'Objective','Objective',NULL,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL),(3,1,'Assessment','Assessment',NULL,'2018-08-24 09:33:17','2018-08-24 09:33:17',NULL,NULL);
/*!40000 ALTER TABLE `object_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_types`
--

DROP TABLE IF EXISTS `object_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_types` (
  `object_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `display_name` varchar(255) NOT NULL,
  `namespace_id` int(11) DEFAULT NULL,
  `parent_object_type_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_type_id`),
  UNIQUE KEY `name` (`name`,`namespace_id`),
  KEY `created_by_id` (`created_by_id`),
  KEY `updated_by_id` (`updated_by_id`),
  KEY `namespace_id` (`namespace_id`),
  KEY `parent_object_type_id` (`parent_object_type_id`),
  CONSTRAINT `object_types_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `object_types_ibfk_2` FOREIGN KEY (`updated_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `object_types_ibfk_3` FOREIGN KEY (`namespace_id`) REFERENCES `namespaces` (`namespace_id`),
  CONSTRAINT `object_types_ibfk_4` FOREIGN KEY (`parent_object_type_id`) REFERENCES `object_types` (`object_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_types`
--

LOCK TABLES `object_types` WRITE;
/*!40000 ALTER TABLE `object_types` DISABLE KEYS */;
INSERT INTO `object_types` VALUES (1,'basic_type','Basic Object',NULL,NULL,'2018-08-24 09:33:16','2018-08-24 09:33:16',NULL,NULL);
/*!40000 ALTER TABLE `object_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objectives`
--

DROP TABLE IF EXISTS `objectives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `objectives` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `notes` text NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `last_deprecated_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_objectives` (`slug`),
  UNIQUE KEY `uq_t_objectives` (`title`),
  KEY `fk_objectives_contexts` (`context_id`),
  KEY `ix_objectives_updated_at` (`updated_at`),
  CONSTRAINT `objectives_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objectives`
--

LOCK TABLES `objectives` WRITE;
/*!40000 ALTER TABLE `objectives` DISABLE KEYS */;
/*!40000 ALTER TABLE `objectives` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objects_without_revisions`
--

DROP TABLE IF EXISTS `objects_without_revisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `objects_without_revisions` (
  `obj_id` int(11) NOT NULL,
  `obj_type` varchar(45) NOT NULL,
  `action` varchar(15) NOT NULL DEFAULT 'created',
  UNIQUE KEY `uq_new_rev` (`obj_id`,`obj_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `options`
--

DROP TABLE IF EXISTS `options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `role` varchar(250) DEFAULT NULL,
  `title` varchar(250) DEFAULT NULL,
  `required` tinyint(1) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_options_contexts` (`context_id`),
  KEY `ix_options_role` (`role`),
  KEY `ix_options_updated_at` (`updated_at`),
  CONSTRAINT `fk_options_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `options`
--

LOCK TABLES `options` WRITE;
/*!40000 ALTER TABLE `options` DISABLE KEYS */;
INSERT INTO `options` VALUES (1,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','Client List',NULL,NULL),(2,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','Employee List',NULL,NULL),(3,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','Ledger Accounts',NULL,NULL),(4,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','Patents',NULL,NULL),(5,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','Personal Identifiable Info',NULL,NULL),(6,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','Source Code',NULL,NULL),(7,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','asset_type','User Data',NULL,NULL),(8,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','1 Month',NULL,NULL),(9,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','1 Week',NULL,NULL),(10,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','1 Year',NULL,NULL),(11,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','2 Months',NULL,NULL),(12,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','2 Weeks',NULL,NULL),(13,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','3 Months',NULL,NULL),(14,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','4 Months',NULL,NULL),(15,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_duration','6 Months',NULL,NULL),(16,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Ad-Hoc',NULL,NULL),(17,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Annual',NULL,NULL),(18,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Bi-Annual',NULL,NULL),(19,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Continuous',NULL,NULL),(20,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Daily',NULL,NULL),(21,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Hourly',NULL,NULL),(22,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Monthly',NULL,NULL),(23,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Quarterly',NULL,NULL),(24,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Semi-Annual',NULL,NULL),(25,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','audit_frequency','Weekly',NULL,NULL),(27,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','control_kind','Detective',NULL,NULL),(28,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','control_kind','Preventative',NULL,NULL),(38,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','directive_kind','Company Policy',NULL,NULL),(39,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','directive_kind','Data Asset Policy',NULL,NULL),(40,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','directive_kind','Operational Group Policy',NULL,NULL),(41,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','directive_kind','Regulation',NULL,NULL),(42,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_status','active',NULL,NULL),(43,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_status','deprecated',NULL,NULL),(44,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_type','Excel',NULL,NULL),(45,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_type','PDF',NULL,NULL),(46,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_type','Text',NULL,NULL),(47,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_type','URL',NULL,NULL),(48,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_type','Word',NULL,NULL),(49,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1980',NULL,NULL),(50,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1981',NULL,NULL),(51,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1982',NULL,NULL),(52,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1983',NULL,NULL),(53,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1984',NULL,NULL),(54,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1985',NULL,NULL),(55,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1986',NULL,NULL),(56,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1987',NULL,NULL),(57,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1988',NULL,NULL),(58,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1989',NULL,NULL),(59,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1990',NULL,NULL),(60,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1991',NULL,NULL),(61,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1992',NULL,NULL),(62,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1993',NULL,NULL),(63,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1994',NULL,NULL),(64,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1995',NULL,NULL),(65,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1996',NULL,NULL),(66,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1997',NULL,NULL),(67,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1998',NULL,NULL),(68,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','1999',NULL,NULL),(69,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2000',NULL,NULL),(70,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2001',NULL,NULL),(71,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2002',NULL,NULL),(72,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2003',NULL,NULL),(73,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2004',NULL,NULL),(74,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2005',NULL,NULL),(75,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2006',NULL,NULL),(76,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2007',NULL,NULL),(77,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2008',NULL,NULL),(78,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2009',NULL,NULL),(79,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2010',NULL,NULL),(80,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2011',NULL,NULL),(81,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2012',NULL,NULL),(82,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','document_year','2013',0,NULL),(83,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','entity_kind','Not Applicable',NULL,NULL),(84,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','entity_type','Business Unit',NULL,NULL),(85,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','entity_type','Division',NULL,NULL),(86,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','entity_type','Functional Group',NULL,NULL),(87,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','entity_type','Legal Entity',NULL,NULL),(88,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','language','English',NULL,NULL),(89,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Building',NULL,NULL),(90,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','HazMat Storage',NULL,NULL),(91,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Kitchen',NULL,NULL),(92,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Lab',NULL,NULL),(93,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Machine Room',NULL,NULL),(94,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Maintenance Facility',NULL,NULL),(95,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Office',NULL,NULL),(96,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Parking Garage',NULL,NULL),(97,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_kind','Workshop',NULL,NULL),(98,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Colo Data Center',NULL,NULL),(99,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Contract Manufacturer',NULL,NULL),(100,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Data Center',NULL,NULL),(101,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Distribution Center',NULL,NULL),(102,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Headquarters',NULL,NULL),(103,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Regional Office',NULL,NULL),(104,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Sales Office',NULL,NULL),(105,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','location_type','Vendor Worksite',NULL,NULL),(106,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','network_zone','Corp',0,NULL),(107,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','network_zone','Prod',0,NULL),(108,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','person_language','English',NULL,NULL),(109,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','product_kind','Not Applicable',NULL,NULL),(110,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','product_type','Appliance',NULL,NULL),(111,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','product_type','Desktop Software',NULL,NULL),(112,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','product_type','SaaS',NULL,NULL),(113,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','reference_type','Database',NULL,NULL),(114,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','reference_type','Document',NULL,NULL),(115,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','reference_type','Numeric Data',NULL,NULL),(116,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','reference_type','Screenshot',NULL,NULL),(117,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','reference_type','Simple Text',NULL,NULL),(118,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','reference_type','Website',NULL,NULL),(119,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','system_kind','Infrastructure',NULL,NULL),(120,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','system_type','Infrastructure',NULL,NULL),(121,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','threat_type','Insider Threat',NULL,NULL),(122,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','threat_type','Outsider Threat',NULL,NULL),(123,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Bi-Weekly',NULL,NULL),(124,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Yearly',NULL,NULL),(125,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Bi-Monthly',NULL,NULL),(126,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Continuous',NULL,NULL),(127,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Daily',NULL,NULL),(128,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Hourly',NULL,NULL),(129,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Indeterminate',0,NULL),(130,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Monthly',NULL,NULL),(131,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Quarterly',NULL,NULL),(132,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Semi-Annually',NULL,NULL),(133,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Transactional',0,NULL),(134,NULL,'2016-05-03 10:37:02','2016-05-03 10:37:02','','verify_frequency','Weekly',NULL,NULL),(135,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','network_zone','3rd Party',NULL,NULL),(136,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','network_zone','Core',NULL,NULL),(137,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','network_zone','Service',NULL,NULL),(138,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','control_kind','Corrective',NULL,NULL),(139,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','control_means','Technical',NULL,NULL),(140,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','control_means','Administrative',NULL,NULL),(141,NULL,'2018-08-24 09:33:15','2018-08-24 09:33:15','','control_means','Physical',NULL,NULL);
/*!40000 ALTER TABLE `options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `org_groups`
--

DROP TABLE IF EXISTS `org_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `org_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_org_groups` (`slug`),
  UNIQUE KEY `uq_t_org_groups` (`title`),
  KEY `fk_org_groups_contexts` (`context_id`),
  KEY `ix_org_groups_updated_at` (`updated_at`),
  CONSTRAINT `fk_org_groups_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `org_groups`
--

LOCK TABLES `org_groups` WRITE;
/*!40000 ALTER TABLE `org_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `org_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `email` varchar(250) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `language_id` int(11) DEFAULT NULL,
  `company` varchar(250) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_people_email` (`email`),
  KEY `fk_people_contexts` (`context_id`),
  KEY `ix_people_name_email` (`name`,`email`),
  KEY `ix_people_updated_at` (`updated_at`),
  CONSTRAINT `fk_people_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people`
--

LOCK TABLES `people` WRITE;
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` VALUES (1,NULL,'2018-08-24 09:33:17','2018-08-24 09:33:17','migrator@example.com','Default Migrator',NULL,NULL,NULL);
/*!40000 ALTER TABLE `people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_profiles`
--

DROP TABLE IF EXISTS `people_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) DEFAULT NULL,
  `last_seen_whats_new` datetime DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_id` (`person_id`),
  KEY `fk_people_profiles_contexts` (`context_id`),
  KEY `ix_people_profiles_updated_at` (`updated_at`),
  CONSTRAINT `people_profiles_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `people_profiles_ibfk_2` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_profiles`
--

LOCK TABLES `people_profiles` WRITE;
/*!40000 ALTER TABLE `people_profiles` DISABLE KEYS */;
INSERT INTO `people_profiles` VALUES (1,1,'2018-08-10 09:33:18','2018-08-24 09:33:18',NULL,'2018-08-24 09:33:18',NULL);
/*!40000 ALTER TABLE `people_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_groups`
--

DROP TABLE IF EXISTS `product_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `notes` text NOT NULL,
  `slug` varchar(250) NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `test_plan` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_product_groups` (`slug`),
  UNIQUE KEY `uq_t_product_groups` (`title`),
  KEY `fk_product_groups_contexts` (`context_id`),
  KEY `ix_product_groups_updated_at` (`updated_at`),
  CONSTRAINT `product_groups_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_groups`
--

LOCK TABLES `product_groups` WRITE;
/*!40000 ALTER TABLE `product_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `kind_id` int(11) DEFAULT NULL,
  `version` varchar(250) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_products` (`slug`),
  UNIQUE KEY `uq_t_products` (`title`),
  KEY `fk_products_contexts` (`context_id`),
  KEY `ix_products_updated_at` (`updated_at`),
  CONSTRAINT `fk_products_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `kind` varchar(250) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_programs` (`slug`),
  UNIQUE KEY `uq_t_programs` (`title`),
  KEY `fk_programs_contexts` (`context_id`),
  KEY `ix_programs_updated_at` (`updated_at`),
  CONSTRAINT `fk_programs_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programs`
--

LOCK TABLES `programs` WRITE;
/*!40000 ALTER TABLE `programs` DISABLE KEYS */;
/*!40000 ALTER TABLE `programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_projects` (`slug`),
  UNIQUE KEY `uq_t_projects` (`title`),
  KEY `fk_projects_contexts` (`context_id`),
  KEY `ix_projects_updated_at` (`updated_at`),
  CONSTRAINT `fk_projects_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proposals`
--

DROP TABLE IF EXISTS `proposals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proposals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` int(11) NOT NULL,
  `instance_type` varchar(250) NOT NULL,
  `content` longtext NOT NULL,
  `agenda` text NOT NULL,
  `decline_reason` text NOT NULL,
  `decline_datetime` datetime DEFAULT NULL,
  `declined_by_id` int(11) DEFAULT NULL,
  `apply_reason` text NOT NULL,
  `apply_datetime` datetime DEFAULT NULL,
  `applied_by_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `proposed_by_id` int(11) DEFAULT NULL,
  `proposed_notified_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `applied_by_id` (`applied_by_id`),
  KEY `declined_by_id` (`declined_by_id`),
  KEY `proposed_by_id` (`proposed_by_id`),
  KEY `fk_instance` (`instance_id`,`instance_type`),
  KEY `fk_proposal_contexts` (`context_id`),
  KEY `ix_proposal_updated_at` (`updated_at`),
  KEY `ix_decline_datetime` (`decline_datetime`),
  KEY `ix_apply_datetime` (`apply_datetime`),
  KEY `ix_proposed_notified_datetime` (`proposed_notified_datetime`),
  CONSTRAINT `proposals_ibfk_1` FOREIGN KEY (`applied_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `proposals_ibfk_2` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `proposals_ibfk_3` FOREIGN KEY (`declined_by_id`) REFERENCES `people` (`id`),
  CONSTRAINT `proposals_ibfk_4` FOREIGN KEY (`proposed_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proposals`
--

LOCK TABLES `proposals` WRITE;
/*!40000 ALTER TABLE `proposals` DISABLE KEYS */;
/*!40000 ALTER TABLE `proposals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reindex_log`
--

DROP TABLE IF EXISTS `reindex_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reindex_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_reindex_complete` tinyint(1) NOT NULL,
  `log` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reindex_log`
--

LOCK TABLES `reindex_log` WRITE;
/*!40000 ALTER TABLE `reindex_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `reindex_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relationships`
--

DROP TABLE IF EXISTS `relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relationships` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `source_id` int(11) NOT NULL,
  `source_type` varchar(250) NOT NULL,
  `destination_id` int(11) NOT NULL,
  `destination_type` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `automapping_id` int(11) DEFAULT NULL,
  `is_external` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_relationships` (`source_id`,`source_type`,`destination_id`,`destination_type`),
  KEY `fk_relationships_contexts` (`context_id`),
  KEY `ix_relationships_destination` (`destination_type`,`destination_id`),
  KEY `ix_relationships_source` (`source_type`,`source_id`),
  KEY `ix_relationships_updated_at` (`updated_at`),
  KEY `relationships_automapping_parent` (`parent_id`),
  KEY `fk_relationships_automapping_id` (`automapping_id`),
  CONSTRAINT `fk_relationships_automapping_id` FOREIGN KEY (`automapping_id`) REFERENCES `automappings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_relationships_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_relationships_parent_id` FOREIGN KEY (`parent_id`) REFERENCES `relationships` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationships`
--

LOCK TABLES `relationships` WRITE;
/*!40000 ALTER TABLE `relationships` DISABLE KEYS */;
/*!40000 ALTER TABLE `relationships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requirements`
--

DROP TABLE IF EXISTS `requirements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `requirements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `notes` text NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `os_state` varchar(250) NOT NULL,
  `status` varchar(250) NOT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `last_deprecated_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_requirements` (`slug`),
  UNIQUE KEY `uq_t_requirements` (`title`),
  KEY `fk_requirements_contexts` (`context_id`),
  KEY `ix_requirements_updated_at` (`updated_at`),
  CONSTRAINT `requirements_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requirements`
--

LOCK TABLES `requirements` WRITE;
/*!40000 ALTER TABLE `requirements` DISABLE KEYS */;
/*!40000 ALTER TABLE `requirements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revision_refresh_log`
--

DROP TABLE IF EXISTS `revision_refresh_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `revision_refresh_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `run_revision_refresh` tinyint(1) NOT NULL,
  `is_revision_refresh_complete` tinyint(1) NOT NULL,
  `log` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revision_refresh_log`
--

LOCK TABLES `revision_refresh_log` WRITE;
/*!40000 ALTER TABLE `revision_refresh_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `revision_refresh_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revisions`
--

DROP TABLE IF EXISTS `revisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `revisions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_id` int(11) NOT NULL,
  `resource_type` varchar(250) NOT NULL,
  `event_id` int(11) NOT NULL,
  `action` enum('created','modified','deleted') NOT NULL,
  `content` longtext NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `source_type` varchar(250) DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `destination_type` varchar(250) DEFAULT NULL,
  `destination_id` int(11) DEFAULT NULL,
  `resource_slug` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `event_id` (`event_id`),
  KEY `revisions_modified_by` (`modified_by_id`),
  KEY `fk_revisions_contexts` (`context_id`),
  KEY `ix_revisions_updated_at` (`updated_at`),
  KEY `fk_revisions_resource` (`resource_type`,`resource_id`),
  KEY `fk_revisions_source` (`source_type`,`source_id`),
  KEY `fk_revisions_destination` (`destination_type`,`destination_id`),
  KEY `ix_revisions_resource_slug` (`resource_slug`),
  CONSTRAINT `fk_revisions_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `revisions_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`),
  CONSTRAINT `revisions_modified_by` FOREIGN KEY (`modified_by_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revisions`
--

LOCK TABLES `revisions` WRITE;
/*!40000 ALTER TABLE `revisions` DISABLE KEYS */;
/*!40000 ALTER TABLE `revisions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `risk_assessments`
--

DROP TABLE IF EXISTS `risk_assessments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `risk_assessments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` text,
  `notes` text,
  `ra_manager_id` int(11) DEFAULT NULL,
  `ra_counsel_id` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `program_id` int(11) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `test_plan` text,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_slug` (`slug`),
  KEY `fk_risk_assessments_manager_person_id` (`ra_manager_id`),
  KEY `fk_risk_assessments_counsel_person_id` (`ra_counsel_id`),
  KEY `fk_risk_assessments_contexts` (`context_id`),
  KEY `ix_risk_assessments_updated_at` (`updated_at`),
  CONSTRAINT `fk_risk_assessments_counsel_person_id` FOREIGN KEY (`ra_counsel_id`) REFERENCES `people` (`id`),
  CONSTRAINT `fk_risk_assessments_manager_person_id` FOREIGN KEY (`ra_manager_id`) REFERENCES `people` (`id`),
  CONSTRAINT `risk_assessments_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risk_assessments`
--

LOCK TABLES `risk_assessments` WRITE;
/*!40000 ALTER TABLE `risk_assessments` DISABLE KEYS */;
/*!40000 ALTER TABLE `risk_assessments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `risk_objects`
--

DROP TABLE IF EXISTS `risk_objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `risk_objects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `risk_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `risk_id` (`risk_id`,`object_id`,`object_type`),
  KEY `fk_risk_objects_contexts` (`context_id`),
  KEY `ix_risk_id` (`risk_id`),
  CONSTRAINT `risk_objects_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `risk_objects_ibfk_2` FOREIGN KEY (`risk_id`) REFERENCES `risks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risk_objects`
--

LOCK TABLES `risk_objects` WRITE;
/*!40000 ALTER TABLE `risk_objects` DISABLE KEYS */;
/*!40000 ALTER TABLE `risk_objects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `risks`
--

DROP TABLE IF EXISTS `risks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `risks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `title` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `notes` text,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_risks` (`slug`),
  UNIQUE KEY `uq_t_risks` (`title`),
  KEY `fk_risks_contexts` (`context_id`),
  CONSTRAINT `risks_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risks`
--

LOCK TABLES `risks` WRITE;
/*!40000 ALTER TABLE `risks` DISABLE KEYS */;
/*!40000 ALTER TABLE `risks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `permissions_json` text NOT NULL,
  `description` text,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `scope` varchar(64) DEFAULT NULL,
  `role_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_roles_contexts` (`context_id`),
  KEY `ix_roles_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (5,'Reader','CODE DECLARED ROLE','This role grants a user basic, read-only, access permission to a GGRC instance.',NULL,'2018-08-24 09:33:20','2018-08-24 09:33:20',NULL,'System',5),(6,'Editor','CODE DECLARED ROLE','Global Editor',NULL,'2018-08-24 09:33:20','2018-08-24 09:33:20',NULL,'System',6),(8,'Administrator','CODE DECLARED ROLE','System Administrator with super-user privileges',NULL,'2018-08-24 09:33:20','2018-08-24 09:33:20',NULL,'Admin',8),(17,'Creator','CODE DECLARED ROLE','Global creator',NULL,'2018-08-24 09:33:20','2018-08-24 09:33:20',NULL,'System',4);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `notes` text NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `last_deprecated_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sections` (`slug`),
  UNIQUE KEY `uq_t_sections` (`title`),
  KEY `fk_sections_contexts` (`context_id`),
  KEY `ix_sections_updated_at` (`updated_at`),
  CONSTRAINT `fk_sections_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `snapshots`
--

DROP TABLE IF EXISTS `snapshots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snapshots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `parent_type` varchar(250) NOT NULL,
  `child_id` int(11) NOT NULL,
  `child_type` varchar(250) NOT NULL,
  `revision_id` int(11) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `parent_type` (`parent_type`,`parent_id`,`child_type`,`child_id`),
  KEY `revision_id` (`revision_id`),
  KEY `ix_snapshots_parent` (`parent_type`,`parent_id`),
  KEY `ix_snapshots_child` (`child_type`,`child_id`),
  KEY `fk_snapshots_contexts` (`context_id`),
  KEY `ix_snapshots_updated_at` (`updated_at`),
  KEY `fk_snapshots_audits` (`parent_id`),
  CONSTRAINT `fk_snapshots_audits` FOREIGN KEY (`parent_id`) REFERENCES `audits` (`id`) ON DELETE CASCADE,
  CONSTRAINT `snapshots_ibfk_1` FOREIGN KEY (`revision_id`) REFERENCES `revisions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `snapshots`
--

LOCK TABLES `snapshots` WRITE;
/*!40000 ALTER TABLE `snapshots` DISABLE KEYS */;
/*!40000 ALTER TABLE `snapshots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `systems`
--

DROP TABLE IF EXISTS `systems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `systems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `infrastructure` tinyint(1) DEFAULT NULL,
  `is_biz_process` tinyint(1) DEFAULT NULL,
  `version` varchar(250) DEFAULT NULL,
  `notes` text NOT NULL,
  `network_zone_id` int(11) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_systems` (`slug`),
  UNIQUE KEY `uq_t_systems` (`title`),
  KEY `fk_systems_contexts` (`context_id`),
  KEY `ix_systems_is_biz_process` (`is_biz_process`),
  KEY `ix_systems_updated_at` (`updated_at`),
  CONSTRAINT `fk_systems_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `systems`
--

LOCK TABLES `systems` WRITE;
/*!40000 ALTER TABLE `systems` DISABLE KEYS */;
/*!40000 ALTER TABLE `systems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_group_objects`
--

DROP TABLE IF EXISTS `task_group_objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_group_objects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_group_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  `object_type` varchar(250) NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_group_id` (`task_group_id`,`object_id`,`object_type`),
  KEY `fk_task_group_objects_contexts` (`context_id`),
  KEY `ix_task_group_id` (`task_group_id`),
  KEY `ix_task_group_objects_updated_at` (`updated_at`),
  CONSTRAINT `fk_task_group_objects_context_id` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_task_group_objects_task_group_id` FOREIGN KEY (`task_group_id`) REFERENCES `task_groups` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_group_objects`
--

LOCK TABLES `task_group_objects` WRITE;
/*!40000 ALTER TABLE `task_group_objects` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_group_objects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_group_tasks`
--

DROP TABLE IF EXISTS `task_group_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_group_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_group_id` int(11) NOT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `sort_index` varchar(250) NOT NULL,
  `description` text,
  `title` varchar(250) NOT NULL,
  `relative_end_day` int(11) DEFAULT NULL,
  `relative_end_month` int(11) DEFAULT NULL,
  `relative_start_day` int(11) DEFAULT NULL,
  `relative_start_month` int(11) DEFAULT NULL,
  `object_approval` tinyint(1) NOT NULL,
  `response_options` text NOT NULL,
  `task_type` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_slug` (`slug`),
  KEY `fk_task_group_tasks_contexts` (`context_id`),
  KEY `ix_task_group_tasks_updated_at` (`updated_at`),
  KEY `fk_task_group_tasks_task_group_id` (`task_group_id`),
  CONSTRAINT `fk_task_group_tasks_context_id` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_task_group_tasks_task_group_id` FOREIGN KEY (`task_group_id`) REFERENCES `task_groups` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_group_tasks`
--

LOCK TABLES `task_group_tasks` WRITE;
/*!40000 ALTER TABLE `task_group_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_group_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_groups`
--

DROP TABLE IF EXISTS `task_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `description` text,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `lock_task_order` tinyint(1) DEFAULT NULL,
  `sort_index` varchar(250) NOT NULL,
  `secondary_contact_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_task_groups` (`slug`),
  KEY `fk_task_groups_contact` (`contact_id`),
  KEY `fk_task_groups_contexts` (`context_id`),
  KEY `ix_task_groups_updated_at` (`updated_at`),
  KEY `fk_task_groups_secondary_contact` (`secondary_contact_id`),
  KEY `fk_task_groups_workflow_id` (`workflow_id`),
  CONSTRAINT `fk_task_groups_contact_id` FOREIGN KEY (`contact_id`) REFERENCES `people` (`id`),
  CONSTRAINT `fk_task_groups_context_id` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_task_groups_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `workflows` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_groups`
--

LOCK TABLES `task_groups` WRITE;
/*!40000 ALTER TABLE `task_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `technology_environments`
--

DROP TABLE IF EXISTS `technology_environments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `technology_environments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `notes` text NOT NULL,
  `slug` varchar(250) NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `test_plan` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_technology_environments` (`slug`),
  UNIQUE KEY `uq_t_technology_environments` (`title`),
  KEY `fk_technology_environments_contexts` (`context_id`),
  KEY `ix_technology_environments_updated_at` (`updated_at`),
  CONSTRAINT `technology_environments_ibfk_1` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `technology_environments`
--

LOCK TABLES `technology_environments` WRITE;
/*!40000 ALTER TABLE `technology_environments` DISABLE KEYS */;
/*!40000 ALTER TABLE `technology_environments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threats`
--

DROP TABLE IF EXISTS `threats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(250) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_t_actors` (`title`),
  UNIQUE KEY `uq_threats` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threats`
--

LOCK TABLES `threats` WRITE;
/*!40000 ALTER TABLE `threats` DISABLE KEYS */;
/*!40000 ALTER TABLE `threats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_context_person` (`role_id`,`context_id`,`person_id`),
  KEY `fk_user_roles_contexts` (`context_id`),
  KEY `ix_user_roles_person` (`person_id`),
  KEY `ix_user_roles_updated_at` (`updated_at`),
  CONSTRAINT `fk_user_roles_contexts` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (2,6,NULL,'2018-08-24 09:33:20','2018-08-24 09:33:20',NULL,1);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendors`
--

DROP TABLE IF EXISTS `vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modified_by_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `description` text NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `slug` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `notes` text NOT NULL,
  `status` varchar(250) NOT NULL DEFAULT 'Draft',
  `os_state` varchar(16) NOT NULL DEFAULT 'Unreviewed',
  `recipients` varchar(250) DEFAULT NULL,
  `send_by_default` tinyint(1) DEFAULT NULL,
  `test_plan` text NOT NULL,
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_vendors_title` (`title`),
  UNIQUE KEY `uq_slug_vendors` (`slug`),
  KEY `fk_vendors_context` (`context_id`),
  KEY `fk_vendors_modified_by` (`modified_by_id`),
  KEY `fk_vendors_status` (`status`),
  KEY `ix_vendors_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendors`
--

LOCK TABLES `vendors` WRITE;
/*!40000 ALTER TABLE `vendors` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_people`
--

DROP TABLE IF EXISTS `workflow_people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `workflow_id` (`workflow_id`,`person_id`),
  KEY `fk_workflow_people_contexts` (`context_id`),
  KEY `ix_person_id` (`person_id`),
  KEY `ix_workflow_id` (`workflow_id`),
  KEY `ix_workflow_people_updated_at` (`updated_at`),
  CONSTRAINT `fk_workflow_people_context_id` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`),
  CONSTRAINT `fk_workflow_people_person_id` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),
  CONSTRAINT `fk_workflow_people_workflow_id` FOREIGN KEY (`workflow_id`) REFERENCES `workflows` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_people`
--

LOCK TABLES `workflow_people` WRITE;
/*!40000 ALTER TABLE `workflow_people` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflows`
--

DROP TABLE IF EXISTS `workflows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflows` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `end_date` date DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `description` text,
  `title` varchar(250) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_by_id` int(11) DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `context_id` int(11) DEFAULT NULL,
  `frequency` varchar(250) DEFAULT NULL,
  `notify_custom_message` text,
  `notify_on_change` tinyint(1) NOT NULL,
  `object_approval` tinyint(1) NOT NULL,
  `next_cycle_start_date` date DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `recurrences` tinyint(1) NOT NULL,
  `non_adjusted_next_cycle_start_date` date DEFAULT NULL,
  `is_old_workflow` tinyint(1) DEFAULT NULL,
  `kind` varchar(250) DEFAULT NULL,
  `is_verification_needed` tinyint(1) NOT NULL,
  `repeat_every` int(11) DEFAULT NULL,
  `unit` enum('day','week','month') DEFAULT NULL,
  `repeat_multiplier` int(11) NOT NULL DEFAULT '0',
  `folder` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_workflows` (`slug`),
  KEY `fk_workflows_contexts` (`context_id`),
  KEY `ix_workflows_updated_at` (`updated_at`),
  KEY `ix_workflows_unit` (`unit`),
  CONSTRAINT `fk_workflows_context_id` FOREIGN KEY (`context_id`) REFERENCES `contexts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflows`
--

LOCK TABLES `workflows` WRITE;
/*!40000 ALTER TABLE `workflows` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflows` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-24  9:34:31
