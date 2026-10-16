// =============================================================================
// CHECKLIST SECUENCIAL PASO A PASO (ALGORITMOS II - COWORKING & RESERVAS 2026)
// =============================================================================

const PHASES = [
  { id: "fase0", code: "00", name: "SETUP & REPOSITORIO GITHUB" },
  { id: "fase1", code: "01", name: "BASE DE DATOS MYSQL & DIAGRAMA DER" },
  { id: "fase2", code: "02", name: "PROGRAMACIÓN ORIENTADA A OBJETOS (C#)" },
  { id: "fase3", code: "03", name: "INTERFAZ WINDOWS FORMS & INTEGRACIÓN" },
  { id: "fase4", code: "04", name: "MANEJO DE ERRORES (SIGNAL 45000)" },
  { id: "fase5", code: "05", name: "REQUERIMIENTOS EVOLUTIVOS (DAO & JSON)" },
  { id: "fase6", code: "06", name: "ENTREGABLES Y PREPARACIÓN DE DEFENSA" }
];

const TASKS = [
  // --- FASE 0 ---
  {
    id: "t01-git-repo",
    phase: "fase0",
    title: "Crear repositorio en GitHub e invitar a los 3 integrantes",
    detail: "Crear el repositorio remoto, configurar permisos de colaboradores y proteger la rama main.",
    codeTip: "git checkout -b feature/nombre-tarea"
  },
  {
    id: "t02-gitignore",
    phase: "fase0",
    title: "Configurar archivo .gitignore para Visual Studio y MySQL",
    detail: "Ignorar carpetas temporales y binarios (.vs/, bin/, obj/, *.user, *.suo) antes del primer commit.",
    codeTip: ".gitignore añadido en la raíz"
  },
  {
    id: "t03-vs-sln",
    phase: "fase0",
    title: "Crear Solución Visual Studio e instalar paquetes NuGet de MySQL",
    detail: "Crear proyecto Windows Forms C#, instalar paquete MySql.Data o MySqlConnector, crear carpeta 'BD/' y hacer commit inicial.",
    codeTip: "Install-Package MySql.Data"
  },

  // --- FASE 1: BASE DE DATOS MYSQL ---
  {
    id: "t04-db-diagram",
    phase: "fase1",
    title: "Diseñar el Diagrama Entidad-Relación (DER) con herramientas gratuitas",
    detail: "Definir las 4 entidades conceptuales (Clientes, Recursos, Tipos de Recurso, Reservas + Auditoría) y sus relaciones 1 a N. Puedes crearlo online gratis o generarlo automáticamente desde MySQL Workbench.",
    codeTip: "Workbench: Database -> Reverse Engineer (Ctrl + R)",
    links: [
      { text: "dbdiagram.io (Pegar SQL gratis)", url: "https://dbdiagram.io" },
      { text: "drawSQL (Visual gratis)", url: "https://drawsql.app" },
      { text: "Eraser.io (Diagramas y Docs)", url: "https://www.eraser.io" }
    ]
  },
  {
    id: "t05-db-tablas-core",
    phase: "fase1",
    title: "Crear tablas mínimas: clientes, tipos_recurso y recursos",
    detail: "Definir PKs autoincrementales, constraints UNIQUE (DNI/email), NOT NULL y tipos de datos coherentes (VARCHAR con longitud real, DECIMAL para costos).",
    codeTip: "PK, FK e integridad referencial"
  },
  {
    id: "t06-db-tabla-reservas",
    phase: "fase1",
    title: "Crear tabla 'reservas' y tabla de auditoría",
    detail: "Campos: id, id_cliente, id_recurso, fecha_inicio, fecha_fin, estado, costo_total. Tabla auditoria_reservas para el trigger.",
    codeTip: "CHECK (fecha_fin > fecha_inicio)"
  },
  {
    id: "t07-db-seeds",
    phase: "fase1",
    title: "Script con datos iniciales de prueba (Seeds)",
    detail: "Cargar tipos de recursos (Sala, Oficina, Puesto), recursos de ejemplo y clientes iniciales para pruebas en Workbench.",
    codeTip: "INSERT INTO tipos_recurso ... INSERT INTO recursos ..."
  },
  {
    id: "t08-sp-clientes",
    phase: "fase1",
    title: "Stored Procedures de Clientes (sp_alta_cliente, sp_modificar_cliente)",
    detail: "SPs para operaciones de escritura con parámetros validados y control de no duplicación de DNI.",
    codeTip: "CALL sp_alta_cliente('Juan', 'Perez', '38999888', ...);"
  },
  {
    id: "t09-sp-recursos",
    phase: "fase1",
    title: "Stored Procedures de Recursos (sp_alta_recurso, sp_modificar_recurso)",
    detail: "SPs de inserción y modificación para salas, oficinas y puestos validando costo por hora positivo.",
    codeTip: "CALL sp_alta_recurso('Sala A', 1, 'Piso 1', 10, 2500.00);"
  },
  {
    id: "t10-sp-reservas",
    phase: "fase1",
    title: "Stored Procedures de Reservas (sp_alta_reserva, sp_cancelar_reserva)",
    detail: "sp_alta_reserva valida fechas y disponibilidad antes de insertar. sp_cancelar_reserva actualiza el estado a CANCELADA.",
    codeTip: "CALL sp_alta_reserva(p_cliente, p_recurso, p_inicio, p_fin);"
  },
  {
    id: "t11-signal-45000",
    phase: "fase1",
    title: "Implementar validación con SIGNAL SQLSTATE '45000' en sp_alta_reserva",
    detail: "Si el recurso ya está ocupado en ese rango, abortar la transacción lanzando un error de negocio específico.",
    codeTip: "SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Recurso ya reservado';"
  },
  {
    id: "t12-vistas-mysql",
    phase: "fase1",
    title: "Crear al menos 2 Vistas útiles (vw_detalle_reservas, vw_resumen_recursos)",
    detail: "vw_detalle_reservas con JOIN de cliente + recurso para DataGridViews. vw_resumen_recursos con totales y disponibilidad.",
    codeTip: "SELECT * FROM vw_detalle_reservas;"
  },
  {
    id: "t13-funcion-udf",
    phase: "fase1",
    title: "Crear Función Almacenada (UDF) con utilidad real",
    detail: "fn_verificar_disponibilidad(p_id_recurso, p_inicio, p_fin) RETURNS BOOLEAN o cálculo de costo según duración.",
    codeTip: "SELECT fn_verificar_disponibilidad(1, '2026-10-20 10:00', '2026-10-20 12:00');"
  },
  {
    id: "t14-trigger-auditoria",
    phase: "fase1",
    title: "Crear Trigger de Auditoría en MySQL",
    detail: "Disparador AFTER INSERT o AFTER UPDATE en reservas para registrar historial de operaciones en auditoria_reservas.",
    codeTip: "CREATE TRIGGER trg_auditoria_reservas AFTER INSERT ON reservas ..."
  },
  {
    id: "t15-script-maestro",
    phase: "fase1",
    title: "Generar y validar script_creacion_completa.sql",
    detail: "Unificar todo el SQL y probar ejecución limpia desde cero en MySQL Workbench. Guardar en BD/script_creacion_completa.sql.",
    codeTip: "Ejecución 100% limpia sin errores en Workbench"
  },

  // --- FASE 2: POO ---
  {
    id: "t16-interfaz",
    phase: "fase2",
    title: "Definir Interfaz IReservable en C#",
    detail: "Contrato con métodos funcionales concretos como PuedeReservarse(DateTime inicio, DateTime fin) y CalcularCosto(TimeSpan duracion).",
    codeTip: "public interface IReservable { ... }"
  },
  {
    id: "t17-clase-abstracta",
    phase: "fase2",
    title: "Crear clase abstracta Recurso : IReservable",
    detail: "Atributos y propiedades comunes (Id, Nombre, Ubicacion, CostoPorHora) y método abstracto/virtual CalcularCosto.",
    codeTip: "public abstract class Recurso : IReservable"
  },
  {
    id: "t18-clases-derivadas",
    phase: "fase2",
    title: "Implementar clases derivadas con justificación funcional (Sala, Oficina, Puesto)",
    detail: "Sala (Capacidad, Proyector), OficinaPrivada (Despacho, BanoPrivado), PuestoTrabajo (MonitorExtra). Sobrescribir cálculo si aplica.",
    codeTip: "public class Sala : Recurso { ... }"
  },
  {
    id: "t19-clases-dominio",
    phase: "fase2",
    title: "Crear entidades de dominio Cliente y Reserva",
    detail: "Encapsulamiento correcto. Reserva mantiene referencias al objeto Cliente y al objeto polimórfico Recurso.",
    codeTip: "public class Reserva { public Recurso RecursoReservado { get; set; } }"
  },
  {
    id: "t20-polimorfismo",
    phase: "fase2",
    title: "Verificar polimorfismo con colecciones genéricas List<Recurso>",
    detail: "Demostrar que una lista List<Recurso> invoca el cálculo específico de cada objeto derivado sin conocer su tipo concreto.",
    codeTip: "foreach (Recurso r in lista) r.CalcularCosto(...);"
  },

  // --- FASE 3: WINDOWS FORMS ---
  {
    id: "t21-conexion-bd",
    phase: "fase3",
    title: "Crear clase centralizada ConexionBD.cs",
    detail: "Método estático para abrir conexión MySqlConnection usando bloques using. Prohibido repetir la cadena de conexión en los Forms.",
    codeTip: "using (var conn = ConexionBD.ObtenerConexion()) { ... }"
  },
  {
    id: "t22-frm-principal",
    phase: "fase3",
    title: "Formulario Principal de Navegación (FrmPrincipal)",
    detail: "Contenedor claro para acceder a la gestión de Clientes, Recursos, Reservas y Reportes.",
    codeTip: "Navegación limpia y formularios hijos"
  },
  {
    id: "t23-frm-clientes",
    phase: "fase3",
    title: "Formulario FrmClientes (DataGridView + Alta/Edición)",
    detail: "Grilla para listar clientes y controles de formulario vinculados a sp_alta_cliente y sp_modificar_cliente.",
    codeTip: "Validar campos vacíos antes de ejecutar"
  },
  {
    id: "t24-frm-recursos",
    phase: "fase3",
    title: "Formulario FrmRecursos (Catálogo y Tipos)",
    detail: "ComboBox de Tipos de Recurso con DisplayMember ('Nombre') y ValueMember ('Id'). Controles dinámicos según el tipo seleccionado.",
    codeTip: "cboTipo.DisplayMember = 'Nombre'; cboTipo.ValueMember = 'Id';"
  },
  {
    id: "t25-frm-reservas",
    phase: "fase3",
    title: "Formulario FrmReservas (Operación Core)",
    detail: "Selección de Cliente, Recurso, DateTimePickers para Fecha/Hora Inicio y Fin, botón de verificar disponibilidad y confirmación con sp_alta_reserva.",
    codeTip: "dateTimePickerInicio.MinDate = DateTime.Now;"
  },
  {
    id: "t26-frm-consultas",
    phase: "fase3",
    title: "Formulario FrmConsultas (Consumo de Vistas MySQL)",
    detail: "Visualización de vw_detalle_reservas y vw_resumen_recursos mediante DataGridView con filtros.",
    codeTip: "SELECT * FROM vw_detalle_reservas"
  },

  // --- FASE 4: MANEJO DE ERRORES ---
  {
    id: "t27-catch-signal",
    phase: "fase4",
    title: "Captura en C# de MySqlException con filtro ex.SqlState == '45000'",
    detail: "Diferenciar el error de negocio enviado por el SP (mostrar MessageBox de advertencia) de caídas de conexión o sintaxis (error crítico).",
    codeTip: "if (ex.SqlState == '45000') MessageBox.Show(ex.Message, 'Validación');"
  },
  {
    id: "t28-auditoria-trycatch",
    phase: "fase4",
    title: "Auditoría de excepciones: Cero bloques catch vacíos",
    detail: "Garantizar que todo catch gestione el error o muestre el mensaje correspondiente. Incorporar catch (Exception ex) secundario.",
    codeTip: "Regla estricta: los errores nunca se ocultan"
  },

  // --- FASE 5: EVOLUTIVOS ---
  {
    id: "t29-patron-dao",
    phase: "fase5",
    title: "Separar acceso a datos en clases DAO (ClienteDAO, RecursoDAO, ReservaDAO)",
    detail: "Mover las consultas y comandos fuera de los formularios hacia clases de acceso a datos dedicadas.",
    codeTip: "Form -> DAO -> ConexionBD -> MySQL"
  },
  {
    id: "t30-modulo-json",
    phase: "fase5",
    title: "Incorporar Exportación / Importación JSON con System.Text.Json",
    detail: "Generar archivo JSON con el catálogo de recursos o historial de reservas para intercambio de información.",
    codeTip: "JsonSerializer.Serialize(listaRecursos, options);"
  },
  {
    id: "t31-config-externa",
    phase: "fase5",
    title: "Extraer conexión hacia App.config (ConfigurationManager)",
    detail: "Retirar la cadena de conexión fija del código fuente y leerla desde <connectionStrings> de App.config.",
    codeTip: "ConfigurationManager.ConnectionStrings['CoworkingDB'].ConnectionString"
  },

  // --- FASE 6: ENTREGA Y DEFENSA ---
  {
    id: "t32-documentacion-readme",
    phase: "fase6",
    title: "Documentación técnica en README.md",
    detail: "Detallar objetivo del sistema, arquitectura de clases, objetos de MySQL utilizados y pasos para ejecutar la solución.",
    codeTip: "README.md con instrucciones claras"
  },
  {
    id: "t33-diagramas",
    phase: "fase6",
    title: "Exportar Diagrama de la Base de Datos (DER) y Diagrama UML",
    detail: "Incluir en la entrega el PDF/imagen del DER (usando dbdiagram.io o Workbench) y el diagrama de clases simplificado.",
    codeTip: "Workbench: File -> Export -> Export as PDF / PNG",
    links: [
      { text: "dbdiagram.io", url: "https://dbdiagram.io" }
    ]
  },
  {
    id: "t34-ensayo-defensa",
    phase: "fase6",
    title: "Ensayo grupal para la defensa oral del proyecto",
    detail: "Cada integrante debe estar capacitado para responder por qué se diseñó cada clase, qué hace la UDF, el SIGNAL 45000 y el trigger.",
    codeTip: "Todos dominan la arquitectura completa"
  }
];

