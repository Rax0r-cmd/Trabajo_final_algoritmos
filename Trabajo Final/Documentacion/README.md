# Documentacion del Trabajo Practico - Algoritmos II

Sistema de Gestion de Coworking y Reservas  
Carrera: Analista de Sistemas  
Profesor: Lic. Adrian Aroca  

Integrantes:
- Jonathan Lester Tullo
- David Samuel Ortega
- Maximiliano Scollo

1. De que trata el proyecto
El proyecto consiste en armar un sistema de escritorio para administrar un espacio de coworking. La idea principal es poder registrar clientes, los espacios que se alquilan (salas de reunion, oficinas privadas y puestos de trabajo) y las reservas que hacen los clientes por fecha y hora. Ademas, si un espacio ya esta ocupado en ese horario, el sistema no tiene que permitir la reserva.

2. Base de datos (MySQL)
La base de datos se llama tp_final_db y el archivo con todo el codigo para crearla es DB_TPFinal.sql dentro de la carpeta DB.

Tablas:
- tipo_recursos: guarda los tipos de espacios (sala de reuniones, oficina privada, puesto de trabajo).
- recursos: los espacios fisicos con su descripcion, ubicacion, precio por hora y el tipo de recurso.
- clientes: datos de las personas que alquilan (nombre, apellido, telefono y mail).
- reservas: es la tabla intermedia que une al cliente con el recurso reservado, la fecha, las horas y el precio total.
- auditoria_reservas: guarda un registro automatico cada vez que alguien cancela una reserva.

Vistas:
- vw_detalle_reservas: muestra la lista de reservas con los nombres de clientes y recursos en vez de los numeros de id.
- vw_resumen_recursos: muestra cuanto dinero recaudo cada sala u oficina y cuantas reservas tuvo.

Funcion:
- fn_verificar_disponibilidad: recibe el id del recurso y la fecha. Devuelve 1 si esta libre o 0 si ya esta reservado.

Procedimientos almacenados:
- sp_alta_cliente: agrega un cliente nuevo.
- sp_modificar_cliente: cambia los datos de un cliente existente.
- sp_alta_recurso: agrega una sala u oficina nueva.
- sp_modificar_recurso: actualiza datos o precios de un recurso.
- sp_alta_reserva: verifica con la funcion si el lugar esta libre. Si esta libre guarda la reserva, si esta ocupado tira un cartel de error usando SIGNAL 45000.
- sp_cancelar_reserva: cambia el estado de la reserva a cancelada.

Trigger:
- trg_auditoria_reservas: salta solo cuando se cancela una reserva y anota la fecha y usuario en la tabla de auditoria.

Cursor:
- sp_calcular_total_recaudado_cursor: recorre fila por fila las reservas confirmadas y va sumando la plata para devolver el total general.

3. Diagrama DER
El diagrama entidad relacion de las tablas lo hicimos en MySQL Workbench y dejamos la imagen guardada en Trabajo Final/DB/Diagrama_DER.png junto con el archivo editable Diagrama_Editable.mwb.

4. Lo que nos falta hacer
- Programar las clases en C# con Windows Forms (clase abstracta Recurso, las clases hijas Sala, OficinaPrivada, PuestoTrabajo, y las clases Cliente y Reserva).
- Armar los formularios de la interfaz grafica.
- Conectar C# con MySQL para llamar a los procedimientos almacenados.
- Hacer la parte de importar y exportar en JSON.
