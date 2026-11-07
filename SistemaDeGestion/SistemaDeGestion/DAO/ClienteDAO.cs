using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.DAO
{
    /// <summary>
    /// Capa de acceso a datos (DAO - Data Access Object) para la entidad Cliente.
    /// Centraliza todas las operaciones sobre la tabla 'clientes' y la invocación
    /// de los procedimientos almacenados 'sp_alta_cliente' y 'sp_modificar_cliente'.
    /// </summary>
    public class ClienteDAO
    {
        public ClienteDAO()
        {
        }

        // =========================================================================
        // ALTAS (Procedimiento: sp_alta_cliente)
        // =========================================================================

        /// <summary>
        /// Agrega un nuevo cliente ejecutando el procedimiento almacenado 'sp_alta_cliente'.
        /// Los valores se reciben directamente por parámetros desde el formulario.
        /// </summary>
        /// <param name="nombre">Nombre del cliente.</param>
        /// <param name="apellido">Apellido del cliente.</param>
        /// <param name="telefono">Teléfono de contacto.</param>
        /// <param name="mail">Correo electrónico del cliente.</param>
        /// <returns>True si se insertó con éxito, False en caso contrario.</returns>
        public bool AgregarCliente(string nombre, string apellido, string telefono, string mail)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_alta_cliente", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("p_nombre", nombre);
                    cmd.Parameters.AddWithValue("p_apellido", apellido);
                    cmd.Parameters.AddWithValue("p_telefono", telefono);
                    cmd.Parameters.AddWithValue("p_mail", mail);

                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Sobrecarga que permite registrar un cliente a partir de una instancia del modelo Cliente.
        /// </summary>
        /// <param name="cliente">Instancia de Cliente con los datos a persistir.</param>
        /// <returns>True si se insertó con éxito, False en caso contrario.</returns>
        public bool AgregarCliente(Cliente cliente)
        {
            if (cliente == null) throw new ArgumentNullException(nameof(cliente));
            return AgregarCliente(cliente.Nombre, cliente.Apellido, cliente.Telefono, cliente.Mail);
        }

        /// <summary>
        /// Alias abreviado de AgregarCliente.
        /// </summary>
        public bool Agregar(string nombre, string apellido, string telefono, string mail)
        {
            return AgregarCliente(nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Alias abreviado de AgregarCliente con modelo.
        /// </summary>
        public bool Agregar(Cliente cliente)
        {
            return AgregarCliente(cliente);
        }

        /// <summary>
        /// Alias en plural de AgregarCliente por compatibilidad con versiones previas.
        /// </summary>
        public bool AgregarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return AgregarCliente(nombre, apellido, telefono, mail);
        }

        // =========================================================================
        // MODIFICACIONES (Procedimiento: sp_modificar_cliente)
        // =========================================================================

        /// <summary>
        /// Modifica los datos de un cliente ejecutando el procedimiento almacenado 'sp_modificar_cliente'.
        /// </summary>
        /// <param name="idCliente">Identificador único del cliente.</param>
        /// <param name="nombre">Nuevo nombre.</param>
        /// <param name="apellido">Nuevo apellido.</param>
        /// <param name="telefono">Nuevo teléfono.</param>
        /// <param name="mail">Nuevo correo electrónico.</param>
        /// <returns>True si la operación se ejecutó correctamente.</returns>
        public bool ModificarCliente(int idCliente, string nombre, string apellido, string telefono, string mail)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_modificar_cliente", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("p_id_cliente", idCliente);
                    cmd.Parameters.AddWithValue("p_nombre", nombre);
                    cmd.Parameters.AddWithValue("p_apellido", apellido);
                    cmd.Parameters.AddWithValue("p_telefono", telefono);
                    cmd.Parameters.AddWithValue("p_mail", mail);

                    int filasAfectadas = cmd.ExecuteNonQuery();
                    return filasAfectadas >= 0;
                }
            }
        }

        /// <summary>
        /// Sobrecarga que permite modificar un cliente a partir de una instancia del modelo Cliente.
        /// </summary>
        /// <param name="cliente">Instancia de Cliente con los datos actualizados.</param>
        /// <returns>True si la operación se ejecutó correctamente.</returns>
        public bool ModificarCliente(Cliente cliente)
        {
            if (cliente == null) throw new ArgumentNullException(nameof(cliente));
            return ModificarCliente(cliente.IdCliente, cliente.Nombre, cliente.Apellido, cliente.Telefono, cliente.Mail);
        }

        /// <summary>
        /// Alias abreviado de ModificarCliente.
        /// </summary>
        public bool Modificar(int idCliente, string nombre, string apellido, string telefono, string mail)
        {
            return ModificarCliente(idCliente, nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Alias abreviado de ModificarCliente con modelo.
        /// </summary>
        public bool Modificar(Cliente cliente)
        {
            return ModificarCliente(cliente);
        }

        /// <summary>
        /// Alias en plural de ModificarCliente por compatibilidad con versiones previas.
        /// </summary>
        public bool ModificarClientes(int idCliente, string nombre, string apellido, string telefono, string mail)
        {
            return ModificarCliente(idCliente, nombre, apellido, telefono, mail);
        }

        // =========================================================================
        // BAJAS (Consulta SQL parametrizada)
        // =========================================================================

        /// <summary>
        /// Elimina un cliente por su ID utilizando consulta parametrizada
        /// (DB_TPFinal.sql no define un SP de eliminación para clientes).
        /// </summary>
        /// <param name="idCliente">ID del cliente a eliminar.</param>
        /// <returns>True si se eliminó al menos una fila, False en caso contrario.</returns>
        public bool EliminarCliente(int idCliente)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "DELETE FROM clientes WHERE id_cliente = @id_cliente";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    cmd.Parameters.AddWithValue("@id_cliente", idCliente);
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Alias abreviado de EliminarCliente.
        /// </summary>
        public bool Eliminar(int idCliente)
        {
            return EliminarCliente(idCliente);
        }

        /// <summary>
        /// Alias en plural de EliminarCliente por compatibilidad.
        /// </summary>
        public bool EliminarClientes(int idCliente)
        {
            return EliminarCliente(idCliente);
        }

        // =========================================================================
        // CONSULTAS Y LISTADOS
        // =========================================================================

        /// <summary>
        /// Retorna un DataTable con todos los clientes para enlazar directamente al DataGridView (dgvClientes).
        /// </summary>
        public DataTable ListarClientes()
        {
            DataTable tabla = new DataTable();

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT id_cliente AS 'ID', " +
                               "nombre AS 'Nombre', " +
                               "apellido AS 'Apellido', " +
                               "telefono AS 'Teléfono', " +
                               "mail AS 'Email', " +
                               "fecha_registro AS 'Fecha de Registro' " +
                               "FROM clientes ORDER BY id_cliente ASC";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    using (MySqlDataAdapter adapter = new MySqlDataAdapter(cmd))
                    {
                        adapter.Fill(tabla);
                    }
                }
            }

            return tabla;
        }

        /// <summary>
        /// Alias genérico para listar clientes.
        /// </summary>
        public DataTable Listar()
        {
            return ListarClientes();
        }

        /// <summary>
        /// Obtiene un cliente por su identificador primario.
        /// </summary>
        /// <param name="idCliente">Identificador único del cliente.</param>
        /// <returns>Instancia de Cliente o null si no existe.</returns>
        public Cliente ObtenerPorId(int idCliente)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT id_cliente, nombre, apellido, telefono, mail, fecha_registro " +
                               "FROM clientes WHERE id_cliente = @id_cliente";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    cmd.Parameters.AddWithValue("@id_cliente", idCliente);
                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            return new Cliente(
                                Convert.ToInt32(reader["id_cliente"]),
                                reader["nombre"].ToString(),
                                reader["apellido"].ToString(),
                                reader["telefono"].ToString(),
                                reader["mail"].ToString(),
                                Convert.ToDateTime(reader["fecha_registro"])
                            );
                        }
                    }
                }
            }

            return null;
        }
    }
}
