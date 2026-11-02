using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;

namespace SistemaDeGestion.Gestoras
{
    /// <summary>
    /// Capa de acceso a datos (DAO - Data Access Object).
    /// Ejecuta las operaciones sobre la base de datos MySQL mediante los procedimientos almacenados,
    /// funciones y vistas definidos en 'DB_TPFinal.sql', recibiendo los datos directamente por parámetros
    /// desde los controles del formulario (sin requerir creación previa de objetos).
    /// </summary>
    public class GestorDAO
    {
        public GestorDAO()
        {
        }

        // =========================================================================
        // CLIENTES (Procedimientos: sp_alta_cliente, sp_modificar_cliente)
        // =========================================================================

        /// <summary>
        /// Agrega un nuevo cliente ejecutando el procedimiento almacenado 'sp_alta_cliente'.
        /// Los valores se reciben directamente por parámetros desde el formulario.
        /// </summary>
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
        /// Alias en plural de AgregarCliente.
        /// </summary>
        public bool AgregarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return AgregarCliente(nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Modifica los datos de un cliente ejecutando el procedimiento almacenado 'sp_modificar_cliente'.
        /// </summary>
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
        /// Alias en plural de ModificarCliente.
        /// </summary>
        public bool ModificarClientes(int idCliente, string nombre, string apellido, string telefono, string mail)
        {
            return ModificarCliente(idCliente, nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Elimina un cliente por su ID utilizando consulta parametrizada (dado que DB_TPFinal.sql no define un SP de eliminación para clientes).
        /// </summary>
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
        /// Alias en plural de EliminarCliente.
        /// </summary>
        public bool EliminarClientes(int idCliente)
        {
            return EliminarCliente(idCliente);
        }

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

        // =========================================================================
        // RECURSOS (Procedimientos: sp_alta_recurso, sp_modificar_recurso)
        // =========================================================================

        /// <summary>
        /// Agrega un recurso (sala, oficina privada, puesto) ejecutando 'sp_alta_recurso'.
        /// Los campos específicos (mobiliario, sillas, categoría) admiten valores nulos según el tipo de recurso.
        /// </summary>
        public bool AgregarRecurso(string nombre, string descripcion, string ubicacion, decimal precio,
                                   bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_alta_recurso", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("p_nombre", nombre);
                    cmd.Parameters.AddWithValue("p_descripcion", (object)descripcion ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_ubicacion", ubicacion);
                    cmd.Parameters.AddWithValue("p_precio", precio);
                    cmd.Parameters.AddWithValue("p_mobiliario_incluido", (object)mobiliarioIncluido ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_cantidad_sillas", (object)cantidadSillas ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_nro_categoria", (object)nroCategoria ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_id_tipo", idTipoRecurso);

                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Modifica un recurso existente ejecutando 'sp_modificar_recurso'.
        /// </summary>
        public bool ModificarRecurso(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precio,
                                     bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_modificar_recurso", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("p_id_recurso", idRecurso);
                    cmd.Parameters.AddWithValue("p_nombre", nombre);
                    cmd.Parameters.AddWithValue("p_descripcion", (object)descripcion ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_ubicacion", ubicacion);
                    cmd.Parameters.AddWithValue("p_precio", precio);
                    cmd.Parameters.AddWithValue("p_mobiliario_incluido", (object)mobiliarioIncluido ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_cantidad_sillas", (object)cantidadSillas ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_nro_categoria", (object)nroCategoria ?? DBNull.Value);
                    cmd.Parameters.AddWithValue("p_id_tipo", idTipoRecurso);

                    int filasAfectadas = cmd.ExecuteNonQuery();
                    return filasAfectadas >= 0;
                }
            }
        }

        /// <summary>
        /// Elimina un recurso por su ID mediante consulta parametrizada.
        /// </summary>
        public bool EliminarRecurso(int idRecurso)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "DELETE FROM recursos WHERE id_recurso = @id_recurso";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    cmd.Parameters.AddWithValue("@id_recurso", idRecurso);
                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Retorna un DataTable con todos los recursos registrados para el DataGridView (dgvRecursos).
        /// </summary>
        public DataTable ListarRecursos()
        {
            DataTable tabla = new DataTable();

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT r.id_recurso AS 'ID', " +
                               "r.nombre AS 'Nombre', " +
                               "r.descripcion AS 'Descripción', " +
                               "r.ubicacion AS 'Ubicación', " +
                               "r.precio_por_hora AS 'Precio/Hora', " +
                               "t.nombre_tipo AS 'Tipo', " +
                               "r.mobiliario_incluido AS 'Mobiliario', " +
                               "r.cantidad_sillas AS 'Cant. Sillas', " +
                               "r.nro_categoria AS 'Categoría' " +
                               "FROM recursos r " +
                               "INNER JOIN tipo_recursos t ON r.id_tipo_recurso = t.id_tipo_recurso " +
                               "ORDER BY r.id_recurso ASC";

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

        // =========================================================================
        // RESERVAS (Procedimientos: sp_alta_reserva, sp_cancelar_reserva, etc.)
        // =========================================================================

        /// <summary>
        /// Crea una nueva reserva ejecutando el procedimiento almacenado 'sp_alta_reserva'.
        /// La propia base de datos valida disponibilidad con 'fn_verificar_disponibilidad'.
        /// </summary>
        public bool AgregarReserva(int idCliente, int idRecurso, DateTime fecha, int horas, decimal total)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_alta_reserva", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("p_id_cliente", idCliente);
                    cmd.Parameters.AddWithValue("p_id_recurso", idRecurso);
                    cmd.Parameters.AddWithValue("p_fecha", fecha);
                    cmd.Parameters.AddWithValue("p_horas", horas);
                    cmd.Parameters.AddWithValue("p_total", total);

                    return cmd.ExecuteNonQuery() > 0;
                }
            }
        }

        /// <summary>
        /// Cancela una reserva existente ejecutando el procedimiento almacenado 'sp_cancelar_reserva'.
        /// Dispara automáticamente el trigger de auditoría 'trg_auditoria_reservas'.
        /// </summary>
        public bool CancelarReserva(int idReserva)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_cancelar_reserva", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    cmd.Parameters.AddWithValue("p_id_reserva", idReserva);

                    int filasAfectadas = cmd.ExecuteNonQuery();
                    return filasAfectadas >= 0;
                }
            }
        }

