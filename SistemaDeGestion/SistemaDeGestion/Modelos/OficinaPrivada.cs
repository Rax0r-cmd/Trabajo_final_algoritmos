using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SistemaDeGestion.Modelos
{
    // Usar herencia de manera funcional y que cada  clase hija tenga su caracteristica y comportamiento propio
    public class OficinaPrivada : Recurso
    {
        //Propiedad unica de la clase hija (dentro del costructor se asigna su valor unico)
        public bool MobiliarioIncluido { get; set; }
        // Constructor vacio
        public OficinaPrivada()
        {
            IdTipoRecurso = 2;
        }

        // Constructor con datos para cuando traemos la info cargada
        public OficinaPrivada(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precioPorHora, bool mobiliarioIncluido, int idTipoRecurso = 2)
            : base(idRecurso, nombre, descripcion, ubicacion, precioPorHora, idTipoRecurso)
        {
            MobiliarioIncluido = mobiliarioIncluido;
        }

      
        // Para el calculo de costo podemos incluir alguna acaracteristica unica para cada una. 
        public override decimal CalcularCosto(int horas)
        {
            decimal costo = PrecioPorHora * horas;
            if (MobiliarioIncluido) 
            {
                return costo + 1500;
            }
            else 
            {
                return costo;
            }
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
