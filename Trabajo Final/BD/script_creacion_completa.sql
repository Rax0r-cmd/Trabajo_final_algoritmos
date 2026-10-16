-- ==============================================================================
-- TRABAJO PRÁCTICO: SISTEMA DE COWORKING Y RESERVAS
-- Materia: Algoritmos II
-- ==============================================================================


-- ==============================================================================
-- PASO 1: CREAR LA BASE DE DATOS
-- Si ya existe una base con este nombre la borramos para empezar de cero,
-- la creamos limpia y nos paramos en ella para trabajar.
-- ==============================================================================
DROP DATABASE IF EXISTS TP_FINAL_DB;
CREATE DATABASE TP_FINAL_DB;
USE TP_FINAL_DB;


-- ==============================================================================
-- PASO 2: CREAR LAS TABLAS
-- Definimos las tablas principales del sistema con sus columnas y tipos de datos.
-- Usamos AUTO_INCREMENT para que los códigos (ID) se numeren solos (1, 2, 3...).
-- ==============================================================================

-- Tabla para guardar los tipos de espacios que ofrecemos (ej: sala, oficina, escritorio)
CREATE TABLE tipo_recursos (
    id_tipo_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(100) NOT NULL
);

-- Tabla para los recursos o espacios físicos que se alquilan
CREATE TABLE recursos (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ubicacion VARCHAR(100) NOT NULL,
    precio_por_hora DECIMAL(10,2) NOT NULL,
    id_tipo_recurso INT NOT NULL,
    
    -- Conectamos esta tabla con la de tipos de recursos
    CONSTRAINT fk_recursos_tipo
        FOREIGN KEY (id_tipo_recurso)
        REFERENCES tipo_recursos(id_tipo_recurso)
);

-- Tabla para los clientes que vienen a trabajar o alquilar
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    mail VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de reservas: relaciona qué cliente reservó qué recurso y cuándo
CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_recurso INT NOT NULL,
    fecha_reserva DATETIME NOT NULL,
    horas INT NOT NULL DEFAULT 1,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Confirmada', -- puede ser Confirmada o Cancelada
    
    -- Conectamos con el cliente
    CONSTRAINT fk_reservas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),
        
    -- Conectamos con el recurso alquilado
    CONSTRAINT fk_reservas_recurso
        FOREIGN KEY (id_recurso)
        REFERENCES recursos(id_recurso)
);

-- Tabla de auditoría: acá se anota automáticamente cuando alguien cancela una reserva
CREATE TABLE auditoria_reservas (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha_accion DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100) DEFAULT 'Sistema'
);


-- ==============================================================================
-- PASO 3: CARGAR DATOS DE EJEMPLO
-- Ponemos datos de prueba para que la base no esté vacía al abrir el programa.
-- ==============================================================================

-- Cargamos 3 tipos de espacios
INSERT INTO tipo_recursos (nombre_tipo) VALUES 
('Sala de Reuniones'),
('Oficina Privada'),
('Puesto de Trabajo');

-- Cargamos salas, oficinas y escritorios con sus precios
INSERT INTO recursos (nombre, descripcion, ubicacion, precio_por_hora, id_tipo_recurso) VALUES 
('Sala Innovación', 'Tiene proyector y pizarra para 10 personas', 'Piso 1 - Sector A', 3500.00, 1),
('Sala Creativa', 'Mesa redonda para 6 personas con tele Smart', 'Piso 1 - Sector B', 2500.00, 1),
('Oficina Ejecutiva 1', 'Oficina privada para 2 personas con aire acondicionado', 'Piso 2 - Of. 201', 4500.00, 2),
('Oficina Individual 2', 'Oficina privada para 1 persona tranquila', 'Piso 2 - Of. 202', 3000.00, 2),
('Escritorio Flex 01', 'Puesto individual con wifi rápido', 'Planta Baja - Box 1', 1200.00, 3),
('Escritorio Flex 02', 'Puesto individual con enchufe y lámpara', 'Planta Baja - Box 2', 1200.00, 3);

-- Cargamos 4 clientes de prueba
INSERT INTO clientes (nombre, apellido, telefono, mail) VALUES 
('Lucas', 'Gonzalez', '1145678901', 'lucas.gonzalez@gmail.com'),
('Mariana', 'Lopez', '1178901234', 'mariana.lopez@hotmail.com'),
('Martin', 'Perez', '1134567890', 'martin.perez@yahoo.com'),
('Sofia', 'Fernandez', '1165432109', 'sofia.fernandez@gmail.com');

