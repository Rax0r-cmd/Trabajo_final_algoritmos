using MySql.Data.MySqlClient;
using MySql.Data.Types;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics.Eventing.Reader;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SistemaDeGestion.Formularios
{
    //=========================================================
    // Agregar acá la var Global para verificar cuando ingresó como Admin.
    //=========================================================
    public partial class FrmPrincipal : Form
    {
        //Variables para guardar las solapas en memoria.
        private TabPage tabGestion;
        public FrmPrincipal()
        {
            InitializeComponent();
        }

        private void FrmPrincipal_Load(object sender, EventArgs e)
        {
            Configuraciones();
        }

        //=============================================================
        //Conexion con DAO
        //=============================================================

        //=============================================================
        //ToolStrip, configuración de solapas con el Login de Admin
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
        //Configuraciónes generales
        //=============================================================
        public void MostrarSolapasAdmin()
        {
            // Si no está la solapa "Gestión", la agrega entre las solapas del tabIndex
            if (!tabControl1.TabPages.Contains(tabGestion))
            {
                tabControl1.TabPages.Insert(2, tabGestion);
            }
        }
        public void OcultarSolapasAdmin()
        {
            // 1. Se guarda la referencia a las pestañas
            tabGestion = tabPageGestion;

            // 2. Las sacamos del TabControl para que no aparezcan
            tabControl1.TabPages.Remove(tabGestion);
        }

        public void Configuraciones()
        {
            OcultarSolapasAdmin();
        }

        private void btnCrearUsuario_Click(object sender, EventArgs e)
        {

        }
    }
}
