using System;

namespace SistemaDeGestion.Modelos
{
    // Interfaz para que cualquier espacio que se pueda alquilar
    // tenga si o si el metodo para chequear si esta disponible.
    // En las interfaces no va codigo, solo se anota el metodo.
    public interface IReservable
    {
        // Devuelve true si esta libre para esa fecha o false si esta ocupado
        bool PuedeReservarse(DateTime fecha);
    }
}
