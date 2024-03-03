USE sp;

DELIMITER $$
$$
CREATE TRIGGER getCurrentFallaYearBI
BEFORE INSERT
ON movement FOR EACH row
BEGIN
    CALL getCurrentFallaYear(NEW.fallaYear);
END;
$$
DELIMITER ;