-- Cargamos algunas reservas hechas
INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado) VALUES 
(1, 1, '2026-11-01 10:00:00', 2, 7000.00, 'Confirmada'),
(2, 3, '2026-11-01 14:00:00', 3, 13500.00, 'Confirmada'),
(3, 5, '2026-11-02 09:00:00', 4, 4800.00, 'Confirmada'),
(1, 2, '2026-11-03 16:00:00', 1, 2500.00, 'Cancelada');


-- ==============================================================================
-- PASO 4: VISTAS E ÍNDICES
-- - Los índices hacen que buscar por fecha o tipo sea más rápido.
-- - Las vistas son consultas que dejamos guardadas para usarlas como si fueran tablas.
-- ==============================================================================

-- Ponemos índices en las columnas donde más vamos a buscar
CREATE INDEX idx_reservas_fecha ON reservas(fecha_reserva);
CREATE INDEX idx_recursos_tipo ON recursos(id_tipo_recurso);

-- Vista 1: Muestra todas las reservas juntas con el nombre del cliente y del recurso
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

-- Vista 2: Muestra cuántas reservas tuvo cada sala u oficina y cuánta plata generó
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
-- PASO 5: FUNCIÓN ALMACENADA (UDF)
-- Esta función chequea si un espacio está libre u ocupado en una fecha y hora.
-- Si está libre devuelve 1. Si ya lo reservaron devuelve 0.
-- ==============================================================================
DELIMITER //

CREATE FUNCTION fn_verificar_disponibilidad(
    p_id_recurso INT,
    p_fecha DATETIME
) 
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_cantidad INT DEFAULT 0;
    
    -- Nos fijamos si hay alguna reserva confirmada justo en ese horario
    SELECT COUNT(*) INTO v_cantidad
    FROM reservas
    WHERE id_recurso = p_id_recurso
      AND fecha_reserva = p_fecha
      AND estado = 'Confirmada';
      
    -- Si la cuenta dio 0 significa que no hay nadie, devolvemos 1 (disponible)
    IF v_cantidad = 0 THEN
        RETURN 1;
    ELSE
        RETURN 0; -- Ocupado
    END IF;
END //

DELIMITER ;


-- ==============================================================================
-- PASO 6: PROCEDIMIENTOS ALMACENADOS (STORED PROCEDURES)
-- Son funciones guardadas dentro de la base para agregar, modificar o cancelar datos.
-- ==============================================================================
DELIMITER //

-- Procedimiento para dar de alta a un cliente nuevo
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

-- Procedimiento para modificar los datos de un cliente que ya existe
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

-- Procedimiento para agregar un recurso nuevo (sala, oficina, etc.)
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

-- Procedimiento para cambiar los datos o precio de un recurso
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

-- Procedimiento para crear una reserva.
-- Tiene un HANDLER para errores y usa SIGNAL 45000 si el lugar ya está ocupado.
CREATE PROCEDURE sp_alta_reserva(
    IN p_id_cliente INT,
    IN p_id_recurso INT,
    IN p_fecha DATETIME,
    IN p_horas INT,
    IN p_total DECIMAL(10,2)
)
BEGIN
    DECLARE v_disponible INT;
    
    -- Handler: si salta cualquier error raro de SQL, lo relanza para no ocultarlo
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        RESIGNAL;
    END;

    -- Usamos nuestra función del PASO 5 para revisar si está libre
    SET v_disponible = fn_verificar_disponibilidad(p_id_recurso, p_fecha);

    -- Si la función devolvió 0, tiramos el error con SIGNAL 45000
    IF v_disponible = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El recurso ya se encuentra reservado en ese dia y horario.';
    ELSE
        -- Si está libre, guardamos la reserva normalmente
        INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado)
        VALUES (p_id_cliente, p_id_recurso, p_fecha, p_horas, p_total, 'Confirmada');
    END IF;
END //

-- Procedimiento para cancelar una reserva que estaba confirmada
CREATE PROCEDURE sp_cancelar_reserva(
    IN p_id_reserva INT
)
BEGIN
    DECLARE v_existe INT DEFAULT 0;

    -- Nos fijamos si el ID que nos pasaron existe en la tabla
    SELECT COUNT(*) INTO v_existe FROM reservas WHERE id_reserva = p_id_reserva;

    IF v_existe = 0 THEN
        -- Si no existe, tiramos error con SIGNAL
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La reserva que intentas cancelar no existe.';
    ELSE
        -- Si existe, le cambiamos el estado a Cancelada
        -- (Al hacer este UPDATE, se va a disparar solo el Trigger del Paso 8)
        UPDATE reservas
        SET estado = 'Cancelada'
        WHERE id_reserva = p_id_reserva;
    END IF;
