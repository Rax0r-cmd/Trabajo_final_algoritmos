<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="src/Img/Logo/Logo_coWorking_con_lema_turquesa_y_blanco.png">
    <source media="(prefers-color-scheme: light)" srcset="src/Img/Logo/Logo_coWorking_para_fondo_blanco.png">
    <img alt="Logo Coworking" src="src/Img/Logo/Logo_coWorking_para_fondo_blanco.png" width="450" />
  </picture>
</p>

# Sistema de Gestión de Coworking y Reservas

<p align="left">
  <img src="https://skillicons.dev/icons?i=cs,dotnet,mysql,git,visualstudio" alt="Tech Stack" />
</p>

Trabajo Práctico Final Integrador de Algoritmos II  
**Carrera:** Analista de Sistemas de Información  
**Institución:** Instituto Argentino de la Empresa  
**Profesor:** Lic. Adrián Aroca  
**Ciclo Lectivo:** 2026  

**Desarrolladores (Grupo 2):**  
- Jonathan Lester Tullo (shonimdp@gmail.com)  
- David Samuel Ortega (davidortegaa86@gmail.com)  
- Maximiliano Scollo (maximilianoscollo17@gmail.com)  

---

## Descripción del Proyecto

Aplicación de escritorio corporativa desarrollada en **C# (.NET Framework 4.7.2)** con interfaz gráfica en **Windows Forms**, conectada de forma centralizada a un motor de base de datos relacional **MySQL / MariaDB (XAMPP)**, diseñada bajo las normas institucionales y pautas académicas de la cátedra.

El sistema administra integralmente las operaciones de un espacio de trabajo colaborativo (**Coworking**):

1. **Gestión de Clientes:** Padrón de clientes registrados con validación de datos de contacto.
2. **Catálogo Polimórfico de Recursos:** Administración de espacios físicos especializados (`Sala`, `OficinaPrivada`, `PuestoTrabajo`) que heredan de una clase abstracta base `Recurso` e implementan la interfaz `IReservable`.
3. **Cálculo Dinámico de Costos:** Sobrescritura polimórfica del método `CalcularCosto(horas)` en cada tipo de recurso, aplicando tarifas base y recargos por comodidades y mobiliario.
4. **Control Estricto de Concurrencia y Solapamiento:** Registro transaccional de reservas mediante Procedimientos Almacenados en MySQL. Si un recurso se encuentra ocupado en el rango horario solicitado, la base de datos aborta la transacción emitiendo `SIGNAL SQLSTATE '45000'`, el cual es capturado y tratado de forma amigable por la aplicación mediante `MySqlException`.
5. **Auditoría Automática:** Trigger en base de datos (`trg_auditoria_reservas`) que registra de forma transparente e inmutable cada cancelación de turnos.
6. **Consultas en Memoria e Intercambio de Datos:** Filtrado avanzado de reservas mediante expresiones **LINQ** en la capa gestora y serialización **JSON** para exportación/importación de registros.

---

## Arquitectura del Sistema

El software adopta una **arquitectura en capas** con separación estricta de responsabilidades (SoC), desacoplando la interfaz visual, la lógica de negocio en memoria, el acceso a datos y el motor relacional:

