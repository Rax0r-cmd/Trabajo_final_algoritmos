using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;
using MySql.Data.Types;
using SistemaDeGestion.DAO;
using SistemaDeGestion.Gestoras;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.Formularios
{
    public partial class FrmPrincipal : Form
    {
        // Instancia unificada del DAO (Fachada)
        private readonly GestorDAO _gestorDAO = new GestorDAO();
        private readonly GestorJson _gestorJson;
        private bool _esAdmin = false;

        // Variables para guardar las solapas en memoria.
        private TabPage tabClientes;
        private TabPage tabRecursos;

        public FrmPrincipal()
        {
            InitializeComponent();
            _gestorJson = new GestorJson(_gestorDAO);
        }

        private void FrmPrincipal_Load(object sender, EventArgs e)
        {
            Configuraciones();
            CargarGrillas();
        }

        //=============================================================
        // MÉTODOS DE POBLADO DE COMPONENTES (DataGridViews desde DAO)
        //=============================================================

        public void CargarGrillas()
        {
            CargarReservas();
            CargarClientes();
            CargarRecursos();
        }

        public void CargarReservas()
        {
            try
            {
                if (this.dgvReservas != null)
                {
                    this.dgvReservas.DataSource = null;
                    this.dgvReservas.DataSource = _gestorDAO.ListarDetalleReservas();
                    FormatearGrillaReservas();
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Error al conectar con MySQL para reservas: " + ex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al poblar grilla de reservas: " + ex.Message);
            }
        }

        // Formatea visualmente la grilla de reservas para el usuario/cliente:
        // Oculta columnas tecnicas (id_reserva, mail) y pone titulos amigables sin guiones bajos
        private void FormatearGrillaReservas()
        {
            if (dgvReservas == null || dgvReservas.Columns.Count == 0) return;

            // Oculto el ID interno de la reserva y el email por estetica y privacidad visual
            if (dgvReservas.Columns.Contains("id_reserva"))
            {
                dgvReservas.Columns["id_reserva"].Visible = false;
            }
            if (dgvReservas.Columns.Contains("mail_cliente"))
            {
                dgvReservas.Columns["mail_cliente"].Visible = false;
            }

            // Titulos legibles en espanol sin guiones bajos
            if (dgvReservas.Columns.Contains("cliente"))
            {
                dgvReservas.Columns["cliente"].HeaderText = "Cliente";
            }
            if (dgvReservas.Columns.Contains("recurso"))
            {
                dgvReservas.Columns["recurso"].HeaderText = "Recurso";
            }
            if (dgvReservas.Columns.Contains("tipo_espacio"))
            {
                dgvReservas.Columns["tipo_espacio"].HeaderText = "Tipo de Espacio";
            }
            if (dgvReservas.Columns.Contains("fecha_reserva"))
            {
                dgvReservas.Columns["fecha_reserva"].HeaderText = "Fecha y Horario";
                dgvReservas.Columns["fecha_reserva"].DefaultCellStyle.Format = "dd/MM/yyyy HH:mm";
                dgvReservas.Columns["fecha_reserva"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvReservas.Columns["fecha_reserva"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            if (dgvReservas.Columns.Contains("horas"))
            {
                dgvReservas.Columns["horas"].HeaderText = "Horas";
                dgvReservas.Columns["horas"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvReservas.Columns["horas"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            if (dgvReservas.Columns.Contains("total"))
            {
                dgvReservas.Columns["total"].HeaderText = "Total ($)";
                dgvReservas.Columns["total"].DefaultCellStyle.Format = "N2";
                dgvReservas.Columns["total"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleRight;
                dgvReservas.Columns["total"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            if (dgvReservas.Columns.Contains("estado"))
            {
                dgvReservas.Columns["estado"].HeaderText = "Estado";
                dgvReservas.Columns["estado"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvReservas.Columns["estado"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
        }

        public void CargarClientes()
        {
            try
            {
                if (this.dgvClientes != null)
                {
                    this.dgvClientes.DataSource = null;
                    this.dgvClientes.DataSource = _gestorDAO.ListarClientes();
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Error al conectar con MySQL para clientes: " + ex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al poblar grilla de clientes: " + ex.Message);
            }
        }

        public void CargarRecursos()
        {
            try
            {
                if (this.dgvRecursos != null)
                {
                    this.dgvRecursos.DataSource = null;
                    this.dgvRecursos.DataSource = _gestorDAO.ListarRecursos();
                    FormatearGrillaRecursos(); // Aplica anchos y alineaciones de columnas
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Error al conectar con MySQL para recursos: " + ex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al poblar grilla de recursos: " + ex.Message);
            }
        }

        /// <summary>
        /// Ajusta anchos y alineaciones de columnas en la grilla de Recursos.
        /// La última columna (Categoría) usa Fill para absorber el espacio sobrante
        /// y evitar la banda gris vacía a la derecha.
        /// </summary>
        private void FormatearGrillaRecursos()
        {
            if (dgvRecursos == null || dgvRecursos.Columns.Count == 0) return;

            dgvRecursos.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.None;

            if (dgvRecursos.Columns.Contains("ID"))
            {
                dgvRecursos.Columns["ID"].Width = 45;
                dgvRecursos.Columns["ID"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvRecursos.Columns["ID"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            if (dgvRecursos.Columns.Contains("Nombre"))
            {
                dgvRecursos.Columns["Nombre"].Width = 130;
            }
            if (dgvRecursos.Columns.Contains("Descripción"))
            {
                dgvRecursos.Columns["Descripción"].Width = 200;
            }
            if (dgvRecursos.Columns.Contains("Ubicación"))
            {
                dgvRecursos.Columns["Ubicación"].Width = 110;
            }
            if (dgvRecursos.Columns.Contains("Precio/Hora"))
            {
                dgvRecursos.Columns["Precio/Hora"].Width = 90;
                dgvRecursos.Columns["Precio/Hora"].DefaultCellStyle.Format = "N2";
                dgvRecursos.Columns["Precio/Hora"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleRight;
                dgvRecursos.Columns["Precio/Hora"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            if (dgvRecursos.Columns.Contains("Tipo"))
            {
                dgvRecursos.Columns["Tipo"].Width = 130;
            }
            if (dgvRecursos.Columns.Contains("Mobiliario"))
            {
                dgvRecursos.Columns["Mobiliario"].Width = 80;
                dgvRecursos.Columns["Mobiliario"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            if (dgvRecursos.Columns.Contains("Cant. Sillas"))
            {
                dgvRecursos.Columns["Cant. Sillas"].Width = 65;
                dgvRecursos.Columns["Cant. Sillas"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvRecursos.Columns["Cant. Sillas"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            // Categoría ocupa el espacio restante para que no quede banda gris vacía a la derecha
            if (dgvRecursos.Columns.Contains("Categoría"))
            {
                dgvRecursos.Columns["Categoría"].AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill;
                dgvRecursos.Columns["Categoría"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvRecursos.Columns["Categoría"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
        }

        //=============================================================
        // ToolStrip, configuración de solapas con el Login de Admin
        //=============================================================
        private void ingresarComoAdministradorToolStripMenuItem_Click(object sender, EventArgs e)
        {
            using (FrmLogin login = new FrmLogin())
            {
                if (login.ShowDialog(this) == DialogResult.OK)
                {
                    MostrarSolapasAdmin();
                }
            }
        }

        private void cerrarSesionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            DialogResult confirmacion = MessageBox.Show("Desea cerrar sesión?", "aviso...", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (confirmacion == DialogResult.Yes)
            {
                OcultarSolapasAdmin();
            }
        }

        // Abre el manual en PDF correspondiente al perfil activo (Cliente o Administrador)
        private void ayudaManualToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                string archivoPdf = _esAdmin ? "Manual_Administrador.pdf" : "Manual_Usuario_Cliente.pdf";

                // Busqueda generica y relativa del PDF para que funcione en cualquier computadora instalada
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string[] rutasCandidatas = new string[]
                {
                    Path.Combine(baseDir, "Manuales_Sistema", archivoPdf),
                    Path.Combine(baseDir, archivoPdf),
                    Path.Combine(baseDir, "..", "Manuales_Sistema", archivoPdf),
                    Path.Combine(baseDir, "..", "..", "Manuales_Sistema", archivoPdf),
                    Path.Combine(baseDir, "..", "..", "..", "Manuales_Sistema", archivoPdf)
                };

                string rutaEncontrada = null;
                foreach (string candidate in rutasCandidatas)
                {
                    try
                    {
                        if (File.Exists(candidate))
                        {
                            rutaEncontrada = Path.GetFullPath(candidate);
                            break;
                        }
                    }
                    catch { }
                }

                if (!string.IsNullOrEmpty(rutaEncontrada))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = rutaEncontrada,
                        UseShellExecute = true
                    });
                }
                else
                {
                    MessageBox.Show($"No se encontró el manual '{archivoPdf}' en la carpeta 'Manuales_Sistema' ni en el directorio de la aplicación.", "Archivo no encontrado", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ocurrió un error al intentar abrir el manual: " + ex.Message, "Error al abrir ayuda", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // =============================================================
        // Funcionalidades JSON (Etapa 6 de la Cátedra)
        // =============================================================
        private void exportarCatalogoJsonToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                using (SaveFileDialog sfd = new SaveFileDialog())
                {
                    sfd.Title = "Exportar Catálogo de Recursos a JSON";
                    sfd.Filter = "Archivos JSON (*.json)|*.json";
                    sfd.FileName = "recursos.json";

                    if (sfd.ShowDialog(this) == DialogResult.OK)
                    {
                        if (_gestorJson.ExportarRecursos(sfd.FileName))
                        {
                            MessageBox.Show("Catálogo de recursos exportado exitosamente a:\n" + sfd.FileName, "Exportación exitosa", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al exportar recursos: " + ex.Message, "Error de exportación", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void importarRecursosJsonToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                using (OpenFileDialog ofd = new OpenFileDialog())
                {
                    ofd.Title = "Importar Recursos desde archivo JSON";
                    ofd.Filter = "Archivos JSON (*.json)|*.json";

                    if (ofd.ShowDialog(this) == DialogResult.OK)
                    {
                        int importados = _gestorJson.ImportarRecursos(ofd.FileName);
                        MessageBox.Show($"Se importaron {importados} recurso(s) exitosamente a la base de datos.", "Importación exitosa", MessageBoxButtons.OK, MessageBoxIcon.Information);

                        // Actualizamos la grilla de recursos y el combo del formulario
                        CargarRecursos();
                        CargarCboRecursos();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al importar recursos: " + ex.Message, "Error de importación", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void exportarReservasJsonToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                using (SaveFileDialog sfd = new SaveFileDialog())
                {
                    sfd.Title = "Exportar Reservas a JSON";
                    sfd.Filter = "Archivos JSON (*.json)|*.json";
                    sfd.FileName = "reservas.json";

                    if (sfd.ShowDialog(this) == DialogResult.OK)
                    {
                        if (_gestorJson.ExportarReservas(sfd.FileName))
                        {
                            MessageBox.Show("Listado de reservas exportado exitosamente a:\n" + sfd.FileName, "Exportación exitosa", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al exportar reservas: " + ex.Message, "Error de exportación", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Opcion de menu Salir
        private void salirToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close(); // Dispara FrmPrincipal_FormClosing
        }

        // Confirmacion de salida obligatoria antes de cerrar (sea por la 'X' o por el menu)
        private void FrmPrincipal_FormClosing(object sender, FormClosingEventArgs e)
        {
            DialogResult confirmacion = MessageBox.Show("¿Está seguro que desea salir del sistema de CoWorking?", "Confirmar salida", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (confirmacion == DialogResult.No)
            {
                e.Cancel = true; // Cancela el cierre y mantiene el programa abierto
            }
        }

        //=============================================================
        // Configuraciones generales
        //=============================================================
        public void MostrarSolapasAdmin()
        {
            _esAdmin = true;
            if (ayudaManualToolStripMenuItem != null)
            {
                ayudaManualToolStripMenuItem.Text = "Ayuda - Manual del Administrador";
            }

            // Si no está la solapa "Gestión", la agrega entre las solapas del tabIndex
            if (!tabControl1.TabPages.Contains(tabClientes))
            {
                tabControl1.TabPages.Insert(2, tabClientes);
            }
            if (!tabControl1.TabPages.Contains(tabRecursos))
            {
                tabControl1.TabPages.Insert(3, tabRecursos);
            }

            // Control de inicio y cierre de sesion en el menu
            if (ingresarComoAdministradorToolStripMenuItem != null) ingresarComoAdministradorToolStripMenuItem.Visible = false;
            if (cerrarSesionToolStripMenuItem != null) cerrarSesionToolStripMenuItem.Visible = true;

            // Los botones de modificar y eliminar reserva solo se muestran cuando el admin inicia sesion
            btnModificarReserva.Visible = true;
            btnEliminarReserva.Visible = true;

            // Opciones de exportacion e importacion JSON exclusivas del Administrador
            if (toolStripSeparatorJson != null) toolStripSeparatorJson.Visible = true;
            if (exportarCatalogoJsonToolStripMenuItem != null) exportarCatalogoJsonToolStripMenuItem.Visible = true;
            if (importarRecursosJsonToolStripMenuItem != null) importarRecursosJsonToolStripMenuItem.Visible = true;
            if (exportarReservasJsonToolStripMenuItem != null) exportarReservasJsonToolStripMenuItem.Visible = true;
        }

        public void OcultarSolapasAdmin()
        {
            _esAdmin = false;
            if (ayudaManualToolStripMenuItem != null)
            {
                ayudaManualToolStripMenuItem.Text = "Ayuda - Manual de Usuario";
            }

            // Control de inicio y cierre de sesion en el menu
            if (ingresarComoAdministradorToolStripMenuItem != null) ingresarComoAdministradorToolStripMenuItem.Visible = true;
            if (cerrarSesionToolStripMenuItem != null) cerrarSesionToolStripMenuItem.Visible = false;

            // 1. Se guarda la referencia a las pestañas
            tabClientes = tabPageClientes;
            tabRecursos = tabPageRecursos;

            // 2. Las sacamos del TabControl para que no aparezcan
            tabControl1.TabPages.Remove(tabClientes);
            tabControl1.TabPages.Remove(tabRecursos);

            // Ocultamos los botones de modificar y eliminar reserva para usuarios no administradores
            btnModificarReserva.Visible = false;
            btnEliminarReserva.Visible = false;

            // Ocultamos las opciones de JSON cuando no es administrador
            if (toolStripSeparatorJson != null) toolStripSeparatorJson.Visible = false;
            if (exportarCatalogoJsonToolStripMenuItem != null) exportarCatalogoJsonToolStripMenuItem.Visible = false;
            if (importarRecursosJsonToolStripMenuItem != null) importarRecursosJsonToolStripMenuItem.Visible = false;
            if (exportarReservasJsonToolStripMenuItem != null) exportarReservasJsonToolStripMenuItem.Visible = false;
        }

        public void Configuraciones()
        {
            OcultarSolapasAdmin();
            CargarCboClientes();
            CargarCboRecursos();

            // Configuramos el selector de fecha para que no permita elegir dias en el pasado
            dtpFechaReserva.MinDate = DateTime.Today;

            // Configuramos el selector de Horario de inicio (integrado en el Diseñador)
            if (cboHorarioInicio != null)
            {
                cboHorarioInicio.DrawMode = DrawMode.OwnerDrawFixed;
                cboHorarioInicio.DrawItem += new DrawItemEventHandler(cboHorarioInicio_DrawItem);
                cboHorarioInicio.SelectedIndexChanged += new EventHandler(cboHorarioInicio_SelectedIndexChanged);
                ActualizarHorariosDisponibles();
            }

            // Configuramos el selector de horas: no permitimos superar las 24 horas por dia
            nudHoras.Minimum = 0;
            nudHoras.Maximum = 24;

            // Recalculo el total en pantalla en tiempo real cuando cambian las horas o el recurso
            nudHoras.ValueChanged += new EventHandler(nudHoras_ValueChanged);
            nudHoras.KeyUp += (s, ev) => ActualizarTotalReserva();
            CmbTipoRecurso.SelectedIndexChanged += new EventHandler(CmbTipoRecurso_SelectedIndexChanged);
            dtpFechaReserva.ValueChanged += new EventHandler(dtpFechaReserva_ValueChanged);

            // Botones de crear siempre activos para poder dar de alta en cualquier momento
            btnCrearUsuario.Enabled = true;
            btnCrearRecurso.Enabled = true;

            // Botones de modificar y eliminar arrancan apagados hasta que el usuario elija una fila
            btnModificarReserva.Enabled = false;
            btnEliminarReserva.Enabled = false;
            btnModificarRecurso.Enabled = false;
            btnEliminarRecurso.Enabled = false;
            btnModificarUsuario.Enabled = false;
            btnEliminarUsuario.Enabled = false;

            // Engancho los eventos de cambio de seleccion de las grillas para prender o apagar botones
            if (dgvClientes != null)
                dgvClientes.SelectionChanged += new EventHandler(dgvClientes_SelectionChanged);
            if (dgvRecursos != null)
                dgvRecursos.SelectionChanged += new EventHandler(dgvRecursos_SelectionChanged);
            if (dgvReservas != null)
                dgvReservas.SelectionChanged += new EventHandler(dgvReservas_SelectionChanged);

            // Engancho los clicks de los botones del panel y de bajas
            btnAgregar.Click += new EventHandler(btnAgregar_Click);
            // btnEliminarUsuario_Click ya esta enganchado en el Designer (FrmPrincipal.Designer.cs linea 140)
            // para no duplicar el evento ni disparar 2 veces el cuadro de confirmacion.
            btnEliminarRecurso.Click += new EventHandler(btnEliminarRecurso_Click);
            btnEliminarReserva.Click += new EventHandler(btnEliminarReserva_Click);
            btnModificarReserva.Click += new EventHandler(btnModificarReserva_Click);
            btnCancelar.Click += new EventHandler(btnLimpiarCampos_Click);
        }

        public void CargarCboClientes()
        {
            try
            {
                if (CmbClientes != null)
                {
                    DataTable dt = _gestorDAO.ListarClientes();

                    // Agrego una columna calculada con Nombre y Apellido para evitar confusiones si hay homonimos
                    if (!dt.Columns.Contains("NombreCompleto"))
                    {
                        dt.Columns.Add("NombreCompleto", typeof(string), "Nombre + ' ' + Apellido");
                    }

                    // Agrego una opcion por defecto para que no cargue un cliente directamente
                    DataRow filaDefault = dt.NewRow();
                    filaDefault["ID"] = 0;
                    filaDefault["Nombre"] = "-- Seleccione un cliente --";
                    filaDefault["Apellido"] = "";
                    filaDefault["NombreCompleto"] = "-- Seleccione un cliente --";
                    dt.Rows.InsertAt(filaDefault, 0);

                    CmbClientes.DataSource = null;
                    CmbClientes.DataSource = dt;
                    CmbClientes.DisplayMember = "NombreCompleto";
                    CmbClientes.ValueMember = "ID";
                    CmbClientes.SelectedIndex = 0;
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Error al conectar con MySQL para clientes: " + ex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al cargar el ComboBox de clientes: " + ex.Message);
            }
        }

        public void CargarCboRecursos()
        {
            try
            {
                if (CmbTipoRecurso != null)
                {
                    DataTable dt = _gestorDAO.ListarRecursos();

                    // Agrego una opcion por defecto para que empiece en Seleccionar recurso
                    DataRow filaDefault = dt.NewRow();
                    filaDefault["ID"] = 0;
                    filaDefault["Nombre"] = "-- Seleccione un recurso --";
                    filaDefault["Precio/Hora"] = 0;
                    filaDefault["Tipo"] = "";
                    dt.Rows.InsertAt(filaDefault, 0);

                    CmbTipoRecurso.DataSource = null;
                    CmbTipoRecurso.DataSource = dt;
                    CmbTipoRecurso.DisplayMember = "Nombre";
                    CmbTipoRecurso.ValueMember = "ID";
                    CmbTipoRecurso.SelectedIndex = 0;
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Error al conectar con MySQL para recursos: " + ex.Message);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al cargar el ComboBox de recursos: " + ex.Message);
            }
        }
        private void btnLimpiarCampos_Click(object sender, EventArgs e)
        {
            // Limpio los campos del formulario volviendo a la opcion por defecto
            if (CmbClientes.Items.Count > 0)
                CmbClientes.SelectedIndex = 0;
            if (CmbTipoRecurso.Items.Count > 0)
                CmbTipoRecurso.SelectedIndex = 0;
            if (cboHorarioInicio != null && cboHorarioInicio.Items.Count > 0)
                cboHorarioInicio.SelectedIndex = 0;

            dtpFechaReserva.Value = DateTime.Now;
            nudHoras.Value = 0;
            lblTotal.Text = "$ 0,00";
            CmbClientes.Focus();
        }

        //=============================================================
        // PANEL DE CONTROL: CREAR RESERVAS Y CÁLCULO EN TIEMPO REAL
        //=============================================================

        // Calcula el costo total en vivo segun el recurso seleccionado y las horas
        private void ActualizarTotalReserva()
        {
            try
            {
                int horas = Convert.ToInt32(nudHoras.Value);
                if (horas <= 0 || CmbTipoRecurso.SelectedValue == null)
                {
                    lblTotal.Text = "$ 0,00";
                    return;
                }

                int idRecurso = 0;
                int.TryParse(CmbTipoRecurso.SelectedValue.ToString(), out idRecurso);
                if (idRecurso <= 0)
                {
                    lblTotal.Text = "$ 0,00";
                    return;
                }

                if (CmbTipoRecurso.SelectedItem is DataRowView filaRecurso)
                {
                    decimal precioHora = 0;
                    if (filaRecurso.Row.Table.Columns.Contains("Precio/Hora") && filaRecurso["Precio/Hora"] != DBNull.Value)
                    {
                        decimal.TryParse(filaRecurso["Precio/Hora"].ToString(), out precioHora);
                    }

                    string tipoStr = filaRecurso.Row.Table.Columns.Contains("Tipo") ? filaRecurso["Tipo"]?.ToString() ?? "" : "";
                    decimal total = 0;

                    if (tipoStr.IndexOf("Sala", StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        int sillas = (filaRecurso.Row.Table.Columns.Contains("Cant. Sillas") && filaRecurso["Cant. Sillas"] != DBNull.Value) ? Convert.ToInt32(filaRecurso["Cant. Sillas"]) : 0;
                        Recurso r = RecursoFactory.CrearRecurso(1, filaRecurso["Nombre"]?.ToString() ?? "Sala", "", "", precioHora, false, sillas, 0);
                        total = r.CalcularCosto(horas);
                    }
                    else if (tipoStr.IndexOf("Oficina", StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        bool mobiliario = filaRecurso.Row.Table.Columns.Contains("Mobiliario") && filaRecurso["Mobiliario"] != DBNull.Value && Convert.ToBoolean(filaRecurso["Mobiliario"]);
                        Recurso r = RecursoFactory.CrearRecurso(2, filaRecurso["Nombre"]?.ToString() ?? "Oficina", "", "", precioHora, mobiliario, 0, 0);
                        total = r.CalcularCosto(horas);
                    }
                    else if (tipoStr.IndexOf("Puesto", StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        int categoria = (filaRecurso.Row.Table.Columns.Contains("Categoría") && filaRecurso["Categoría"] != DBNull.Value) ? Convert.ToInt32(filaRecurso["Categoría"]) : 1;
                        Recurso r = RecursoFactory.CrearRecurso(3, filaRecurso["Nombre"]?.ToString() ?? "Puesto", "", "", precioHora, false, 0, categoria);
                        total = r.CalcularCosto(horas);
                    }
                    else
                    {
                        total = precioHora * horas;
                    }

                    lblTotal.Text = $"$ {total:N2}";
                }
                else
                {
                    lblTotal.Text = "$ 0,00";
                }
            }
            catch
            {
                lblTotal.Text = "$ 0,00";
            }
        }

        private void nudHoras_ValueChanged(object sender, EventArgs e)
        {
            ActualizarTotalReserva();
        }

        private void CmbTipoRecurso_SelectedIndexChanged(object sender, EventArgs e)
        {
            ActualizarTotalReserva();
            ActualizarHorariosDisponibles();
        }

        private void dtpFechaReserva_ValueChanged(object sender, EventArgs e)
        {
            ActualizarHorariosDisponibles();
        }

        // Dibuja los horarios en el combo: pinta en rojo los que dicen '(Ocupado)' y normal los disponibles
        private void cboHorarioInicio_DrawItem(object sender, DrawItemEventArgs e)
        {
            if (e.Index < 0) return;
            e.DrawBackground();

            string texto = cboHorarioInicio.Items[e.Index].ToString();
            bool ocupado = texto.Contains("Ocupado");

            // Si está ocupado usamos pincel rojo, sino el color normal del texto
            using (Brush brush = new SolidBrush(ocupado ? Color.Red : e.ForeColor))
            {
                e.Graphics.DrawString(texto, e.Font, brush, e.Bounds);
            }
            e.DrawFocusRectangle();
        }

        // Si el usuario hace clic en un turno ocupado, le avisamos y volvemos a la seleccion inicial
        private void cboHorarioInicio_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cboHorarioInicio.SelectedItem != null && cboHorarioInicio.SelectedItem.ToString().Contains("Ocupado"))
            {
                MessageBox.Show("Ese horario ya se encuentra ocupado. Por favor seleccione un horario libre.", "Horario no disponible", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                cboHorarioInicio.SelectedIndex = 0;
            }
        }

        // Revisa la base de datos y marca en rojo con (Ocupado) los turnos ya reservados del dia
        public void ActualizarHorariosDisponibles()
        {
            if (cboHorarioInicio == null) return;

            cboHorarioInicio.Items.Clear();
            cboHorarioInicio.Items.Add("-- Seleccione un horario --");

            int idRecurso = 0;
            if (CmbTipoRecurso.SelectedValue != null)
            {
                int.TryParse(CmbTipoRecurso.SelectedValue.ToString(), out idRecurso);
            }

            DateTime fechaElegida = dtpFechaReserva.Value.Date;
            string nombreRecurso = "";
            if (CmbTipoRecurso.SelectedItem is DataRowView fila)
            {
                nombreRecurso = fila["Nombre"]?.ToString() ?? "";
            }

            DataTable dtReservas = null;
            try
            {
                dtReservas = _gestorDAO.ListarDetalleReservas();
            }
            catch { }

            for (int h = 7; h <= 22; h++)
            {
                DateTime inicioTurno = fechaElegida.AddHours(h);
                DateTime finTurno = inicioTurno.AddHours(1);

                // Si la fecha seleccionada es hoy, no mostramos los horarios que ya pasaron
                if (fechaElegida == DateTime.Today && inicioTurno <= DateTime.Now)
                {
                    continue;
                }

                bool ocupado = false;

                if (idRecurso > 0 && dtReservas != null && !string.IsNullOrEmpty(nombreRecurso))
                {
                    foreach (DataRow row in dtReservas.Rows)
                    {
                        if (row["estado"]?.ToString() == "Confirmada" && row["recurso"]?.ToString() == nombreRecurso)
                        {
                            DateTime fechaRes = Convert.ToDateTime(row["fecha_reserva"]);
                            int duracion = Convert.ToInt32(row["horas"]);
                            DateTime finRes = fechaRes.AddHours(duracion);

                            if (inicioTurno < finRes && finTurno > fechaRes)
                            {
                                ocupado = true;
                                break;
                            }
                        }
                    }
                }

                if (ocupado)
                {
                    cboHorarioInicio.Items.Add($"{h:D2}:00 (Ocupado)");
                }
                else
                {
                    cboHorarioInicio.Items.Add($"{h:D2}:00");
                }
            }

            cboHorarioInicio.SelectedIndex = 0;
        }

        // Aca conecto los campos del panel de control con el GestorDAO para guardar la reserva
        private void btnAgregar_Click(object sender, EventArgs e)
        {
            // Valido que hayan elegido un cliente valido (no la opcion por defecto)
            if (CmbClientes.SelectedIndex <= 0 || CmbClientes.SelectedValue == null || Convert.ToInt32(CmbClientes.SelectedValue) <= 0)
            {
                MessageBox.Show("Por favor seleccione un cliente de la lista.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                CmbClientes.Focus();
                return;
            }

            // Valido que hayan elegido un recurso valido (no la opcion por defecto)
            if (CmbTipoRecurso.SelectedIndex <= 0 || CmbTipoRecurso.SelectedValue == null || Convert.ToInt32(CmbTipoRecurso.SelectedValue) <= 0)
            {
                MessageBox.Show("Por favor seleccione un recurso para reservar.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                CmbTipoRecurso.Focus();
                return;
            }

            // Valido que hayan elegido un horario de inicio valido
            if (cboHorarioInicio == null || cboHorarioInicio.SelectedIndex <= 0 || cboHorarioInicio.SelectedItem == null)
            {
                MessageBox.Show("Por favor seleccione un horario de inicio para la reserva.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                cboHorarioInicio?.Focus();
                return;
            }

            // Valido que las horas sean mayores a cero y no superen 24 horas
            if (nudHoras.Value <= 0 || nudHoras.Value > 24)
            {
                MessageBox.Show("La cantidad de horas de uso debe ser como mínimo 1 y como máximo 24 horas por reserva.", "Horas inválidas", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                nudHoras.Focus();
                return;
            }

            // Valido que el horario no este ocupado
            if (cboHorarioInicio.SelectedItem.ToString().Contains("Ocupado"))
            {
                MessageBox.Show("El horario seleccionado ya se encuentra ocupado para este recurso. Por favor elija un horario disponible.", "Horario no disponible", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                cboHorarioInicio.Focus();
                return;
            }

            // Combinamos la fecha elegida con el horario seleccionado (limpiando texto extra si lo hubiera)
            string horarioLimpio = cboHorarioInicio.SelectedItem.ToString().Split(' ')[0];
            TimeSpan horaInicio = TimeSpan.Parse(horarioLimpio);
            DateTime fecha = dtpFechaReserva.Value.Date.Add(horaInicio);

            // Valido que la fecha y hora no sea anterior al momento actual
            if (fecha < DateTime.Now)
            {
                MessageBox.Show("El horario seleccionado ya transcurrió. Por favor elija un horario futuro.", "Horario no válido", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                cboHorarioInicio.Focus();
                return;
            }

            try
            {
                int idCliente = Convert.ToInt32(CmbClientes.SelectedValue);
                int idRecurso = Convert.ToInt32(CmbTipoRecurso.SelectedValue);
                int horas = Convert.ToInt32(nudHoras.Value);

                // Calculo el total usando el metodo polimorfico del modelo de clases
                decimal total = 0;
                if (CmbTipoRecurso.SelectedItem is DataRowView filaRecurso)
                {
                    decimal precioHora = Convert.ToDecimal(filaRecurso["Precio/Hora"]);
                    string tipoStr = filaRecurso["Tipo"].ToString();

                    if (tipoStr == "Sala de Reuniones")
                    {
                        int sillas = filaRecurso["Cant. Sillas"] != DBNull.Value ? Convert.ToInt32(filaRecurso["Cant. Sillas"]) : 0;
                        Recurso r = RecursoFactory.CrearRecurso(1, filaRecurso["Nombre"].ToString(), "", "", precioHora, false, sillas, 0);
                        total = r.CalcularCosto(horas);
                    }
                    else if (tipoStr == "Oficina Privada")
                    {
                        bool mobiliario = filaRecurso["Mobiliario"] != DBNull.Value && Convert.ToBoolean(filaRecurso["Mobiliario"]);
                        Recurso r = RecursoFactory.CrearRecurso(2, filaRecurso["Nombre"].ToString(), "", "", precioHora, mobiliario, 0, 0);
                        total = r.CalcularCosto(horas);
                    }
                    else if (tipoStr == "Puesto de Trabajo")
                    {
                        int categoria = filaRecurso["Categoría"] != DBNull.Value ? Convert.ToInt32(filaRecurso["Categoría"]) : 1;
                        Recurso r = RecursoFactory.CrearRecurso(3, filaRecurso["Nombre"].ToString(), "", "", precioHora, false, 0, categoria);
                        total = r.CalcularCosto(horas);
                    }
                    else
                    {
                        total = precioHora * horas;
                    }
                }
                else
                {
                    total = 1000 * horas;
                }

                // Llamo al metodo del GestorDAO que ejecuta el procedure sp_alta_reserva en MySQL
                bool guardo = _gestorDAO.AgregarReserva(idCliente, idRecurso, fecha, horas, total);

                if (guardo)
                {
                    MessageBox.Show("Reserva confirmada con éxito.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    // Recargo la grilla de reservas para que aparezca la nueva fila al instante
                    CargarReservas();
                    ActualizarHorariosDisponibles();

                    // Limpio los campos del panel de control
                    btnLimpiarCampos_Click(null, null);
                }
                else
                {
                    MessageBox.Show("No se pudo registrar la reserva en la base de datos.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (MySqlException ex)
            {
                // Si MySQL disparo la alarma con SIGNAL 45000 por solapamiento de turnos, muestro el mensaje claro
                MessageBox.Show(ex.Message, "Horario no disponible", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ocurrió un error al procesar la reserva: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        //=============================================================
        // CONTROLES DE CLIENTES
        //=============================================================

        // Abre el formulario de clientes y recarga la grilla al cerrar
        private void btnCrearUsuario_Click(object sender, EventArgs e)
        {
            using (FrmEditorClientes editorClientes = new FrmEditorClientes())
            {
                if (editorClientes.ShowDialog(this) == DialogResult.OK)
                {
                    // Recargo la tabla y el combo de clientes
                    CargarClientes();
                    CargarCboClientes();
                }
            }
        }

        // Modificar cliente seleccionado
        private void btnModificarUsuario_Click(object sender, EventArgs e)
        {
            if (dgvClientes.SelectedRows.Count > 0)
            {
                var fila = dgvClientes.SelectedRows[0];
                int idCliente = Convert.ToInt32(fila.Cells["ID"].Value);
                string nombre = fila.Cells["Nombre"].Value?.ToString() ?? "";
                string apellido = fila.Cells["Apellido"].Value?.ToString() ?? "";
                string telefono = fila.Cells["Teléfono"].Value?.ToString() ?? "";
                string mail = fila.Cells["Email"].Value?.ToString() ?? "";

                using (FrmEditorClientes editorClientes = new FrmEditorClientes(idCliente, nombre, apellido, telefono, mail))
                {
                    if (editorClientes.ShowDialog(this) == DialogResult.OK)
                    {
                        CargarClientes();
                        CargarCboClientes();
                    }
                }
            }
        }

        // Eliminar cliente seleccionado
        private void btnEliminarUsuario_Click(object sender, EventArgs e)
        {
            if (dgvClientes.SelectedRows.Count > 0)
            {
                var fila = dgvClientes.SelectedRows[0];
                int idCliente = Convert.ToInt32(fila.Cells["ID"].Value);
                string nombre = fila.Cells["Nombre"].Value?.ToString() ?? "este cliente";

                DialogResult confirmacion = MessageBox.Show($"¿Está seguro que desea eliminar a {nombre}?", "Confirmar baja", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (confirmacion == DialogResult.Yes)
                {
                    try
                    {
                        if (_gestorDAO.EliminarCliente(idCliente))
                        {
                            MessageBox.Show("Cliente eliminado correctamente.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            CargarClientes();
                            CargarCboClientes();
                        }
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("No se pudo eliminar el cliente: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        // Activa o desactiva los botones de cliente segun si hay fila seleccionada en la grilla
        private void dgvClientes_SelectionChanged(object sender, EventArgs e)
        {
            bool haySeleccion = dgvClientes.SelectedRows.Count > 0;
            btnModificarUsuario.Enabled = haySeleccion;
            btnEliminarUsuario.Enabled = haySeleccion;
        }

        //=============================================================
        // CONTROLES DE RECURSOS
        //=============================================================

        // Abre el formulario de recursos y recarga la grilla al cerrar
        private void btnCrearRecurso_Click(object sender, EventArgs e)
        {
            using (FrmEditorRecursos editorRecursos = new FrmEditorRecursos())
            {
                if (editorRecursos.ShowDialog(this) == DialogResult.OK)
                {
                    // Recargo la tabla y el combo de recursos
                    CargarRecursos();
                    CargarCboRecursos();
                }
            }
        }

        // Modificar recurso seleccionado
        private void btnModificarRecurso_Click(object sender, EventArgs e)
        {
            if (dgvRecursos.SelectedRows.Count > 0)
            {
                var fila = dgvRecursos.SelectedRows[0];
                int idRecurso = Convert.ToInt32(fila.Cells["ID"].Value);
                string nombre = fila.Cells["Nombre"].Value?.ToString() ?? "";
                string descripcion = fila.Cells["Descripción"].Value?.ToString() ?? "";
                string ubicacion = fila.Cells["Ubicación"].Value?.ToString() ?? "";
                decimal precio = fila.Cells["Precio/Hora"].Value != DBNull.Value ? Convert.ToDecimal(fila.Cells["Precio/Hora"].Value) : 0;
                string tipo = fila.Cells["Tipo"].Value?.ToString() ?? "";
                bool mobiliario = fila.Cells["Mobiliario"].Value != DBNull.Value && Convert.ToBoolean(fila.Cells["Mobiliario"].Value);
                int sillas = fila.Cells["Cant. Sillas"].Value != DBNull.Value ? Convert.ToInt32(fila.Cells["Cant. Sillas"].Value) : 0;
                int categoria = fila.Cells["Categoría"].Value != DBNull.Value ? Convert.ToInt32(fila.Cells["Categoría"].Value) : 0;

                using (FrmEditorRecursos editorRecursos = new FrmEditorRecursos(idRecurso, nombre, descripcion, ubicacion, precio, tipo, mobiliario, sillas, categoria))
                {
                    if (editorRecursos.ShowDialog(this) == DialogResult.OK)
                    {
                        CargarRecursos();
                        CargarCboRecursos();
                    }
                }
            }
        }

        // Eliminar recurso seleccionado
        private void btnEliminarRecurso_Click(object sender, EventArgs e)
        {
            if (dgvRecursos.SelectedRows.Count > 0)
            {
                var fila = dgvRecursos.SelectedRows[0];
                int idRecurso = Convert.ToInt32(fila.Cells["ID"].Value);
                string nombre = fila.Cells["Nombre"].Value?.ToString() ?? "este recurso";

                DialogResult confirmacion = MessageBox.Show($"¿Está seguro que desea eliminar {nombre}?", "Confirmar eliminación", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (confirmacion == DialogResult.Yes)
                {
                    try
                    {
                        if (_gestorDAO.EliminarRecurso(idRecurso))
                        {
                            MessageBox.Show("Recurso eliminado correctamente.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            CargarRecursos();
                            CargarCboRecursos();
                        }
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("No se pudo eliminar el recurso: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        // Activa o desactiva los botones de recursos segun si hay fila seleccionada
        private void dgvRecursos_SelectionChanged(object sender, EventArgs e)
        {
            bool haySeleccion = dgvRecursos.SelectedRows.Count > 0;
            btnModificarRecurso.Enabled = haySeleccion;
            btnEliminarRecurso.Enabled = haySeleccion;
        }

        //=============================================================
        // CONTROLES DE RESERVAS
        //=============================================================

        // Cancelar reserva seleccionada aplicando borrado logico
        private void btnEliminarReserva_Click(object sender, EventArgs e)
        {
            if (dgvReservas.SelectedRows.Count > 0)
            {
                var fila = dgvReservas.SelectedRows[0];
                // En la vista vw_detalle_reservas la columna primaria es id_reserva
                int idReserva = Convert.ToInt32(fila.Cells["id_reserva"].Value);

                DialogResult confirmacion = MessageBox.Show("¿Está seguro que desea cancelar la reserva seleccionada?", "Confirmar cancelación", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (confirmacion == DialogResult.Yes)
                {
                    try
                    {
                        // Llama al procedure sp_cancelar_reserva para hacer borrado logico
                        if (_gestorDAO.CancelarReserva(idReserva))
                        {
                            MessageBox.Show("Reserva cancelada correctamente.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            CargarReservas();
                        }
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("No se pudo cancelar la reserva: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        // Modificar fecha u horas de la reserva seleccionada (disponible solo para el admin)
        private void btnModificarReserva_Click(object sender, EventArgs e)
        {
            if (dgvReservas.SelectedRows.Count == 0)
            {
                MessageBox.Show("Por favor seleccione una reserva de la lista para modificar.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            var fila = dgvReservas.SelectedRows[0];
            int idReserva = Convert.ToInt32(fila.Cells["id_reserva"].Value);
            string cliente = fila.Cells["cliente"].Value?.ToString() ?? "Cliente";
            string recurso = fila.Cells["recurso"].Value?.ToString() ?? "Recurso";
            DateTime fechaActual = fila.Cells["fecha_reserva"].Value != DBNull.Value ? Convert.ToDateTime(fila.Cells["fecha_reserva"].Value) : DateTime.Now;
            int horasActuales = fila.Cells["horas"].Value != DBNull.Value ? Convert.ToInt32(fila.Cells["horas"].Value) : 1;
            decimal totalActual = fila.Cells["total"].Value != DBNull.Value ? Convert.ToDecimal(fila.Cells["total"].Value) : 0;
            decimal precioPorHora = horasActuales > 0 ? (totalActual / horasActuales) : 1000;

            using (Form frmModificar = new Form())
            {
                frmModificar.Text = $"Modificar Reserva #{idReserva}";
                frmModificar.Size = new Size(420, 380);
                frmModificar.StartPosition = FormStartPosition.CenterParent;
                frmModificar.FormBorderStyle = FormBorderStyle.FixedDialog;
                frmModificar.MaximizeBox = false;
                frmModificar.MinimizeBox = false;
                frmModificar.BackColor = Color.FromArgb(24, 30, 40);
                frmModificar.ForeColor = Color.White;

                Label lblInfo = new Label { Text = $"Cliente: {cliente}\nRecurso: {recurso}", Location = new Point(25, 20), Size = new Size(350, 45), Font = new Font("Segoe UI", 9.5f, FontStyle.Bold) };
                Label lblFecha = new Label { Text = "Nueva Fecha y Hora:", Location = new Point(25, 75), Size = new Size(350, 20), Font = new Font("Segoe UI", 9) };
                DateTimePicker dtpNuevaFecha = new DateTimePicker { Location = new Point(25, 100), Size = new Size(350, 26), Format = DateTimePickerFormat.Custom, CustomFormat = "dd/MM/yyyy HH:mm", MinDate = DateTime.Today };
                if (fechaActual >= DateTime.Today) dtpNuevaFecha.Value = fechaActual;

                Label lblHoras = new Label { Text = "Horas de uso (1 a 24 hs):", Location = new Point(25, 135), Size = new Size(350, 20), Font = new Font("Segoe UI", 9) };
                NumericUpDown nudNuevasHoras = new NumericUpDown { Location = new Point(25, 160), Size = new Size(120, 26), Minimum = 1, Maximum = 24, Value = Math.Min(Math.Max(horasActuales, 1), 24) };

                Label lblNuevoTotal = new Label { Text = $"Nuevo Total: $ {totalActual:N2}", Location = new Point(25, 200), Size = new Size(350, 30), Font = new Font("Segoe UI", 11, FontStyle.Bold), ForeColor = Color.LightGreen };

                nudNuevasHoras.ValueChanged += (s, ev) =>
                {
                    decimal nuevoTotal = precioPorHora * nudNuevasHoras.Value;
                    lblNuevoTotal.Text = $"Nuevo Total: $ {nuevoTotal:N2}";
                };

                Button btnGuardar = new Button { Text = "Guardar Cambios", Location = new Point(45, 260), Size = new Size(145, 38), BackColor = Color.FromArgb(40, 167, 69), ForeColor = Color.White, FlatStyle = FlatStyle.Flat };
                Button btnCancelar = new Button { Text = "Cancelar", Location = new Point(210, 260), Size = new Size(145, 38), BackColor = Color.FromArgb(108, 117, 125), ForeColor = Color.White, FlatStyle = FlatStyle.Flat };

                btnGuardar.Click += (s, ev) =>
                {
                    if (dtpNuevaFecha.Value.Date < DateTime.Today)
                    {
                        MessageBox.Show("La fecha no puede ser anterior al día de hoy.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        return;
                    }

                    try
                    {
                        decimal nuevoTotal = precioPorHora * nudNuevasHoras.Value;
                        bool modificado = _gestorDAO.ModificarReserva(idReserva, dtpNuevaFecha.Value, Convert.ToInt32(nudNuevasHoras.Value), nuevoTotal);
                        if (modificado)
                        {
                            MessageBox.Show("Reserva modificada con éxito.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                            frmModificar.DialogResult = DialogResult.OK;
                            frmModificar.Close();
                        }
                        else
                        {
                            MessageBox.Show("No se pudo modificar la reserva en la base de datos.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                    catch (MySqlException myEx)
                    {
                        MessageBox.Show(myEx.Message, "Horario no disponible", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Error al modificar reserva: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                };

                btnCancelar.Click += (s, ev) => { frmModificar.Close(); };

                frmModificar.Controls.Add(lblInfo);
                frmModificar.Controls.Add(lblFecha);
                frmModificar.Controls.Add(dtpNuevaFecha);
                frmModificar.Controls.Add(lblHoras);
                frmModificar.Controls.Add(nudNuevasHoras);
                frmModificar.Controls.Add(lblNuevoTotal);
                frmModificar.Controls.Add(btnGuardar);
                frmModificar.Controls.Add(btnCancelar);

                if (frmModificar.ShowDialog(this) == DialogResult.OK)
                {
                    CargarReservas();
                }
            }
        }

        // Activa o desactiva los botones de reservas segun seleccion
        private void dgvReservas_SelectionChanged(object sender, EventArgs e)
        {
            bool haySeleccion = dgvReservas.SelectedRows.Count > 0;
            btnModificarReserva.Enabled = haySeleccion;
            btnEliminarReserva.Enabled = haySeleccion;
        }

        private void dgvRecursos_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }
    }
}
