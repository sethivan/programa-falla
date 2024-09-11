USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER member_beforeInsert
BEFORE INSERT
ON `member` FOR EACH ROW
BEGIN
	IF NEW.categoryFk IS NULL THEN
		CALL calculateMemberCategory(NEW.birthdate, NEW.categoryFk);
	END IF;
END