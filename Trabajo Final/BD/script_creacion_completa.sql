-- ==============================================================================
-- TRABAJO PRÁCTICO FINAL: SISTEMA DE GESTIÓN DE COWORKING Y RESERVAS
-- Materia: Algoritmos II (Analista de Sistemas de Información)
-- Profesor: Lic. Adrián Aroca
-- Archivo: DB_TPFinal.sql
-- Nivel: Explicado paso a paso de forma clara y didáctica (Nivel estudiante)
-- ==============================================================================

-- ==============================================================================
-- UNIDAD 1: INTRODUCCIÓN A LA GESTIÓN DE BASES DE DATOS
-- Concepto: Creamos la base de datos si no existe y nos paramos en ella para usarla.
-- ==============================================================================
DROP DATABASE IF EXISTS TP_FINAL_DB;
CREATE DATABASE TP_FINAL_DB;
USE TP_FINAL_DB;


-- ==============================================================================
-- UNIDAD 2 Y 3: LENGUAJE SQL, MODELOS Y NORMALIZACIÓN (DDL)
-- Concepto: Tablas, Tipos de Datos (INT, VARCHAR, DECIMAL, DATETIME),
-- Claves Primarias (PK AUTO_INCREMENT) y Claves Foráneas (FK con CONSTRAINT).
-- ==============================================================================

-- Tabla 1: Tipos de Recursos (Categorías de espacios: salas, oficinas, escritorios)
CREATE TABLE tipo_recursos (
    id_tipo_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(100) NOT NULL
);

-- Tabla 2: Recursos (Espacios físicos que el cliente puede reservar)
CREATE TABLE recursos (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ubicacion VARCHAR(100) NOT NULL,
    precio_por_hora DECIMAL(10,2) NOT NULL,
    id_tipo_recurso INT NOT NULL,
    
    -- Clave foránea que relaciona cada recurso con su tipo
    CONSTRAINT fk_recursos_tipo
        FOREIGN KEY (id_tipo_recurso)
        REFERENCES tipo_recursos(id_tipo_recurso)
);

-- Tabla 3: Clientes (Personas registradas que alquilan los espacios)
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    mail VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 4: Reservas (La operación principal: une a un cliente con un recurso en una fecha)
CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_recurso INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    horas INT NOT NULL DEFAULT 1,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Confirmada', -- 'Confirmada', 'Cancelada' o 'Finalizada'
    
    -- Clave foránea con Clientes
    CONSTRAINT fk_reservas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),
        
    -- Clave foránea con Recursos
    CONSTRAINT fk_reservas_recurso
        FOREIGN KEY (id_recurso)
        REFERENCES recursos(id_recurso)
);

-- Tabla 5: Auditoría de Reservas (Requerido para registrar cambios o cancelaciones con Trigger)
CREATE TABLE auditoria_reservas (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha_accion DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100) DEFAULT 'Sistema'
);


-- ==============================================================================
-- UNIDAD 4 Y 5: INTEGRIDAD DE DATOS Y SENTENCIAS SQL EN DETALLE (DML)
-- Concepto: Cargar datos iniciales suficientes con INSERT INTO para probar el sistema.
-- ==============================================================================

-- 1. Insertamos categorías de recursos
INSERT INTO tipo_recursos (nombre_tipo) VALUES 
('Sala de Reuniones'),
('Oficina Privada'),
('Puesto de Trabajo');

-- 2. Insertamos recursos de coworking
INSERT INTO recursos (nombre, descripcion, ubicacion, precio_por_hora, id_tipo_recurso) VALUES 
('Sala Innovación', 'Sala con proyector y pizarra para 10 personas', 'Piso 1 - Sector A', 3500.00, 1),
('Sala Creativa', 'Mesa redonda para 6 personas con TV Smart', 'Piso 1 - Sector B', 2500.00, 1),
('Oficina Ejecutiva 1', 'Oficina privada para 2 personas con escritorio ergonómico', 'Piso 2 - Of. 201', 4500.00, 2),
('Oficina Individual 2', 'Oficina privada pequeña individual con vista exterior', 'Piso 2 - Of. 202', 3000.00, 2),
('Escritorio Flex 01', 'Puesto individual en espacio compartido con conexión rápida', 'Planta Baja - Box 1', 1200.00, 3),
('Escritorio Flex 02', 'Puesto individual en espacio compartido', 'Planta Baja - Box 2', 1200.00, 3);

