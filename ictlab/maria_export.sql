-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.1.22-MariaDB-1~jessie - mariadb.org binary distribution
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for chibb
CREATE DATABASE IF NOT EXISTS `chibb` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `chibb`;

-- Dumping structure for table chibb.Node
CREATE TABLE IF NOT EXISTS `Node` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(32) NOT NULL,
  `Loc_x` float NOT NULL DEFAULT '-1',
  `Loc_y` float NOT NULL DEFAULT '-1',
  `Loc_z` float NOT NULL DEFAULT '-1',
  `NodeParent` int(11) DEFAULT '6',
  `Enabled` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`ID`),
  KEY `FK_Node_Node` (`NodeParent`),
  CONSTRAINT `FK_Node_Node` FOREIGN KEY (`NodeParent`) REFERENCES `Node` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table chibb.Node: ~7 rows (approximately)
/*!40000 ALTER TABLE `Node` DISABLE KEYS */;
INSERT INTO `Node` (`ID`, `Name`, `Loc_x`, `Loc_y`, `Loc_z`, `NodeParent`, `Enabled`) VALUES
	(1, 'Hallway', -1, -1, -1, 6, 1),
	(2, 'LivingRoom', -1, -1, -1, 6, 1),
	(3, 'Kitchen', -1, -1, -1, 6, 1),
	(4, 'Bedroom', -1, -1, -1, 6, 1),
	(5, 'Bathroom', -1, -1, -1, 6, 1),
	(6, 'Unassigned', -1, -1, -1, 6, 1),
	(7, 'TestNode', -1, -1, -1, 1, 1);
/*!40000 ALTER TABLE `Node` ENABLE KEYS */;

