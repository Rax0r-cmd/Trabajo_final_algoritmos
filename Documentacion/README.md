# Documentación del Sistema

**Sistema de Gestión de Coworking y Reservas**  
**Desarrolladores:** Jonathan Lester Tullo, Maximiliano Scollo, David Samuel Ortega  
**Estado:** Versión Parcial Funcional (En Desarrollo Activo)  
**Año:** 2026

> **Documentos oficiales generados (Word .docx y PDF .pdf):**  
> Se encuentran disponibles por separado para consulta técnica y presentación:  
> 1. **Documentación del Desarrollo:** [Documentacion_Desarrollo.docx](Documentacion_Desarrollo.docx) · [Documentacion_Desarrollo.pdf](Documentacion_Desarrollo.pdf) (Explicación técnica del sistema, capas y POO).  
> 2. **Diccionario de Datos:** [Diccionario_de_Datos.docx](Diccionario_de_Datos.docx) · [Diccionario_de_Datos.pdf](Diccionario_de_Datos.pdf) (Estructura completa de MySQL: tablas, campos, relaciones, vistas, SPs, funciones y triggers).  
> 3. **Manual de Usuario:** [Manual_de_Usuario.docx](Manual_de_Usuario.docx) · [Manual_de_Usuario.pdf](Manual_de_Usuario.pdf) (Operación de cada solapa y perfiles del sistema).  
> *(Los 3 documentos mantienen un formato homogéneo: normas de estilo sobrias, sin menciones a "TP", con portada unificada, índice con líneas de puntos guía y numeración de página precisa).*

---

## 1. Documentación del Desarrollo (Para otros desarrolladores)

### ¿De qué se trata el proyecto?
El sistema es una aplicación de escritorio desarrollada en C# con Windows Forms conectada a una base de datos MySQL bajo XAMPP. Sirve para administrar un espacio de coworking: gestionar clientes, los lugares físicos que se alquilan (salas de reunión, oficinas privadas y puestos de trabajo/box) y las reservas por fecha y hora. La base de datos cuenta con una regla estricta que no permite reservas duplicadas en un mismo horario (`SIGNAL SQLSTATE '45000'`) y registra cualquier cancelación en una tabla de auditoría.

### ¿Cómo nos organizamos entre nosotros?
- **Jonathan Lester Tullo (`shonimdp@gmail.com`):** Creó la base de datos completa en MySQL (tablas, relaciones, vistas, trigger, función y procedimientos almacenados), armó el proyecto base en Visual Studio con .NET Framework 4.7.2, configuró el paquete NuGet `MySql.Data`, programó la clase estática de conexión `Conexion.cs` y las clases base del modelo (`IReservable.cs`, `EstadoReserva.cs`, `Recurso.cs`).
- **Maximiliano Scollo (`maximilianoscollo17@gmail.com`):** Programó las clases hijas (`Sala.cs`, `OficinaPrivada.cs`, `PuestoTrabajo.cs`), implementó la lógica de cálculo polimórfico de costos (`CalcularCosto`) y validación de fechas (`PuedeReservarse`), programó las clases `Cliente.cs` y `Reserva.cs`, armó la clase `GestoraCoworking.cs` con métodos de lista y consultas LINQ, y actualizó el diagrama Entidad-Relación (DER).
- **David Samuel Ortega (`davidortegaa86@gmail.com`):** Diseñó la interfaz gráfica en Windows Forms, armó la pantalla de Login con validación y enlace directo de soporte a WhatsApp, preparó los fondos y logos del coworking, y desarrolló el formulario principal (`FrmPrincipal`) con las tres solapas (Control, Reservas y Gestión), implementando el bloqueo y desbloqueo de permisos de administrador y la alternancia de grillas con radio buttons.

### Arquitectura en Capas
1. **Presentación (Formularios):** `FrmLogin` y `FrmPrincipal`. Muestran controles, reciben eventos del usuario y muestran los resultados.
2. **Negocio (Gestoras):** `GestoraCoworking.cs` maneja la lista de reservas en memoria y realiza búsquedas y filtros mediante LINQ.
3. **Modelos (Entidades):** Clases que representan el dominio (`Cliente`, `Reserva`, `Recurso`, `Sala`, `OficinaPrivada`, `PuestoTrabajo`, `EstadoReserva`, `IReservable`).
4. **Conexión (ConexionDB):** `Conexion.cs` centraliza la cadena de conexión a MySQL y entrega objetos `MySqlConnection` listos para ser abiertos y cerrados con bloques `using`.
5. **Persistencia (MySQL):** Base de datos `tp_final_db` con procedimientos almacenados, vistas, funciones y triggers.

