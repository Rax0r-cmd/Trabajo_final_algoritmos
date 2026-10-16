# Sistema de Gestion de Coworking y Reservas

<p align="left">
  <img src="https://skillicons.dev/icons?i=cs,dotnet,mysql,git,visualstudio" alt="Tech Stack" />
</p>

Trabajo Practico Final de Algoritmos II  
Carrera: Analista de Sistemas  
Institucion: Instituto Argentino de la Empresa  
Profesor: Lic. Adrian Aroca  

Desarrolladores:  
Jonathan Lester Tullo · David Samuel Ortega · Maximiliano Scollo  

---

## Descripcion del Proyecto

Este proyecto consiste en desarrollar una aplicacion de escritorio en C# con Windows Forms conectada a una base de datos en MySQL, basada en las consignas oficiales y pautas de presentacion de la catedra.

El sistema administra un espacio de trabajo compartido (Coworking), permitiendo:

1. Gestionar Clientes: registrar y modificar los datos de las personas que alquilan los espacios.
2. Gestionar Recursos: administrar los diferentes tipos de espacios disponibles (salas de reunion, oficinas privadas y puestos de escritorio) con su precio por hora.
3. Gestionar Reservas: registrar el alquiler de un recurso para un cliente en una fecha y horario determinado. Si el lugar ya se encuentra ocupado, la base de datos rechaza la reserva mediante una validacion personalizada (SIGNAL SQLSTATE '45000').
4. Cancelar Reservas: permitir cancelaciones y registrar automaticamente cada movimiento en una tabla de auditoria mediante un Trigger.

---

## Como usar / Instalacion

### 1. Clonar el repositorio

Clonar con HTTPS:
```bash
git clone https://github.com/Rax0r-cmd/Trabajo_final_algoritmos.git
```

Clonar con SSH:
```bash
git clone git@github.com:Rax0r-cmd/Trabajo_final_algoritmos.git
```

### 2. Base de Datos (MySQL)

Abrir MySQL Workbench o phpMyAdmin y ejecutar el script ubicado en:
```text
Trabajo Final/DB/DB_TPFinal.sql
```
Esto crea la base de datos `tp_final_db`, las tablas, las vistas, los procedimientos almacenados, las funciones y los triggers necesarios.

### 3. Ejecutar la aplicacion

Abrir la solucion en Visual Studio desde la carpeta:
```text
Trabajo Final/src/
```
Compilar y presionar F5 (Iniciar) para ejecutar el sistema.

---

## Organizacion del Repositorio

```text
Trabajo Final/
├── DB/
│   ├── DB_TPFinal.sql          (script SQL completo con tablas, vistas, SPs y triggers)
│   ├── Diagrama_DER.png        (diagrama Entidad-Relacion visual generado en Workbench)
│   └── Diagrama_Editable.mwb   (archivo del modelo de MySQL Workbench)
├── src/                        (codigo fuente de la aplicacion en C# Windows Forms)
└── Documentacion/              (notas y documentacion del trabajo practico)
```

---

## Tecnologias Utilizadas

Lenguaje: C# (Windows Forms con .NET Framework)  
Base de Datos: MySQL / MariaDB  
Modelado: MySQL Workbench  
Control de Versiones: Git y GitHub  
