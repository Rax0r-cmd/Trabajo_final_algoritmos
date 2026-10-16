CREATE DATABASE TP_FINAL_DB;

USE TP_FINAL_DB;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono INT NOT NULL,
    mail VARCHAR(255)
);

CREATE TABLE tipo_recursos (
    id_tipo_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(100) NOT NULL
);

CREATE TABLE recursos (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    ubicacion VARCHAR(100) NOT NULL,
    id_tipo_recurso INT NOT NULL,
    
    CONSTRAINT fk_recursos_tipo
        FOREIGN KEY (id_tipo_recurso)
        REFERENCES tipo_recursos(id_tipo_recurso)
);

CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_recurso INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    
    CONSTRAINT fk_reservas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),
    CONSTRAINT fk_reservas_recurso
        FOREIGN KEY (id_recurso)
        REFERENCES recursos(id_recurso)
);
