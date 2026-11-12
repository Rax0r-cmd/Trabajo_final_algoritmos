using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Text;
using System.Web.Script.Serialization;
using SistemaDeGestion.Modelos;

namespace SistemaDeGestion.Gestoras
{
    // DTO para serializacion y deserializacion del catalogo de recursos
    public class RecursoJsonDTO
    {
        public int IdTipoRecurso { get; set; }
        public string TipoEspacio { get; set; }
        public string Nombre { get; set; }
        public string Descripcion { get; set; }
        public string Ubicacion { get; set; }
        public decimal PrecioPorHora { get; set; }
        public bool? MobiliarioIncluido { get; set; }
        public int? CantidadSillas { get; set; }
        public int? NroCategoria { get; set; }
    }

    // DTO para exportar el reporte de reservas registradas
    public class ReservaJsonDTO
    {
        public int IdReserva { get; set; }
        public string Cliente { get; set; }
        public string Recurso { get; set; }
        public string TipoEspacio { get; set; }
        public string FechaReserva { get; set; }
        public int Horas { get; set; }
        public decimal Total { get; set; }
        public string Estado { get; set; }
    }

    /// <summary>
    /// Gestor encargado de la persistencia e intercambio en formato JSON (Etapa 6 de la Cátedra).
    /// Permite exportar e importar datos utilizando objetos reales del modelo.
    /// </summary>
    public class GestorJson
    {
        private readonly GestorDAO _gestorDAO;
        private readonly JavaScriptSerializer _serializer;

        public GestorJson(GestorDAO gestorDAO)
        {
            _gestorDAO = gestorDAO ?? new GestorDAO();
            _serializer = new JavaScriptSerializer();
        }

        // =========================================================================
        // EXPORTAR CATÁLOGO DE RECURSOS A JSON
        // =========================================================================
        public bool ExportarRecursos(string rutaArchivo)
        {
            try
            {
                DataTable tabla = _gestorDAO.ListarRecursos();
                List<RecursoJsonDTO> lista = new List<RecursoJsonDTO>();

                foreach (DataRow fila in tabla.Rows)
                {
                    string tipo = fila["Tipo"]?.ToString() ?? "";
                    int idTipo = 1;
                    if (tipo.IndexOf("Oficina", StringComparison.OrdinalIgnoreCase) >= 0) idTipo = 2;
                    else if (tipo.IndexOf("Puesto", StringComparison.OrdinalIgnoreCase) >= 0) idTipo = 3;

                    RecursoJsonDTO dto = new RecursoJsonDTO
                    {
                        IdTipoRecurso = idTipo,
                        TipoEspacio = tipo,
                        Nombre = fila["Nombre"]?.ToString() ?? "",
                        Descripcion = fila["Descripción"]?.ToString() ?? "",
                        Ubicacion = fila["Ubicación"]?.ToString() ?? "",
                        PrecioPorHora = fila["Precio/Hora"] != DBNull.Value ? Convert.ToDecimal(fila["Precio/Hora"]) : 0,
                        MobiliarioIncluido = fila["Mobiliario"] != DBNull.Value ? (bool?)Convert.ToBoolean(fila["Mobiliario"]) : null,
                        CantidadSillas = fila["Cant. Sillas"] != DBNull.Value ? (int?)Convert.ToInt32(fila["Cant. Sillas"]) : null,
                        NroCategoria = fila["Categoría"] != DBNull.Value ? (int?)Convert.ToInt32(fila["Categoría"]) : null
                    };
                    lista.Add(dto);
                }

                string jsonCrudo = _serializer.Serialize(lista);
                string jsonFormateado = FormatearJson(jsonCrudo);

                File.WriteAllText(rutaArchivo, jsonFormateado, Encoding.UTF8);
                return true;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al exportar catálogo de recursos a JSON: " + ex.Message, ex);
            }
        }