-- Dumping structure for table chibb.Sensor
CREATE TABLE IF NOT EXISTS `Sensor` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `AccessToken` char(32) NOT NULL,
  `Name` varchar(32) NOT NULL,
  `Enabled` tinyint(1) NOT NULL DEFAULT '1',
  `Type` int(11) NOT NULL DEFAULT '4',
  `NodeParent` int(11) NOT NULL DEFAULT '6',
  `LastUpdate` datetime DEFAULT NULL,
  `LastValue` double DEFAULT NULL,
  `Loc_x` float NOT NULL DEFAULT '-1',
  `Loc_y` float NOT NULL DEFAULT '-1',
  `Loc_z` float NOT NULL DEFAULT '-1',
  `Description` varchar(254) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`),
  KEY `FK_Sensor_Sensor_Type` (`Type`),
  KEY `FK_Sensor_Node` (`NodeParent`),
  CONSTRAINT `FK_Sensor_Node` FOREIGN KEY (`NodeParent`) REFERENCES `Node` (`ID`),
  CONSTRAINT `FK_Sensor_Sensor_Type` FOREIGN KEY (`Type`) REFERENCES `Sensor_Type` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table chibb.Sensor: ~35 rows (approximately)
/*!40000 ALTER TABLE `Sensor` DISABLE KEYS */;
INSERT INTO `Sensor` (`ID`, `AccessToken`, `Name`, `Enabled`, `Type`, `NodeParent`, `LastUpdate`, `LastValue`, `Loc_x`, `Loc_y`, `Loc_z`, `Description`) VALUES
	(1, 'H5v37GXVK7ZXZpKFj5MmPB2HGopukmEv', 'Heater_temperature', 1, 3, 1, '2017-06-07 19:08:22', 20, -1, -1, -1, ''),
	(2, '8KZj6keenZCRjB4uXtAcVakiMB7HAO5w', 'Clock', 0, 4, 6, '2017-06-07 18:49:18', 1483372800, -1, -1, -1, ''),
	(3, 'zXKhTpgSm8w3YF2DcWvP6AN4fwlmFrvN', 'hallway_heater_0', 1, 1, 1, '2017-06-07 19:08:22', 2200, -1, -1, -1, ''),
	(4, 'i45f9twmWHHFHtH0kyqws7N9I49feMFf', 'hallway_light_0', 1, 1, 1, '2017-06-07 19:07:15', 9, -1, -1, -1, 'test2'),
	(5, 'xv7j0QuZfRxPEptI29ppkRGBFbAEu99p', 'hallway_light_1', 1, 1, 1, '2017-06-07 19:07:15', 9, -1, -1, -1, ''),
	(6, 'SbqJgQO9POeyUGu5cEFRTcco84Og0MMi', 'hallway_light_2', 1, 1, 1, '2017-06-07 19:07:15', 9, -1, -1, -1, ''),
	(7, 'UJwzi6sp1ut2N3QX0PtuS0t1LOCjNZfE', 'living_room_tv_0', 0, 1, 2, '0000-00-00 00:00:00', NULL, -1, -1, -1, ''),
	(8, 'JbpkrIAixRVRth4L1iDKn3QMgGuoNUDs', 'living_room_light_0', 1, 1, 2, '2017-06-07 19:08:22', 9, -1, -1, -1, ''),
	(9, 'ZfIKeWLk02nTGR27CB1o6FJBewbLFEpF', 'living_room_light_1', 1, 1, 2, '2017-06-07 19:08:22', 9, -1, -1, -1, ''),
	(10, 'NWx6RrxnYMhIiHfSgYi6vXj3zEyeqSFp', 'living_room_light_2', 1, 1, 2, '2017-06-07 19:08:22', 9, -1, -1, -1, ''),
	(11, 'ZtkQcDyy1EMqXR4wPUX0zrkfD98zFU8i', 'living_room_light_3', 1, 1, 2, '2017-06-07 19:08:22', 9, -1, -1, -1, ''),
	(12, 'ygjj3aR7ugjWlPRhRUSFwfa4OSPXUfaQ', 'living_room_light_4', 1, 1, 2, '2017-06-07 19:08:22', 9, -1, -1, -1, ''),
	(13, 'UgP4yM9fbLeefB8g6kmRNSQErZA0Ifll', 'living_room_light_5', 1, 1, 2, '2017-06-07 19:08:22', 9, -1, -1, -1, ''),
	(14, 'TgHGKRZq2JwWILFcfPShVfccKf4otfLl', 'bedroom_light_0', 1, 1, 4, '2017-06-07 19:03:55', 9, -1, -1, -1, ''),
	(15, 'ihf1YOm6ycWbB3gSyvFDlPwGaCQfrj9s', 'bedroom_light_1', 1, 1, 4, '2017-06-07 19:03:55', 9, -1, -1, -1, ''),
	(16, 'hxKFVEr1uejFFE0WqJXyYTjUsJjMRe8f', 'bedroom_light_2', 1, 1, 4, '2017-06-07 19:03:55', 9, -1, -1, -1, ''),
	(17, 'u84YlRSMmooiGNaaD6wjPWiyUagAEDjM', 'bedroom_light_3', 1, 1, 4, '2017-06-07 19:03:55', 9, -1, -1, -1, ''),
	(18, 'n6A5lZ7QBTy1xWxtW0gDFImHO1OgmKJo', 'bedroom_light_4', 1, 1, 4, '2017-06-07 19:03:55', 9, -1, -1, -1, ''),
	(19, 'MQ7oAZ2RgXTSQs3zLHraypIUKbM8qDuZ', 'bedroom_tv_0', 1, 1, 4, '0000-00-00 00:00:00', NULL, -1, -1, -1, ''),
	(20, 'sECm9XrJcK1Zkhp3qHRSbhM2rMQ1iLkj', 'kitchen_light_0', 1, 1, 3, '2017-06-07 19:07:23', 9, -1, -1, -1, ''),
	(21, 'cVZo3x1uI4SQHgetpOrTmU0DpEvRj1R2', 'kitchen_light_1', 1, 1, 3, '2017-06-07 19:07:23', 9, -1, -1, -1, ''),
	(22, 'fDZnDnooLMsp0FMFFcqQs0VAeVCzzxP1', 'kitchen_light_2', 1, 1, 3, '2017-06-07 19:07:23', 9, -1, -1, -1, ''),
	(23, '6qp3KmYNv9JzSSrAYCr24sghEngMDL9O', 'kitchen_light_3', 1, 1, 3, '2017-06-07 19:07:23', 9, -1, -1, -1, ''),
	(24, 'gDiYZuJ0CsZJ9vNuPN37fIVcfn3W5ZJW', 'kitchen_light_4', 1, 1, 3, '2017-06-07 19:07:23', 9, -1, -1, -1, ''),
	(25, 'ikFXKwLprBHsaDqm0jr6KBlbTusC4LTL', 'kitchen_stove_0', 1, 1, 3, '2017-06-07 19:07:21', 1200, -1, -1, -1, ''),
	(26, 'J9LpL5c5Gg7i1wUkuWclHhYfUWSCVLHj', 'kitchen_microwave_0', 1, 1, 3, '0000-00-00 00:00:00', NULL, -1, -1, -1, ''),
	(27, 'zjAwvXTAVBcYPFakk2qrHaK9CbUl6Jho', 'bathroom_shower_0', 1, 1, 5, '2017-06-07 19:03:49', 150, -1, -1, -1, ''),
	(28, 'qzI42glUj60H0e7g6nVjuYtheaaMeDYC', 'bathroom_bath_0', 0, 1, 5, '0000-00-00 00:00:00', NULL, -1, -1, -1, ''),
	(29, 'NQeu9RzTqKXzzq7CmCoEDt9ULrt6q4z1', 'bathroom_light_0', 1, 1, 5, '2017-06-07 19:08:19', 9, -1, -1, -1, ''),
	(30, 'DkP9PVlY61qTjyAvsgHSeHSfoaQzfy86', 'bathroom_light_1', 1, 1, 5, '2017-06-07 19:08:19', 9, -1, -1, -1, ''),
	(31, 'JgcVj2Opl3VGvhh8RRzVMH5RlafKQCIn', 'bathroom_light_2', 1, 1, 5, '2017-06-07 19:08:19', 9, -1, -1, -1, ''),
	(32, 'migS9gOy3GG4aHDxEQ2QSIApTvXpTOXY', 'bathroom_light_3', 1, 1, 5, '2017-06-07 19:08:19', 9, -1, -1, -1, ''),
	(33, '2afrNNCl12ENyCFTm3MXJq1aU0iAoebq', 'bathroom_toilet_0', 1, 2, 5, '2017-06-07 19:08:18', 6, -1, -1, -1, ''),
	(34, 'V6qlCwTgPLjDf11GN8WeZGBx5Ws4uovM', 'bathroom_shower_0', 1, 2, 5, '2017-06-07 19:03:49', 8, -1, -1, -1, ''),
	(35, 'CqAnOH5XqVeUoefKZODeiKPvgg21JBBh', 'bathroom_bath_0', 0, 2, 5, '0000-00-00 00:00:00', NULL, -1, -1, -1, '');
/*!40000 ALTER TABLE `Sensor` ENABLE KEYS */;

-- Dumping structure for table chibb.Sensor_Type
CREATE TABLE IF NOT EXISTS `Sensor_Type` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Description` varchar(32) NOT NULL DEFAULT '0',
  `Color` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table chibb.Sensor_Type: ~4 rows (approximately)
