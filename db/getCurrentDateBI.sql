USE sp;

DELIMITER $$
$$
CREATE TRIGGER getCurrentDateBI
BEFORE INSERT
ON movement FOR EACH row
BEGIN
    CALL getCurrentDate(NEW.transactionDate);
END;
$$
DELIMITER ;