DROP PROCEDURE IF EXISTS sp.calculateMemberFallaAge;

DELIMITER $$
$$

CREATE PROCEDURE sp.calculateMemberFallaAge(vBirthdate DATETIME)
/*
A partir de la data de naixement del faller calcula l'edat a dia 19 de març de l'exercici actual.
@params vBirthdate: date
*/
BEGIN
    DECLARE vFallaDate DATETIME;
    DECLARE vFallaAge INT;

    CALL getCurrentFallaYear(vFallaYear);

    SET vFallaDate = DATE(CONCAT(vFallaYear, '-03-19'));
    SET vFallaAge = DATEDIFF(vFallaDate, vBirthdate) / 365;
END
$$
DELIMITER ;