using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SistemaDeGestion.Modelos
{
    public class Cliente
    {
        public int IdCliente { get; set; }
        public string Nombre { get; set; }
        public string Apellido { get; set; }
        public string Telefono { get; set; }
        public string Mail { get; set; }
        public DateTime FechaRegistro { get; set; }

        public Cliente()
        {
        }

        public Cliente(int idCliente, string nombre, string apellido, string telefono, string mail, DateTime fechaRegistro)
        {
            IdCliente = idCliente;
            Nombre = nombre;
            Apellido = apellido;
            Telefono = telefono;
            Mail = mail;
            FechaRegistro = fechaRegistro;
        }
    }
}
