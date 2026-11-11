-- Primero que nada borra la base de datos si existe para evitar errores, la creamos nuevamente y la ponemos en uso.
drop database if exists tp_final_db;
create database tp_final_db;
use tp_final_db;

-- --------------------------------------------------
-- TABLAS
-- --------------------------------------------------

-- tipos de lugar (salas de reunion, oficinas, escritorios)
create table tipo_recursos (
    id_tipo_recurso int auto_increment primary key,
    nombre_tipo varchar(100) not null
);
-- aca guardamos si el lugar es una sala, una oficina o un escritorio

-- los lugares o salas que se pueden alquilar
create table recursos (
    id_recurso int auto_increment primary key,
    nombre varchar(100) not null,
    descripcion text,
    ubicacion varchar(100) not null,
    precio_por_hora decimal(10,2) not null,
    -- recursos detalle --
    mobiliario_incluido boolean null,
    cantidad_sillas int null,
    nro_categoria int null,
    -- =============== --
    id_tipo_recurso int not null,
    constraint fk_recursos_tipo
        foreign key (id_tipo_recurso)
        references tipo_recursos(id_tipo_recurso)
);
-- esta tabla guarda los lugares con su precio por hora y se conecta con tipo_recursos

-- los clientes que reservan
create table clientes (
    id_cliente int auto_increment primary key,
    nombre varchar(100) not null,
    apellido varchar(100) not null,
    telefono varchar(20) not null,
    mail varchar(255) not null,
    fecha_registro datetime default current_timestamp
);
-- guardamos los datos basicos de los clientes que alquilan

-- tabla pivote (o intermedia): une clientes con recursos (relacion muchos a muchos)
create table reservas (
    id_reserva int auto_increment primary key,
    id_cliente int not null,
    id_recurso int not null,
    fecha_reserva datetime not null,
    horas int not null default 1,
    total decimal(10,2) not null,
    estado varchar(20) not null default 'Confirmada',
    constraint fk_reservas_cliente
        foreign key (id_cliente)
        references clientes(id_cliente),
    constraint fk_reservas_recurso
        foreign key (id_recurso)
        references recursos(id_recurso)
);
-- esta es la tabla intermedia que junta al cliente con el recurso reservado, la fecha y el total

-- tabla para guardar el historial si alguien cancela una reserva
create table auditoria_reservas (
    id_auditoria int auto_increment primary key,
    id_reserva int not null,
    accion varchar(50) not null,
    fecha_accion datetime default current_timestamp,
    usuario varchar(100) default 'Sistema'
);
-- aca se guarda un registro solo si alguien cancela una reserva


-- --------------------------------------------------
-- CARGA DE DATOS PARA PROBAR QUE ANDE TODO
-- --------------------------------------------------

insert into tipo_recursos (nombre_tipo) values 
('Sala de Reuniones'),
('Oficina Privada'),
('Puesto de Trabajo');

insert into recursos (nombre, descripcion, ubicacion, precio_por_hora, mobiliario_incluido, cantidad_sillas, nro_categoria, id_tipo_recurso) values 
('Sala Innovacion', 'Proyector y pizarra para 10 personas', 'Piso 1 - Sector A', 3500.00, null, 40, null, 1),
('Sala Creativa', 'Mesa para 6 personas con TV', 'Piso 1 - Sector B', 2500.00, null, 70, null, 1),
('Oficina Ejecutiva 1', 'Oficina privada para 2 personas', 'Piso 2 - Of. 201', 4500.00, true, null, null, 2),
('Oficina Individual 2', 'Oficina privada individual', 'Piso 2 - Of. 202', 3000.00, false, null, null, 2),
('Puesto de trabajo 1', 'Puesto individual', 'Planta Baja - Box 1', 1200.00, null, null, 1, 3),
('Puesto de trabajo 2', 'Puesto compartido', 'Planta Baja - Box 2', 1800.00, null, null, 3, 3);

insert into clientes (nombre, apellido, telefono, mail) values 
('Lucas', 'Gonzalez', '1145678901', 'lucas.gonzalez@gmail.com'),
('Mariana', 'Lopez', '1178901234', 'mariana.lopez@hotmail.com'),
('Martin', 'Perez', '1134567890', 'martin.perez@yahoo.com'),
('Sofia', 'Fernandez', '1165432109', 'sofia.fernandez@gmail.com');

insert into reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado) values 
(1, 1, '2026-11-01 10:00:00', 2, 7000.00, 'Confirmada'),
(2, 3, '2026-11-01 14:00:00', 3, 13500.00, 'Confirmada'),
(3, 5, '2026-11-02 09:00:00', 4, 4800.00, 'Confirmada'),
(1, 2, '2026-11-03 16:00:00', 1, 2500.00, 'Cancelada');
-- cargamos datos de ejemplo para que las tablas no arranquen vacias al abrir el sistema


