CREATE DATABASE LendingClub;

USE LendingClub;

Select * from loans;
select * from NonfarmPayroll;

#Join the tables and select all
select * from loans l join NonfarmPayroll N on (l.addr_state =N.abbrev);


##This section to clear out a null value from the NonfarmPayroll table and set the primary key as "abbrev"
SET SQL_SAFE_UPDATES = 0;

DELETE FROM NonfarmPayroll
	WHERE abbrev IS NULL;

ALTER TABLE NonfarmPayroll
	CHANGE COLUMN abbrev 
    abbrev VARCHAR(2) PRIMARY KEY;

ALTER TABLE NonfarmPayroll
	CHANGE COLUMN `2017 Yearly Earnings`
    `2017_Yearly_Earnings` FLOAT;

ALTER TABLE NonfarmPayroll
	CHANGE COLUMN `2016 Yearly Earnings`
    `2016_Yearly_Earnings` FLOAT;

ALTER TABLE NonfarmPayroll
	CHANGE COLUMN `2015 Yearly Earnings`
    `2015_Yearly_Earnings` FLOAT;

##Change the auto-generated index from pandas to member_id and set it as the primary key
ALTER TABLE LendingClub.loans
CHANGE COLUMN `index` `member_id` BIGINT NOT NULL PRIMARY KEY;

##Here we attempted to set the state abbrev as a foreign key. We realized Connecticut was improperly abbreviated CN
SELECT * from loans where addr_state not in (SELECT abbrev from NonfarmPayroll);

UPDATE NonfarmPayroll SET abbrev = 'CT' WHERE state= 'Connecticut';

##Need both fields to be the same type (in this case VARCHAR(2) to create foreign key link
ALTER TABLE loans
	CHANGE COLUMN addr_state
    addr_state VARCHAR(2);

ALTER TABLE loans
	ADD FOREIGN KEY (addr_state) REFERENCES NonfarmPayroll (abbrev);


## Create some views to display the data
CREATE VIEW total_by_state AS
	SELECT SUM(l.funded_amnt) AS total_loans, n.state
    FROM loans l JOIN NonfarmPayroll n on l.addr_state = n.abbrev
    GROUP BY n.state
    ORDER BY total_loans DESC;
    
SELECT * FROM total_by_state;


DROP VIEW delinquencies;

CREATE VIEW delinquencies AS
	SELECT ROUND(SUM(l.out_prncp),0) AS delinquent_amt, 
    CAST((SUM(l.out_prncp)/SUM(l.funded_amnt)) * 100 AS DECIMAL(18, 2)) AS delinq_rate,
    n.state
    FROM loans l JOIN NonfarmPayroll n on l.addr_state = n.abbrev
	WHERE (l.loan_status != 'Fully Paid' AND l.loan_status != 'Current')
    GROUP BY n.state
    ORDER BY delinq_rate DESC;
    
SELECT * FROM delinquencies;

CREATE VIEW earnings_growth AS
    SELECT CAST(((2017_Yearly_Earnings/2016_Yearly_Earnings) -1) *100 AS DECIMAL(18, 2)) AS annual_earnings_growth,
    state
	FROM NonfarmPayroll;
    
SELECT delinquent_amt, delinq_rate, annual_earnings_growth, d.state 
FROM delinquencies d JOIN earnings_growth e on d.state = e.state;