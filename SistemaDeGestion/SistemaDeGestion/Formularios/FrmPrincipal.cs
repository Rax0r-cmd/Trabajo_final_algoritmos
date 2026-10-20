using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SistemaDeGestion.Formularios
{
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
            
        }

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
        public void MostrarSolapasAdmin()
        {
            if (!tabControl1.TabPages.Contains(tabGestion))
            {
                tabControl1.TabPages.Insert(2, tabGestion);
            }
        }

        public void Configuraciones()
        {
            // 1. Se guarda la referencia a las pestañas
            tabGestion = tabPageGestion;

            // 2. Las sacamos del TabControl para que no aparezcan
            tabControl1.TabPages.Remove(tabGestion);

            rbUsuario.Checked = true;
        }
    }
}