-- --------------------------------------------------
-- VISTAS (Consultas ya armadas para no repetir codigo)
-- --------------------------------------------------

create index idx_reservas_fecha on reservas(fecha_reserva);
create index idx_recursos_tipo on recursos(id_tipo_recurso);

-- vista para ver las reservas con el nombre del cliente y del lugar
create view vw_detalle_reservas as
select 
    r.id_reserva,
    concat(c.nombre, ' ', c.apellido) as cliente,
    c.mail as mail_cliente,
    rec.nombre as recurso,
    t.nombre_tipo as tipo_espacio,
    r.fecha_reserva,
    r.horas,
    r.total,
    r.estado
from
	reservas r
inner join clientes c on r.id_cliente = c.id_cliente
inner join recursos rec on r.id_recurso = rec.id_recurso
inner join tipo_recursos t on rec.id_tipo_recurso = t.id_tipo_recurso;
-- con esta vista vemos la lista de reservas con nombres reales en vez de numeros de id

-- vista para ver cuantas reservas tuvo cada lugar y cuanta plata junto
create view vw_resumen_recursos as
select 
    rec.id_recurso,
    rec.nombre as recurso,
    t.nombre_tipo as tipo,
    rec.precio_por_hora,
    count(r.id_reserva) as cantidad_reservas,
    ifnull(sum(case when r.estado = 'Confirmada' then r.total else 0 end), 0) as total_recaudado
from
	recursos rec
inner join tipo_recursos t on rec.id_tipo_recurso = t.id_tipo_recurso
left join reservas r on rec.id_recurso = r.id_recurso
group by rec.id_recurso, rec.nombre, t.nombre_tipo, rec.precio_por_hora;
-- te muestra el resumen de cada sala: cuantas veces se reservo y el total facturado


-- --------------------------------------------------
-- FUNCION: Para saber si un lugar esta libre (calcula solapamiento de horarios)
-- --------------------------------------------------

delimiter //

create function fn_verificar_disponibilidad(
    p_id_recurso int,
    p_fecha datetime,
    p_horas int
) 
returns int
deterministic
reads sql data
begin
    declare v_cantidad int default 0;
    declare v_duracion int;
    declare v_fecha_fin datetime;
    
    -- si mandan horas nulas o <= 0, asumimos 1 hora por defecto
    if p_horas is null or p_horas <= 0 then
        set v_duracion = 1;
    else
        set v_duracion = p_horas;
    end if;

    set v_fecha_fin = date_add(p_fecha, interval v_duracion hour);
    
    -- Chequeo matematico de superposicion de intervalos:
    -- (nuevo_inicio < fin_existente) AND (nuevo_fin > inicio_existente)
    select count(*) into v_cantidad
    from reservas
    where id_recurso = p_id_recurso 
      and estado = 'Confirmada'
      and p_fecha < date_add(fecha_reserva, interval horas hour)
      and v_fecha_fin > fecha_reserva;
      
    if v_cantidad = 0 then
        return 1; -- 1: Libre
    else
        return 0; -- 0: Ocupado (hay solapamiento)
    end if;
end //

delimiter ;
-- la funcion se fija si hay reservas que se superpongan en ese rango de horas: 1 (libre), 0 (ocupado)


-- --------------------------------------------------
-- PROCEDIMIENTOS ALMACENADOS (Para agregar, modificar y cancelar)
-- --------------------------------------------------

delimiter //

-- para agregar un cliente nuevo
create procedure sp_alta_cliente(
    in p_nombre varchar(100),
    in p_apellido varchar(100),
    in p_telefono varchar(20),
    in p_mail varchar(255)
)
begin
    insert into clientes (nombre, apellido, telefono, mail)
    values (p_nombre, p_apellido, p_telefono, p_mail);
end //
-- guarda un cliente nuevo en la tabla clientes con los datos que le mandamos

-- para cambiar los datos de un cliente
create procedure sp_modificar_cliente(
    in p_id_cliente int,
    in p_nombre varchar(100),
    in p_apellido varchar(100),
    in p_telefono varchar(20),
    in p_mail varchar(255)
)
begin
    update clientes
    set nombre = p_nombre,
        apellido = p_apellido,
        telefono = p_telefono,
        mail = p_mail
    where id_cliente = p_id_cliente;
end //
-- busca al cliente por su id y le actualiza los datos

