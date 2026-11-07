using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MySql.Data.MySqlClient;  // Importante para poder usar para la conexion a mysql.

namespace SistemaDeGestion.ConexionDB
{

    //Datos de conexion a la base de datos mysql via xamp o workbench.
    public static class Conexion
    {
        private static string cadenaConexion =
        "server=localhost;" +
        "port=3306;" +
        "database=tp_final_db;" +
        "uid=root;" +
        "pwd=";

        //Este metodo lo que hace es devolver el objeto mysqlconnection listo para usar.
        //Aca es donde se crea la conexion, pero se abre con .Open() donde lo necesitemos usar en cualquier parte del proyecto.
        public static MySqlConnection CrearConexion()
        {
            // Lee automáticamente el connectionString definido en el App.config con fallback a cadenaConexion
            string cadena = ConfigurationManager.ConnectionStrings["ConexionDB"]?.ConnectionString;
            if (string.IsNullOrEmpty(cadena))
            {
                cadena = cadenaConexion;
            }
            return new MySqlConnection(cadena);
        }
    }

}