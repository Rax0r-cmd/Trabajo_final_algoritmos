# Sistema de Gestión de Coworking y Reservas

Trabajo Práctico Final Integrador de **Algoritmos II**  
Carrera: **Analista de Sistemas de Información** (2º año)  
Institución: **Instituto Argentino de la Empresa**  
Profesor: **Lic. Adrián Aroca**  

---

## 📌 Descripción del Proyecto

Este proyecto consiste en desarrollar una aplicación de escritorio en **C# con Windows Forms** conectada a una base de datos en **MySQL**, basada en las **Consignas oficiales** y **Pautas de presentación** de la cátedra.

El sistema administra un espacio de trabajo compartido (**Coworking**), permitiendo:
1. **Gestionar Clientes**: registrar y modificar los datos de las personas que alquilan los espacios.
2. **Gestionar Recursos**: administrar los diferentes tipos de espacios disponibles (salas de reunión, oficinas privadas y puestos de escritorio) con su respectiva información y precio por hora.
3. **Gestionar Reservas**: registrar el alquiler de un recurso para un cliente en una fecha y horario determinado. Si el lugar ya se encuentra ocupado, la base de datos rechaza la reserva mediante una validación personalizada (`SIGNAL SQLSTATE '45000'`).
4. **Cancelar Reservas**: permitir cancelaciones y registrar automáticamente cada movimiento en una tabla de auditoría mediante un `Trigger`.

---

## 📂 Organización del Repositorio

El trabajo se encuentra centralizado dentro de la carpeta **`Trabajo Final`**:

* **`Trabajo Final/DB/`**:
  * `DB_TPFinal.sql`: script SQL completo con la creación de la base de datos, tablas, datos iniciales de prueba, vistas, funciones, procedimientos almacenados y triggers.
  * `Diagrama_DER.png`: diagrama Entidad-Relación visual de las tablas generado en MySQL Workbench.
  * `Diagrama_Editable.mwb`: archivo original del modelo de MySQL Workbench.
* **`Trabajo Final/src/`**: código fuente de la aplicación en C# (Windows Forms con Programación Orientada a Objetos).
* **`Trabajo Final/Documentacion/`**: notas, explicaciones de cada entrega y diagramas de clases.

---

## 👥 Reparto de Tareas del Equipo (3 Integrantes)

| Integrante | Módulo Asignado | Responsabilidades Principales |
| :--- | :--- | :--- |
| **Integrante 1** | **Reservas & Lógica Core** | • Tablas y procedimientos de reservas (`sp_alta_reserva`, `sp_cancelar_reserva`).<br>• Función de disponibilidad (`fn_verificar_disponibilidad`) y control de solapamiento con `SIGNAL 45000`.<br>• Formulario `FrmReservas` y captura de excepciones MySQL en C#.<br>• Clase de acceso a datos `ReservaDAO.cs`. |
| **Integrante 2** | **POO & Catálogo de Recursos** | • Tablas y procedimientos de recursos y categorías.<br>• Clases en C#: clase abstracta `Recurso`, clases derivadas (`Sala`, `OficinaPrivada`, `PuestoTrabajo`) e interfaz `IReservable`.<br>• Formulario `FrmRecursos`.<br>• Módulo de importación y exportación JSON.<br>• Clase `RecursoDAO.cs`. |
| **Integrante 3** | **Clientes, Vistas & UI General** | • Tablas y procedimientos de clientes (`sp_alta_cliente`, `sp_modificar_cliente`).<br>• Trigger de auditoría (`trg_auditoria_reservas`) y vistas SQL (`vw_detalle_reservas`, `vw_resumen_recursos`).<br>• Pantalla de inicio `FrmPrincipal`, formulario `FrmClientes` y pantalla de consultas con tablas.<br>• Clase de conexión `ConexionBD.cs` y `ClienteDAO.cs`. |

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** C# (.NET Framework / Windows Forms).
* **Base de Datos:** MySQL / MariaDB.
* **Modelado:** MySQL Workbench (EER Diagram).
* **Control de Versiones:** Git y GitHub.