        /// <summary>
        /// Consulta la vista 'vw_detalle_reservas' creada en DB_TPFinal.sql con nombres descriptivos de cliente y espacio.
        /// </summary>
        public DataTable ListarDetalleReservas()
        {
            DataTable tabla = new DataTable();

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT * FROM vw_detalle_reservas ORDER BY fecha_reserva DESC";

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
        /// Consulta la vista 'vw_resumen_recursos' creada en DB_TPFinal.sql con cantidad de reservas y recaudación por espacio.
        /// </summary>
        public DataTable ListarResumenRecursos()
        {
            DataTable tabla = new DataTable();

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT * FROM vw_resumen_recursos";

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
        /// Ejecuta el procedimiento con cursor 'sp_calcular_total_recaudado_cursor' para obtener la suma de ingresos confirmados.
        /// </summary>
        public decimal CalcularTotalRecaudadoCursor()
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_calcular_total_recaudado_cursor", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;

                    MySqlParameter pTotal = new MySqlParameter("p_total_general", MySqlDbType.Decimal)
                    {
                        Direction = ParameterDirection.Output,
                        Precision = 10,
                        Scale = 2
                    };
                    cmd.Parameters.Add(pTotal);

                    cmd.ExecuteNonQuery();

                    return pTotal.Value != DBNull.Value ? Convert.ToDecimal(pTotal.Value) : 0m;
                }
            }
        }

        /// <summary>
        /// Invoca la función de MySQL 'fn_verificar_disponibilidad' para comprobar si un recurso está libre en una fecha/hora dada.
        /// </summary>
        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT fn_verificar_disponibilidad(@id_recurso, @fecha)";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    cmd.Parameters.AddWithValue("@id_recurso", idRecurso);
                    cmd.Parameters.AddWithValue("@fecha", fecha);

                    object resultado = cmd.ExecuteScalar();
                    return resultado != null && Convert.ToInt32(resultado) == 1;
                }
            }
        }
    }
}
