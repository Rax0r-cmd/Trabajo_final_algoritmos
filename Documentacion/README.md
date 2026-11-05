# Documentación del Sistema y Memoria Técnica Integradora

**Asignatura:** Algoritmos II · Ciclo Lectivo 2026  
**Carrera:** Analista de Sistemas de Información  
**Institución:** Instituto Argentino de la Empresa  
**Docente a cargo:** Lic. Adrián Aroca  
**Tema:** Sistema de Gestión de Coworking y Reservas  
**Equipo de Desarrollo:**  
- Jonathan Lester Tullo (`shonimdp@gmail.com`)
- David Samuel Ortega (`davidortegaa86@gmail.com`)
- Maximiliano Scollo (`maximilianoscollo17@gmail.com`)

---

## 1. Documentos Oficiales Generados (.docx y .pdf)

Todos los documentos respetan rigurosamente las **Pautas Generales de Presentación de Trabajos Prácticos** de la cátedra:
- Hoja tamaño **A4** con márgenes de **2,54 cm** en los cuatro lados.
- Tipografía **Arial 11 pt**, interlineado **1,5** y alineación **justificada**.
- Jerarquía de títulos estricta: Título 18 pt negrita centrado; H1 16 pt negrita; H2 13 pt negrita; H3 11 pt negrita.
- Normas **APA 7.ª edición** para rotulado de figuras, tablas sin líneas verticales y listado final de referencias bibliográficas.
- Portada institucional obligatoria completa (institución, carrera, materia, docente, comisión, ciclo lectivo, integrantes y versión).

### Entregables Oficiales:
1. **Documento Único Integrador Oficial (Reglamentario por Grupo):**
   - [TP_Final_AlgoritmosII_Grupo2.docx](TP_Final_AlgoritmosII_Grupo2.docx) · [TP_Final_AlgoritmosII_Grupo2.pdf](TP_Final_AlgoritmosII_Grupo2.pdf) (23 páginas completas con arquitectura POO, modelo relacional MySQL, código formateado en monospace, manual de usuario, referencias APA 7 y checklist).
2. **Módulo Técnico de Arquitectura y POO:**
   - [Documentacion_Desarrollo.docx](Documentacion_Desarrollo.docx) · [Documentacion_Desarrollo.pdf](Documentacion_Desarrollo.pdf) (Explicación técnica del sistema, capas, herencia, justificación de polimorfismo en `CalcularCosto`, patrón DAO y manejo de excepciones con `SIGNAL 45000`).
3. **Módulo Técnico de Base de Datos MySQL:**
   - [Diccionario_de_Datos.docx](Diccionario_de_Datos.docx) · [Diccionario_de_Datos.pdf](Diccionario_de_Datos.pdf) (Estructura de tablas, claves foráneas, vistas, función `fn_verificar_disponibilidad` con fórmula de solapamiento, procedimientos almacenados y trigger `trg_auditoria_reservas`).
4. **Módulo Operativo de Usuario:**
   - [Manual_de_Usuario.docx](Manual_de_Usuario.docx) · [Manual_de_Usuario.pdf](Manual_de_Usuario.pdf) (Puesta en marcha, pantalla `FrmLogin`, credenciales de administrador, enlace interactivo a WhatsApp y operación de solapas Control, Reservas y Gestión).

---

## 2. Diagramas Técnicos Incluidos

- **Diagrama Entidad-Relación (DER) MySQL Workbench:** `DB/Diagrama_DER.png` (887 × 575 px, 300 DPI, pixel-perfect con todas las columnas de recursos visibles).
- **Diagrama Conceptual de Bloques (Borrador de Diseño):** `DB/Diagrama_DER_Borrador.png` (Flujo de interacción cliente-espacio-reserva).
- **Diagrama de Clases Simplificado (UML):** `DB/Diagrama_Clases_UML.png` (1800 × 1150 px, 300 DPI, clases abstractas, interfaces, herencia funcional, agregaciones y capa DAO).

---

## 3. Resumen de Cumplimiento de Pautas

| Sección | Requisito de la Cátedra | Estado |
|---|---|:---:|
| **00 // Formato y Estilo** | A4, márgenes 2,54 cm, Arial 11 pt, interlineado 1,5, justificado, APA 7.ª | **100% CUMPLE** |
| **01 // Portada Obligatoria** | Instituto, carrera, docente, ciclo 2026, datos de los 3 integrantes, versión. | **100% CUMPLE** |
| **02 // Índice y Organización** | Tabla de contenidos con puntos guía y saltos de página en cada sección principal. | **100% CUMPLE** |
| **03 // Base de Datos MySQL** | Tablas 3NF, DER Workbench, SP con `SIGNAL 45000`, vistas, función y trigger. | **100% CUMPLE** |
| **04 // Arquitectura y POO** | Diagrama UML, clase abstracta, justificación de polimorfismo y patrón DAO. | **100% CUMPLE** |
| **05 // Errores y Decisiones** | `Conexion.cs` con `using`, captura `MySqlException` (45000) y esquema JSON. | **100% CUMPLE** |
| **06 // Ejecución y Código** | Instrucciones XAMPP/Visual Studio y cajas de código monospace (`Consolas`). | **100% CUMPLE** |
| **07 // Cierre y Entrega** | Referencias APA 7 y PDF reglamentario `TP_Final_AlgoritmosII_Grupo2.pdf`. | **100% CUMPLE** |