-- 3. Insertamos clientes de prueba
INSERT INTO clientes (nombre, apellido, telefono, mail) VALUES 
('Lucas', 'Gonzalez', '1145678901', 'lucas.gonzalez@gmail.com'),
('Mariana', 'Lopez', '1178901234', 'mariana.lopez@hotmail.com'),
('Martin', 'Perez', '1134567890', 'martin.perez@yahoo.com'),
('Sofia', 'Fernandez', '1165432109', 'sofia.fernandez@gmail.com');

-- 4. Insertamos reservas iniciales
INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado) VALUES 
(1, 1, '2026-11-01 10:00:00', 2, 7000.00, 'Confirmada'),
(2, 3, '2026-11-01 14:00:00', 3, 13500.00, 'Confirmada'),
(3, 5, '2026-11-02 09:00:00', 4, 4800.00, 'Confirmada'),
(1, 2, '2026-11-03 16:00:00', 1, 2500.00, 'Cancelada');


-- ==============================================================================
-- VISTAS E ÍNDICES
-- Concepto: 
-- - ÍNDICES: Hacen que las búsquedas por fecha o tipo sean mucho más veloces.
-- - VISTAS: Tablas virtuales que combinan datos para no tener que escribir los JOINs siempre.
-- ==============================================================================

-- Índices
CREATE INDEX idx_reservas_fecha ON reservas(fecha_reserva);
CREATE INDEX idx_recursos_tipo ON recursos(id_tipo_recurso);

-- Vista 1: Detalle completo de reservas (Con nombres de clientes, recurso y estado)
CREATE VIEW vw_detalle_reservas AS
SELECT 
    r.id_reserva,
    CONCAT(c.nombre, ' ', c.apellido) AS cliente,
    c.mail AS contacto_cliente,
    rec.nombre AS recurso,
    t.nombre_tipo AS tipo,
    r.fecha_reserva,
    r.horas,
    r.total,
    r.estado
FROM reservas r
INNER JOIN clientes c ON r.id_cliente = c.id_cliente
INNER JOIN recursos rec ON r.id_recurso = rec.id_recurso
INNER JOIN tipo_recursos t ON rec.id_tipo_recurso = t.id_tipo_recurso;

-- Vista 2: Resumen por cada recurso (Cuántas veces se reservó y cuánto dinero generó)
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


-- ==============================================================================
-- UNIDAD: UDF (USER DEFINED FUNCTION) Y CTE (COMMON TABLE EXPRESSION)
-- Concepto:
-- - UDF: Función creada por nosotros que recibe datos y devuelve un único resultado.
-- - CTE: Tabla temporal (WITH ... AS) para organizar consultas complejas de forma limpia.
-- ==============================================================================

DELIMITER //

-- Función UDF: Devuelve 1 (Disponible) si no hay reservas confirmadas para ese recurso en esa fecha, o 0 (Ocupado).
CREATE FUNCTION fn_verificar_disponibilidad(
    p_id_recurso INT,
    p_fecha DATETIME
) 
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_cantidad INT DEFAULT 0;
    
    -- Contamos cuántas reservas activas existen en esa fecha para ese recurso
    SELECT COUNT(*) INTO v_cantidad
    FROM reservas
    WHERE id_recurso = p_id_recurso
      AND fecha_reserva = p_fecha
      AND estado = 'Confirmada';
      
    -- Si la cuenta es cero, está libre; de lo contrario está ocupado
    IF v_cantidad = 0 THEN
        RETURN 1; -- 1 = Libre / Disponible
    ELSE
        RETURN 0; -- 0 = Ocupado
    END IF;
END //

DELIMITER ;


-- ==============================================================================
-- PROCEDIMIENTOS ALMACENADOS (STORED PROCEDURES)
-- Con HANDLERS de error y SIGNAL SQLSTATE '45000'
-- Concepto:
-- - Procedimientos: Bloques de código guardados en la BD para dar altas y modificaciones.
-- - SIGNAL: Lanza un cartel de error personalizado que viaja hasta C# si algo está mal.
-- - HANDLER: Bloque que atrapa cualquier falla interna de SQL para que no se caiga la base.
-- ==============================================================================

DELIMITER //

-- Procedimiento 1: Alta de un nuevo Cliente
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

-- Procedimiento 1b: Modificar Cliente
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



-- Procedimiento 2: Alta de un nuevo Recurso
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


-- Procedimiento 3: Modificar datos de un Recurso existente
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


