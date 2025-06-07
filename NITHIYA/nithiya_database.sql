create database paperdb;
use paperdb;
CREATE TABLE submission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255),
    student_id VARCHAR(50),
    email VARCHAR(255),
    college VARCHAR(255),
    stream VARCHAR(100),
    course VARCHAR(100),
    title VARCHAR(255),
    abstract TEXT,
    doc_link TEXT,
    doc_upload_path TEXT,
    status VARCHAR(50)
);
select * from submission;
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
INSERT INTO admins (username, password) VALUES ('admin', 'admin2005');