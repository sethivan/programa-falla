DROP PROCEDURE IF EXISTS sp.getCurrentDate;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`getCurrentDate`(INOUT vDate DATETIME)
/*
* Si la data d'entrada es NULL, fica com a data l'actual.
*
* @params vDate: datetime
*/
BEGIN
	IF vDate IS NULL THEN
        SET vDate = NOW();
    END IF;
END