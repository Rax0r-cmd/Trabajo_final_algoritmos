using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;
using MySql.Data.Types;
using SistemaDeGestion.DAO;
using SistemaDeGestion.Gestoras;

namespace SistemaDeGestion.Formularios
{
    //=========================================================
    // Agregar acá la var Global para verificar cuando ingresó como Admin.
    //=========================================================
    public partial class FrmPrincipal : Form
    {
        // Instancia unificada del DAO (Fachada)
        private readonly GestorDAO _gestorDAO = new GestorDAO();

        // Variables para guardar las solapas en memoria.
        private TabPage tabClientes;
        private TabPage tabRecursos;

        public FrmPrincipal()
        {
            InitializeComponent();
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
                    //FormatearGrillaRecursos();
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
        /*
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
            if (dgvRecursos.Columns.Contains("Categoría"))
            {
                dgvRecursos.Columns["Categoría"].Width = 75;
                dgvRecursos.Columns["Categoría"].DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                dgvRecursos.Columns["Categoría"].HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
        }
        */

        //=============================================================
        // ToolStrip, configuración de solapas con el Login de Admin
        //=============================================================
        private void ingresarComoAdministradorToolStripMenuItem_Click(object sender, EventArgs e)
        {
            using (FrmLogin login = new FrmLogin())
            {
                if (login.ShowDialog() == DialogResult.OK)
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

        //=============================================================
        // Configuraciones generales
        //=============================================================
        public void MostrarSolapasAdmin()
        {
            // Si no está la solapa "Gestión", la agrega entre las solapas del tabIndex
            if (!tabControl1.TabPages.Contains(tabClientes))
            {
                tabControl1.TabPages.Insert(2, tabClientes);
            }
            if (!tabControl1.TabPages.Contains(tabRecursos))
            {
                tabControl1.TabPages.Insert(3, tabRecursos);
            }
        }

        public void OcultarSolapasAdmin()
        {
            // 1. Se guarda la referencia a las pestañas
            tabClientes = tabPageClientes;
            tabRecursos = tabPageRecursos;

            // 2. Las sacamos del TabControl para que no aparezcan
            tabControl1.TabPages.Remove(tabClientes);
            tabControl1.TabPages.Remove(tabRecursos);
        }

        public void Configuraciones()
        {
            OcultarSolapasAdmin();
            CargarCboClientes();
            CargarCboRecursos();
            //Reservas
            btnModificarReserva.Enabled = false;
            btnEliminarReserva.Enabled = false;


            //Recursos
            btnModificarRecurso.Enabled = false;
            btnEliminarRecurso.Enabled = false;

            //Cliente
            btnModificarUsuario.Enabled = false;
            btnEliminarUsuario.Enabled = false;
        }

        public void CargarCboClientes()
        {
            try
            {
                if (CmbClientes != null)
                {
                    CmbClientes.DataSource = null;
                    CmbClientes.DataSource = _gestorDAO.ListarClientes();
                    CmbClientes.DisplayMember = "Nombre";
                    CmbClientes.ValueMember = "ID";
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
                    CmbTipoRecurso.DataSource = null;
                    CmbTipoRecurso.DataSource = _gestorDAO.ListarRecursos();
                    CmbTipoRecurso.DisplayMember = "Nombre";
                    CmbTipoRecurso.ValueMember = "ID";
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
            //limpiar los campos del formulario

            CmbClientes.SelectedIndex = -1;
            CmbTipoRecurso.SelectedIndex = -1;
            dtpFechaReserva.Value = DateTime.Now;
            nudHoras.Value = 0;
            CmbClientes.Focus();
        }

        //=============================================================
        // Controles de Clientes
        //=============================================================
        private void btnCrearUsuario_Click(object sender, EventArgs e)
        {
            using (FrmEditorClientes editorClientes = new FrmEditorClientes())
            {
                editorClientes.ShowDialog();
                CargarClientes();
            }
        }

        private void btnModificarUsuario_Click(object sender, EventArgs e)
        {
            if(dgvClientes.SelectedRows.Count > 0)
            {
                using (FrmEditorClientes editorClientes = new FrmEditorClientes())
                {
                    editorClientes.ShowDialog();
                    CargarClientes();
                }
            }
        }

        private void btnEliminarUsuario_Click(object sender, EventArgs e)
        {
            
        }

        //=============================================================
        // Controles de Clientes
        //=============================================================

        private void btnCrearRecurso_Click(object sender, EventArgs e)
        {
            //metodo para abrir el formulario de creacion de recursos
            using (FrmEditorRecursos editorRecursos = new FrmEditorRecursos())
            {
                editorRecursos.ShowDialog();
                CargarRecursos();
            }
        }

        private void btnModificarRecurso_Click(object sender, EventArgs e)
        {
            //metodo para abrir el formulario de edicion de recursos si hay una fila seleccionada en dgvRecursos
            if (dgvRecursos.SelectedRows.Count > 0)
            {
                using (FrmEditorRecursos editorRecursos = new FrmEditorRecursos())
                {
                    editorRecursos.ShowDialog();
                    CargarRecursos();
                }
            }
        }

        private void dgvRecursos_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}
