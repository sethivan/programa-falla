USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER lottery_beforeInsert
BEFORE INSERT
ON lottery FOR EACH ROW
BEGIN
	IF NEW.assigned IS NULL THEN
		CALL getCurrentDate(NEW.assigned);
	END IF;
END