// =============================================================================
// ESTADO Y PERSISTENCIA (localStorage)
// =============================================================================

const STORAGE_KEY = "coworking_flat_checklist_state_v2";

let appState = {
  tasks: {},        // { [id]: { completed: boolean, note: string } }
  statusFilter: "all",
  searchQuery: ""
};

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      appState.tasks = parsed.tasks || {};
    }
  } catch (e) {
    console.error("Error al cargar localStorage:", e);
  }
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ tasks: appState.tasks }));
    showSaveIndicator();
  } catch (e) {
    console.error("Error al guardar en localStorage:", e);
  }
}

function showSaveIndicator() {
  const el = document.getElementById("save-status");
  if (!el) return;
  el.innerText = `Sincronizado ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
}

// =============================================================================
// CÁLCULO DE PROGRESO
// =============================================================================

function updateProgress() {
  const total = TASKS.length;
  let done = 0;
  TASKS.forEach(t => {
    if (appState.tasks[t.id]?.completed) done++;
  });

  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  const bar = document.getElementById("progress-fill");
  const txt = document.getElementById("progress-text");
  if (bar) bar.style.width = `${pct}%`;
  if (txt) txt.innerText = `${done}/${total} tareas (${pct}%)`;
}

// =============================================================================
// RENDERIZADO DE LISTA PLANA
// =============================================================================

function renderChecklist() {
  const container = document.getElementById("checklist-container");
  if (!container) return;
  container.innerHTML = "";

  const query = appState.searchQuery.toLowerCase().trim();
  let visibleTasksCount = 0;

  PHASES.forEach(phase => {
    const phaseTasks = TASKS.filter(t => t.phase === phase.id);

    const filteredTasks = phaseTasks.filter(t => {
      const isDone = appState.tasks[t.id]?.completed || false;
      if (appState.statusFilter === "pending" && isDone) return false;
      if (appState.statusFilter === "completed" && !isDone) return false;

      if (query) {
        const matchTitle = t.title.toLowerCase().includes(query);
        const matchDetail = t.detail.toLowerCase().includes(query);
        const matchCode = (t.codeTip || "").toLowerCase().includes(query);
        if (!matchTitle && !matchDetail && !matchCode) return false;
      }
      return true;
    });

    if (filteredTasks.length === 0) return;

    visibleTasksCount += filteredTasks.length;
    const phaseDone = phaseTasks.filter(t => appState.tasks[t.id]?.completed).length;

    const group = document.createElement("section");
    group.className = "phase-group";

    group.innerHTML = `
      <div class="phase-header">
        <span class="phase-title">${phase.code} // ${phase.name}</span>
        <span class="phase-stats">${phaseDone}/${phaseTasks.length}</span>
      </div>
      <div class="phase-list" id="list-${phase.id}"></div>
    `;

    const listEl = group.querySelector(`#list-${phase.id}`);

    filteredTasks.forEach(task => {
      const isDone = appState.tasks[task.id]?.completed || false;
      const note = appState.tasks[task.id]?.note || "";

      let linksHtml = "";
      if (task.links && task.links.length > 0) {
        linksHtml = task.links.map(l => 
          `<a href="${l.url}" target="_blank" rel="noopener noreferrer" class="task-link">↗ ${escapeHtml(l.text)}</a>`
        ).join(" ");
      }

      const row = document.createElement("div");
      row.className = `task-row ${isDone ? "completed" : ""}`;
      row.id = `row-${task.id}`;

      row.innerHTML = `
        <button class="task-check-btn ${isDone ? "checked" : ""}" data-task-id="${task.id}" title="Marcar tarea">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke-width="4"><polyline points="20 6 9 17 4 12"/></svg>
        </button>
        <div class="task-content">
          <div class="task-main-line">
            <span class="task-text">${task.title}</span>
          </div>
          <div class="task-detail">${task.detail}</div>
          <div class="task-meta-row">
            ${task.codeTip ? `<span class="task-code-tip">${escapeHtml(task.codeTip)}</span>` : ""}
            ${linksHtml}
          </div>
          <div class="task-note-box">
            <input type="text" class="task-note-input" data-note-task-id="${task.id}" 
                   placeholder="// nota o PR (ej: commit a7b9c...)" 
                   value="${escapeHtml(note)}">
          </div>
        </div>
      `;

      listEl.appendChild(row);
    });

    container.appendChild(group);
  });

  if (visibleTasksCount === 0) {
    container.innerHTML = `<div class="empty-state">// No hay tareas que coincidan con el filtro actual</div>`;
  }

  // Events
  container.querySelectorAll(".task-check-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      toggleTask(btn.dataset.taskId);
    });
  });

  container.querySelectorAll(".task-note-input").forEach(inp => {
    inp.addEventListener("change", (e) => {
      saveTaskNote(inp.dataset.noteTaskId, e.target.value);
    });
  });
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function toggleTask(id) {
  if (!appState.tasks[id]) {
    appState.tasks[id] = { completed: false, note: "" };
  }
  appState.tasks[id].completed = !appState.tasks[id].completed;
  saveState();
  updateProgress();
  renderChecklist();
}

