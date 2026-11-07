using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.DAO
{
    /// <summary>
    /// Capa de acceso a datos (DAO - Data Access Object) para los recursos físicos del coworking.
    /// Centraliza las operaciones sobre las tablas 'recursos' y 'tipo_recursos',
    /// invocando los procedimientos 'sp_alta_recurso' y 'sp_modificar_recurso'.
    /// </summary>
    public class RecursoDAO
    {
        public RecursoDAO()
        {
        }

        // =========================================================================
        // ALTAS (Procedimiento: sp_alta_recurso)
        // =========================================================================

        /// <summary>
        /// Agrega un recurso (sala de reuniones, oficina privada o puesto de trabajo)
        /// ejecutando el procedimiento almacenado 'sp_alta_recurso'.
        /// Los campos específicos (mobiliario, sillas, categoría) admiten valores nulos según el tipo de recurso.
        /// </summary>
        /// <param name="nombre">Nombre identificatorio del recurso.</param>
        /// <param name="descripcion">Descripción detallada o equipamiento.</param>
        /// <param name="ubicacion">Ubicación física (piso, sector, box).</param>
        /// <param name="precio">Tarifa por hora del recurso.</param>
        /// <param name="mobiliarioIncluido">Aplica a Oficina Privada (true/false) o null.</param>
        /// <param name="cantidadSillas">Aplica a Sala de Reuniones o null.</param>
        /// <param name="nroCategoria">Aplica a Puesto de Trabajo (1, 2 o 3) o null.</param>
        /// <param name="idTipoRecurso">1: Sala de Reuniones, 2: Oficina Privada, 3: Puesto de Trabajo.</param>
        /// <returns>True si se insertó con éxito, False en caso contrario.</returns>
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
        /// Sobrecarga polimórfica que permite agregar cualquier subtipo de Recurso (Sala, OficinaPrivada, PuestoTrabajo).
        /// </summary>
        /// <param name="recurso">Instancia polimórfica derivada de Recurso.</param>
        /// <returns>True si se insertó con éxito, False en caso contrario.</returns>
        public bool AgregarRecurso(Recurso recurso)
        {
            if (recurso == null) throw new ArgumentNullException(nameof(recurso));

            bool? mobiliario = null;
            int? sillas = null;
            int? categoria = null;

            if (recurso is Sala sala)
            {
                sillas = sala.CantSillas;
            }
            else if (recurso is OficinaPrivada oficina)
            {
                mobiliario = oficina.MobiliarioIncluido;
            }
            else if (recurso is PuestoTrabajo puesto)
            {
                categoria = puesto.NroCategoria;
            }

            return AgregarRecurso(recurso.Nombre, recurso.Descripcion, recurso.Ubicacion, recurso.PrecioPorHora,
                                  mobiliario, sillas, categoria, recurso.IdTipoRecurso);
        }

        /// <summary>
        /// Alias abreviado de AgregarRecurso.
        /// </summary>
        public bool Agregar(string nombre, string descripcion, string ubicacion, decimal precio,
                            bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return AgregarRecurso(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        /// <summary>
        /// Alias abreviado de AgregarRecurso con modelo.
        /// </summary>
        public bool Agregar(Recurso recurso)
        {
            return AgregarRecurso(recurso);
        }

        // =========================================================================
        // MODIFICACIONES (Procedimiento: sp_modificar_recurso)
        // =========================================================================

        /// <summary>
        /// Modifica un recurso existente ejecutando el procedimiento almacenado 'sp_modificar_recurso'.
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
        /// Sobrecarga polimórfica que permite modificar cualquier subtipo de Recurso.
        /// </summary>
        public bool ModificarRecurso(Recurso recurso)
        {
            if (recurso == null) throw new ArgumentNullException(nameof(recurso));

            bool? mobiliario = null;
            int? sillas = null;
            int? categoria = null;

            if (recurso is Sala sala)
            {
                sillas = sala.CantSillas;
            }
            else if (recurso is OficinaPrivada oficina)
            {
                mobiliario = oficina.MobiliarioIncluido;
            }
            else if (recurso is PuestoTrabajo puesto)
            {
                categoria = puesto.NroCategoria;
            }

            return ModificarRecurso(recurso.IdRecurso, recurso.Nombre, recurso.Descripcion, recurso.Ubicacion, recurso.PrecioPorHora,
                                    mobiliario, sillas, categoria, recurso.IdTipoRecurso);
        }

        /// <summary>
        /// Alias abreviado de ModificarRecurso.
        /// </summary>
        public bool Modificar(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precio,
                              bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return ModificarRecurso(idRecurso, nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        /// <summary>
        /// Alias abreviado de ModificarRecurso con modelo.
        /// </summary>
        public bool Modificar(Recurso recurso)
        {
            return ModificarRecurso(recurso);
        }

        // =========================================================================
        // BAJAS (Consulta SQL parametrizada)
        // =========================================================================

        /// <summary>
        /// Elimina un recurso por su ID mediante consulta parametrizada.
        /// </summary>
        /// <param name="idRecurso">ID del recurso a eliminar.</param>
        /// <returns>True si se eliminó, False en caso contrario.</returns>
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
        /// Alias abreviado de EliminarRecurso.
        /// </summary>
        public bool Eliminar(int idRecurso)
        {
            return EliminarRecurso(idRecurso);
        }

        // =========================================================================
        // CONSULTAS Y LISTADOS
        // =========================================================================

        /// <summary>
        /// Retorna un DataTable con todos los recursos registrados para el DataGridView (dgvRecursos).
        /// Incluye el nombre descriptivo del tipo de recurso mediante un INNER JOIN con 'tipo_recursos'.
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

        /// <summary>
        /// Alias genérico para listar recursos.
        /// </summary>
        public DataTable Listar()
        {
            return ListarRecursos();
        }

        /// <summary>
        /// Retorna el catálogo de tipos de recursos (Salas, Oficinas, Puestos) para poblar ComboBoxes.
        /// </summary>
        public DataTable ListarTiposRecurso()
        {
            DataTable tabla = new DataTable();

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT id_tipo_recurso, nombre_tipo FROM tipo_recursos ORDER BY id_tipo_recurso ASC";

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
        /// Obtiene una instancia polimórfica de Recurso (Sala, OficinaPrivada o PuestoTrabajo) según su ID.
        /// </summary>
        /// <param name="idRecurso">ID del recurso.</param>
        /// <returns>Instancia de Recurso correspondiente o null si no se encuentra.</returns>
        public Recurso ObtenerPorId(int idRecurso)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT id_recurso, nombre, descripcion, ubicacion, precio_por_hora, " +
                               "mobiliario_incluido, cantidad_sillas, nro_categoria, id_tipo_recurso " +
                               "FROM recursos WHERE id_recurso = @id_recurso";

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    cmd.Parameters.AddWithValue("@id_recurso", idRecurso);
                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            int id = Convert.ToInt32(reader["id_recurso"]);
                            string nombre = reader["nombre"].ToString();
                            string descripcion = reader["descripcion"] != DBNull.Value ? reader["descripcion"].ToString() : string.Empty;
                            string ubicacion = reader["ubicacion"].ToString();
                            decimal precio = Convert.ToDecimal(reader["precio_por_hora"]);
                            int idTipo = Convert.ToInt32(reader["id_tipo_recurso"]);

                            switch (idTipo)
                            {
                                case 1: // Sala de Reuniones
                                    int sillas = reader["cantidad_sillas"] != DBNull.Value ? Convert.ToInt32(reader["cantidad_sillas"]) : 0;
                                    return new Sala(id, nombre, descripcion, ubicacion, precio, sillas, idTipo);

                                case 2: // Oficina Privada
                                    bool mobiliario = reader["mobiliario_incluido"] != DBNull.Value && Convert.ToBoolean(reader["mobiliario_incluido"]);
                                    return new OficinaPrivada(id, nombre, descripcion, ubicacion, precio, mobiliario, idTipo);

                                case 3: // Puesto de Trabajo
                                    int categoria = reader["nro_categoria"] != DBNull.Value ? Convert.ToInt32(reader["nro_categoria"]) : 1;
                                    return new PuestoTrabajo(id, nombre, descripcion, ubicacion, precio, categoria, idTipo);

                                default:
                                    return null;
                            }
                        }
                    }
                }
            }

            return null;
        }
    }
}
