using System;
using System.Windows.Forms;
using SistemaDeGestion.Gestoras;

namespace SistemaDeGestion
{
    public partial class FrmEditorClientes : Form
    {
        // Instancia del gestor para guardar en la base de datos
        private readonly GestorDAO _gestorDAO = new GestorDAO();
        private int _idCliente = 0;

        public FrmEditorClientes()
        {
            InitializeComponent();

            // Aca engancho los eventos de los botones para no alterar el designer
            this.btnAgregar.Click += new EventHandler(btnAgregar_Click);
            this.button1.Click += new EventHandler(btnCancelar_Click);

            // Validaciones de teclado en tiempo real (bloquea numeros en nombre y apellido, etc.)
            this.txtCNombre.KeyPress += new KeyPressEventHandler(SoloLetras_KeyPress);
            this.txtCApellido.KeyPress += new KeyPressEventHandler(SoloLetras_KeyPress);
            this.txtCTelefono.KeyPress += new KeyPressEventHandler(SoloTelefono_KeyPress);
            this.txtCMail.KeyPress += new KeyPressEventHandler(SoloEmail_KeyPress);
        }

        // Constructor para modo modificacion: precarga los datos del cliente seleccionado
        public FrmEditorClientes(int idCliente, string nombre, string apellido, string telefono, string mail) : this()
        {
            _idCliente = idCliente;
            txtCNombre.Text = nombre;
            txtCApellido.Text = apellido;
            txtCTelefono.Text = telefono;
            txtCMail.Text = mail;

            this.Text = "Modificar Cliente";
            this.label5.Text = "Modificar Cliente";
            this.btnAgregar.Text = "Guardar cambios";
        }

        // Permite unicamente letras (incluye tildes y eñes), espacios y teclas de control
        private void SoloLetras_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (char.IsControl(e.KeyChar)) return;

            if (!char.IsLetter(e.KeyChar) && e.KeyChar != ' ')
            {
                e.Handled = true; // Bloquea numeros y simbolos
            }
        }

        // Permite unicamente numeros, signos telefonicos (+, -) y teclas de control
        private void SoloTelefono_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (char.IsControl(e.KeyChar)) return;

            if (!char.IsDigit(e.KeyChar) && e.KeyChar != '+' && e.KeyChar != '-' && e.KeyChar != ' ')
            {
                e.Handled = true; // Bloquea letras y caracteres invalidos
            }
        }

        // Evita espacios en la casilla de correo
        private void SoloEmail_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == ' ')
            {
                e.Handled = true;
            }
        }

        // Funcion para revisar que los datos ingresados sean correctos
        public bool ValidarControles()
        {
            errorProvider1.Clear();
            bool esValido = true;

            // Validar Nombre
            if (string.IsNullOrWhiteSpace(txtCNombre.Text))
            {
                errorProvider1.SetError(txtCNombre, "El nombre es obligatorio.");
                esValido = false;
            }
            else if (System.Text.RegularExpressions.Regex.IsMatch(txtCNombre.Text, @"[0-9]"))
            {
                errorProvider1.SetError(txtCNombre, "El nombre no puede contener números.");
                esValido = false;
            }
            else if (txtCNombre.Text.Trim().Length < 2)
            {
                errorProvider1.SetError(txtCNombre, "El nombre debe tener al menos 2 letras.");
                esValido = false;
            }

            // Validar Apellido
            if (string.IsNullOrWhiteSpace(txtCApellido.Text))
            {
                errorProvider1.SetError(txtCApellido, "El apellido es obligatorio.");
                esValido = false;
            }
            else if (System.Text.RegularExpressions.Regex.IsMatch(txtCApellido.Text, @"[0-9]"))
            {
                errorProvider1.SetError(txtCApellido, "El apellido no puede contener números.");
                esValido = false;
            }
            else if (txtCApellido.Text.Trim().Length < 2)
            {
                errorProvider1.SetError(txtCApellido, "El apellido debe tener al menos 2 letras.");
                esValido = false;
            }

            // Validar Telefono
            if (string.IsNullOrWhiteSpace(txtCTelefono.Text))
            {
                errorProvider1.SetError(txtCTelefono, "El teléfono es obligatorio.");
                esValido = false;
            }
            else if (System.Text.RegularExpressions.Regex.IsMatch(txtCTelefono.Text, @"[a-zA-Z]"))
            {
                errorProvider1.SetError(txtCTelefono, "El teléfono no puede contener letras.");
                esValido = false;
            }
            else if (txtCTelefono.Text.Trim().Length < 6)
            {
                errorProvider1.SetError(txtCTelefono, "El teléfono debe tener al menos 6 dígitos.");
                esValido = false;
            }

            // Validar Correo
            if (string.IsNullOrWhiteSpace(txtCMail.Text))
            {
                errorProvider1.SetError(txtCMail, "El correo electrónico es obligatorio.");
                esValido = false;
            }
            else if (!txtCMail.Text.Contains("@") || !txtCMail.Text.Contains(".") || txtCMail.Text.Contains(" "))
            {
                errorProvider1.SetError(txtCMail, "Ingrese un correo electrónico válido (ej: usuario@mail.com).");
                esValido = false;
            }

            return esValido;
        }

        // Boton para guardar el cliente en la base
        private void btnAgregar_Click(object sender, EventArgs e)
        {
            // Primero valido que los campos esten bien cargados
            if (!ValidarControles())
            {
                MessageBox.Show("Por favor complete los campos obligatorios marcados con error.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                string nombre = txtCNombre.Text.Trim();
                string apellido = txtCApellido.Text.Trim();
                string telefono = txtCTelefono.Text.Trim();
                string mail = txtCMail.Text.Trim();

                // Le paso los datos al GestorDAO para que lo guarde o actualice en MySQL
                bool guardo;
                if (_idCliente > 0)
                {
                    guardo = _gestorDAO.ModificarCliente(_idCliente, nombre, apellido, telefono, mail);
                }
                else
                {
                    guardo = _gestorDAO.AgregarCliente(nombre, apellido, telefono, mail);
                }

                if (guardo)
                {
                    string accion = _idCliente > 0 ? "modificado" : "guardado";
                    MessageBox.Show($"Cliente {accion} correctamente.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    this.DialogResult = DialogResult.OK;
                    this.Close();
                }
                else
                {
                    MessageBox.Show("No se pudo guardar el cliente en la base de datos.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ocurrió un error al guardar el cliente: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Boton para cancelar y salir
        private void btnCancelar_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }

        private void FrmEditorClientes_Load(object sender, EventArgs e)
        {

        }
    }
}