```mermaid
flowchart TD
    UI["<div style='min-width:380px;text-align:left;padding:6px;'><b>1. Capa de Presentación (Windows Forms)</b><br/>• FrmLogin: Autenticación de Administradores y enlace a WhatsApp<br/>• FrmPrincipal: Navegación por Solapas (Control, Reservas y Gestión)<br/>• Grillas interactivas DataGridView para turnos y catálogos</div>"]

    BLL["<div style='min-width:340px;text-align:left;padding:6px;'><b>2. Capa de Negocio y Dominio (POO)</b><br/>• GestoraCoworking: Colecciones en memoria y filtros LINQ<br/>• Recurso (Abstracta) -> Sala, OficinaPrivada, PuestoTrabajo<br/>• Polimorfismo en método CalcularCosto(horas)<br/>• Contrato formal IReservable · Cliente · Reserva · Estados</div>"]

    DAL["<div style='min-width:340px;text-align:left;padding:6px;'><b>3. Capa de Acceso a Datos (DAO)</b><br/>• GestorDAO: Mapeo relacional y comandos parametrizados<br/>• Conexion.cs: Conexión MySqlConnection central con using<br/>• Cadena de conexión externalizada en App.config<br/>• Tratamiento de excepción SIGNAL 45000 (Error 1644)</div>"]

    DB["<div style='min-width:380px;text-align:left;padding:6px;'><b>4. Base de Datos Relacional (MySQL - tp_final_db)</b><br/>• Stored Procedures: sp_alta_reserva, sp_cancelar_reserva, sp_alta_cliente<br/>• Regla Anti-solapamiento: fn_verificar_disponibilidad y SIGNAL 45000<br/>• Vistas analíticas: vw_detalle_reservas y vw_resumen_recursos<br/>• Trigger inmutable de auditoría: trg_auditoria_reservas</div>"]

    UI -->|Consultas y filtrado en memoria| BLL
    UI -->|Persistencia transaccional y carga de grillas| DAL
    BLL -->|Entidades del dominio a persistir| DB
    DAL -->|Ejecución de SP y lectura de vistas SQL| DB
```

---

## Puesta en Marcha e Instalación

### 1. Requisito Previo Obligatorio: Base de Datos en MySQL

Antes de instalar o ejecutar la aplicación, es indispensable tener corriendo el motor de persistencia relacional con el esquema del sistema:

1. **Iniciar MySQL:** Abrir el panel de control de **XAMPP** y encender el servicio **MySQL** (verificar que quede en verde en el puerto predeterminado `3306`).
2. **Cargar el Esquema:** Abrir **phpMyAdmin** (`http://localhost/phpmyadmin`) o **MySQL Workbench**, importar y ejecutar por única vez el archivo:
   ```text
   DB/DB_TPFinal.sql
   ```
   *Esto creará automáticamente la base `tp_final_db`, las 5 tablas normalizadas, las vistas analíticas, los procedimientos almacenados con validación `SIGNAL 45000`, la función de disponibilidad horaria y el trigger de auditoría con datos de prueba.*

---

### 2. Modos de Uso del Sistema

Una vez que la base de datos está activa, podés elegir cualquiera de las siguientes opciones:

#### Opción A: Instalación directa con el Instalador Oficial (Recomendada)

No se requiere tener abierto ni instalado Visual Studio:

1. Ir a la carpeta `Instalador/` del repositorio.
2. Hacer doble clic directamente en el archivo **`InstaladorCoWorking.msi`**.
3. Seguir los pasos del asistente de Windows Installer ("Siguiente" $\rightarrow$ "Instalar").
4. El instalador creará automáticamente los accesos directos en el **Escritorio** y en el Menú Inicio.

#### Opción B: Ejecución desde el código fuente en Visual Studio