function saveTaskNote(id, note) {
  if (!appState.tasks[id]) {
    appState.tasks[id] = { completed: false, note: "" };
  }
  appState.tasks[id].note = note;
  saveState();
}

// =============================================================================
// REPORTE MARKDOWN & EXPORTACIÓN
// =============================================================================

function generateMarkdownReport() {
  const total = TASKS.length;
  const done = TASKS.filter(t => appState.tasks[t.id]?.completed).length;
  const pct = Math.round((done / total) * 100);

  let md = `## 📋 Estado del Proyecto · Coworking & Reservas\n`;
  md += `**Progreso:** ${done}/${total} tareas completadas (${pct}%)\n\n`;

  PHASES.forEach(phase => {
    const list = TASKS.filter(t => t.phase === phase.id);
    md += `### ${phase.code} // ${phase.name}\n`;
    list.forEach(t => {
      const isDone = appState.tasks[t.id]?.completed;
      const check = isDone ? "[x]" : "[ ]";
      const note = appState.tasks[t.id]?.note ? ` _(${appState.tasks[t.id].note})_` : "";
      md += `- ${check} ${t.title}${note}\n`;
    });
    md += `\n`;
  });

  return md;
}

function copyMarkdown() {
  const md = generateMarkdownReport();
  navigator.clipboard.writeText(md).then(() => {
    showToast("Reporte Markdown copiado para GitHub / WhatsApp");
  }).catch(() => {
    showToast("Error al copiar automáticamente");
  });
}

