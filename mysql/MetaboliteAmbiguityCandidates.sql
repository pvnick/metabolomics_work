USE Metabolomics;
CREATE TABLE `MetaboliteAmbiguityCandidates` (
  `AmbiguityID` int(10) NOT NULL,
  `KeggID` varchar(50) NOT NULL DEFAULT '',
  KEY (`AmbiguityID`),
  KEY (`KeggID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1
