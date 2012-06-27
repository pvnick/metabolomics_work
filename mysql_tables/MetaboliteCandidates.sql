USE Metabolomics;
CREATE TABLE MetaboliteCandidates (
	KeggID varchar(50),
	PubChemID int,
	MET3DID varchar(50),
	Name varchar(255),
	PRIMARY KEY (`KeggID`),
	KEY (`PubChemID`),
	KEY (`MET3DID`)
);