function exportJSON() {
  const blob = new Blob([JSON.stringify({ tasks: appState.tasks }, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `coworking-checklist-progress-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Backup exportado en JSON");
}

function importJSON(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const parsed = JSON.parse(e.target.result);
      if (parsed.tasks) {
        appState.tasks = parsed.tasks;
        saveState();
        updateProgress();
        renderChecklist();
        showToast("Progreso importado con éxito");
      }
    } catch (err) {
      alert("Error al importar: " + err.message);
    }
  };
  reader.readAsText(file);
}

function showToast(msg) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.innerText = msg;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 3000);
}

// =============================================================================
// INICIALIZACIÓN INMEDIATA
// =============================================================================

function initApp() {
  loadState();

  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      appState.statusFilter = btn.dataset.status;
      renderChecklist();
    });
  });

  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      appState.searchQuery = e.target.value;
      renderChecklist();
    });
  }

  const btnReset = document.getElementById("btn-reset");
  if (btnReset) {
    btnReset.addEventListener("click", () => {
      if (confirm("¿Desmarcar todas las tareas?")) {
        appState.tasks = {};
        saveState();
        updateProgress();
        renderChecklist();
        showToast("Checklist reiniciado");
      }
    });
  }

  const modal = document.getElementById("guide-modal");
  const btnGuide = document.getElementById("btn-toggle-guide");
  const btnCloseModal = document.getElementById("btn-close-modal");

  if (btnGuide && modal) {
    btnGuide.addEventListener("click", () => modal.classList.remove("hidden"));
  }
  if (btnCloseModal && modal) {
    btnCloseModal.addEventListener("click", () => modal.classList.add("hidden"));
  }
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.add("hidden");
    });
  }

  const btnExportMd = document.getElementById("btn-export-md");
  if (btnExportMd) btnExportMd.addEventListener("click", copyMarkdown);

  const btnBackup = document.getElementById("btn-backup");
  if (btnBackup) btnBackup.addEventListener("click", exportJSON);

  const fileImport = document.getElementById("file-import");
  if (fileImport) {
    fileImport.addEventListener("change", (e) => {
      if (e.target.files.length > 0) importJSON(e.target.files[0]);
    });
  }

  updateProgress();
  renderChecklist();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp);
} else {
  initApp();
}