### Clases en C# explicadas sin vueltas
- **`Conexion.cs`:** Clase `static` (porque no representa un objeto del negocio sino una utilidad global) con el método `CrearConexion()`. No abre la conexión de prepo, sino que cada formulario o método la abre con `.Open()` dentro de un `using` para que se cierre sola apenas termina y no quede memoria colgada.
- **`IReservable.cs`:** Interfaz con el método `bool PuedeReservarse(DateTime fecha)`. Es como un contrato que obliga a cualquier espacio alquilable a tener una validación de disponibilidad.
- **`EstadoReserva.cs`:** Enum con los valores `Pendiente`, `Confirmada` y `Cancelada`. Evita errores de tipeo y guarda como texto directo en la base con `.ToString()`.
- **`Recurso.cs`:** Clase abstracta base. Nadie alquila "un recurso" genérico, sino un tipo específico. Contiene las propiedades comunes (`IdRecurso`, `Nombre`, `Descripcion`, `Ubicacion`, `PrecioPorHora`, `IdTipoRecurso`) y el método abstracto `CalcularCosto(int horas)`.
- **`Sala.cs`:** Hereda de `Recurso`. Suma la propiedad `CantSillas`. En `CalcularCosto`, si tiene más de 30 sillas suma $8.000 extras, y si supera las 60 sillas suma $16.000.
- **`OficinaPrivada.cs`:** Hereda de `Recurso`. Suma la propiedad `MobiliarioIncluido`. Si viene amueblada, suma un extra fijo de $1.500 al alquiler.
- **`PuestoTrabajo.cs`:** Hereda de `Recurso`. Suma `NroCategoria` (1, 2 o 3). Suma un plus de $3.500 (cat 1), $5.500 (cat 2) o $8.000 (cat 3).
- **`Cliente.cs` y `Reserva.cs`:** Modelos de datos para el cliente que reserva y el detalle de la reserva.
- **`GestoraCoworking.cs`:** Administra la lista de reservas en memoria, permitiendo altas, cancelaciones, modificaciones y búsquedas con LINQ.
- **`GestorDAO.cs`:** Módulo en desarrollo para vincular las acciones de pantalla directamente con los procedimientos de MySQL.

---

## 2. Diccionario de Datos (Estructura de Base de Datos MySQL)

### Tablas

#### 1. `tipo_recursos`
| Campo | Tipo | Nulo | Clave | Descripción |
|---|---|---|---|---|
| `id_tipo_recurso` | INT | NO | PK (AI) | Identificador único del tipo de espacio. |
| `nombre_tipo` | VARCHAR(100) | NO | - | Nombre de la categoría (Sala, Oficina, Puesto). |

#### 2. `recursos`
| Campo | Tipo | Nulo | Clave | Descripción |
|---|---|---|---|---|
| `id_recurso` | INT | NO | PK (AI) | Identificador del espacio físico. |
| `nombre` | VARCHAR(100) | NO | - | Nombre comercial del espacio (ej. Sala Innovación). |
| `descripcion` | TEXT | SÍ | - | Detalle de comodidades incluidas. |
| `ubicacion` | VARCHAR(100) | NO | - | Piso y sector dentro del edificio. |
| `precio_por_hora` | DECIMAL(10,2) | NO | - | Tarifa base por hora. |
| `mobiliario_incluido` | BOOLEAN | SÍ | - | Solo para oficinas: si viene equipada. |
| `cantidad_sillas` | INT | SÍ | - | Solo para salas: cantidad de sillas disponibles. |
| `nro_categoria` | INT | SÍ | - | Solo para puestos: nivel del box de trabajo. |
| `id_tipo_recurso` | INT | NO | FK | Apunta a `tipo_recursos.id_tipo_recurso`. |

#### 3. `clientes`
| Campo | Tipo | Nulo | Clave | Descripción |
|---|---|---|---|---|
| `id_cliente` | INT | NO | PK (AI) | Número identificador del cliente. |
| `nombre` | VARCHAR(100) | NO | - | Nombre del cliente. |
| `apellido` | VARCHAR(100) | NO | - | Apellido del cliente. |
| `telefono` | VARCHAR(20) | NO | - | Teléfono de contacto. |
| `mail` | VARCHAR(255) | NO | - | Correo electrónico de contacto. |
| `fecha_registro` | DATETIME | NO | Default Now | Fecha y hora de alta en el sistema. |

#### 4. `reservas` (Tabla Intermedia)
| Campo | Tipo | Nulo | Clave | Descripción |
|---|---|---|---|---|
| `id_reserva` | INT | NO | PK (AI) | Identificador de la reserva. |
| `id_cliente` | INT | NO | FK | Cliente que alquila (`clientes.id_cliente`). |
| `id_recurso` | INT | NO | FK | Espacio alquilado (`recursos.id_recurso`). |
| `fecha_reserva` | DATETIME | NO | - | Día y hora de inicio del alquiler. |
| `horas` | INT | NO | Default 1 | Horas totales de uso. |
| `total` | DECIMAL(10,2) | NO | - | Importe final a abonar. |
| `estado` | VARCHAR(20) | NO | Default Conf | 'Confirmada', 'Cancelada' o 'Pendiente'. |

