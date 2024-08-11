USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER member_beforeInsert
BEFORE INSERT
ON `member` FOR EACH ROW
BEGIN
	CALL calculateMemberCategory(NEW.birthdate, NEW.categoryFk);
END