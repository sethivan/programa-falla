USE sp;

DELIMITER $$
$$
CREATE DEFINER=`root`@`localhost` TRIGGER member_beforeUpdate
BEFORE UPDATE
ON `member` FOR EACH ROW
BEGIN
	CALL calculateMemberCategory(NEW.birthdate, NEW.categoryFk);
	CALL modifyMembershipHistory(NEW.id, NEW.isRegistered);
END
$$
DELIMITER ;