using System;
using System.Data;
using MySql.Data.MySqlClient;
using SistemaDeGestion.ConexionDB;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.DAO
{
    /// <summary>
    /// Capa de acceso a datos (DAO - Data Access Object) para las reservas del coworking.
    /// Centraliza las operaciones sobre las tablas 'reservas', 'auditoria_reservas',
    /// los procedimientos 'sp_alta_reserva', 'sp_modificar_reserva', 'sp_cancelar_reserva',
    /// 'sp_calcular_total_recaudado_cursor', la función 'fn_verificar_disponibilidad'
    /// y las vistas 'vw_detalle_reservas' y 'vw_resumen_recursos'.
    /// </summary>
    public class ReservaDAO
    {
        public ReservaDAO()
        {
        }

        // =========================================================================
        // ALTAS (Procedimiento: sp_alta_reserva)
        // =========================================================================

        /// <summary>
        /// Crea una nueva reserva ejecutando el procedimiento almacenado 'sp_alta_reserva'.
        /// La propia base de datos valida disponibilidad mediante 'fn_verificar_disponibilidad'
        /// y lanza una excepción SIGNAL 45000 si el recurso ya está ocupado en ese horario.
        /// </summary>
        /// <param name="idCliente">Identificador del cliente solicitante.</param>
        /// <param name="idRecurso">Identificador del recurso a alquilar.</param>
        /// <param name="fecha">Fecha y hora de inicio de la reserva.</param>
        /// <param name="horas">Cantidad de horas de uso.</param>
        /// <param name="total">Importe total calculado.</param>
        /// <returns>True si la reserva se creó exitosamente.</returns>
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
        /// Sobrecarga que permite persistir una reserva a partir de una instancia del modelo Reserva.
        /// </summary>
        /// <param name="reserva">Instancia de la reserva.</param>
        /// <returns>True si se registró con éxito.</returns>
        public bool AgregarReserva(Reserva reserva)
        {
            if (reserva == null) throw new ArgumentNullException(nameof(reserva));
            return AgregarReserva(reserva.IdCliente, reserva.IdRecurso, reserva.Fecha, reserva.Horas, reserva.Total);
        }

        /// <summary>
        /// Alias abreviado de AgregarReserva.
        /// </summary>
        public bool Agregar(int idCliente, int idRecurso, DateTime fecha, int horas, decimal total)
        {
            return AgregarReserva(idCliente, idRecurso, fecha, horas, total);
        }

        /// <summary>
        /// Alias abreviado de AgregarReserva con modelo.
        /// </summary>
        public bool Agregar(Reserva reserva)
        {
            return AgregarReserva(reserva);
        }

        // =========================================================================
        // MODIFICACIONES (Procedimiento: sp_modificar_reserva)
        // =========================================================================

        /// <summary>
        /// Modifica la fecha, duración o importe de una reserva ejecutando 'sp_modificar_reserva'.
        /// Valida disponibilidad para el nuevo horario sin colisionar con otras reservas confirmadas.
        /// </summary>
        /// <param name="idReserva">ID de la reserva a modificar.</param>
        /// <param name="fecha">Nueva fecha y hora.</param>
        /// <param name="horas">Nueva cantidad de horas.</param>
        /// <param name="total">Nuevo importe total.</param>
        /// <returns>True si la modificación fue exitosa.</returns>
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

        /// <summary>
        /// Sobrecarga que modifica una reserva a partir de una instancia del modelo Reserva.
        /// </summary>
        public bool ModificarReserva(Reserva reserva)
        {
            if (reserva == null) throw new ArgumentNullException(nameof(reserva));
            return ModificarReserva(reserva.IdReserva, reserva.Fecha, reserva.Horas, reserva.Total);
        }

        /// <summary>
        /// Alias abreviado de ModificarReserva.
        /// </summary>
        public bool Modificar(int idReserva, DateTime fecha, int horas, decimal total)
        {
            return ModificarReserva(idReserva, fecha, horas, total);
        }

        // =========================================================================
        // CANCELACIONES (Procedimiento: sp_cancelar_reserva y Trigger trg_auditoria_reservas)
        // =========================================================================

        /// <summary>
        /// Cancela una reserva existente ejecutando el procedimiento almacenado 'sp_cancelar_reserva'.
        /// Cambia el estado a 'Cancelada' y dispara automáticamente el trigger 'trg_auditoria_reservas'
        /// que deja asentada la auditoría en la tabla 'auditoria_reservas'.
        /// </summary>
        /// <param name="idReserva">ID de la reserva a cancelar.</param>
        /// <returns>True si la cancelación se procesó correctamente.</returns>
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
        /// Alias abreviado de CancelarReserva.
        /// </summary>
        public bool Cancelar(int idReserva)
        {
            return CancelarReserva(idReserva);
        }

        // =========================================================================
        // VISTAS (vw_detalle_reservas y vw_resumen_recursos)
        // =========================================================================

        /// <summary>
        /// Consulta la vista 'vw_detalle_reservas' creada en DB_TPFinal.sql.
        /// Proyecta la información legible con nombres del cliente y del espacio físico
        /// para enlazar directamente a la grilla de reservas del formulario.
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
        /// Alias genérico para listar reservas.
        /// </summary>
        public DataTable Listar()
        {
            return ListarDetalleReservas();
        }

        /// <summary>
        /// Consulta la vista 'vw_resumen_recursos' creada en DB_TPFinal.sql
        /// con la métrica de cantidad de reservas y recaudación histórica por espacio.
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

        // =========================================================================
        // CURSORES Y FUNCIONES (sp_calcular_total_recaudado_cursor y fn_verificar_disponibilidad)
        // =========================================================================

        /// <summary>
        /// Ejecuta el procedimiento con cursor 'sp_calcular_total_recaudado_cursor'
        /// para obtener la sumatoria acumulada de ingresos confirmados recorridos fila por fila.
        /// </summary>
        /// <returns>Importe total recaudado en formato decimal.</returns>
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
        /// Invoca la función almacenada 'fn_verificar_disponibilidad(p_id_recurso, p_fecha, p_horas)'
        /// para determinar mediante cálculo de intervalos si el espacio está libre en la fecha y duración indicada.
        /// </summary>
        /// <param name="idRecurso">ID del recurso a consultar.</param>
        /// <param name="fecha">Fecha y hora de inicio proyectada.</param>
        /// <param name="horas">Cantidad de horas requeridas (por defecto 1).</param>
        /// <returns>True si el espacio está libre (1), False si está ocupado (0).</returns>
        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha, int horas = 1)
        {
            using (MySqlConnection conexion = Conexion.CrearConexion())
            {
                conexion.Open();
                string query = "SELECT fn_verificar_disponibilidad(@id_recurso, @fecha, @horas)";

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

        /// <summary>
        /// Sobrecarga de compatibilidad con 2 parámetros (asume duración de 1 hora).
        /// </summary>
        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha)
        {
            return VerificarDisponibilidad(idRecurso, fecha, 1);
        }
    }
}
