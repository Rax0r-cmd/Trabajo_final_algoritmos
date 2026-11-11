using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SistemaDeGestion
{
    public partial class FrmEditorClientes : Form
    {
        public FrmEditorClientes()
        {
            InitializeComponent();
        }

        public void ValidarControles()
        {
            if(string.IsNullOrWhiteSpace(txtCNombre.Text))
            {
                errorProvider1.SetError(txtCNombre, "El nombre es obligatorio.");
            }
            if(string.IsNullOrWhiteSpace(txtCApellido.Text))
            {
                errorProvider1.SetError(txtCApellido, "El apellido es obligatorio.");
            }
            if(string.IsNullOrWhiteSpace(txtCTelefono.Text))
            {
                errorProvider1.SetError(txtCTelefono, "El teléfono es obligatorio.");
            }
            if(string.IsNullOrWhiteSpace(txtCMail.Text))
            {
                errorProvider1.SetError(txtCMail, "El correo electrónico es obligatorio.");
            }
        }

        private void btnAgregar_Click(object sender, EventArgs e)
        {
            
        }

        private void btnCancelar_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void FrmEditorClientes_Load(object sender, EventArgs e)
        {

        }
    }
}
