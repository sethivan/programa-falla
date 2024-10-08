DROP PROCEDURE IF EXISTS sp.modifyMembershipHistory;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`modifyMembershipHistory`(
	IN vId INT, IN vIsRegistered BOOLEAN
)
/*
* A partir de l'id del faller i si està en actiu, modifica la taula
* amb l'historial "membershipHistory".
*
* @params vId: int
* @params vIsRegistered: boolean
*/
BEGIN
	DECLARE vIsCurrentlyRegistered BOOLEAN;
	DECLARE vFallaYear INT;

	CALL getCurrentFallaYear(vFallaYear);

	SELECT isRegistered INTO vIsCurrentlyRegistered FROM member WHERE id = vId;

		IF vIsCurrentlyRegistered = 0 AND vIsRegistered = 1 THEN
			INSERT INTO membershipHistory (
				fallaYearFk, position, falla, memberFk
			) VALUES (vFallaYear, 'vocal', 'Sants Patrons', vId);
		END IF;
	
		IF vIsCurrentlyRegistered = 1 AND vIsRegistered = 0 THEN
			DELETE FROM membershipHistory
			WHERE memberFk = vId AND fallaYearFk = vFallaYear;
		END IF;
END