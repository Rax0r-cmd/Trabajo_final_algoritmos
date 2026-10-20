using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SistemaDeGestion.Modelos
{
    public class Reserva
    {
        public int IdReserva { get; set; }
        public int IdCliente { get; set; }
        public int IdRecurso { get; set; }
        public DateTime Fecha { get; set; }
        public int Horas { get; set; }
        public decimal Total { get; set; }
        public EstadoReserva EstadoReserva { get; set; }

        public Reserva()
        {
        }

        public Reserva(int idReserva, int idCliente, int idRecurso, DateTime fecha, int horas, decimal total, EstadoReserva estadoReserva)
        {
            IdReserva = idReserva;
            IdCliente = idCliente;
            IdRecurso = idRecurso;
            Fecha = fecha;
            Horas = horas;
            Total = total;
            EstadoReserva = estadoReserva;
        }
        // Constructor que no recibe EstadoReserva y pasa "Confirmada" por defecto
        public Reserva(int idReserva, int idCliente, int idRecurso, DateTime fecha, int horas, decimal total)
            : this(idReserva, idCliente, idRecurso, fecha, horas, total, EstadoReserva.Confirmada)
        {
        }
    }
}