Para desarrolladores que deseen depurar o inspeccionar el código:

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Rax0r-cmd/Trabajo_final_algoritmos.git
   ```
2. Abrir la solución `SistemaDeGestion/SistemaDeGestion.sln` (o `.slnx`) en **Microsoft Visual Studio 2022**.
3. Restaurar paquetes NuGet (para vincular `MySql.Data`).
4. Seleccionar la configuración `Debug` o `Release` (`Any CPU`) y presionar **F5** (o botón *Iniciar*).

---

### 3. Credenciales de Acceso

- **Modo Cliente (Autogestión):** Acceso libre sin credenciales para consultar catálogo de espacios y registrar reservas.
- **Modo Administrador (Control Total):** Menú superior $\rightarrow$ *Ingresar como Administrador*:
  - **Usuario:** `Admin`
  - **Contraseña:** `123456`

*(Al autenticarse como administrador se habilitan las solapas de Gestión de Clientes, Administración de Recursos físicos, reprogramación/cancelación de turnos y exportación/importación en formato JSON).*

---

## Organización del Repositorio

```text
├── Instalador/                 (Paquete de distribución oficial de Windows Installer)
│   └── InstaladorCoWorking.msi (Paquete Windows Installer autónomo con la aplicación completa)
├── SistemaDeGestion/           (Código fuente y soluciones C# WinForms .NET Framework 4.7.2)
│   ├── SistemaDeGestion/       (Proyecto principal de la aplicación de escritorio)
│   │   ├── Modelos/            (Clases POO: Recurso, Sala, OficinaPrivada, PuestoTrabajo, Cliente, Reserva, RecursoFactory)
│   │   ├── DAO/                (Patrón DAO: ClienteDAO, RecursoDAO, ReservaDAO)
│   │   ├── Gestoras/           (GestorDAO, GestoraCoworking con LINQ y GestorJson para exportación/importación)
│   │   ├── ConexionDB/         (Conexion.cs con gestión centralizada MySqlConnection y using)
│   │   ├── Formularios/        (FrmPrincipal, FrmLogin y controles de navegación por pestañas)
│   │   ├── Enum/               (EstadoReserva.cs tipado: Pendiente, Confirmada, Cancelada)
│   │   └── App.config          (Cadena de conexión configurable a MySQL)
│   ├── SistemaDeGestion.sln    (Solución estándar de Microsoft Visual Studio 2022)
│   └── SistemaDeGestion.slnx   (Solución moderna XML de Visual Studio)
├── DB/                         (Persistencia relacional MySQL y diagramas de ingeniería)
│   ├── DB_TPFinal.sql          (Script SQL completo: tablas, vistas, SPs con SIGNAL 45000, función y trigger)
│   ├── Diagrama_DER.png        (Diagrama Entidad-Relación exportado de MySQL Workbench)
│   ├── Diagrama_Clases_UML.png (Diagrama de clases del dominio POO según rúbrica académica)
│   └── Diagrama_Editable.mwb   (Modelo editable en MySQL Workbench)
├── Manuales_Sistema/           (Manuales operativos integrados y accesibles desde la app)
│   ├── Manual_Usuario_Cliente.pdf (Guía de autogestión de turnos y catálogo para clientes)
│   └── Manual_Administrador.pdf   (Manual de gestión de clientes, recursos y reportes para admin)
├── Documentacion/              (Documentación institucional reglamentaria en DOCX y PDF)
│   ├── TP_Final_AlgoritmosII_Grupo2.pdf  (Informe integrador único maquetado en A4 - 22 páginas)
│   ├── Documentacion_Desarrollo.pdf      (Memoria técnica sobre POO, polimorfismo y capas)
│   ├── Diccionario_de_Datos.pdf          (Diccionario relacional de tablas y objetos MySQL)
│   └── Manual_de_Usuario.pdf             (Manual integral de usuario y administración)
├── Registro_de_cambios.txt     (Historial cronológico detallado de evoluciones y correcciones)
└── src/                        (Recursos gráficos: logotipos vectoriales, fondos e iconos)
```

---

## Tecnologías y Herramientas Utilizadas

- **Lenguaje de Programación:** C# (.NET Framework 4.7.2)
- **Interfaz de Usuario:** Windows Forms (WinForms)
- **Motor de Base de Datos:** MySQL / MariaDB (Entorno XAMPP v10.4+)
- **Acceso a Datos:** ADO.NET con MySQL Connector (`MySql.Data`) y Patrón DAO (`GestorDAO.cs`)
- **Herramienta de Modelado de Datos:** MySQL Workbench 8.0 CE
- **Entorno de Desarrollo:** Visual Studio 2022
- **Control de Versiones:** Git y GitHub
- **Normas de Presentación:** APA 7.ª edición y Pautas Institucionales del Instituto Argentino de la Empresa
