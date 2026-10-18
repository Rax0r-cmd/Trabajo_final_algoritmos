using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SistemaDeGestion.Modelos
{
    public class Sala : Recurso
    {
        public Sala()
        {
            IdTipoRecurso = 1;
        }

        public Sala(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precioPorHora, int idTipoRecurso = 1)
            : base(idRecurso, nombre, descripcion, ubicacion, precioPorHora, idTipoRecurso)
        {
        }
        
        // Para el calculo de costo podemos incluir alguna acaracteristica unica praa cada una. 
        public override decimal CalcularCosto(int horas)
        {
            return PrecioPorHora * horas;
        }

        // Implementamos el metodo abstracto de la interfaz IReservable
        // Cada clase hija va a verificar si está disponible para esa fecha y la gestora es la que autoriza la reserva. 
        // La gestora va a preguntar si está disponible para esa fecha.
        public override bool PuedeReservarse(DateTime fecha)
        {
            if (fecha < DateTime.Now)
            { 
                // Si es una fecha anterio a la actual
                return false;
            }
            else 
            {
                // Cuando ya se pueda acceder a la base de datos, declarar 
                //una lista de reservas que recorra todas las reservas que ya estan
                List<Reserva> reservas = new List<Reserva>();
                foreach(Reserva reserva in reservas)
                {
                    // Si la fecha de reserva es la misma que la consultada pero el id recurso es el mismo o esta confirmada
                    // Devuelve false 
                    if(reserva.Fecha == fecha && reserva.IdRecurso == IdRecurso && reserva.EstadoReserva == EstadoReserva.Confirmada)
                    {
                        return false;
                    }
                }
                //Si no se encontro ninguna reserva para la fecha, devuelve true
                return true;
            }
        }
    }
}
