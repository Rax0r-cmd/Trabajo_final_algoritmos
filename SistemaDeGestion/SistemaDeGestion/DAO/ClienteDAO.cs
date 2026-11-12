using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.DAO
{
    
    public class ClienteDAO
    {
        public ClienteDAO()
        {
        }

        // =========================================================================
        // ALTAS (Procedimiento: sp_alta_cliente)
        // =========================================================================

        
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

        
        public bool AgregarCliente(Cliente cliente)
        {
            if (cliente == null) throw new ArgumentNullException(nameof(cliente));
            return AgregarCliente(cliente.Nombre, cliente.Apellido, cliente.Telefono, cliente.Mail);
        }

        
        public bool Agregar(string nombre, string apellido, string telefono, string mail)
        {
            return AgregarCliente(nombre, apellido, telefono, mail);
        }

        
        public bool Agregar(Cliente cliente)
        {
            return AgregarCliente(cliente);
        }

        
        public bool AgregarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return AgregarCliente(nombre, apellido, telefono, mail);
        }

        // =========================================================================
        // MODIFICACIONES (Procedimiento: sp_modificar_cliente)
        // =========================================================================

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

        public bool ModificarCliente(string nombre, string apellido, string telefono, string mail)
        {
            return ModificarCliente(0, nombre, apellido, telefono, mail);
        }

        
        public bool ModificarCliente(Cliente cliente)
        {
            if (cliente == null) throw new ArgumentNullException(nameof(cliente));
            return ModificarCliente(cliente.Nombre, cliente.Apellido, cliente.Telefono, cliente.Mail);
        }

        
        public bool Modificar(string nombre, string apellido, string telefono, string mail)
        {
            return ModificarCliente(nombre, apellido, telefono, mail);
        }

        
        public bool Modificar(Cliente cliente)
        {
            return ModificarCliente(cliente);
        }

        
        public bool ModificarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return ModificarCliente(nombre, apellido, telefono, mail);
        }

        // =========================================================================
        // BAJAS (Consulta SQL parametrizada)
        // =========================================================================

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

        
        public bool Eliminar(int idCliente)
        {
            return EliminarCliente(idCliente);
        }

        
        public bool EliminarClientes(int idCliente)
        {
            return EliminarCliente(idCliente);
        }

        // =========================================================================
        // CONSULTAS Y LISTADOS
        // =========================================================================

        
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

        
        public DataTable Listar()
        {
            return ListarClientes();
        }

        
        public Cliente ObtenerPorId(int idCliente)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT id_cliente, nombre, apellido, telefono, mail, fecha_registro " +
                               "FROM clientes WHERE id_cliente = p_id_cliente";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            return new Cliente(
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
