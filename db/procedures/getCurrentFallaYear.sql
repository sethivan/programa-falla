DROP PROCEDURE IF EXISTS sp.getCurrentFallaYear;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`getCurrentFallaYear`(INOUT vFallaYear INT)
BEGIN
	DECLARE vLastFallaYear INT;

	SELECT fallaYearFk INTO vLastFallaYear
	FROM movement ORDER BY id DESC LIMIT 1;

	IF vFallaYear IS NULL THEN
		SET vFallaYear = vLastFallaYear;
	END IF;
END