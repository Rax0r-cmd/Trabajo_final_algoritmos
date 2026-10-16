DROP DATABASE IF EXISTS TP_FINAL_DB;
CREATE DATABASE TP_FINAL_DB;
USE TP_FINAL_DB;

-- --------------------------------------------------
-- TABLAS
-- --------------------------------------------------

-- Tipos de espacios (salas, oficinas, escritorios)
CREATE TABLE tipo_recursos (
    id_tipo_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(100) NOT NULL
);

-- Recursos / espacios
CREATE TABLE recursos (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ubicacion VARCHAR(100) NOT NULL,
    precio_por_hora DECIMAL(10,2) NOT NULL,
    id_tipo_recurso INT NOT NULL,
    CONSTRAINT fk_recursos_tipo
        FOREIGN KEY (id_tipo_recurso)
        REFERENCES tipo_recursos(id_tipo_recurso)
);

-- Clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    mail VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reservas
CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_recurso INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    horas INT NOT NULL DEFAULT 1,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Confirmada',
    CONSTRAINT fk_reservas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),
    CONSTRAINT fk_reservas_recurso
        FOREIGN KEY (id_recurso)
        REFERENCES recursos(id_recurso)
);

-- Tabla de auditoria para el trigger
CREATE TABLE auditoria_reservas (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha_accion DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100) DEFAULT 'Sistema'
);


-- --------------------------------------------------
-- DATOS DE PRUEBA
-- --------------------------------------------------

INSERT INTO tipo_recursos (nombre_tipo) VALUES 
('Sala de Reuniones'),
('Oficina Privada'),
('Puesto de Trabajo');

INSERT INTO recursos (nombre, descripcion, ubicacion, precio_por_hora, id_tipo_recurso) VALUES 
('Sala Innovación', 'Proyector y pizarra para 10 personas', 'Piso 1 - Sector A', 3500.00, 1),
('Sala Creativa', 'Mesa para 6 personas con TV', 'Piso 1 - Sector B', 2500.00, 1),
('Oficina Ejecutiva 1', 'Oficina privada para 2 personas', 'Piso 2 - Of. 201', 4500.00, 2),
('Oficina Individual 2', 'Oficina privada individual', 'Piso 2 - Of. 202', 3000.00, 2),
('Escritorio Flex 01', 'Puesto individual en compartido', 'Planta Baja - Box 1', 1200.00, 3),
('Escritorio Flex 02', 'Puesto individual en compartido', 'Planta Baja - Box 2', 1200.00, 3);

INSERT INTO clientes (nombre, apellido, telefono, mail) VALUES 
('Lucas', 'Gonzalez', '1145678901', 'lucas.gonzalez@gmail.com'),
('Mariana', 'Lopez', '1178901234', 'mariana.lopez@hotmail.com'),
('Martin', 'Perez', '1134567890', 'martin.perez@yahoo.com'),
('Sofia', 'Fernandez', '1165432109', 'sofia.fernandez@gmail.com');

INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado) VALUES 
(1, 1, '2026-11-01 10:00:00', 2, 7000.00, 'Confirmada'),
(2, 3, '2026-11-01 14:00:00', 3, 13500.00, 'Confirmada'),
(3, 5, '2026-11-02 09:00:00', 4, 4800.00, 'Confirmada'),
(1, 2, '2026-11-03 16:00:00', 1, 2500.00, 'Cancelada');


-- --------------------------------------------------
-- INDICES Y VISTAS
-- --------------------------------------------------

CREATE INDEX idx_reservas_fecha ON reservas(fecha_reserva);
CREATE INDEX idx_recursos_tipo ON recursos(id_tipo_recurso);

-- Vista con el detalle de las reservas y nombres de cliente/recurso
CREATE VIEW vw_detalle_reservas AS
SELECT 
    r.id_reserva,
    CONCAT(c.nombre, ' ', c.apellido) AS cliente,
    c.mail AS mail_cliente,
    rec.nombre AS recurso,
    t.nombre_tipo AS tipo_espacio,
    r.fecha_reserva,
    r.horas,
    r.total,
    r.estado
