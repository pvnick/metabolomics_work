USE Metabolomics;
CREATE TABLE `MetaboliteCandidates` (
  `KeggID` varchar(50) NOT NULL DEFAULT '',
  `PubChemID` int(11) DEFAULT NULL,
  `MET3DID` varchar(50) DEFAULT NULL,
  `InChIKey` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`KeggID`),
  KEY `PubChemID` (`PubChemID`),
  KEY `MET3DID` (`MET3DID`),
  KEY `InChIKey` (`InChIKey`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1