-- para agregar un recurso nuevo (sala, oficina, etc.)
create procedure sp_alta_recurso(
    in p_nombre varchar(100),
    in p_descripcion text,
    in p_ubicacion varchar(100),
    in p_precio decimal(10,2),
    in p_mobiliario_incluido boolean,
    in p_cantidad_sillas int,
    in p_nro_categoria int,
    in p_id_tipo int
)
begin
    insert into recursos (nombre, descripcion, ubicacion, precio_por_hora, mobiliario_incluido, cantidad_sillas, nro_categoria, id_tipo_recurso)
    values (p_nombre, p_descripcion, p_ubicacion, p_precio, p_mobiliario_incluido, p_cantidad_sillas, p_nro_categoria, p_id_tipo);
end //
-- agrega una nueva sala u oficina a la tabla recursos

-- para modificar un recurso que ya existe
create procedure sp_modificar_recurso(
    in p_id_recurso int,
    in p_nombre varchar(100),
    in p_descripcion text,
    in p_ubicacion varchar(100),
    in p_precio decimal(10,2),
    in p_mobiliario_incluido boolean,
    in p_cantidad_sillas int,
    in p_nro_categoria int,
    in p_id_tipo int
)
begin
    update recursos
    set nombre = p_nombre,
        descripcion = p_descripcion,
        ubicacion = p_ubicacion,
        precio_por_hora = p_precio,
        mobiliario_incluido = p_mobiliario_incluido,
        cantidad_sillas = p_cantidad_sillas,
        nro_categoria = p_nro_categoria,
        id_tipo_recurso = p_id_tipo
    where id_recurso = p_id_recurso;
end //
-- busca un recurso por su id y le cambia los datos o el precio

-- para guardar una reserva nueva validando datos y disponibilidad sin solapamientos
create procedure sp_alta_reserva(
    in p_id_cliente int,
    in p_id_recurso int,
    in p_fecha datetime,
    in p_horas int,
    in p_total decimal(10,2)
)
begin
    declare v_disponible int;
    
    -- si pasa algun error de sql
    declare exit handler for sqlexception
    begin
        resignal;
    end;

    -- Validacion 1: Cantidad de horas valida
    if p_horas is null or p_horas <= 0 then
        signal sqlstate '45000'
            set message_text = 'La cantidad de horas de la reserva debe ser mayor a 0.';
    end if;

    -- Validacion 2: Total valido
    if p_total is null or p_total < 0 then
        signal sqlstate '45000'
            set message_text = 'El importe total de la reserva no puede ser negativo.';
    end if;

    -- Validacion 3: Chequear que el cliente exista
    if not exists (select 1 from clientes where id_cliente = p_id_cliente) then
        signal sqlstate '45000'
            set message_text = 'El cliente especificado no existe en el sistema.';
    end if;

    -- Validacion 4: Chequear que el recurso exista
    if not exists (select 1 from recursos where id_recurso = p_id_recurso) then
        signal sqlstate '45000'
            set message_text = 'El recurso especificado no existe en el sistema.';
    end if;

    -- nos fijamos si esta libre en todo el intervalo llamando a la funcion con p_horas
    set v_disponible = fn_verificar_disponibilidad(p_id_recurso, p_fecha, p_horas);

    -- si da 0 significa que se superpone con otra reserva confirmada
    if v_disponible = 0 then
        signal sqlstate '45000'
            set message_text = 'El recurso ya se encuentra reservado u ocupado en ese intervalo de horario.';
    else
        insert into reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado)
        values (p_id_cliente, p_id_recurso, p_fecha, p_horas, p_total, 'Confirmada');
    end if;
end //
-- chequea si el lugar esta libre en todo el intervalo; si esta libre inserta, si hay choque tira error 45000

-- para modificar fecha u horario de una reserva existente verificando disponibilidad
create procedure sp_modificar_reserva(
    in p_id_reserva int,
    in p_fecha datetime,
    in p_horas int,
    in p_total decimal(10,2)
)
begin
    declare v_id_recurso int;
    declare v_colision int default 0;
    declare v_fecha_fin datetime;

    -- chequeamos que la reserva exista y obtenemos su recurso
    select id_recurso into v_id_recurso from reservas where id_reserva = p_id_reserva;

    if v_id_recurso is null then
        signal sqlstate '45000'
            set message_text = 'La reserva que intentas modificar no existe.';
    end if;

    if p_horas is null or p_horas <= 0 then
        signal sqlstate '45000'
            set message_text = 'La cantidad de horas debe ser mayor a 0.';
    end if;

    if p_total is null or p_total < 0 then
        signal sqlstate '45000'
            set message_text = 'El importe total no puede ser negativo.';
    end if;

    set v_fecha_fin = date_add(p_fecha, interval p_horas hour);

    -- verificar colision con OTRA reserva confirmada (excluyendo la misma reserva que editamos)
    select count(*) into v_colision
    from reservas
    where id_recurso = v_id_recurso
      and id_reserva != p_id_reserva
      and estado = 'Confirmada'
      and p_fecha < date_add(fecha_reserva, interval horas hour)
      and v_fecha_fin > fecha_reserva;

    if v_colision > 0 then
        signal sqlstate '45000'
            set message_text = 'No se puede modificar la reserva: el recurso ya se encuentra ocupado en ese nuevo horario.';
    else
        update reservas
        set fecha_reserva = p_fecha,
            horas = p_horas,
            total = p_total
        where id_reserva = p_id_reserva;
    end if;
