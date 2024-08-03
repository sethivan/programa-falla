DROP PROCEDURE IF EXISTS sp.calculateFallaYear;

DELIMITER $$
$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`calculateFallaYear`(OUT vSelf INT)
BEGIN
	DECLARE vDate DATETIME;
	DECLARE vDay INT;
    DECLARE vMonth INT;
    DECLARE vYear INT;
   
	SET vDate = NOW();
	SET vDay = DAY(vDate);
    SET vMonth = MONTH(vDate);
    SET vYear = YEAR(vDate);
   
   	CASE
	   	WHEN vMonth > 3 THEN
	   		SET vSelf = vYear + 1;
	   	WHEN vMonth < 2 THEN
	   		SET vSelf = vYear;
	   	WHEN vMonth = 3 AND vDay > 19 THEN 
	   		SET vSelf = vYear + 1;
	   	WHEN vMonth = 3 AND vDay <= 19 THEN
	   		SET vSelf = vYear;
	END CASE;
END
$$
DELIMITER ;