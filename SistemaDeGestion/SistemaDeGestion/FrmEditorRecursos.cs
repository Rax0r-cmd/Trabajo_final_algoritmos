using System;
using System.Data;
using System.Windows.Forms;
using SistemaDeGestion.Gestoras;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion
{
    public partial class FrmEditorRecursos : Form
    {
        // Instancia del gestor para comunicarnos con la base de datos
        private readonly GestorDAO _gestorDAO = new GestorDAO();
        private int _idRecurso = 0;

        public FrmEditorRecursos()
        {
            InitializeComponent();

            // Aca conecto los eventos de los botones para no tocar el designer
            this.btnAgregar.Click += new EventHandler(btnAgregar_Click);
            this.button1.Click += new EventHandler(button1_Click);
            this.cboTipoRecurso.SelectedIndexChanged += new EventHandler(cboTipoRecurso_SelectedIndexChanged);

            // Validacion de teclado para que en el precio solo se puedan escribir numeros y coma decimal
            this.textBox2.KeyPress += new KeyPressEventHandler(SoloDecimales_KeyPress);
        }

        // Constructor para modo modificacion: precarga los datos del recurso seleccionado
        public FrmEditorRecursos(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precio, string tipoTexto, bool mobiliario, int sillas, int categoria) : this()
        {
            _idRecurso = idRecurso;
            textBox1.Text = nombre;
            textBox4.Text = descripcion;
            textBox3.Text = ubicacion;
            textBox2.Text = precio.ToString("0.##");

            CargarTiposRecurso();
            if (cboTipoRecurso.Items.Count > 0)
            {
                for (int i = 0; i < cboTipoRecurso.Items.Count; i++)
                {
                    DataRowView drv = cboTipoRecurso.Items[i] as DataRowView;
                    if (drv != null && drv["nombre_tipo"].ToString().Equals(tipoTexto, StringComparison.OrdinalIgnoreCase))
                    {
                        cboTipoRecurso.SelectedIndex = i;
                        break;
                    }
                }
            }

            ckMobiliarioIncluido.Checked = mobiliario;
            nudCantSillas.Value = Math.Max(nudCantSillas.Minimum, Math.Min(nudCantSillas.Maximum, sillas));
            nudCatPuesto.Value = Math.Max(nudCatPuesto.Minimum, Math.Min(nudCatPuesto.Maximum, categoria));

            this.Text = "Modificar Recurso";
            this.label5.Text = "Modificar Recurso";
            this.btnAgregar.Text = "Guardar cambios";
        }

        // Bloquea letras o caracteres extraños en el campo precio
        private void SoloDecimales_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (char.IsControl(e.KeyChar)) return;

            // Permite solo digitos, punto y coma
            if (!char.IsDigit(e.KeyChar) && e.KeyChar != ',' && e.KeyChar != '.')
            {
                e.Handled = true;
            }

            // Evita ingresar mas de un punto o coma decimal
            if ((e.KeyChar == ',' || e.KeyChar == '.') && (textBox2.Text.Contains(",") || textBox2.Text.Contains(".")))
            {
                e.Handled = true;
            }
        }

        private void FrmEditorRecursos_Load(object sender, EventArgs e)
        {
            // Cargar las opciones en el desplegable de tipos de recursos
            CargarTiposRecurso();

            // Arranco con los campos especificos acomodados segun la opcion que quedo elegida
            ActualizarVisibilidadCampos();
        }

        // Funcion para llenar el combo con los 3 tipos de recursos
        private void CargarTiposRecurso()
        {
            try
            {
                DataTable tablaTipos = _gestorDAO.Recursos.ListarTiposRecurso();
                if (tablaTipos != null && tablaTipos.Rows.Count > 0)
                {
                    cboTipoRecurso.DataSource = tablaTipos;
                    cboTipoRecurso.DisplayMember = "nombre_tipo";
                    cboTipoRecurso.ValueMember = "id_tipo_recurso";
                    cboTipoRecurso.DropDownStyle = ComboBoxStyle.DropDownList;
                    return;
                }
            }
            catch
            {
                // Si la base no responde en este momento, cargo las 3 opciones a mano para que no quede vacio
            }

            DataTable tablaManual = new DataTable();
            tablaManual.Columns.Add("id_tipo_recurso", typeof(int));
            tablaManual.Columns.Add("nombre_tipo", typeof(string));
            tablaManual.Rows.Add(1, "Sala de Reuniones");
            tablaManual.Rows.Add(2, "Oficina Privada");
            tablaManual.Rows.Add(3, "Puesto de Trabajo");

            cboTipoRecurso.DataSource = tablaManual;
            cboTipoRecurso.DisplayMember = "nombre_tipo";
            cboTipoRecurso.ValueMember = "id_tipo_recurso";
            cboTipoRecurso.DropDownStyle = ComboBoxStyle.DropDownList;
        }

        // Aca muestro u oculto los controles segun que tipo de recurso eligio el usuario
        private void cboTipoRecurso_SelectedIndexChanged(object sender, EventArgs e)
        {
            ActualizarVisibilidadCampos();
        }

        private void ActualizarVisibilidadCampos()
        {
            if (cboTipoRecurso.SelectedValue == null) return;

            int idTipo;
            if (!int.TryParse(cboTipoRecurso.SelectedValue.ToString(), out idTipo)) return;

            if (idTipo == 1)
            {
                // Es Sala de Reuniones: solo muestro Cantidad de sillas
                label7.Visible = true;
                nudCantSillas.Visible = true;

                ckMobiliarioIncluido.Visible = false;
                label8.Visible = false;
                nudCatPuesto.Visible = false;
            }
            else if (idTipo == 2)
            {
                // Es Oficina Privada: solo muestro el checkbox de Mobiliario incluido
                ckMobiliarioIncluido.Visible = true;

                label7.Visible = false;
                nudCantSillas.Visible = false;
                label8.Visible = false;
                nudCatPuesto.Visible = false;
            }
            else if (idTipo == 3)
            {
                // Es Puesto de Trabajo: solo muestro la Categoria del puesto
                label8.Visible = true;
                nudCatPuesto.Visible = true;

                label7.Visible = false;
                nudCantSillas.Visible = false;
                ckMobiliarioIncluido.Visible = false;
            }
        }

        // Valido que no me dejen datos en blanco o numeros negativos
        private bool ValidarCampos()
        {
            errorProvider1.Clear();
            bool esValido = true;

            if (string.IsNullOrWhiteSpace(textBox1.Text))
            {
                errorProvider1.SetError(textBox1, "El nombre del recurso es obligatorio.");
                esValido = false;
            }

            if (string.IsNullOrWhiteSpace(textBox3.Text))
            {
                errorProvider1.SetError(textBox3, "La ubicación es obligatoria.");
                esValido = false;
            }

            decimal precio;
            if (string.IsNullOrWhiteSpace(textBox2.Text) || !decimal.TryParse(textBox2.Text.Trim(), out precio) || precio <= 0)
            {
                errorProvider1.SetError(textBox2, "Ingrese un precio por hora numérico mayor a cero.");
                esValido = false;
            }

            if (cboTipoRecurso.SelectedIndex < 0)
            {
                errorProvider1.SetError(cboTipoRecurso, "Debe seleccionar un tipo de recurso.");
                esValido = false;
            }

            return esValido;
        }

        // Evento al apretar Guardar
        private void btnAgregar_Click(object sender, EventArgs e)
        {
            if (!ValidarCampos())
            {
                MessageBox.Show("Por favor revise los campos marcados con error.", "Atención", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                // Tomo los datos ingresados en el formulario
                string nombre = textBox1.Text.Trim();
                string ubicacion = textBox3.Text.Trim();
                string descripcion = textBox4.Text.Trim();
                decimal precio = decimal.Parse(textBox2.Text.Trim());
                int idTipo = Convert.ToInt32(cboTipoRecurso.SelectedValue);

                bool mobiliario = ckMobiliarioIncluido.Checked;
                int sillas = Convert.ToInt32(nudCantSillas.Value);
                int categoria = Convert.ToInt32(nudCatPuesto.Value);

                bool guardo;
                if (_idRecurso > 0)
                {
                    // Si estamos modificando, llamamos a ModificarRecurso pasando el ID existente
                    guardo = _gestorDAO.ModificarRecurso(_idRecurso, nombre, descripcion, ubicacion, precio, mobiliario, sillas, categoria, idTipo);
                }
                else
                {
                    // Si es nuevo recurso, usamos el patron Factory
                    Recurso nuevoRecurso = RecursoFactory.CrearRecurso(idTipo, nombre, descripcion, ubicacion, precio, mobiliario, sillas, categoria);
                    guardo = _gestorDAO.AgregarRecurso(nuevoRecurso);
                }

                if (guardo)
                {
                    string accion = _idRecurso > 0 ? "modificado" : "guardado";
                    MessageBox.Show($"Recurso {accion} correctamente.", "Éxito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    this.DialogResult = DialogResult.OK;
                    this.Close();
                }
                else
                {
                    MessageBox.Show("No se pudo guardar el recurso en la base de datos.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ocurrió un error al guardar: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Boton cancelar para cerrar la ventana
        private void button1_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }
    }
}
