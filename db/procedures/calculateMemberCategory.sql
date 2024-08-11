DROP PROCEDURE IF EXISTS sp.calculateMemberCategory;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`calculateMemberCategory`(
	IN vBirthdate DATETIME, OUT vCategoryFk INT
)
/*
* A partir de la data de naixement del faller
* calcula la categoria a la que pertany.
*
* @params vBirthdate: date
* @params vCategoryFk: int
*/
BEGIN
	DECLARE vFallaAge INT;
	CALL calculateMemberFallaAge(vBirthdate, vFallaAge);
	CASE 
		WHEN vFallaAge < 5 THEN
			SET vCategoryFk = 5;
		WHEN vFallaAge >= 5 AND vFallaAge <= 9 THEN
			SET vCategoryFk = 4;
		WHEN vFallaAge >= 10 AND vFallaAge <= 13 THEN
			SET vCategoryFk = 3;
		WHEN vFallaAge >= 14 AND vFallaAge <= 17 THEN
			SET vCategoryFk = 2;
		ELSE
			SET vCategoryFk = 1;
	END CASE;
END