END //


-- ==============================================================================
-- PASO 7: CURSOR
-- Un cursor funciona como un 'while' o 'foreach' en programación:
-- va leyendo fila por fila una consulta y va sumando la plata de cada reserva.
-- ==============================================================================
CREATE PROCEDURE sp_calcular_total_recaudado_cursor(
    OUT p_total_general DECIMAL(10,2)
)
BEGIN
    -- Variables para controlar el bucle y acumular la plata
    DECLARE v_fin INT DEFAULT FALSE;
    DECLARE v_monto DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_acumulador DECIMAL(10,2) DEFAULT 0.00;

    -- Declaramos el cursor con las reservas confirmadas que queremos leer
    DECLARE cur_reservas CURSOR FOR 
        SELECT total FROM reservas WHERE estado = 'Confirmada';

    -- Handler: cuando ya no queden más filas que leer (NOT FOUND), ponemos v_fin en TRUE
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fin = TRUE;

    -- Abrimos el cursor para empezar a leer
    OPEN cur_reservas;

    -- Bucle que lee registro por registro
    bucle_reservas: LOOP
        -- Traemos el monto de la fila actual
        FETCH cur_reservas INTO v_monto;
        
        -- Si se terminaron las filas, salimos del bucle
        IF v_fin THEN
            LEAVE bucle_reservas;
        END IF;

        -- Sumamos el monto al total acumulado
        SET v_acumulador = v_acumulador + v_monto;
    END LOOP;

    -- Cerramos el cursor cuando terminamos
    CLOSE cur_reservas;

    -- Guardamos el total final en la variable de salida (OUT)
    SET p_total_general = v_acumulador;
END //


-- ==============================================================================
-- PASO 8: TRIGGER (DISPARADOR)
-- Es una acción automática: cada vez que alguien cancela una reserva (UPDATE),
-- este trigger salta solo y anota en la tabla auditoria_reservas qué pasó y cuándo.
-- ==============================================================================
CREATE TRIGGER trg_auditoria_reservas
AFTER UPDATE ON reservas
FOR EACH ROW
BEGIN
    -- Solo guardamos en auditoría si el estado cambió a 'Cancelada'
    IF NEW.estado = 'Cancelada' AND OLD.estado != 'Cancelada' THEN
        INSERT INTO auditoria_reservas (id_reserva, accion, fecha_accion, usuario)
        VALUES (NEW.id_reserva, 'Cancelacion de reserva', NOW(), CURRENT_USER());
    END IF;
END //

DELIMITER ;


-- ==============================================================================
-- PASO 9: CONSULTAS DE EJEMPLO PARA MOSTRAR AL PROFESOR
-- Son consultas preparadas para probar que todo anda bien y mostrarlas en clase.
-- ==============================================================================

-- 1. CONSULTA CON JOIN Y FILTRADO (Unidad 6 y 7):
-- Muestra las reservas confirmadas con el nombre del cliente y el lugar
SELECT 
    r.id_reserva,
    c.nombre AS cliente,
    rec.nombre AS espacio_alquilado,
    r.fecha_reserva,
    r.total
FROM reservas r
INNER JOIN clientes c ON r.id_cliente = c.id_cliente
INNER JOIN recursos rec ON r.id_recurso = rec.id_recurso
WHERE r.estado = 'Confirmada'
ORDER BY r.fecha_reserva ASC;


-- 2. SUBCONSULTAS (Unidad Subconsultas):
-- a) Lugares que todavía NUNCA nadie reservó (usa una subconsulta con NOT IN)
SELECT id_recurso, nombre, ubicacion
FROM recursos
WHERE id_recurso NOT IN (SELECT DISTINCT id_recurso FROM reservas);

-- b) Clientes que gastaron más que el promedio general de todas las reservas
SELECT nombre, apellido, mail
FROM clientes
WHERE id_cliente IN (
    SELECT id_cliente 
    FROM reservas 
    WHERE total > (SELECT AVG(total) FROM reservas)
);


-- 3. CTE (Tabla temporal con WITH ... AS de la Unidad UDF y CTE):
-- Agrupa los recursos por tipo y calcula el precio promedio de cada categoría
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
