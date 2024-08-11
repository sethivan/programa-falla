USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER fallaYear_beforeUpdate
BEFORE UPDATE
ON fallaYear FOR EACH ROW
BEGIN
	CALL getCurrentDate(NEW.finished);
END