end //
-- modifica la reserva validando que el nuevo horario no choque con otras reservas

-- para cancelar una reserva que estaba hecha
create procedure sp_cancelar_reserva(
    in p_id_reserva int
)
begin
    declare v_estado varchar(20);

    -- chequeamos que la reserva exista y su estado actual
    select estado into v_estado from reservas where id_reserva = p_id_reserva;

    if v_estado is null then
        signal sqlstate '45000'
            set message_text = 'La reserva que intentas cancelar no existe.';
    elseif v_estado = 'Cancelada' then
        signal sqlstate '45000'
            set message_text = 'La reserva seleccionada ya fue cancelada previamente.';
    else
        update reservas
        set estado = 'Cancelada'
        where id_reserva = p_id_reserva;
    end if;
end //
-- busca la reserva y le cambia el estado a cancelada para que se dispare el trigger

-- --------------------------------------------------
-- CURSOR (Para recorrer las reservas fila por fila)
-- --------------------------------------------------

-- procedimiento con cursor que va sumando la plata de todas las reservas confirmadas
create procedure sp_calcular_total_recaudado_cursor(
    out p_total_general decimal(10,2)
)
begin
    declare v_fin int default false;
    declare v_monto decimal(10,2) default 0.00;
    declare v_acumulador decimal(10,2) default 0.00;

    -- consulta que va a recorrer el cursor
    declare cur_reservas cursor for 
        select
			total from reservas where estado = 'Confirmada';

    -- cuando no hay mas filas ponemos v_fin en true
    declare continue handler for not found set v_fin = true;

    open cur_reservas;

    -- bucle para ir leyendo una por una
    bucle_reservas: loop
        fetch cur_reservas into v_monto;
        
        if v_fin then
            leave bucle_reservas;
        end if;

        set v_acumulador = v_acumulador + v_monto;
    end loop;

    close cur_reservas;

    set p_total_general = v_acumulador;
end //
-- el cursor va leyendo una por una las reservas confirmadas y va sumando los totales en una variable


-- --------------------------------------------------
-- TRIGGER
-- --------------------------------------------------

-- si alguien cancela una reserva, guarda automaticamente el registro en auditoria
create trigger trg_auditoria_reservas
after update on reservas
for each row
begin
    if new.estado = 'Cancelada' and old.estado != 'Cancelada' then
        insert into auditoria_reservas (id_reserva, accion, fecha_accion, usuario)
        values (new.id_reserva, 'Cancelacion de reserva', now(), current_user());
    end if;
end //

delimiter ;
-- este trigger salta solo cuando se cancela una reserva y lo anota en la tabla auditoria_reservas

/*
-- --------------------------------------------------
-- CONSULTAS DE EJEMPLO POR SI QUEREMOS PROBAR QUE TODO ESTA BIEN :)
-- --------------------------------------------------

-- ver reservas confirmadas con el nombre de cada cliente
select 
    r.id_reserva,
    c.nombre as cliente,
    rec.nombre as espacio,
    r.fecha_reserva,
    r.total
from reservas r
inner join clientes c on r.id_cliente = c.id_cliente
inner join recursos rec on r.id_recurso = rec.id_recurso
where r.estado = 'Confirmada'
order by r.fecha_reserva asc;
-- junta reservas, clientes y recursos con inner join para mostrar datos legibles

-- lugares que nunca se reservaron
select id_recurso, nombre, ubicacion
from recursos
where id_recurso not in (select distinct id_recurso from reservas);
-- busca recursos que no estan en la lista de reservas hechas

-- clientes que gastaron mas que el promedio
select nombre, apellido, mail
from clientes
where id_cliente in (
    select id_cliente 
    from reservas 
    where total > (select avg(total) from reservas)
);
-- subconsulta para encontrar los clientes que gastaron mas que el promedio general

-- promedio de precios por tipo de lugar
with resumenportipo as (
    select 
        t.nombre_tipo,
        count(rec.id_recurso) as cantidad_recursos,
        avg(rec.precio_por_hora) as precio_promedio_por_hora
    from tipo_recursos t
    left join recursos rec on t.id_tipo_recurso = rec.id_tipo_recurso
    group by t.id_tipo_recurso, t.nombre_tipo
)
select * from resumenportipo;
-- usa una tabla temporal (cte) para calcular el promedio de precios de cada tipo de lugar
*/