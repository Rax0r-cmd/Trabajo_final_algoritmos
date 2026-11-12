using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.DAO
{
    public class RecursoDAO
    {
        public RecursoDAO()
        {
        }

        // =========================================================================
        // ALTAS (Procedimiento: sp_alta_recurso)
        // =========================================================================

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

        // Sobrecarga para agregar un recurso pasando un objeto Recurso 

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

        
        public bool Agregar(string nombre, string descripcion, string ubicacion, decimal precio,
                            bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return AgregarRecurso(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }



        // Sobrecarga para agregar un recurso pasando un objeto Recurso 

        public bool Agregar(Recurso recurso)
        {
            return AgregarRecurso(recurso);
        }

        // =========================================================================
        // MODIFICACIONES (Procedimiento: sp_modificar_recurso)
        // =========================================================================

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

        public bool ModificarRecurso(string nombre, string descripcion, string ubicacion, decimal precio,
                                     bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return ModificarRecurso(0, nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        
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

            return ModificarRecurso(recurso.Nombre, recurso.Descripcion, recurso.Ubicacion, recurso.PrecioPorHora,
                                    mobiliario, sillas, categoria, recurso.IdTipoRecurso);
        }

        
        public bool Modificar(string nombre, string descripcion, string ubicacion, decimal precio,
                              bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return ModificarRecurso(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        
        public bool Modificar(Recurso recurso)
        {
            return ModificarRecurso(recurso);
        }

        // =========================================================================
        // BAJAS (Consulta SQL parametrizada)
        // =========================================================================

        
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

        
        public bool Eliminar(int idRecurso)
        {
            return EliminarRecurso(idRecurso);
        }

        // =========================================================================
        // CONSULTAS Y LISTADOS
        // =========================================================================

        
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

        
        public DataTable Listar()
        {
            return ListarRecursos();
        }

        
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

        /*
        public Recurso ObtenerPorId(int idRecurso)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT id_recurso, nombre, descripcion, ubicacion, precio_por_hora, " +
                               "mobiliario_incluido, cantidad_sillas, nro_categoria, id_tipo_recurso " +
                               "FROM recursos WHERE id_recurso = p_id_recurso";

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
        */
    }
}
