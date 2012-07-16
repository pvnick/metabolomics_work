USE Metabolomics;
CREATE TABLE `MetaboliteAmbiguities` (
  `AmbiguityID` int(10) NOT NULL AUTO_INCREMENT,
  `ScanID` int(10) NOT NULL DEFAULT 0,
  PRIMARY KEY (`AmbiguityID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1