FROM reservas r
INNER JOIN clientes c ON r.id_cliente = c.id_cliente
INNER JOIN recursos rec ON r.id_recurso = rec.id_recurso
INNER JOIN tipo_recursos t ON rec.id_tipo_recurso = t.id_tipo_recurso;

-- Vista resumen para ver reservas totales y recaudacion por recurso
CREATE VIEW vw_resumen_recursos AS
SELECT 
    rec.id_recurso,
    rec.nombre AS recurso,
    t.nombre_tipo AS tipo,
    rec.precio_por_hora,
    COUNT(r.id_reserva) AS cantidad_reservas,
    IFNULL(SUM(CASE WHEN r.estado = 'Confirmada' THEN r.total ELSE 0 END), 0) AS total_recaudado
FROM recursos rec
INNER JOIN tipo_recursos t ON rec.id_tipo_recurso = t.id_tipo_recurso
LEFT JOIN reservas r ON rec.id_recurso = r.id_recurso
GROUP BY rec.id_recurso, rec.nombre, t.nombre_tipo, rec.precio_por_hora;


-- --------------------------------------------------
-- FUNCION: DISPONIBILIDAD
-- --------------------------------------------------

DELIMITER //

-- Devuelve 1 si esta libre o 0 si ya esta reservado en esa fecha
CREATE FUNCTION fn_verificar_disponibilidad(
    p_id_recurso INT,
    p_fecha DATETIME
) 
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_cantidad INT DEFAULT 0;
    
    SELECT COUNT(*) INTO v_cantidad
    FROM reservas
    WHERE id_recurso = p_id_recurso
      AND fecha_reserva = p_fecha
      AND estado = 'Confirmada';
      
    IF v_cantidad = 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END //

DELIMITER ;


-- --------------------------------------------------
-- STORED PROCEDURES
-- --------------------------------------------------

DELIMITER //

-- Alta cliente
CREATE PROCEDURE sp_alta_cliente(
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_mail VARCHAR(255)
)
BEGIN
    INSERT INTO clientes (nombre, apellido, telefono, mail)
    VALUES (p_nombre, p_apellido, p_telefono, p_mail);
END //

-- Modificar cliente
CREATE PROCEDURE sp_modificar_cliente(
    IN p_id_cliente INT,
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_mail VARCHAR(255)
)
BEGIN
    UPDATE clientes
    SET nombre = p_nombre,
        apellido = p_apellido,
        telefono = p_telefono,
        mail = p_mail
    WHERE id_cliente = p_id_cliente;
END //

-- Alta recurso
CREATE PROCEDURE sp_alta_recurso(
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT,
    IN p_ubicacion VARCHAR(100),
    IN p_precio DECIMAL(10,2),
    IN p_id_tipo INT
)
BEGIN
    INSERT INTO recursos (nombre, descripcion, ubicacion, precio_por_hora, id_tipo_recurso)
    VALUES (p_nombre, p_descripcion, p_ubicacion, p_precio, p_id_tipo);
END //

-- Modificar recurso
CREATE PROCEDURE sp_modificar_recurso(
    IN p_id_recurso INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion TEXT,
    IN p_ubicacion VARCHAR(100),
    IN p_precio DECIMAL(10,2),
    IN p_id_tipo INT
)
BEGIN
    UPDATE recursos
    SET nombre = p_nombre,
        descripcion = p_descripcion,
        ubicacion = p_ubicacion,
        precio_por_hora = p_precio,
        id_tipo_recurso = p_id_tipo
    WHERE id_recurso = p_id_recurso;
END //

-- Alta de reserva (valida disponibilidad con la funcion y tira error con signal si esta ocupado)
CREATE PROCEDURE sp_alta_reserva(
    IN p_id_cliente INT,
    IN p_id_recurso INT,
    IN p_fecha DATETIME,
    IN p_horas INT,
    IN p_total DECIMAL(10,2)
)
BEGIN
    DECLARE v_disponible INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        RESIGNAL;
    END;

    SET v_disponible = fn_verificar_disponibilidad(p_id_recurso, p_fecha);

    IF v_disponible = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El recurso ya se encuentra reservado en ese dia y horario.';
    ELSE
        INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado)
        VALUES (p_id_cliente, p_id_recurso, p_fecha, p_horas, p_total, 'Confirmada');
    END IF;
