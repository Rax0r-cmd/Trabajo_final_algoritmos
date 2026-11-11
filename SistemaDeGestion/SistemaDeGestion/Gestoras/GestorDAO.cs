using SistemaDeGestion.DAO;
using SistemaDeGestion.Modelos;
using System;
using System.Data;

namespace SistemaDeGestion.Gestoras
{
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

        public ClienteDAO Clientes => _clienteDAO;
        public RecursoDAO Recursos => _recursoDAO;
        public ReservaDAO Reservas => _reservaDAO;

        // CLIENTES
        public bool AgregarCliente(string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.AgregarCliente(nombre, apellido, telefono, mail);
        }

        public bool AgregarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.AgregarClientes(nombre, apellido, telefono, mail);
        }

        public bool ModificarCliente(string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.ModificarCliente(nombre, apellido, telefono, mail);
        }

        public bool ModificarClientes(string nombre, string apellido, string telefono, string mail)
        {
            return _clienteDAO.ModificarClientes(nombre, apellido, telefono, mail);
        }

        public bool EliminarCliente(int idCliente)
        {
            return _clienteDAO.EliminarCliente(idCliente);
        }

        public bool EliminarClientes(int idCliente)
        {
            return _clienteDAO.EliminarClientes(idCliente);
        }

        public DataTable ListarClientes()
        {
            return _clienteDAO.ListarClientes();
        }

        public DataTable Listar()
        {
            return _clienteDAO.Listar();
        }

        // RECURSOS



        public bool AgregarRecurso(string nombre, string descripcion, string ubicacion, decimal precio,
                                   bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return _recursoDAO.AgregarRecurso(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        
        public bool ModificarRecurso(string nombre, string descripcion, string ubicacion, decimal precio,
                                     bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return _recursoDAO.ModificarRecurso(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

        public bool Modificar(string nombre, string descripcion, string ubicacion, decimal precio,
                              bool? mobiliarioIncluido, int? cantidadSillas, int? nroCategoria, int idTipoRecurso)
        {
            return _recursoDAO.Modificar(nombre, descripcion, ubicacion, precio, mobiliarioIncluido, cantidadSillas, nroCategoria, idTipoRecurso);
        }

      
        public bool EliminarRecurso(int idRecurso)
        {
            return _recursoDAO.EliminarRecurso(idRecurso);
        }


        public DataTable ListarRecursos()
        {
            return _recursoDAO.ListarRecursos();
        }

        // Sobrecargas  para recibir objetos Recurso de la factory
        public bool AgregarRecurso(Recurso recurso)
        {
            return _recursoDAO.AgregarRecurso(recurso);
        }

        public bool ModificarRecurso(Recurso recurso)
        {
            return _recursoDAO.ModificarRecurso(recurso);
        }

        public bool Modificar(Recurso recurso)
        {
            return _recursoDAO.Modificar(recurso);
        }


        // RESERVAS
        public bool AgregarReserva(int idCliente, int idRecurso, DateTime fecha, int horas, decimal total)
        {
            return _reservaDAO.AgregarReserva(idCliente, idRecurso, fecha, horas, total);
        }

        public bool CancelarReserva(int idReserva)
        {
            return _reservaDAO.CancelarReserva(idReserva);
        }

        public DataTable ListarDetalleReservas()
        {
            return _reservaDAO.ListarDetalleReservas();
        }

        public DataTable ListarResumenRecursos()
        {
            return _reservaDAO.ListarResumenRecursos();
        }

        public decimal CalcularTotalRecaudadoCursor()
        {
            return _reservaDAO.CalcularTotalRecaudadoCursor();
        }

        public bool VerificarDisponibilidad(int idRecurso, DateTime fecha)
        {
            return _reservaDAO.VerificarDisponibilidad(idRecurso, fecha);
        }
    }
}
