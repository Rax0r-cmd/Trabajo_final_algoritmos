using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.DAO
{
    
    public class ReservaDAO
    {
        public ReservaDAO()
        {
        }

        // =========================================================================
        // ALTAS (Procedimiento: sp_alta_reserva)
        // =========================================================================

        
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

        
        public bool AgregarReserva(Reserva reserva)
        {
            if (reserva == null) throw new ArgumentNullException(nameof(reserva));
            return AgregarReserva(reserva.IdCliente, reserva.IdRecurso, reserva.Fecha, reserva.Horas, reserva.Total);
        }

        
        public bool Agregar(int idCliente, int idRecurso, DateTime fecha, int horas, decimal total)
        {
            return AgregarReserva(idCliente, idRecurso, fecha, horas, total);
        }

        
        public bool Agregar(Reserva reserva)
        {
            return AgregarReserva(reserva);
        }

        // =========================================================================
        // MODIFICACIONES (Procedimiento: sp_modificar_reserva)
        // =========================================================================

        public bool ModificarReserva(int idReserva, DateTime fecha, int horas, decimal total)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                using (MySqlCommand cmd = new MySqlCommand("sp_modificar_reserva", conexion))
                {
                    cmd.CommandType = CommandType.StoredProcedure;
                    
                    cmd.Parameters.AddWithValue("p_id_reserva", idReserva);
                    cmd.Parameters.AddWithValue("p_fecha", fecha);
                    cmd.Parameters.AddWithValue("p_horas", horas);
                    cmd.Parameters.AddWithValue("p_total", total);

                    int filasAfectadas = cmd.ExecuteNonQuery();
                    return filasAfectadas >= 0;
                }
            }
        }

        public bool ModificarReserva(Reserva reserva)
        {
            if (reserva == null) throw new ArgumentNullException(nameof(reserva));
            return ModificarReserva(reserva.IdReserva, reserva.Fecha, reserva.Horas, reserva.Total);
        }

        
        public bool Modificar(int idReserva, DateTime fecha, int horas, decimal total)
        {
            return ModificarReserva(idReserva, fecha, horas, total);
        }

        // =========================================================================
        // CANCELACIONES (Procedimiento: sp_cancelar_reserva y Trigger trg_auditoria_reservas)
        // =========================================================================

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

        
        public bool Cancelar(int idReserva)
        {
            return CancelarReserva(idReserva);
        }

        // =========================================================================
        // VISTAS (vw_detalle_reservas y vw_resumen_recursos)
        // =========================================================================

        
        public DataTable ListarDetalleReservas()
        {
            DataTable tabla = new DataTable();
            string query = "SELECT * FROM vw_detalle_reservas ORDER BY fecha_reserva DESC";

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
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
            return ListarDetalleReservas();
        }

        
        public DataTable ListarResumenRecursos()
        {
            DataTable tabla = new DataTable();
            string query = "SELECT * FROM vw_resumen_recursos";

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {

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
        // CURSORES Y FUNCIONES (sp_calcular_total_recaudado_cursor y fn_verificar_disponibilidad)
        // =========================================================================

        
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

        
        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha, int horas = 1)
        {
            string query = "SELECT fn_verificar_disponibilidad(@id_recurso, @fecha, @horas)";

            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();

                using (MySqlCommand cmd = new MySqlCommand(query, conexion))
                {
                    cmd.Parameters.AddWithValue("@id_recurso", idRecurso);
                    cmd.Parameters.AddWithValue("@fecha", fecha);
                    cmd.Parameters.AddWithValue("@horas", horas <= 0 ? 1 : horas);

                    object resultado = cmd.ExecuteScalar();
                    return resultado != null && Convert.ToInt32(resultado) == 1;
                }
            }
        }

        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha)
        {
            return VerificarDisponibilidad(idRecurso, fecha, 1);
        }
    }
}
