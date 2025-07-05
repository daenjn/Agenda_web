.headers on
.mode column
PRAGMA foreign_keys = ON;

CREATE TABLE personas (
    id_persona integer PRIMARY KEY AUTOINCREMENT,
    nombre varchar(50),
    email varchar(50)
);

INSERT INTO personas(nombre,email)
VALUES
('Dejah','dejah@email.com'),
('Jonh','jonh@email.com'),
('Cris','cris@gmail.com');

SELECT * FROM personas;
