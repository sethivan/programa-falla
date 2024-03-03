DROP PROCEDURE IF EXISTS sp.getCurrentFallaYear;

DELIMITER $$
$$

CREATE PROCEDURE sp.getCurrentFallaYear(INOUT vFallaYear INT)
/*
Si l'exercici d'entrada es NULL, fica com a exercici l'actual.
@params vFallaYear: int
*/
BEGIN
    DECLARE vLastFallaYear INT;

    SELECT fallaYear INTO vLastFallaYear FROM movement ORDER BY id DESC LIMIT 1;
	IF vFallaYear IS NULL THEN
        SET vFallaYear = vLastFallaYear;
    END IF;
END
$$
DELIMITER ;