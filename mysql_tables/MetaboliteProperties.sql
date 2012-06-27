USE Metabolomics;
CREATE TABLE MetaboliteProperties (
	KeggID varchar(50),
	Property varchar(255),
	Value double,
	PRIMARY KEY (`KeggID`, `Property`)
);
