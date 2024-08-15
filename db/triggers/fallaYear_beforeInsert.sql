USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER fallaYear_beforeInsert
BEFORE INSERT
ON fallaYear FOR EACH ROW
BEGIN
	IF NEW.created IS NULL THEN
		CALL getCurrentDate(NEW.created);
	END IF;
	IF NEW.code IS NULL THEN
		CALL calculateFallaYear(NEW.code);
	END IF;
END
