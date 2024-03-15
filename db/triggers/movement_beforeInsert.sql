USE sp;

DELIMITER $$
$$
CREATE DEFINER=`root`@`localhost` TRIGGER movement_beforeInsert
BEFORE INSERT
ON movement FOR EACH ROW
BEGIN
    CALL getCurrentFallaYear(NEW.fallaYear);
   	CALL getCurrentDate(NEW.transactionDate); 
END
$$
DELIMITER ;