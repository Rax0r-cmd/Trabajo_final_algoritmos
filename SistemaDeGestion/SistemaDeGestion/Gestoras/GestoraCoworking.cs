using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.Gestoras
{
    public class GestoraCoworking
    {
        // Lista que va a guardar todas las reservas realizadas
        List<Reserva> ListaReservas = new List<Reserva>();
        
        public void AgregarReserva(Reserva reserva)
        {
            ListaReservas.Add(reserva);
        }

        public void MostrarReservas()
        {
            foreach(Reserva reserva in ListaReservas)
            {
                Console.WriteLine(reserva);
            }
        }

        public List<Reserva> ObtenerReservasPorFecha(DateTime fecha)
        {
            return ListaReservas.Where(r => r.Fecha == fecha).ToList();
        }
        
        public List<Reserva> ObtenerReservasPorCliente(Cliente cliente)
        {
            return ListaReservas.Where(r => r.IdCliente == cliente.IdCliente).ToList();
        }    

        public List<Reserva> ObtenerReservasPorRecurso(Recurso recurso)
        {
            return ListaReservas.Where(r => r.IdRecurso == recurso.IdRecurso).ToList();
        }    

        public List<Reserva> ObtenerReservasPorEstado(EstadoReserva estado)
        {
            return ListaReservas.Where(r => r.EstadoReserva == estado).ToList();
        }    

        public void CancelarReserva(int idReserva)
        {
            Reserva reserva = ListaReservas.FirstOrDefault(r => r.IdReserva == idReserva);
            if (reserva != null)
            {
                reserva.EstadoReserva = EstadoReserva.Cancelada;
            }
        }   


        public void ConfirmarReserva(int idReserva)
        {
            Reserva reserva = ListaReservas.FirstOrDefault(r => r.IdReserva == idReserva);
            if (reserva != null)
            {
                reserva.EstadoReserva = EstadoReserva.Confirmada;
            }
        }   

        public void ModificarReserva(int idReserva, DateTime fecha, int horas)
        {
            Reserva reserva = ListaReservas.FirstOrDefault(r => r.IdReserva == idReserva);
            if (reserva != null)
            {
                reserva.Fecha = fecha;
                reserva.Horas = horas;
            }
        }


        public void FinalizarReserva(int idReserva)
        {
            Reserva reserva = ListaReservas.FirstOrDefault(r => r.IdReserva == idReserva);
            if (reserva != null)
            {
                reserva.EstadoReserva = EstadoReserva.Finalizada;
            }
        }

        
    }

}
