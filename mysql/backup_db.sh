#!/bin/bash

/opt/local/bin/mysqldump5 --skip-triggers --compact --no-create-info -uroot metabolomics > metabolomics_db.sql
