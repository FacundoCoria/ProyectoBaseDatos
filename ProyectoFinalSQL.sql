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
    PRIMARY KEY (id_clase, ci_alumno),
    FOREIGN KEY (id_clase) REFERENCES clase(id),
    FOREIGN KEY (ci_alumno) REFERENCES alumnos(ci),
    FOREIGN KEY (id_equipamiento) REFERENCES equipamiento(id)
);