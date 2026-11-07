using System;
using System.Data;
using SistemaDeGestion.DAO;

namespace SistemaDeGestion.Gestoras
{
    /// <summary>
    /// Capa de acceso a datos unificada (Patrón Facade / Fachada DAO).
    /// Mantiene compatibilidad total con la implementación anterior delegando
    /// las responsabilidades en las clases DAO especializadas:
    /// - <see cref="ClienteDAO"/>: Operaciones sobre clientes.
    /// - <see cref="RecursoDAO"/>: Operaciones sobre recursos del coworking.
    /// - <see cref="ReservaDAO"/>: Operaciones sobre reservas, vistas, cursores y funciones.
    /// </summary>
    public class GestorDAO
    {
        private readonly ClienteDAO _clienteDAO;
        private readonly RecursoDAO _recursoDAO;
        private readonly ReservaDAO _reservaDAO;

        public GestorDAO()
        {
            _clienteDAO = new ClienteDAO();
            _recursoDAO = new RecursoDAO();
            _reservaDAO = new ReservaDAO();
        }

        // Acceso directo a las instancias DAO individuales
        public ClienteDAO Clientes => _clienteDAO;
        public RecursoDAO Recursos => _recursoDAO;
        public ReservaDAO Reservas => _reservaDAO;

        // =========================================================================
        // CLIENTES (Delegación en ClienteDAO)
        // =========================================================================

        /// <summary>
        /// Agrega un nuevo cliente ejecutando el procedimiento almacenado 'sp_alta_cliente'.
        /// </summary>
        public bool AgregarCliente(string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.AgregarCliente(nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Alias en plural de AgregarCliente.
        /// </summary>
        public bool AgregarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.AgregarClientes(nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Modifica los datos de un cliente ejecutando el procedimiento almacenado 'sp_modificar_cliente'.
        /// </summary>
        public bool ModificarCliente(int idCliente, string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.ModificarCliente(idCliente, nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Alias en plural de ModificarCliente.
        /// </summary>
        public bool ModificarClientes(int idCliente, string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.ModificarClientes(idCliente, nombre, apellido, telefono, mail);
        }

        /// <summary>
        /// Elimina un cliente por su ID utilizando consulta parametrizada.
        /// </summary>
        public bool EliminarCliente(int idCliente)
        {
            return _clienteDAO.EliminarCliente(idCliente);
        }

        /// <summary>
        /// Alias en plural de EliminarCliente.
        /// </summary>
        public bool EliminarClientes(int idCliente)
        {
            return _clienteDAO.EliminarClientes(idCliente);
        }

        /// <summary>
        /// Retorna un DataTable con todos los clientes para enlazar directamente al DataGridView.
        /// </summary>
        public DataTable ListarClientes()
        {
            return _clienteDAO.ListarClientes();
        }

        /// <summary>
        /// Alias genérico para listar clientes.
        /// </summary>
        public DataTable Listar()
        {
            return _clienteDAO.Listar();
        }

        // =========================================================================
        // RECURSOS (Delegación en RecursoDAO)
        // =========================================================================

        /// <summary>
        /// Agrega un recurso (sala, oficina privada, puesto) ejecutando 'sp_alta_recurso'.
        /// </summary>
        public bool AgregarRecurso(string nombre, string descripcion, string ubicacion, decimal precio,
                                   bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return _recursoDAO.AgregarRecurso(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        /// <summary>
        /// Modifica un recurso existente ejecutando 'sp_modificar_recurso'.
        /// </summary>
        public bool ModificarRecurso(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precio,
                                     bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return _recursoDAO.ModificarRecurso(idRecurso, nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        /// <summary>
        /// Elimina un recurso por su ID mediante consulta parametrizada.
        /// </summary>
        public bool EliminarRecurso(int idRecurso)
        {
            return _recursoDAO.EliminarRecurso(idRecurso);
        }

        /// <summary>
        /// Retorna un DataTable con todos los recursos registrados para el DataGridView (dgvRecursos).
        /// </summary>
        public DataTable ListarRecursos()
        {
            return _recursoDAO.ListarRecursos();
        }

        // =========================================================================
        // RESERVAS (Delegación en ReservaDAO)
        // =========================================================================

        /// <summary>
        /// Crea una nueva reserva ejecutando el procedimiento almacenado 'sp_alta_reserva'.
        /// </summary>
        public bool AgregarReserva(int idCliente, int idRecurso, DateTime fecha, int horas, decimal total)
        {
            return _reservaDAO.AgregarReserva(idCliente, idRecurso, fecha, horas, total);
        }

        /// <summary>
        /// Cancela una reserva existente ejecutando el procedimiento almacenado 'sp_cancelar_reserva'.
        /// </summary>
        public bool CancelarReserva(int idReserva)
        {
            return _reservaDAO.CancelarReserva(idReserva);
        }

        /// <summary>
        /// Consulta la vista 'vw_detalle_reservas' con nombres descriptivos de cliente y espacio.
        /// </summary>
        public DataTable ListarDetalleReservas()
        {
            return _reservaDAO.ListarDetalleReservas();
        }

        /// <summary>
        /// Consulta la vista 'vw_resumen_recursos' con cantidad de reservas y recaudación por espacio.
        /// </summary>
        public DataTable ListarResumenRecursos()
        {
            return _reservaDAO.ListarResumenRecursos();
        }

        /// <summary>
        /// Ejecuta el procedimiento con cursor 'sp_calcular_total_recaudado_cursor'.
        /// </summary>
        public decimal CalcularTotalRecaudadoCursor()
        {
            return _reservaDAO.CalcularTotalRecaudadoCursor();
        }

        /// <summary>
        /// Invoca la función 'fn_verificar_disponibilidad' para comprobar disponibilidad.
        /// </summary>
        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha)
        {
            return _reservaDAO.VerificarDisponibilidad(idRecurso, fecha);
        }
    }
}
