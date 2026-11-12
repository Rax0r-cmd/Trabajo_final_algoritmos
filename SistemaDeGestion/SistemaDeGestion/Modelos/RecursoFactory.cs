using System;

namespace SistemaDeGestion.Modelos
{
    // Aca armo la fabrica para crear los recursos segun lo que elija el usuario en pantalla
    // Uso el patron Factory para instanciar la clase hija correcta sin llenar de codigo el formulario
    public static class RecursoFactory
    {
        // Funcion que devuelve el objeto creado (Sala, Oficina o Puesto) segun el id de tipo
        public static Recurso CrearRecurso(int idTipo, string nombre, string descripcion, string ubicacion, decimal precio,
                                           bool mobiliario, int sillas, int categoria)
        {
            switch (idTipo)
            {
                case 1:
                    // Si eligio 1 es Sala de Reuniones y le pasamos la cantidad de sillas
                    return new Sala(nombre, descripcion, ubicacion, precio, sillas, 1);

                case 2:
                    // Si eligio 2 es Oficina Privada y le pasamos si tiene mobiliario o no
                    return new OficinaPrivada(nombre, descripcion, ubicacion, precio, mobiliario, 2);

                case 3:
                    // Si eligio 3 es Puesto de Trabajo y le pasamos el numero de categoria
                    return new PuestoTrabajo(nombre, descripcion, ubicacion, precio, categoria, 3);

                default:
                    throw new ArgumentException("El tipo de recurso seleccionado no es valido.");
            }
        }
    }
}