        // =========================================================================
        // IMPORTAR RECURSOS DESDE JSON
        // =========================================================================
        public int ImportarRecursos(string rutaArchivo)
        {
            try
            {
                if (!File.Exists(rutaArchivo))
                {
                    throw new FileNotFoundException("El archivo JSON especificado no existe.");
                }

                string contenidoJson = File.ReadAllText(rutaArchivo, Encoding.UTF8);
                List<RecursoJsonDTO> lista = _serializer.Deserialize<List<RecursoJsonDTO>>(contenidoJson);

                if (lista == null || lista.Count == 0)
                {
                    return 0;
                }

                int importados = 0;
                foreach (RecursoJsonDTO dto in lista)
                {
                    // Validamos datos minimos obligatorios
                    if (string.IsNullOrWhiteSpace(dto.Nombre) || dto.PrecioPorHora <= 0) continue;

                    bool mobiliario = dto.MobiliarioIncluido.HasValue && dto.MobiliarioIncluido.Value;
                    int sillas = dto.CantidadSillas.GetValueOrDefault(0);
                    int categoria = dto.NroCategoria.GetValueOrDefault(1);

                    // Instanciamos el objeto polimorfico a traves del patron Factory
                    Recurso nuevoRecurso = RecursoFactory.CrearRecurso(
                        dto.IdTipoRecurso,
                        dto.Nombre,
                        dto.Descripcion ?? "",
                        dto.Ubicacion ?? "",
                        dto.PrecioPorHora,
                        mobiliario,
                        sillas,
                        categoria
                    );

                    // Persistimos en MySQL
                    if (_gestorDAO.AgregarRecurso(nuevoRecurso))
                    {
                        importados++;
                    }
                }

                return importados;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al importar recursos desde JSON: " + ex.Message, ex);
            }
        }

        // =========================================================================
        // EXPORTAR RESERVAS A JSON
        // =========================================================================
        public bool ExportarReservas(string rutaArchivo)
        {
            try
            {
                DataTable tabla = _gestorDAO.ListarDetalleReservas();
                List<ReservaJsonDTO> lista = new List<ReservaJsonDTO>();

                foreach (DataRow fila in tabla.Rows)
                {
                    ReservaJsonDTO dto = new ReservaJsonDTO
                    {
                        IdReserva = fila["id_reserva"] != DBNull.Value ? Convert.ToInt32(fila["id_reserva"]) : 0,
                        Cliente = fila["cliente"]?.ToString() ?? "",
                        Recurso = fila["recurso"]?.ToString() ?? "",
                        TipoEspacio = fila["tipo_espacio"]?.ToString() ?? "",
                        FechaReserva = fila["fecha_reserva"] != DBNull.Value ? Convert.ToDateTime(fila["fecha_reserva"]).ToString("dd/MM/yyyy HH:mm") : "",
                        Horas = fila["horas"] != DBNull.Value ? Convert.ToInt32(fila["horas"]) : 0,
                        Total = fila["total"] != DBNull.Value ? Convert.ToDecimal(fila["total"]) : 0,
                        Estado = fila["estado"]?.ToString() ?? ""
                    };
                    lista.Add(dto);
                }

                string jsonCrudo = _serializer.Serialize(lista);
                string jsonFormateado = FormatearJson(jsonCrudo);

                File.WriteAllText(rutaArchivo, jsonFormateado, Encoding.UTF8);
                return true;
            }
            catch (Exception ex)
            {
                throw new Exception("Error al exportar reservas a JSON: " + ex.Message, ex);
            }
        }

        // =========================================================================
        // UTILIDAD: FORMATEADOR / INDENTADOR PROLIJO DE JSON
        // =========================================================================
        public static string FormatearJson(string json)
        {
            if (string.IsNullOrWhiteSpace(json)) return string.Empty;

            StringBuilder sb = new StringBuilder();
            bool entreComillas = false;
            int nivel = 0;
            const string sangria = "  ";

            for (int i = 0; i < json.Length; i++)
            {
                char c = json[i];

                if (c == '\"' && (i == 0 || json[i - 1] != '\\'))
                {
                    entreComillas = !entreComillas;
                    sb.Append(c);
                }
                else if (!entreComillas)
                {
                    switch (c)
                    {
                        case '{':
                        case '[':
                            sb.Append(c);
                            sb.AppendLine();
                            nivel++;
                            AgregarSangria(sb, nivel, sangria);
                            break;
                        case '}':
                        case ']':
                            sb.AppendLine();
                            nivel = Math.Max(0, nivel - 1);
                            AgregarSangria(sb, nivel, sangria);
                            sb.Append(c);
                            break;
                        case ',':
                            sb.Append(c);
                            sb.AppendLine();
                            AgregarSangria(sb, nivel, sangria);
                            break;
                        case ':':
                            sb.Append(": ");
                            break;
                        default:
                            if (!char.IsWhiteSpace(c))
                            {
                                sb.Append(c);
                            }
                            break;
                    }
                }
                else
                {
                    sb.Append(c);
                }
            }

            return sb.ToString();
        }

        private static void AgregarSangria(StringBuilder sb, int nivel, string sangria)
        {
            for (int j = 0; j < nivel; j++)
            {
                sb.Append(sangria);
            }
        }
    }
}

