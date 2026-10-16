# Documentación del Proyecto - Coworking y Reservas

Este documento es para ir anotando todo lo que vamos haciendo en el Trabajo Práctico de **Algoritmos II**, explicado de forma sencilla para tenerlo a mano cuando tengamos que defender el proyecto o armar el informe final.

---

## 📌 ¿De qué trata el sistema?
Es una aplicación para administrar un espacio de **Coworking** (oficinas compartidas). 
Básicamente permite:
- Registrar clientes.
- Cargar espacios que se alquilan (salas de reunión, oficinas privadas y puestos de escritorio) con su precio por hora.
- Hacer reservas para que un cliente use una sala en un día y horario específico.
- Cancelar reservas si el cliente no puede venir.

---

## ✅ Parte 1: Base de Datos (MySQL) - YA TERMINADA

Todo el código de la base de datos está guardado y probado en `Trabajo Final/DB/DB_TPFinal.sql`.

### 1. Tablas creadas
* **`tipo_recursos`**: guarda las categorías de los lugares (`Sala de Reuniones`, `Oficina Privada`, `Puesto de Trabajo`).
* **`recursos`**: son los lugares físicos con su nombre, descripción, ubicación y precio por hora. Se conecta con el tipo de recurso.
* **`clientes`**: los datos de las personas que alquilan (nombre, apellido, teléfono, mail).
* **`reservas` (Tabla pivote o intermedia)**: une al cliente con el recurso que reservó, la fecha, las horas y el total a pagar. Es la tabla principal del sistema.
* **`auditoria_reservas`**: tabla especial donde se anota automáticamente cuando alguien cancela una reserva.

### 2. Diagrama DER
* Lo armamos en MySQL Workbench y lo guardamos en la carpeta `DB`:
  - `Diagrama_DER.png`: la foto del diagrama para pegar en el informe.
  - `Diagrama_Editable.mwb`: el archivo editable por si queremos cambiar algo después.
* Muestra las tablas conectadas con relaciones de 1 a N (uno a muchos).

### 3. Procedimientos Almacenados (Stored Procedures)
Los usamos para no escribir consultas largas desde el código:
* **`sp_alta_cliente`** y **`sp_modificar_cliente`**: para agregar o actualizar clientes.
* **`sp_alta_recurso`** y **`sp_modificar_recurso`**: para dar de alta salas u oficinas y cambiarles el precio.
* **`sp_alta_reserva`**: guarda una reserva nueva. **Ojo:** primero usa la función de disponibilidad. Si la sala ya está ocupada en ese horario, tira un error con `SIGNAL SQLSTATE '45000'` para avisar que no se puede.
* **`sp_cancelar_reserva`**: le cambia el estado a 'Cancelada'.

### 4. Vistas (Views)
Son consultas que dejamos guardadas para no hacer `JOIN` todo el tiempo:
* **`vw_detalle_reservas`**: muestra la lista de reservas con los nombres reales de los clientes y las salas (en vez de mostrar solo números de ID).
* **`vw_resumen_recursos`**: muestra cada lugar con cuántas reservas tuvo y cuánta plata recaudó en total.

### 5. Función de Disponibilidad (UDF)
* **`fn_verificar_disponibilidad`**: le pasamos el ID del lugar y la fecha/hora. Si está libre devuelve `1`, si ya hay alguien devuelve `0`.

### 6. Trigger (Disparador automático)
* **`trg_auditoria_reservas`**: salta solo después de que alguien cancela una reserva y anota en `auditoria_reservas` la fecha, qué reserva fue y quién lo hizo.

### 7. Cursor
* **`sp_calcular_total_recaudado_cursor`**: recorre las reservas confirmadas una por una (como un bucle `while`) y va sumando la plata en una variable para saber la recaudación total.

---

## ⏳ Próximos pasos (lo que nos falta hacer de a poco)

* [ ] **Parte 2: Programación Orientada a Objetos en C#**
  - Crear la clase abstracta `Recurso` y las clases que heredan de ella (`Sala`, `OficinaPrivada`, `PuestoTrabajo`).
  - Crear la interfaz `IReservable`.
  - Crear las clases `Cliente` y `Reserva`.
* [ ] **Parte 3: Formularios de Windows Forms**
  - Pantalla principal con menú.
  - Pantallas para cargar clientes, recursos y hacer reservas.
* [ ] **Parte 4: Conectar C# con MySQL**
  - Armar la clase de conexión y los métodos para ejecutar los procedimientos que ya creamos.
* [ ] **Parte 5: Manejo de errores y archivo JSON**
  - Atapar el error `45000` de MySQL desde C# para mostrar un cartel lindo al usuario si la sala está ocupada.
  - Exportar/importar datos en JSON.
