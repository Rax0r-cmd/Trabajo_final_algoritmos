# Sistema de Gestión de Coworking y Reservas · Algoritmos II (2026)

Este repositorio contiene el proyecto integrador anual de **Algoritmos II** (Analista de Sistemas de Información, Instituto Argentino de la Empresa - Prof. Lic. Adrián Aroca).

---

## 📌 Checklist y Planificador Interactivo del Equipo

Para ver y gestionar el checklist interactivo con guardado automático, filtros por integrante y métricas en tiempo real:

1. Abre directamente en tu navegador el archivo:
   - `index.html` (o accede mediante XAMPP a `http://localhost/ALGORITMOS2/index.html`).
2. Características del checklist:
   - **Persistencia automática**: Se guarda en el navegador (`localStorage`).
   - **Filtrado por integrante**: Ver solo lo que le toca a cada uno (Integrante 1, 2 o 3).
   - **Copiar Reporte Git**: Genera un resumen en Markdown listo para pegar en GitHub Issues o Pull Requests.
   - **Exportar / Importar JSON**: Para sincronizar el avance con tus compañeros.
   - **Modal de Guía**: Cheat-sheet de comandos Git, código de `SIGNAL 45000` y diseño de clases POO.

---

## 👥 Reparto de Módulos (3 Integrantes)

| Integrante | Módulo Principal | Entregables Clave |
| :--- | :--- | :--- |
| **Integrante 1** | **Reservas & Lógica Core** | • Tablas y SPs de Reservas (`sp_alta_reserva`, `sp_cancelar_reserva`)<br>• Función UDF `fn_verificar_disponibilidad`<br>• Validación con `SIGNAL SQLSTATE '45000'`<br>• Formulario `FrmReservas`<br>• Captura de `MySqlException` y `SqlState` en C#<br>• `ReservaDAO.cs` |
| **Integrante 2** | **POO & Catálogo de Recursos** | • Tablas y SPs de Recursos y Tipos de Recurso<br>• Clase abstracta `Recurso`, derivadas (`Sala`, `OficinaPrivada`, `PuestoTrabajo`)<br>• Interfaz `IReservable` y Polimorfismo con `List<Recurso>`<br>• Formulario `FrmRecursos`<br>• Módulo JSON (Exportar / Importar recursos)<br>• `RecursoDAO.cs` |
| **Integrante 3** | **Clientes, Vistas & UI General** | • Tablas y SPs de Clientes (`sp_alta_cliente`, `sp_modificar_cliente`)<br>• Tabla y Trigger de Auditoría (`trg_auditoria_reservas`)<br>• 2 Vistas SQL (`vw_detalle_reservas`, `vw_resumen_recursos`)<br>• Formulario Principal (`FrmPrincipal`) y `FrmClientes`<br>• Formulario de Consultas (`FrmConsultas`) con DataGridViews<br>• `ConexionBD.cs`, `App.config` y `ClienteDAO.cs` |

---

## 🐙 Flujo de Trabajo en GitHub

1. **Clonar el repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
2. **Crear una rama para tu tarea específica**:
   ```bash
   git checkout -b feature/nombre-de-tu-tarea
   ```
3. **Guardar cambios y subir**:
   ```bash
   git add .
   git commit -m "feat: descripción clara de lo implementado"
   git push -u origin feature/nombre-de-tu-tarea
   ```
4. **Abrir Pull Request (PR)** en GitHub para que otro compañero lo revise y mergee a `main`.
