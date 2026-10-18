using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SistemaDeGestion.Modelos
{
    public class PuestoTrabajo : Recurso
    {
        //Propiedad unica de la clase hija (dentro del costructor se asigna su valor unico)
        public int NroCategoria { get; set; }
        public PuestoTrabajo()
        {
            IdTipoRecurso = 3;
        }

        public PuestoTrabajo(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precioPorHora, int nroCategoria, int idTipoRecurso = 3)
            : base(idRecurso, nombre, descripcion, ubicacion, precioPorHora, idTipoRecurso)
        {
            NroCategoria = nroCategoria;
        }

        
        // Para el calculo de costo podemos incluir alguna acaracteristica unica praa cada una. 
        public override decimal CalcularCosto(int horas)
        {
            decimal costo = PrecioPorHora * horas;
            if (NroCategoria == 1) 
            {
                return costo + 3500;
            }
            else if (NroCategoria == 2) 
            {
                return costo + 5500;
            }
            else if (NroCategoria == 3) 
            {
                return costo + 8000;
            }
            return costo;
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
