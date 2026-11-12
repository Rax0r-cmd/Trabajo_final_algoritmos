using SistemaDeGestion.Formularios;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Windows.Forms;

namespace SistemaDeGestion
{
    public partial class FrmLogin : Form
    {
        public FrmLogin()
        {
            InitializeComponent();

            // Bloqueo de caracteres sospechosos, simbolos y SQL en tiempo real:
            // Usuario solo letras (ej: Admin), Password solo numeros (ej: 123456)
            this.TxtUsuario.KeyPress += new KeyPressEventHandler(TxtUsuario_KeyPress);
            this.TxtContrasenia.KeyPress += new KeyPressEventHandler(TxtContrasenia_KeyPress);
        }

        // Permite unicamente letras y teclas de control; bloquea numeros, simbolos (#, $, %) y comillas
        private void TxtUsuario_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (char.IsControl(e.KeyChar)) return;

            if (!char.IsLetter(e.KeyChar))
            {
                e.Handled = true; // Bloquea cualquier caracter que no sea letra
            }
        }

        // Permite unicamente digitos numericos y teclas de control; bloquea letras y simbolos
        private void TxtContrasenia_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (char.IsControl(e.KeyChar)) return;

            if (!char.IsDigit(e.KeyChar))
            {
                e.Handled = true; // Bloquea letras y simbolos especiales
            }
        }

        private void LbltituloCw_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void BtnLogin_Click(object sender, EventArgs e)
        {
            string Usuario = TxtUsuario.Text.Trim();
            string Contraseña = TxtContrasenia.Text.Trim();

            if(Usuario != "Admin")
            {
                MessageBox.Show("El Usuario es incorrecto", "Advertencia...", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                TxtUsuario.Focus();
                return;
            }
            if(Contraseña != "123456")
            {
                MessageBox.Show("La Contraseña es incorrecta", "Advertencia...", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                TxtContrasenia.Focus();
                return;
            }

            MessageBox.Show("Acceso Permitido", "Bienvenido", MessageBoxButtons.OK, MessageBoxIcon.Information);
            // aca va el codigo donde el formulario de login pasa al frmprincipal
            this.DialogResult = DialogResult.OK;
            this.Hide();
        }

        private void FrmLogin_Load(object sender, EventArgs e)
        {

        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            linkLabel1.LinkVisited = true;

            string telefono = "5492233014626";
            string mensaje = "Hola, soy usuario de CoWorking, me contacto para pedir asesoramiento con respecto al usuario y la contraseña, ¡muchas gracias!";

            // Escapa caracteres especiales y espacios para la URL
            string url = $"https://wa.me/{telefono}?text={Uri.EscapeDataString(mensaje)}";

            // En .NET Core / .NET 5+ se recomienda UseShellExecute = true
            Process.Start(new ProcessStartInfo
            {
                FileName = url,
                UseShellExecute = true
            });
        }
    }
}