/*!40000 ALTER TABLE `Sensor_Type` DISABLE KEYS */;
INSERT INTO `Sensor_Type` (`ID`, `Description`, `Color`) VALUES
	(1, 'PowerMeter', 16776960),
	(2, 'WaterMeter', 65535),
	(3, 'Temperature', 16711680),
	(4, 'Unassigned', 0);
/*!40000 ALTER TABLE `Sensor_Type` ENABLE KEYS */;

-- Dumping structure for table chibb.Sensor_Unregistered
CREATE TABLE IF NOT EXISTS `Sensor_Unregistered` (
  `RegisterToken` char(7) NOT NULL,
  `Expiration` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Name` varchar(32) NOT NULL,
  `Type` int(11) DEFAULT NULL,
  `NodeParent` int(11) NOT NULL,
  `Loc_x` float NOT NULL,
  `Loc_y` float NOT NULL,
  `Loc_z` float NOT NULL,
  `Description` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table chibb.Sensor_Unregistered: ~0 rows (approximately)
/*!40000 ALTER TABLE `Sensor_Unregistered` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sensor_Unregistered` ENABLE KEYS */;

-- Dumping structure for table chibb.User
CREATE TABLE IF NOT EXISTS `User` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `AccessToken` varchar(32) NOT NULL,
  `EmailAddress` varchar(254) NOT NULL,
  `PasswordHash` char(64) NOT NULL,
  `UserType` tinyint(4) NOT NULL,
  `LastLogin` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table chibb.User: ~8 rows (approximately)
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` (`ID`, `AccessToken`, `EmailAddress`, `PasswordHash`, `UserType`, `LastLogin`) VALUES
	(1, 'Vwxyercfi9W84fGW9tWcrOJVS08ledW5', 'someone@example.com', 'mypass', 0, NULL),
	(2, 'b3cbbdfb5c670117a18cc2a5cbabe4e1', 'someone2@example.com', '123', 0, '2017-06-09 00:41:00'),
	(3, '', 'someone3@example.com', '123', 0, NULL),
	(4, '', 'someone@example.nl', '123', 0, NULL),
	(5, '', 'someone2@example.nl', '123', 0, NULL),
	(6, '', 'someone3@example.nl', '123', 0, NULL),
	(7, '', 'someone4@example.nl', '123', 0, NULL),
	(8, '', 'someone11@example.com', '123', 0, NULL);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;

-- Dumping structure for view chibb.Sensors
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `Sensors` (
	`AccessToken` CHAR(32) NOT NULL COLLATE 'utf8mb4_general_ci',
	`SensorName` VARCHAR(32) NOT NULL COLLATE 'utf8mb4_general_ci',
	`Enabled` TINYINT(1) NOT NULL,
	`LastUpdate` DATETIME NULL,
	`LastValue` DOUBLE NULL,
	`Loc_x` FLOAT NOT NULL,
	`Loc_y` FLOAT NOT NULL,
	`Loc_z` FLOAT NOT NULL,
	`SensorDescription` VARCHAR(254) NOT NULL COLLATE 'utf8mb4_general_ci',
	`SensorType` VARCHAR(32) NOT NULL COLLATE 'utf8mb4_general_ci',
	`TypeColor` INT(11) NOT NULL,
	`ParentName` VARCHAR(32) NOT NULL COLLATE 'utf8mb4_general_ci'
) ENGINE=MyISAM;

-- Dumping structure for procedure chibb.INSTANCE_EDIT
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSTANCE_EDIT`(
	IN `sensorID` INT,
	IN `nodeID` INT,
	IN `newName` VARCHAR(32),
	IN `newEnabled` TINYINT(1),
	IN `newX` FLOAT,
	IN `newY` FLOAT,
	IN `newZ` FLOAT,
	IN `newDesc` VARCHAR(256),
	IN `newType` VARCHAR(32)

)
BEGIN
	IF(nodeID < 0 && sensorID < 0) THEN
		SIGNAL SQLSTATE '50001' SET MESSAGE_TEXT='Invalid arguments';
	END IF;
	
	IF(sensorID > 0) THEN
		UPDATE Sensor as s SET s.Name = newName, s.Enabled = newEnabled, s.Loc_x = newX, s.Loc_y = newY, s.Loc_z = newZ, s.Description = newDesc, s.`Type` = (SELECT t.ID FROM Sensor_Type as t WHERE t.Description = newType LIMIT 1) WHERE s.ID = sensorID;
	ELSE
		UPDATE Node as n SET n.Name = newName, n.Loc_x = newX,n.Loc_y = newY, n.Loc_z = newZ, n.Enabled = newEnabled WHERE n.ID = nodeID;
	END IF;

END//
DELIMITER ;

-- Dumping structure for procedure chibb.INSTANCE_GET_ALL
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSTANCE_GET_ALL`()
BEGIN
	SELECT 
	s.ID as SensorID, 
	s.Name as SensorName, 
	s.Enabled as SensorEnabled, 
	s.LastUpdate, s.LastValue, 
	s.Loc_x, s.Loc_y, s.Loc_z, s.Description,
	n.ID as NodeID, 
	n.Name as NodeName, 
	n.Enabled as NodeEnabled,
	t.Description as 'Type', t.Color,
	CASE 
		WHEN TIMESTAMPDIFF(MINUTE, s.LastUpdate, CURRENT_TIMESTAMP()) < 3 THEN 'Active'
		WHEN TIMESTAMPDIFF(MINUTE, s.LastUpdate, CURRENT_TIMESTAMP()) < 30 THEN 'Intermittent Failures'
		ELSE 'Inactive'
	END
	AS Status 
	FROM Sensor AS s
	INNER JOIN Node AS n
	ON n.ID = s.NodeParent
	INNER JOIN Sensor_Type as t
	ON t.ID = s.`Type`
	ORDER BY n.ID, s.NodeParent, s.Name, t.ID;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.INSTANCE_REMOVE
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `INSTANCE_REMOVE`(
	IN `instanceID` INT
,
	IN `instanceType` ENUM('Sensor','Node')
)
BEGIN
	IF (instanceType = 'Sensor') THEN
		DELETE FROM Sensor WHERE ID = instanceID;
	ELSE 
		DELETE FROM Node WHERE ID = instanceID;
	END IF;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.NODE_GETALL_NAME
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `NODE_GETALL_NAME`()
BEGIN
	SELECT Name 
	FROM Node;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.SENSOR_GET
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `SENSOR_GET`(
	IN `access_token` VARCHAR(64)


)
    COMMENT 'Gets one single sensor filtered on access token'
BEGIN
	SELECT s.SensorName as Name, s.ParentName as Location, s.Enabled, s.SensorType as Type, s.LastUpdate, s.LastValue
	FROM Sensors as s
	
	WHERE s.AccessToken = access_token;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.SENSOR_GET_AS_ENTITY
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `SENSOR_GET_AS_ENTITY`()
BEGIN
	SELECT s.SensorName, s.Loc_x, s.Loc_y, s.Loc_z, s.SensorType, s.TypeColor, s.ParentName
	FROM Sensors as s;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.SENSOR_REGISTER
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `SENSOR_REGISTER`(
	IN `token` CHAR(7),
	IN `name` VARCHAR(32),
	IN `type` VARCHAR(32),
	IN `parent` VARCHAR(32),
	IN `loc_x` FLOAT,
	IN `loc_y` FLOAT,
	IN `loc_z` FLOAT,
	IN `description` VARCHAR(254)



)
BEGIN

SET @sensorParent = (SELECT p.ID FROM Node as p WHERE p.Name = parent);
SET @sensorType = (SELECT t.ID FROM Sensor_Type as t WHERE t.Description = type);

INSERT INTO Sensor_Unregistered(RegisterToken, Name, Type, NodeParent, Loc_x, Loc_y, Loc_z, Description, Expiration) 
VALUES(token, name, @sensorType, @sensorParent, loc_x, loc_y, loc_z, description, NOW()+100);
END//
DELIMITER ;

-- Dumping structure for procedure chibb.SENSOR_TYPE_GETALL_DESCRIPTION
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `SENSOR_TYPE_GETALL_DESCRIPTION`()
BEGIN
	SELECT Description FROM Sensor_Type;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.SENSOR_UPDATE
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `SENSOR_UPDATE`(
	IN `access_token` VARCHAR(64),
	IN `value` FLOAT

)
    COMMENT 'Updates a sensor with a value'
BEGIN
	SET @parent = (SELECT s.NodeParent FROM Sensor as s WHERE s.AccessToken = access_token);
	IF NODE_IS_PARENT_ENABLED(@parent) AND (SELECT Enabled = 1 FROM Sensor as s WHERE s.AccessToken = access_token) THEN
		UPDATE Sensor as s
		SET s.LastUpdate = NOW(), LastValue = value
		WHERE s.AccessToken = access_token;
	END IF;
END//
DELIMITER ;

-- Dumping structure for procedure chibb.USER_INSERT
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `USER_INSERT`(
	IN `email` VARCHAR(254),
	IN `password` CHAR(64),
	IN `role` VARCHAR(50)

)
BEGIN
	IF (SELECT COUNT(*) FROM User WHERE EmailAddress = email) > 0 THEN
		SIGNAL SQLSTATE '50000' SET MESSAGE_TEXT = 'Email address already registered';
	ELSE
		INSERT INTO User (EmailAddress, PasswordHash, UserType, AccessToken) VALUES (email, password, role, '');
	END IF;
END//
DELIMITER ;

-- Dumping structure for function chibb.NODE_IS_PARENT_ENABLED
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `NODE_IS_PARENT_ENABLED`(
	`paramNodeID` INT


) RETURNS bit(1)
BEGIN

	SET @enabled := (SELECT n.Enabled FROM Node as n WHERE paramNodeID = n.ID);
	SET @parent := (SELECT n.NodeParent FROM Node as n WHERE paramNodeID = n.ID);
	
	WHILE TRUE DO
		SET @enabled := (SELECT n.Enabled FROM Node as n WHERE n.ID = @parent);
		SET @parent := (SELECT n.NodeParent FROM Node as n WHERE n.ID = @parent);
		
		IF @enabled = 0 THEN
			RETURN 0;
		END IF;
	
		IF @parent IS NULL OR @parent = 6 THEN
			RETURN 1;
		END IF;
	END WHILE;
END//
DELIMITER ;

-- Dumping structure for function chibb.RANDHASH
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `RANDHASH`(
	`seed` DOUBLE


) RETURNS char(64) CHARSET utf8mb4
BEGIN
	RETURN SHA2(CAST(UNIX_TIMESTAMP(NOW(4))*seed as CHAR), 256);	
END//
DELIMITER ;

-- Dumping structure for function chibb.SENSOR_VERIFY
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `SENSOR_VERIFY`(
	`token` CHAR(7)








) RETURNS char(64) CHARSET utf8mb4
BEGIN
	SET @dt = (SELECT u.Expiration FROM Sensor_Unregistered AS u WHERE u.RegisterToken = token);
	
	# Checks if a sensor is actually present.
	IF (@dt = NULL) THEN
		SIGNAL SQLSTATE '50002' SET MESSAGE_TEXT='Invalid Data';
	END IF;
	
	
	# Checks if the verification is done in time.
	# Throws an error if not
	IF (TIMESTAMPDIFF(SECOND, NOW(),@dt) > SEC_TO_TIME(90) ) THEN
		DELETE FROM Sensor_Unregistered WHERE RegisterToken = token;
		SIGNAL SQLSTATE '50003' SET MESSAGE_TEXT='Sensor verification time limit has expired';
	ELSE
	#	 Generates an access token based on ID and
		# moves the record to the Sensor table
		SET @uid = (SELECT MAX(ID)+1 FROM Sensor);
		SET @accTok = (RANDHASH(@uid));
		INSERT INTO Sensor(Accesstoken, Name, `Type`, NodeParent, Loc_x, Loc_y, Loc_z, Description, Enabled)
				SELECT @accTok, u.Name, u.`Type`, u.NodeParent, u.Loc_x, u.Loc_y, u.Loc_z, u.Description, 1
				FROM Sensor_Unregistered as u WHERE u.Registertoken = token;
		DELETE FROM Sensor_Unregistered WHERE RegisterToken = token;
		RETURN @accToken;
	END IF;
	
END//
DELIMITER ;

-- Dumping structure for function chibb.USER_LOGIN
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `USER_LOGIN`(
	`email` VARCHAR(254),
	`password` VARCHAR(32)




) RETURNS char(32) CHARSET utf8mb4
BEGIN
	IF(EXISTS(SELECT * FROM User WHERE EmailAddress = email AND PasswordHash = password)) THEN
		SET @uid = (SELECT ID FROM User WHERE EmailAddress = email AND PasswordHash = password);
		SET @accTok = (SELECT RANDHASH(@uid));
		UPDATE User SET AccessToken = @accTok, LastLogin = NOW() WHERE EmailAddress = email AND PasswordHash = password;
		RETURN @accTok;
	ELSE
		SIGNAL SQLSTATE '50001' SET MESSAGE_TEXT='No user registered with email';
	END IF;
END//
DELIMITER ;

-- Dumping structure for view chibb.Sensors
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `Sensors`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `Sensors` AS select `s`.`AccessToken` AS `AccessToken`,`s`.`Name` AS `SensorName`,`s`.`Enabled` AS `Enabled`,`s`.`LastUpdate` AS `LastUpdate`,`s`.`LastValue` AS `LastValue`,`s`.`Loc_x` AS `Loc_x`,`s`.`Loc_y` AS `Loc_y`,`s`.`Loc_z` AS `Loc_z`,`s`.`Description` AS `SensorDescription`,`t`.`Description` AS `SensorType`,`t`.`Color` AS `TypeColor`,`n`.`Name` AS `ParentName` from ((`Sensor` `s` join `Sensor_Type` `t` on((`s`.`Type` = `t`.`ID`))) join `Node` `n` on((`s`.`NodeParent` = `n`.`ID`)));

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
