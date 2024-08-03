USE sp;

DELIMITER $$
$$
CREATE DEFINER=`root`@`localhost` TRIGGER summaryMembersFallaYear_beforeInsert
BEFORE INSERT
ON summaryMembersFallaYear FOR EACH ROW
BEGIN
	CALL getCurrentFallaYear(NEW.fallaYearFk);
END
$$
DELIMITER ;