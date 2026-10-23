using System;

public class GestorDAO

{
	public GestorDAO()
	{


	}
    //Creación de metodos para la inserción, modificación y eliminación de Clientes y Recursos
    public void AgregarClientes (int idCliente, string nombre, string apellido, string telefono, string mail, DateTime fechaRegistro)
    {
        int idCliente;
        string nombre;
        string apellido;
        string telefono;
        string mail;
        DateTime fechaRegistro;

        // Apertura conexión
        using (Mysqlconnection conexion = Conexion.CrearConexion()) ;
        conexion.open; 

    }
	
}
