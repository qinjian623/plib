--导入csv文件
LOAD DATA LOCAL INFILE 'asdf.csv' INTO TABLE asdftable FIELDS TERMINATED BY ',' ENCLOSED BY '"' lines terminated by '\n' IGNORE 1 LINES;
