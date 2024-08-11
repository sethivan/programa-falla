USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER fallaYear_beforeInsert
BEFORE INSERT
ON fallaYear FOR EACH ROW
BEGIN
	CALL getCurrentDate(NEW.created);
	CALL calculateFallaYear(NEW.code);
END