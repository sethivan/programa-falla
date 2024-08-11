USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER movement_beforeInsert
BEFORE INSERT
ON movement FOR EACH ROW
BEGIN
	CALL getCurrentFallaYear(NEW.fallaYearFk);
	CALL getCurrentDate(NEW.transactionDate);
END