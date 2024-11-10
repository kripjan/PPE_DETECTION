select * from companies;
desc companies;

ALTER TABLE companies MODIFY pword VARCHAR2(255); -- increasing the max length of pword column

-- creating cameras table
CREATE TABLE cameras (
    camera_id INT PRIMARY KEY, 
    serial_number VARCHAR2(255) UNIQUE NOT NULL, 
    physical_location VARCHAR2(50) NOT NULL, 
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) references companies(company_id)
);


-- ensuring camera id auto increments
CREATE SEQUENCE camera_id_sequence;

CREATE OR REPLACE TRIGGER camera_id_on_insert
  BEFORE INSERT ON cameras
  FOR EACH ROW
BEGIN
  SELECT camera_id_sequence.nextval
  INTO :new.camera_id
  FROM dual;
END;

desc cameras



-- creating frames table
CREATE TABLE frames (
    frame_id INT PRIMARY KEY, 
    datetime TIMESTAMP NOT NULL, 
    camera_id INT NOT NULL,
    FOREIGN KEY (camera_id) references cameras(camera_id)
);


-- ensuring frame id auto increments
CREATE SEQUENCE frame_id_sequence;

CREATE OR REPLACE TRIGGER frame_id_on_insert
  BEFORE INSERT ON frames
  FOR EACH ROW
BEGIN
  SELECT frame_id_sequence.nextval
  INTO :new.frame_id
  FROM dual;
END;

desc frames


-- creating objects table
CREATE TABLE objects (
    object_id INT PRIMARY KEY, 
    object_name VARCHAR(50) NOT NULL
);


-- ensuring object id auto increments
CREATE SEQUENCE object_id_sequence;

CREATE OR REPLACE TRIGGER object_id_on_insert
  BEFORE INSERT ON objects
  FOR EACH ROW
BEGIN
  SELECT object_id_sequence.nextval
  INTO :new.object_id
  FROM dual;
END;

desc objects;



-- creating the bridge table betn frames and objects
CREATE TABLE frame_object (
    frame_id INT, 
    object_id INT,
    FOREIGN KEY (frame_id) references frames(frame_id),
    FOREIGN KEY (object_id) references objects(object_id),
    PRIMARY KEY (frame_id, object_id)
);

desc frame_object;

-- showing all tables in this database
select * from user_tables;

commit;