-- Procedimiento 4: Alta de Reserva con validación de disponibilidad y HANDLER de excepción
CREATE PROCEDURE sp_alta_reserva(
    IN p_id_cliente INT,
    IN p_id_recurso INT,
    IN p_fecha DATETIME,
    IN p_horas INT,
    IN p_total DECIMAL(10,2)
)
BEGIN
    DECLARE v_disponible INT;
    
    -- HANDLER: Si ocurre un error inesperado de SQL, lo atrapa y lo reenvía
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        RESIGNAL;
    END;

    -- Usamos nuestra función UDF para saber si está disponible
    SET v_disponible = fn_verificar_disponibilidad(p_id_recurso, p_fecha);

    -- Si NO está disponible (da 0), lanzamos el SIGNAL con código 45000
    IF v_disponible = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El recurso ya se encuentra reservado para ese dia y horario.';
    ELSE
        -- Si está disponible, guardamos la reserva
        INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado)
        VALUES (p_id_cliente, p_id_recurso, p_fecha, p_horas, p_total, 'Confirmada');
    END IF;
END //


-- Procedimiento 5: Cancelar una Reserva
CREATE PROCEDURE sp_cancelar_reserva(
    IN p_id_reserva INT
)
BEGIN
    DECLARE v_existe INT DEFAULT 0;

    -- Verificamos si la reserva realmente existe
    SELECT COUNT(*) INTO v_existe FROM reservas WHERE id_reserva = p_id_reserva;

    IF v_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La reserva que intentas cancelar no existe.';
    ELSE
        -- Cambiamos el estado a Cancelada (esto disparará automáticamente el Trigger)
        UPDATE reservas
        SET estado = 'Cancelada'
        WHERE id_reserva = p_id_reserva;
    END IF;
END //


-- ==============================================================================
-- UNIDAD: CURSORES
-- Concepto:
-- Un cursor permite recorrer una tabla fila por fila (como un "foreach" o "while" en C#).
-- Acá creamos un procedimiento que lee cada reserva confirmada y va sumando el total.
-- ==============================================================================
CREATE PROCEDURE sp_calcular_total_recaudado_cursor(
    OUT p_total_general DECIMAL(10,2)
)
BEGIN
    -- 1. Variables de control
    DECLARE v_fin INT DEFAULT FALSE;
    DECLARE v_monto DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_acumulador DECIMAL(10,2) DEFAULT 0.00;

    -- 2. Declaramos el CURSOR con la consulta a recorrer
    DECLARE cur_reservas CURSOR FOR 
        SELECT total FROM reservas WHERE estado = 'Confirmada';

    -- 3. Declaramos un HANDLER para que avise cuando se terminaron los registros (NOT FOUND)
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fin = TRUE;

    -- 4. Abrimos el cursor
    OPEN cur_reservas;

    -- 5. Bucle para procesar fila a fila
    bucle_reservas: LOOP
        -- Extraemos el valor de la fila actual
        FETCH cur_reservas INTO v_monto;
        
        -- Si ya no hay más filas, salimos del bucle
        IF v_fin THEN
            LEAVE bucle_reservas;
        END IF;

        -- Sumamos al acumulador
        SET v_acumulador = v_acumulador + v_monto;
    END LOOP;

    -- 6. Cerramos el cursor
    CLOSE cur_reservas;

    -- 7. Asignamos el valor final al parámetro de salida (OUT)
    SET p_total_general = v_acumulador;
END //


-- ==============================================================================
-- UNIDAD: TRIGGERS (DISPARADORES)
-- Concepto:
-- Un trigger es código automático que "salta" solo cuando pasa algo en la tabla.
-- Este trigger se activa DESPUÉS de hacer un UPDATE en la tabla reservas.
-- Si la reserva pasó a 'Cancelada', guarda un registro en la tabla de auditoría.
-- ==============================================================================
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


-- ==============================================================================
-- CONSULTAS DE DEMOSTRACIÓN DE UNIDADES CLAVE
-- Para que el alumno pueda ejecutarlas y mostrarlas en la defensa oral
-- ==============================================================================

-- 1. CONSULTA CON JOIN Y FILTRADO (Unidad 6 y 7):
-- Muestra todas las reservas confirmadas ordenadas por fecha:
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


-- 2. CONSULTAS CON SUBCONSULTAS (Unidad Subconsultas):
-- a) Recursos que nunca fueron reservados:
SELECT id_recurso, nombre, ubicacion
FROM recursos
WHERE id_recurso NOT IN (SELECT DISTINCT id_recurso FROM reservas);

-- b) Clientes que realizaron reservas por un importe superior al promedio general:
SELECT nombre, apellido, mail
FROM clientes
WHERE id_cliente IN (
    SELECT id_cliente 
    FROM reservas 
    WHERE total > (SELECT AVG(total) FROM reservas)
);


-- 3. CONSULTA CON CTE (Unidad UDF y CTE):
-- Agrupa los recursos por su tipo y saca promedios utilizando una tabla temporal legible:
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
