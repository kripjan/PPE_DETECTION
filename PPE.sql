CREATE TABLE Users (
    user_id INT PRIMARY KEY, 
    first_name VARCHAR2(20) NOT NULL, 
    last_name VARCHAR2(20) NOT NULL, 
    email VARCHAR2(50) UNIQUE NOT NULL, 
    pword VARCHAR2(150) NOT NULL, 
    phone_number VARCHAR2(20) NOT NULL
);

CREATE SEQUENCE user_id_sequence;

CREATE OR REPLACE TRIGGER user_id_on_insert
  BEFORE INSERT ON Users
  FOR EACH ROW
BEGIN
  SELECT user_id_sequence.nextval
  INTO :new.user_id
  FROM dual;
END;
