CREATE DATABASE IF NOT EXISTS sp;
USE sp;

CREATE TABLE IF NOT EXISTS category(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fee DECIMAL(10, 2) NOT NULL,
	name VARCHAR(10),
	description VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS family(
	id INT AUTO_INCREMENT PRIMARY KEY,
	discount DECIMAL(10, 2) NOT NULL,
	isDirectDebited BOOLEAN
);

CREATE TABLE IF NOT EXISTS member(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	surname VARCHAR(100) NOT NULL,
	birthdate DATE NOT NULL,
	gender ENUM('M', 'F'),
	dni VARCHAR(10),
	address VARCHAR(100),
	phoneNumber VARCHAR(15),
	isRegistered BOOLEAN,
	familyFk INT NOT NULL,
	categoryFk INT NOT NULL,
	email VARCHAR(50),
	CONSTRAINT member_family_FK
	FOREIGN KEY(familyFk)
	REFERENCES family(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT member_category_FK
	FOREIGN KEY(categoryFk)
	REFERENCES category(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS fallaYear(
	code INT PRIMARY KEY,
	created DATE,
	finished DATE
);

CREATE TABLE IF NOT EXISTS movement(
	id INT AUTO_INCREMENT PRIMARY KEY,
	transactionDate DATE NOT NULL,
	amount DECIMAL(10, 2) NOT NULL,
	idType INT NOT NULL,
	idConcept INT NOT NULL,
	fallaYearFk INT NOT NULL,
	memberFk INT NOT NULL,
	description VARCHAR(100),
	receiptNumber INT,
	CONSTRAINT movement_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT movement_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS membershipHistory(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fallaYearFk INT NOT NULL,
	position VARCHAR(30) NOT NULL,
	falla VARCHAR(50) NOT NULL,
	memberFk INT NOT NULL,
	CONSTRAINT membershipHistory_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT membershipHistory_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS summaryMembersFallaYear(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fallaYearFk INT NOT NULL,
	memberFk INT NOT NULL,
	assignedFee DECIMAL(10, 2) NOT NULL,
	assignedLottery DECIMAL(10, 2) NOT NULL,
	assignedRaffle DECIMAL(10, 2) NOT NULL,
	payedFee DECIMAL(10, 2) NOT NULL,
	payedLottery DECIMAL(10, 2) NOT NULL,
	payedRaffle DECIMAL(10, 2) NOT NULL,
	difference DECIMAL(10, 2) AS (
    assignedFee + assignedLottery + assignedRaffle - 
    (payedFee + payedLottery + payedRaffle)) VIRTUAL,
	CONSTRAINT summaryMembersFallaYear_fallaYear_FK
	FOREIGN KEY(fallaYearFk)
	REFERENCES fallaYear(code)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT summaryMembersFallaYear_member_FK
	FOREIGN KEY(memberFk)
	REFERENCES member(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);