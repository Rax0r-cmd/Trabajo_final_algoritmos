using System;

namespace SistemaDeGestion.Modelos
{
    // Clase abstracta:
    // La hago abstract porque en la realidad nadie alquila "un recurso" suelto en el aire,
    // vos alquilas una sala, una oficina o un escritorio.
    // Al ponerle abstract nadie puede hacer "new Recurso()" por error, y ademas me ahorro
    // repetir en cada clase las cosas que tienen todos en comun (nombre, precio, ubicacion).
    // Tambien le implemento la interfaz IReservable para que cumpla con la regla de reserva.
    public abstract class Recurso : IReservable
    {
        // Propiedades que comparten todos los lugares del coworking
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

        // Este metodo viene de la interfaz IReservable.
        // Lo dejamos preparado con una regla logica: no te deja reservar para dias que ya pasaron.
        public virtual bool PuedeReservarse(DateTime fecha)
        {
            return fecha.Date >= DateTime.Today;
        }

        // Metodo abstracto para calcular el costo:
        // Lo pongo abstracto y sin llaves porque cada lugar calcula la plata segun lo suyo
        // (por ejemplo si una sala tiene proyector o si la oficina tiene mas escritorios).
        // Como aca no tiene codigo, obligo a que cada clase hija (Sala, Oficina, Puesto)
        // haga su propia cuenta usando override. Esto es polimorfismo puro.
        public abstract decimal CalcularCosto(int horas);
    }
}