#### 5. `auditoria_reservas`
| Campo | Tipo | Nulo | Clave | Descripción |
|---|---|---|---|---|
| `id_auditoria` | INT | NO | PK (AI) | Identificador del registro histórico. |
| `id_reserva` | INT | NO | - | ID de la reserva cancelada. |
| `accion` | VARCHAR(50) | NO | - | Detalle de la acción ('Cancelacion de reserva'). |
| `fecha_accion` | DATETIME | NO | Default Now | Fecha y hora exacta de la baja. |
| `usuario` | VARCHAR(100) | SÍ | Default Sist | Usuario del sistema que canceló. |

### Vistas
- `vw_detalle_reservas`: Une reservas, clientes y recursos mostrando nombres reales y legibles.
- `vw_resumen_recursos`: Muestra cuántas reservas tuvo cada sala y cuánto dinero recaudó en total.

### Función
- `fn_verificar_disponibilidad(p_id_recurso, p_fecha, p_horas)`: Evalúa matemáticamente el solapamiento temporal de rangos horarios (`(nuevo_inicio < fin_existente) AND (nuevo_fin > inicio_existente)`). Devuelve `1` si el lugar está libre durante todo el intervalo y `0` si ya existe una reserva confirmada en conflicto.

### Procedimientos Almacenados
- `sp_alta_cliente`: Da de alta un nuevo cliente.
- `sp_modificar_cliente`: Actualiza los datos de un cliente existente.
- `sp_alta_recurso`: Registra un nuevo espacio con sus datos y atributos específicos.
- `sp_modificar_recurso`: Actualiza la información o tarifa de un recurso.
- `sp_alta_reserva`: Valida horas positivas, importe y existencia de cliente/recurso. Chequea con `fn_verificar_disponibilidad` la duración completa. Si está libre, inserta la reserva; si está ocupado, interrumpe con `SIGNAL SQLSTATE '45000'` impidiendo solapamientos.
- `sp_modificar_reserva`: Permite reprogramar fecha u horario de una reserva comprobando disponibilidad frente a las demás reservas confirmadas.
- `sp_cancelar_reserva`: Pasa el estado de una reserva a 'Cancelada'. Si no existe o ya estaba cancelada, emite alerta con `SIGNAL 45000`.
- `sp_calcular_total_recaudado_cursor`: Cursor que recorre fila por fila sumando el total facturado de reservas confirmadas.

### Trigger
- `trg_auditoria_reservas`: Salta automáticamente tras un `UPDATE` en `reservas` cuando el estado cambia a 'Cancelada', anotándolo en `auditoria_reservas`.

---

## 3. Manual de Usuario (Estado actual funcional)

### Requisitos previos
1. Abrir XAMPP y presionar **Start** en MySQL (puerto 3306).
2. Ejecutar el script `DB/DB_TPFinal.sql` en phpMyAdmin o MySQL Workbench.
3. Abrir la solución `SistemaDeGestion.slnx` en Visual Studio y presionar **F5**.

### Pantalla de Login (`FrmLogin`)
- **Acceso Administrador:** Usuario: `Admin` | Contraseña: `123456`.
- **Aviso de error:** Si se tipea mal, avisa con un mensaje y enfoca la casilla a corregir.
- **Asistencia por WhatsApp:** Enlace inferior que abre WhatsApp con un mensaje preconfigurado para soporte técnico.

### Pantalla Principal (`FrmPrincipal`)
- **Solapa CONTROL:** Permite seleccionar cliente, tipo de recurso, fecha con calendario gráfico y cantidad de horas, calculando el importe total y permitiendo confirmar con el botón "Agregar".
- **Solapa RESERVAS:** Grilla donde se listan las reservas realizadas, con botones para "Modificar Reserva" y "Eliminar Reserva" (cancelación).
- **Menú Superior:** Opción "Ingresar como Administrador" para habilitar la solapa de gestión, y opción "Cerrar sesión" para ocultarla nuevamente.
- **Solapa GESTIÓN (Solo Administradores):**
  - Dos botones de opción (Radio Buttons): **Usuarios** y **Recursos**.
  - Al pulsar uno u otro, conmuta automáticamente el título y la grilla visible entre Clientes y Recursos.
  - Botones "Crear", "Modificar" y "Eliminar" para gestionar cada catálogo.

### Estado actual de desarrollo
- **100% Funcional hoy:** Base de datos con todas las reglas, clases del modelo con herencia y polimorfismo, gestora con LINQ, interfaz gráfica completa con login, roles, control de permisos y navegación entre solapas y grillas.
- **En proceso:** Conectar los formularios con la base de datos vía `GestorDAO.cs` e implementar la exportación/importación en formato JSON.
