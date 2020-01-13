#CREATE DATABASE CCLoanLaptops;
use CCLoanLaptops;

CREATE TABLE LoanedLaptops (
  CCassetTag VARCHAR(255), 
  assetTag VARCHAR(255), 
  DateBorrowed VARCHAR(255),
  BorrowedBy VARCHAR(255),
  LentBy VARCHAR(255), 
  ReturnedBy VARCHAR(255),
  ReceivedBy VARCHAR(255),
  DateReturned VARCHAR(255), 
  TimeReturned VARCHAR(255), 
  TimeBorrowed VARCHAR(255)
);

alter table LoanedLaptops add column `id` int(255) unsigned primary KEY AUTO_INCREMENT;

#GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' WITH GRANT OPTION;
