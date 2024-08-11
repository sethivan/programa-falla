DROP PROCEDURE IF EXISTS sp.calculateMemberFallaAge;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`calculateMemberFallaAge`(IN vBirthdate DATETIME, OUT vFallaAge INT)
/*
* A partir de la data de naixement del faller calcula l'edat a dia 19 de març de l'exercici actual.
*
* @params vBirthdate: date
* @params vFallaAge; int
*/
BEGIN
	DECLARE vFallaYear INT;
    DECLARE vFallaDate DATETIME;

    CALL getCurrentFallaYear(vFallaYear);
   	SET vFallaDate = DATE(CONCAT(vFallaYear, '-03-19'));
    SET vFallaAge = YEAR(vFallaDate)-YEAR(vBirthdate);
    IF (MONTH(vFallaDate) < MONTH(vBirthdate) OR (MONTH(vFallaDate) = MONTH(vBirthdate) AND DAY(vFallaDate) < DAY(vBirthdate))) THEN
    SET vFallaAge = vFallaAge - 1;
END IF;
END