END //

-- Cancelar reserva
CREATE PROCEDURE sp_cancelar_reserva(
    IN p_id_reserva INT
)
BEGIN
    DECLARE v_existe INT DEFAULT 0;

    SELECT COUNT(*) INTO v_existe FROM reservas WHERE id_reserva = p_id_reserva;

    IF v_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La reserva que intentas cancelar no existe.';
    ELSE
        UPDATE reservas
        SET estado = 'Cancelada'
        WHERE id_reserva = p_id_reserva;
    END IF;
END //


-- --------------------------------------------------
-- CURSOR
-- --------------------------------------------------

-- Procedimiento con cursor para recorrer reservas confirmadas y sumar el total
CREATE PROCEDURE sp_calcular_total_recaudado_cursor(
    OUT p_total_general DECIMAL(10,2)
)
BEGIN
    DECLARE v_fin INT DEFAULT FALSE;
    DECLARE v_monto DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_acumulador DECIMAL(10,2) DEFAULT 0.00;

    DECLARE cur_reservas CURSOR FOR 
        SELECT total FROM reservas WHERE estado = 'Confirmada';

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fin = TRUE;

    OPEN cur_reservas;

    bucle_reservas: LOOP
        FETCH cur_reservas INTO v_monto;
        
        IF v_fin THEN
            LEAVE bucle_reservas;
        END IF;

        SET v_acumulador = v_acumulador + v_monto;
    END LOOP;

    CLOSE cur_reservas;

    SET p_total_general = v_acumulador;
END //


-- --------------------------------------------------
-- TRIGGER
-- --------------------------------------------------

-- Guarda en auditoria cuando se cancela una reserva
CREATE TRIGGER trg_auditoria_reservas
AFTER UPDATE ON reservas
FOR EACH ROW
BEGIN
    IF NEW.estado = 'Cancelada' AND OLD.estado != 'Cancelada' THEN
        INSERT INTO auditoria_reservas (id_reserva, accion, fecha_accion, usuario)
        VALUES (NEW.id_reserva, 'Cancelacion de reserva', NOW(), CURRENT_USER());
    END IF;
END //

DELIMITER ;


-- --------------------------------------------------
-- CONSULTAS DE PRUEBA
-- --------------------------------------------------

-- 1. Reservas confirmadas con join
SELECT 
    r.id_reserva,
    c.nombre AS cliente,
    rec.nombre AS espacio,
    r.fecha_reserva,
    r.total
FROM reservas r
INNER JOIN clientes c ON r.id_cliente = c.id_cliente
INNER JOIN recursos rec ON r.id_recurso = rec.id_recurso
WHERE r.estado = 'Confirmada'
ORDER BY r.fecha_reserva ASC;

-- 2. Subconsultas
-- Recursos sin reservas
SELECT id_recurso, nombre, ubicacion
FROM recursos
WHERE id_recurso NOT IN (SELECT DISTINCT id_recurso FROM reservas);

-- Clientes que gastaron mas que el promedio
SELECT nombre, apellido, mail
FROM clientes
WHERE id_cliente IN (
    SELECT id_cliente 
    FROM reservas 
    WHERE total > (SELECT AVG(total) FROM reservas)
);

-- 3. CTE para ver promedios por tipo de recurso
WITH ResumenPorTipo AS (
    SELECT 
        t.nombre_tipo,
        COUNT(rec.id_recurso) AS cantidad_recursos,
        AVG(rec.precio_por_hora) AS precio_promedio_por_hora
    FROM tipo_recursos t
    LEFT JOIN recursos rec ON t.id_tipo_recurso = rec.id_tipo_recurso
    GROUP BY t.id_tipo_recurso, t.nombre_tipo
)
SELECT * FROM ResumenPorTipo;
