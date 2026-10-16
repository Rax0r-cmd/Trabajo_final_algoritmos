using System;

namespace SistemaDeGestion.Modelos
{
    // Clase abstracta para los lugares del coworking.
    // La hago abstract para no crear un recurso suelto y usarla de base para las demas.
    // Tambien implementa IReservable para saber si se puede alquilar.
    public abstract class Recurso : IReservable
    {
        // Propiedades que comparten todos los lugares
        public int IdRecurso { get; set; }
        public string Nombre { get; set; }
        public string Descripcion { get; set; }
        public string Ubicacion { get; set; }
        public decimal PrecioPorHora { get; set; }
        public int IdTipoRecurso { get; set; }

        // Constructor vacio
        public Recurso()
        {
        }

        // Constructor con datos para cuando traemos la info cargada
        public Recurso(int idRecurso, string nombre, string descripcion, string ubicacion, decimal precioPorHora, int idTipoRecurso)
        {
            IdRecurso = idRecurso;
            Nombre = nombre;
            Descripcion = descripcion;
            Ubicacion = ubicacion;
            PrecioPorHora = precioPorHora;
            IdTipoRecurso = idTipoRecurso;
        }

        // Revisa que no se reserve una fecha que ya paso
        public virtual bool PuedeReservarse(DateTime fecha)
        {
            return fecha.Date >= DateTime.Today;
        }

        // Metodo para sacar el precio total segun las horas que se alquila.
        // Es abstracto porque cada lugar (sala, oficina, etc.) tiene su propia cuenta.
        public abstract decimal CalcularCosto(int horas);
    }
}
