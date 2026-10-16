# Sistema de Gestion de Coworking y Reservas

![C#](https://img.shields.io/badge/C%23-239120?logo=csharp&logoColor=white)
![.NET](https://img.shields.io/badge/.NET-512BD4?logo=dotnet&logoColor=white)
![Windows Forms](https://img.shields.io/badge/Windows_Forms-0078D7?logo=windows&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)

Trabajo Practico Final de Algoritmos II  
Carrera: Analista de Sistemas  
Institucion: Instituto Argentino de la Empresa  
Profesor: Lic. Adrian Aroca  

Desarrolladores:
- Jonathan Lester Tullo
- David Samuel Ortega
- Maximiliano Scollo

---

## Descripcion del Proyecto

Este proyecto consiste en desarrollar una aplicacion de escritorio en C# con Windows Forms conectada a una base de datos en MySQL, basada en las consignas oficiales y pautas de presentacion de la catedra.

El sistema administra un espacio de trabajo compartido (Coworking), permitiendo:
1. Gestionar Clientes: registrar y modificar los datos de las personas que alquilan los espacios.
2. Gestionar Recursos: administrar los diferentes tipos de espacios disponibles (salas de reunion, oficinas privadas y puestos de escritorio) con su precio por hora.
3. Gestionar Reservas: registrar el alquiler de un recurso para un cliente en una fecha y horario determinado. Si el lugar ya se encuentra ocupado, la base de datos rechaza la reserva mediante una validacion personalizada (SIGNAL SQLSTATE '45000').
4. Cancelar Reservas: permitir cancelaciones y registrar automaticamente cada movimiento en una tabla de auditoria mediante un Trigger.

---

## Organizacion del Repositorio

El trabajo se encuentra centralizado dentro de la carpeta Trabajo Final:

- Trabajo Final/DB/:
  - DB_TPFinal.sql: script SQL completo con la creacion de la base de datos, tablas, datos iniciales de prueba, vistas, funcion de disponibilidad, procedimientos almacenados y triggers.
  - Diagrama_DER.png: diagrama Entidad-Relacion visual de las tablas generado en MySQL Workbench.
  - Diagrama_Editable.mwb: archivo original del modelo de MySQL Workbench.
- Trabajo Final/src/: codigo fuente de la aplicacion en C# (Windows Forms con Programacion Orientada a Objetos).
- Trabajo Final/Documentacion/: notas y explicaciones del trabajo practico.

---

## Tecnologias Utilizadas

- Lenguaje: C# (Windows Forms con .NET).
- Base de Datos: MySQL / MariaDB.
- Modelado: MySQL Workbench.
- Control de Versiones: Git y GitHub.
