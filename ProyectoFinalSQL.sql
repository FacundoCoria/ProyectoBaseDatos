Create schema proyectoFinal;

CREATE TABLE login (
    correo VARCHAR(50) PRIMARY KEY,
    contraseña VARCHAR(50) NOT NULL
);

CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL
);

CREATE TABLE equipamiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_actividad INT,
    descripcion VARCHAR(50) NOT NULL,
    costo DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_actividad) REFERENCES actividades(id)
);

CREATE TABLE instructores (
    ci CHAR(8) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL
);

CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

CREATE TABLE alumnos (
    ci CHAR(8) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(50)
);

CREATE TABLE clase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ci_instructor CHAR(8),
    id_actividad INT,
    id_turno INT,
    dictada BOOLEAN DEFAULT FALSE,
    tipo_clase ENUM('grupal', 'individual') NOT NULL,
    FOREIGN KEY (ci_instructor) REFERENCES instructores(ci),
    FOREIGN KEY (id_actividad) REFERENCES actividades(id),
    FOREIGN KEY (id_turno) REFERENCES turnos(id)
);

CREATE TABLE alumno_clase (
    id_clase INT,
    ci_alumno CHAR(8),
    id_equipamiento INT,
    PRIMARY KEY (id_clase, ci_alumno, id_equipamiento),
    FOREIGN KEY (id_clase) REFERENCES clase(id),
    FOREIGN KEY (ci_alumno) REFERENCES alumnos(ci),
    FOREIGN KEY (id_equipamiento) REFERENCES equipamiento(id)
);

ALTER TABLE clase
ADD CONSTRAINT unique_instructor_turno UNIQUE (ci_instructor, id_turno);

DROP TABLE alumno_clase;


ALTER TABLE login ADD COLUMN rol ENUM('administrador', 'instructor', 'estudiante') NOT NULL;
ALTER TABLE login ADD COLUMN ci CHAR(8) NOT NULL;

INSERT INTO actividades (descripcion, costo)
VALUES ('snowboard', 250),
    ('ski', 300),
    ('moto de nieve', 500);

INSERT INTO turnos (hora_inicio, hora_fin)
VALUES ('09:00', '11:00'),
       ('12:00', '14:00'),
       ('16:00', '18:00');

INSERT INTO equipamiento (id_actividad, descripcion, costo) VALUES
(1, 'Tabla de snowboard', 300.00),
(1, 'Botas de snowboard', 150.00),
(2, 'Esquís', 400.00),
(2, 'Botas de esquí', 120.00),
(3, 'Moto de nieve', 800.00),
(3, 'Casco para moto de nieve', 100.00);

INSERT INTO login(correo, contraseña, rol, ci) VALUES
('administrativo1@mail.com', 'admin', 'administrador', 11111111);

ALTER TABLE alumno_clase ADD COLUMN costo_adicional DECIMAL(10, 2) DEFAULT 0.0;


Delete from instructores;
Delete from login;
Delete from alumno_clase;