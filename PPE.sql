drop table users;

CREATE TABLE companies (
    company_id INT PRIMARY KEY, 
    company_name VARCHAR2(20) NOT NULL, 
    email VARCHAR2(50) UNIQUE NOT NULL, 
    pword VARCHAR2(150) NOT NULL, 
    phone_number VARCHAR2(20) NOT NULL
);

CREATE SEQUENCE company_id_sequence;

CREATE OR REPLACE TRIGGER company_id_on_insert
  BEFORE INSERT ON companies
  FOR EACH ROW
BEGIN
  SELECT company_id_sequence.nextval
  INTO :new.company_id
  FROM dual;
END;

select * from companies;
