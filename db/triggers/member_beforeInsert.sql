USE sp;

DELIMITER $$
$$
CREATE DEFINER=`root`@`localhost` TRIGGER member_beforeInsert
BEFORE INSERT
ON `member` FOR EACH ROW
BEGIN
    CALL calculateMemberCategory(NEW.birthdate, NEW.idCategory);
END
$$
DELIMITER ;