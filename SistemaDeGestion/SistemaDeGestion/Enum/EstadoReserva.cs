namespace SistemaDeGestion.Modelos
{
    // Armo este enum con los 3 estados posibles de una reserva.
    // Lo uso en vez de poner texto a mano para no equivocarme al tipear despues en el codigo.
    public enum EstadoReserva
    {
        Pendiente,
        Confirmada,
        Cancelada,
        Finalizada
    }
}
