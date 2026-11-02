import os
import subprocess
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Colores sobrios y minimalistas (estricto blanco y negro / escala de grises segun pautas)
COLOR_BLACK = RGBColor(0x11, 0x11, 0x11)
COLOR_DARK_GRAY = RGBColor(0x22, 0x22, 0x22)
COLOR_MUTED_GRAY = RGBColor(0x55, 0x55, 0x55)
HEX_BORDER = "CCCCCC"
HEX_HEADER_BG = "F2F2F2"

def setup_document(doc):
    # Portada (Sección 1): Márgenes A4, SIN encabezado ni pie de página
    sec1 = doc.sections[0]
    sec1.page_width = Inches(8.27)   # A4: 210 mm
    sec1.page_height = Inches(11.69) # A4: 297 mm
    sec1.top_margin = Inches(1.0)    # 2.54 cm
    sec1.bottom_margin = Inches(1.0) # 2.54 cm
    sec1.left_margin = Inches(1.0)   # 2.54 cm
    sec1.right_margin = Inches(1.0)  # 2.54 cm
    sec1.different_first_page_header_footer = False
    sec1.footer.paragraphs[0].text = ""

    # Tipografía Arial 11 pt, interlineado 1.5, texto justificado según pautas
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_DARK_GRAY
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_after = Pt(4)

def start_body_section(doc, short_title):
    # Sección 2 para Índice y Contenido (comienza en página 2 con pie de página real al fondo)
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.0)
    sec2.right_margin = Inches(1.0)
    sec2.footer_distance = Inches(0.5)
    sec2.different_first_page_header_footer = False

    # Pie de página real anclado en la parte inferior
    sec2.footer.is_linked_to_previous = False
    p_ft = sec2.footer.paragraphs[0]
    p_ft.text = ""
    p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ft.paragraph_format.space_after = Pt(0)
    r_ft = p_ft.add_run(f"{short_title}  |  Pág. ")
    r_ft.font.name = 'Arial'
    r_ft.font.size = Pt(9)
    r_ft.font.color.rgb = COLOR_MUTED_GRAY

    fld_page = parse_xml(
        r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr><w:t>2</w:t></w:r></w:fldSimple>' % nsdecls('w')
    )
    p_ft._p.append(fld_page)

    # Tipografia Arial 11 pt, interlineado 1.5, texto justificado segun seccion 1 de Pautas
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_DARK_GRAY
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_after = Pt(4)

def set_cell_shading(cell, fill_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_padding(cell, top=50, bottom=50, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if i == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for j, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_padding(cell, top=45, bottom=45, left=90, right=90)
            if col_widths and j < len(col_widths):
                cell.width = col_widths[j]
            if i == 0:
                set_cell_shading(cell, HEX_HEADER_BG)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_after = Pt(0)
                    for run in p.runs:
                        run.font.name = 'Arial'
                        run.font.bold = True
                        run.font.size = Pt(9.0)
                        run.font.color.rgb = COLOR_BLACK
            else:
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_after = Pt(0)
                    for run in p.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(8.5)
                        run.font.color.rgb = COLOR_DARK_GRAY

def add_cover(doc, doc_title, doc_subtitle):
    # Logotipo corporativo centrado en la parte superior
    logo_path = os.path.abspath("src/Img/Logo/Logo_coWorking_para_fondo_blanco.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.abspath("src/Img/Logo/Logo_coWorking_con_lema_turquesa_y_blanco.png")

    p_logo = doc.add_paragraph()
    p_logo.paragraph_format.space_before = Pt(20)
    p_logo.paragraph_format.space_after = Pt(12)
    p_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(logo_path):
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(3.2))

    # Titulo principal del sistema
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("SISTEMA DE GESTIÓN DE COWORKING Y RESERVAS")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_BLACK

    # Titulo del documento especifico
    p_docname = doc.add_paragraph()
    p_docname.paragraph_format.space_before = Pt(8)
    p_docname.paragraph_format.space_after = Pt(4 if doc_subtitle else 20)
    p_docname.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_docname = p_docname.add_run(doc_title)
    r_docname.font.name = 'Arial'
    r_docname.font.size = Pt(13)
    r_docname.font.bold = True
    r_docname.font.color.rgb = COLOR_DARK_GRAY

    if doc_subtitle:
        p_subtitle = doc.add_paragraph()
        p_subtitle.paragraph_format.space_after = Pt(20)
        p_subtitle.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_subtitle = p_subtitle.add_run(doc_subtitle)
        r_subtitle.font.name = 'Arial'
        r_subtitle.font.size = Pt(10.5)
        r_subtitle.font.italic = True
        r_subtitle.font.color.rgb = COLOR_MUTED_GRAY

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(18)
    p_div.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("—" * 38)
    r_div.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)

    meta_items = [
        ("Producto", "Sistema de Gestión de Coworking y Reservas"),
        ("Desarrolladores", "Jonathan Lester Tullo, Maximiliano Scollo, David Samuel Ortega"),
        ("Versión", "1.0 (Versión Funcional)"),
        ("Año", "2026")
    ]
    for label, val in meta_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(0)
        p_item.paragraph_format.space_after = Pt(3)
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_lbl = p_item.add_run(f"{label}: ")
        r_lbl.font.name = 'Arial'
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(10)
        r_lbl.font.color.rgb = COLOR_BLACK

        r_val = p_item.add_run(val)
        r_val.font.name = 'Arial'
        r_val.font.size = Pt(10)
        r_val.font.color.rgb = COLOR_DARK_GRAY

def add_toc_header(doc):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = False
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run("ÍNDICE DE CONTENIDOS")
    run.font.name = 'Arial'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(8)
    r_div = p_div.add_run("—" * 38)
    r_div.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)

def add_toc(doc, items):
    add_toc_header(doc)
    target_right = Inches(6.00)
    for title, page_num, level in items:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2.5 if level == 1 else 1.5)
        p.paragraph_format.space_after = Pt(2.5 if level == 1 else 1.5)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

        indent = Inches(0)
        if level == 2:
            indent = Inches(0.22)
            p.paragraph_format.left_indent = indent

        # Tab stop nativo de python-docx con alineación derecha y puntos guía continuos
        p.paragraph_format.tab_stops.add_tab_stop(
            target_right + indent,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.DOTS
        )

        r1 = p.add_run(title)
        r1.font.name = 'Arial'
        r1.font.size = Pt(10.0 if level == 1 else 9.5)
        r1.font.bold = (level == 1)
        r1.font.color.rgb = COLOR_BLACK if level == 1 else COLOR_DARK_GRAY

        r_tab = p.add_run('\t')
        r_tab.font.name = 'Arial'

        r2 = p.add_run(str(page_num))
        r2.font.name = 'Arial'
        r2.font.size = Pt(10.0 if level == 1 else 9.5)
        r2.font.bold = (level == 1)
        r2.font.color.rgb = COLOR_BLACK if level == 1 else COLOR_DARK_GRAY

def add_h1(doc, text, page_break_before=False):
    # Seccion principal: 16 pt negrita segun pautas
    p = doc.add_paragraph()
    if page_break_before:
        p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK
    return p

def add_h2(doc, text):
    # Subseccion: 13 pt negrita segun pautas
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK
    return p

def add_h3(doc, text):
    # Tercer nivel: 11 pt negrita segun pautas
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_DARK_GRAY
    return p

def add_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Arial'
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_BLACK
    r_t = p.add_run(text)
    r_t.font.name = 'Arial'
    r_t.font.italic = italic
    r_t.font.color.rgb = COLOR_DARK_GRAY
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Arial'
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_BLACK
    r_t = p.add_run(text)
    r_t.font.name = 'Arial'
    r_t.font.color.rgb = COLOR_DARK_GRAY
    return p

def add_note_box(doc, text, bold_title="Nota importante: "):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_padding(cell, top=80, bottom=80, left=120, right=120)
    set_cell_shading(cell, "F7F7F7")
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="333333"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p.add_run(bold_title)
    r1.font.name = 'Arial'
    r1.font.bold = True
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = COLOR_BLACK
    r2 = p.add_run(text)
    r2.font.name = 'Arial'
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = COLOR_DARK_GRAY
    doc.add_paragraph().paragraph_format.space_after = Pt(1)

def save_doc_safely(doc, base_name):
    target_path = os.path.join("Documentacion", f"{base_name}.docx")
    try:
        doc.save(target_path)
        print(f"Guardado exitosamente: {target_path}")
    except PermissionError:
        alt_path = os.path.join("Documentacion", f"{base_name}_Nuevo.docx")
        doc.save(alt_path)
        print(f"Aviso: {target_path} está abierto en Word. Guardado como alternativa en: {alt_path}")


# =============================================================================
# 1. DOCUMENTACIÓN DEL DESARROLLO (Conforme a Consignas de la Cátedra)
# =============================================================================
def generate_desarrollo():
    doc = Document()
    setup_document(doc)
    add_cover(doc, "DOCUMENTACIÓN DEL DESARROLLO", "Explicación Técnica del Sistema, Arquitectura y POO")
    start_body_section(doc, "Documentación del Desarrollo")

    desarrollo_toc = [
        ("1. Objetivo y Descripción del Sistema", "3", 1),
        ("2. Tecnologías, Herramientas y Lenguajes Utilizados", "3", 1),
        ("3. Organización del Trabajo en Equipo", "4", 1),
        ("4. Arquitectura del Sistema por Capas", "4", 1),
        ("4.1. Capa de Presentación (Windows Forms)", "4", 2),
        ("4.2. Capa de Negocio (Gestoras y Reglas)", "4", 2),
        ("4.3. Capa de Modelos (Entidades de Dominio)", "4", 2),
        ("4.4. Capa de Conexión (ConexionDB)", "4", 2),
        ("4.5. Capa de Persistencia (MySQL)", "4", 2),
        ("5. Programación Orientada a Objetos y Clases C#", "5", 1),
        ("5.1. Conexión centralizada (Conexion.cs)", "5", 2),
        ("5.2. Interfaz de disponibilidad (IReservable.cs)", "5", 2),
        ("5.3. Enumerador de estado (EstadoReserva.cs)", "5", 2),
        ("5.4. Clase base abstracta (Recurso.cs)", "5", 2),
        ("5.5. Herencia y Polimorfismo (Sala, Oficina, Puesto)", "5", 2),
        ("5.6. Clases de negocio (Cliente.cs y Reserva.cs)", "6", 2),
        ("5.7. Gestión en memoria y persistencia (Gestora / DAO)", "6", 2),
        ("6. Manejo de Errores y Excepciones (MySQL + C#)", "6", 1),
        ("7. Estado Actual de Avance y Requerimientos Evolutivos", "7", 1),
        ("8. Instrucciones para la Ejecución del Proyecto", "7", 1),
    ]
    add_toc(doc, desarrollo_toc)

    # 1. Objetivo
    add_h1(doc, "1. Objetivo y Descripción del Sistema", page_break_before=True)
    add_p(doc,
        "Este proyecto consiste en el desarrollo de una aplicación de escritorio programada en C# con Windows Forms, conectada de manera centralizada a una base de datos MySQL alojada en el entorno de XAMPP. "
        "El objetivo principal es administrar de forma integral un espacio de coworking, permitiendo la gestión de clientes, el catálogo de recursos alquilables (salas de reunión, oficinas privadas y puestos de trabajo) y el control de reservas por fecha y horario."
    )
    add_p(doc,
        "El sistema resuelve los problemas operativos fundamentales del negocio: asegura que no existan reservas duplicadas para un mismo recurso en el mismo horario mediante validaciones estrictas en la base de datos, calcula automáticamente los costos de alquiler aplicando tarifas base y recargos por comodidades, y mantiene un registro automático de auditoría para cada cancelación."
    )

    # 2. Tecnologias y Lenguajes
    add_h1(doc, "2. Tecnologías, Herramientas y Lenguajes Utilizados", page_break_before=False)
    add_p(doc,
        "La solución se apoya en un stack tecnológico moderno, robusto y estandarizado para entornos de escritorio:"
    )
    add_bullet(doc, "Lenguaje principal orientado a objetos con tipado estático, herencia, interfaces, colecciones genéricas y LINQ.", bold_prefix="C# (.NET Framework 4.7.2): ")
    add_bullet(doc, "Framework para la interfaz gráfica de usuario en Windows (formularios FrmLogin y FrmPrincipal con DataGridView, ComboBox y TabControl).", bold_prefix="Windows Forms (WinForms): ")
    add_bullet(doc, "Motor relacional para la persistencia centralizada en localhost:3306 (integridad referencial, vistas, triggers de auditoría, funciones y procedimientos almacenados con SIGNAL 45000).", bold_prefix="MySQL / MariaDB (v10.4+ en XAMPP): ")
    add_bullet(doc, "Controlador oficial de Oracle para ADO.NET (v9.5.0), que administra las conexiones MySqlConnection y comandos MySqlCommand.", bold_prefix="MySql.Data: ")
    add_bullet(doc, "Entorno de desarrollo integrado utilizado para la compilación, diseño visual, gestión de dependencias NuGet y depuración del código.", bold_prefix="Microsoft Visual Studio 2022: ")
    add_bullet(doc, "Sistema de control de versiones distribuido y plataforma en la nube para el trabajo coordinado en equipo y control de cambios.", bold_prefix="Git y GitHub: ")
    add_bullet(doc, "Herramientas visuales de administración para la ejecución del script SQL (DB_TPFinal.sql) y verificación de datos.", bold_prefix="MySQL Workbench y phpMyAdmin: ")
    add_bullet(doc, "Protocolo URI de enlace directo (wa.me) para derivar consultas técnicas a la línea de soporte del coworking.", bold_prefix="WhatsApp API / Web: ")

    # 3. Organización
    add_h1(doc, "3. Organización del Trabajo en Equipo", page_break_before=False)
    add_p(doc,
        "El desarrollo del proyecto se organizó de manera modular entre los tres integrantes del equipo, coordinando cambios mediante control de versiones en Git/GitHub y documentando cada etapa técnica:"
    )
    add_bullet(doc, "Diseño y creación de la base de datos MySQL en XAMPP (tablas, relaciones, procedimientos almacenados, vistas, funciones y trigger). Creación de la solución base en Visual Studio, instalación de dependencias NuGet (MySql.Data), programación de la clase centralizada Conexion.cs y diseño de la clase abstracta base Recurso.cs junto con la interfaz IReservable.cs.", bold_prefix="Jonathan Lester Tullo (shonimdp@gmail.com): ")
    add_bullet(doc, "Programación de las clases derivadas (Sala.cs, OficinaPrivada.cs y PuestoTrabajo.cs) implementando el cálculo polimórfico de costos y disponibilidad. Implementación de los modelos Cliente.cs y Reserva.cs, programación de la clase GestoraCoworking.cs con colecciones en memoria y actualización del diagrama Entidad-Relación (DER).", bold_prefix="Maximiliano Scollo (maximilianoscollo17@gmail.com): ")
    add_bullet(doc, "Diseño completo de la interfaz de usuario en Windows Forms, desarrollo del formulario de autenticación (FrmLogin) con control de credenciales y asistencia técnica vía WhatsApp, preparación de recursos gráficos y maquetado del formulario principal (FrmPrincipal) con solapas para Control, Reservas y Gestión administrativa.", bold_prefix="David Samuel Ortega (davidortegaa86@gmail.com): ")

    # 4. Arquitectura
    add_h1(doc, "4. Arquitectura del Sistema por Capas", page_break_before=False)
    add_p(doc,
        "Para garantizar la separación de responsabilidades y evitar que los formularios concentren toda la lógica del sistema, la aplicación se organizó en las siguientes capas:"
    )
    add_bullet(doc, "Formularios FrmLogin y FrmPrincipal. Su función es interactuar con el usuario, capturar eventos, validar entradas y presentar la información en controles adecuados (DataGridView, ComboBox, DateTimePicker).", bold_prefix="4.1. Capa de Presentación (Windows Forms): ")
    add_bullet(doc, "La clase GestoraCoworking.cs administra las listas en memoria y coordina las reglas del negocio, aplicando búsquedas y filtrados de reservas por fecha, cliente o estado.", bold_prefix="4.2. Capa de Negocio (Gestoras y Reglas): ")
    add_bullet(doc, "Representan las entidades del dominio de la aplicación: Cliente, Reserva, Recurso y sus clases derivadas especializadas.", bold_prefix="4.3. Capa de Modelos (Entidades de Dominio): ")
    add_bullet(doc, "La clase estática Conexion.cs centraliza los parámetros de conexión hacia el servidor MySQL en localhost:3306, entregando conexiones que se abren puntualmente bajo bloques using.", bold_prefix="4.4. Capa de Conexión (ConexionDB): ")
    add_bullet(doc, "La base de datos MySQL asegura la consistencia de los datos en disco, encapsulando operaciones críticas mediante procedimientos almacenados, funciones de verificación y triggers de auditoría.", bold_prefix="4.5. Capa de Persistencia (MySQL): ")

    # Imagen del Diagrama Conceptual de Bloques
    p_img = doc.add_paragraph()
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    der_borrador_path = os.path.abspath("DB/Diagrama_DER_Borrador.png")
    if os.path.exists(der_borrador_path):
        r_img = p_img.add_run()
        r_img.add_picture(der_borrador_path, width=Inches(5.4))
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figura 1: Diagrama Conceptual y Bloques del Sistema (Borrador)")
    r_cap.font.name = 'Arial'
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_MUTED_GRAY

    # 5. POO
    add_h1(doc, "5. Programación Orientada a Objetos y Clases C#", page_break_before=False)
    add_p(doc,
        "A continuación se detallan las decisiones de diseño adoptadas en la implementación orientada a objetos:"
    )

    add_h2(doc, "5.1. Conexión centralizada (Conexion.cs)")
    add_p(doc,
        "La clase Conexion es de tipo static porque no representa una entidad del negocio sino un servicio utilitario de infraestructura. "
        "Su método CrearConexion() entrega una instancia configurada de MySqlConnection pero no ejecuta .Open() de forma anticipada. Cada formulario o método abre la conexión cuando la requiere mediante la instrucción using, garantizando que los recursos se liberen inmediatamente al concluir la operación."
    )

    add_h2(doc, "5.2. Interfaz de disponibilidad (IReservable.cs)")
    add_p(doc,
        "Define el contrato bool PuedeReservarse(DateTime fecha). "
        "El uso de una interfaz permite desacoplar la capacidad de reserva de la jerarquía de herencia: cualquier elemento presente o futuro del coworking que deba verificar disponibilidad implementa este contrato sin requerir modificaciones en el resto del sistema."
    )

    add_h2(doc, "5.3. Enumerador de estado (EstadoReserva.cs)")
    add_p(doc,
        "Contiene los valores tipados: Pendiente, Confirmada y Cancelada. "
        "Evita el uso de cadenas de texto literales en el código fuente, previniendo errores de tipeo y asegurando compatibilidad con la columna VARCHAR de la base de datos mediante .ToString()."
    )

    add_h2(doc, "5.4. Clase base abstracta (Recurso.cs)")
    add_p(doc,
        "Recurso es una clase abstracta porque en el dominio del problema no se reservan recursos genéricos, sino tipos específicos de espacios. "
        "Reúne los atributos y propiedades comunes (IdRecurso, Nombre, Descripcion, Ubicacion, PrecioPorHora, IdTipoRecurso) y define la firma abstracta CalcularCosto(int horas), forzando a que cada clase derivada implemente su propia regla de facturación."
    )

    add_h2(doc, "5.5. Herencia y Polimorfismo (Sala, Oficina, Puesto)")
    add_p(doc, "Las clases derivadas especializan el comportamiento base incorporando características propias:")
    add_bullet(doc, "Incorpora la propiedad CantSillas. En CalcularCosto, multiplica la tarifa base por las horas y añade un adicional por mantenimiento ($8.000 para salas de más de 30 sillas y $16.000 para más de 60).", bold_prefix="Sala: ")
    add_bullet(doc, "Incorpora la propiedad booleana MobiliarioIncluido. Si la oficina cuenta con equipamiento completo, añade un adicional fijo de $1.500 al valor del alquiler.", bold_prefix="OficinaPrivada: ")
    add_bullet(doc, "Incorpora la propiedad NroCategoria (1, 2 o 3). Aplica un plus tarifario según el nivel de comodidades del box ($3.500 para categoría 1, $5.500 para categoría 2 y $8.000 para categoría 3).", bold_prefix="PuestoTrabajo: ")

    add_h2(doc, "5.6. Clases de negocio (Cliente.cs y Reserva.cs)")
    add_p(doc,
        "Cliente modela los datos del usuario (IdCliente, Nombre, Apellido, Telefono, Mail, FechaRegistro).\n"
        "Reserva actúa como entidad relacional que vincula al cliente con el recurso, la fecha y hora asignadas, la duración, el total calculado y el estado correspondiente."
    )

    add_h2(doc, "5.7. Gestión en memoria y persistencia (Gestora / DAO)")
    add_p(doc,
        "GestoraCoworking administra colecciones genéricas List<Reserva> en memoria para realizar consultas, modificaciones y cancelaciones. "
        "En una etapa evolutiva posterior, las operaciones de persistencia serán trasladadas progresivamente a clases específicas de acceso a datos (GestorDAO) para completar el desacoplamiento total de los formularios."
    )

    add_h1(doc, "6. Manejo de Errores y Excepciones (MySQL + C#)", page_break_before=False)
    add_p(doc,
        "Para salvaguardar la consistencia en operaciones críticas de base de datos, el sistema implementa una doble estrategia de control de excepciones:"
    )
    add_bullet(doc, "El procedimiento almacenado sp_alta_reserva evalúa mediante fn_verificar_disponibilidad si el recurso se encuentra ocupado calculando el intervalo exacto (fecha y duración en horas). De existir superposición horaria, la base interrumpe la transacción ejecutando SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El recurso ya se encuentra reservado u ocupado en ese intervalo de horario.', impidiendo la inserción de registros duplicados o solapados.", bold_prefix="1. Validación en Base de Datos: ")
    add_bullet(doc, "En el código C#, las llamadas a MySQL se protegen mediante bloques catch (MySqlException ex). La aplicación examina si ex.SqlState == \"45000\" para capturar el error de negocio y presentar al usuario un mensaje informativo claro en pantalla, diferenciándolo de fallas de infraestructura o red.", bold_prefix="2. Captura Específica en C#: ")
    add_bullet(doc, "Se incorpora un bloque secundario catch (Exception ex) para capturar cualquier anomalía no prevista, evitando en todos los casos el uso de bloques catch vacíos.", bold_prefix="3. Errores Generales: ")

    add_h1(doc, "7. Estado Actual de Avance y Requerimientos Evolutivos", page_break_before=False)
    add_p(doc,
        "Conforme al desarrollo progresivo por etapas planificado para el sistema:"
    )
    add_bullet(doc, "Base de datos MySQL completa con integridad referencial, procedimientos almacenados, vistas, función de verificación y trigger de auditoría. Modelos C# completos con herencia, clases abstractas, interfaces y polimorfismo. Formularios Windows Forms funcionales con autenticación de usuarios, roles de acceso y disposición visual terminada.", bold_prefix="Etapas Implementadas (1 a 4): ")
    add_bullet(doc, "Separación definitiva de clases DAO de acceso a datos (Etapa 5), incorporación de importación/exportación de catálogos y reservas en formato JSON y configuración externa de la cadena de conexión (Etapa 6).", bold_prefix="Etapas Evolutivas Planificadas (5 y 6): ")

    add_h1(doc, "8. Instrucciones para la Ejecución del Proyecto", page_break_before=False)
    add_p(doc,
        "Para ejecutar la aplicación en un entorno de desarrollo o prueba local:"
    )
    add_bullet(doc, "Iniciar el panel de XAMPP y activar el servicio MySQL en el puerto 3306.", bold_prefix="1. Servidor de Base de Datos: ")
    add_bullet(doc, "Abrir MySQL Workbench o phpMyAdmin y ejecutar el script ubicado en DB/DB_TPFinal.sql. Esto creará la base de datos tp_final_db junto con sus tablas, vistas, funciones, procedimientos y datos iniciales de prueba.", bold_prefix="2. Carga de la Base: ")
    add_bullet(doc, "Abrir la solución SistemaDeGestion.slnx en Visual Studio 2022, verificar que las referencias NuGet a MySql.Data se encuentren resueltas y presionar F5 (Iniciar depuración).", bold_prefix="3. Compilación y Ejecución: ")

    save_doc_safely(doc, "Documentacion_Desarrollo")


# =============================================================================
# 2. DICCIONARIO DE DATOS (Conforme a Pautas y A4)
# =============================================================================
def generate_diccionario():
    doc = Document()
    setup_document(doc)
    add_cover(doc, "DICCIONARIO DE DATOS", "Estructura de la Base de Datos MySQL")
    start_body_section(doc, "Diccionario de Datos")

    diccionario_toc = [
        ("1. Información General de la Base de Datos", "3", 1),
        ("2. Tabla: tipo_recursos (Categorías)", "3", 1),
        ("3. Tabla: recursos (Espacios físicos y tarifas)", "3", 1),
        ("4. Tabla: clientes (Datos de contacto)", "4", 1),
        ("5. Tabla: reservas (Tabla Intermedia / Pivote)", "4", 1),
        ("6. Tabla: auditoria_reservas (Registro histórico)", "5", 1),
        ("7. Claves Foráneas y Relaciones entre Tablas", "5", 1),
        ("8. Vistas del Sistema", "5", 1),
        ("9. Funciones Almacenadas", "6", 1),
        ("10. Procedimientos Almacenados (Stored Procedures)", "6", 1),
        ("11. Trigger de Auditoría Automática", "6", 1),
    ]
    add_toc(doc, diccionario_toc)

    headers = ["Nombre del Campo", "Tipo de Dato", "Nulo", "Clave", "Descripción"]

    # 1. Info general
    add_h1(doc, "1. Información General de la Base de Datos", page_break_before=True)
    add_p(doc,
        "La base de datos del sistema se encuentra alojada en un servidor MySQL/MariaDB bajo el entorno de XAMPP. "
        "El archivo de creación completo con datos de ejemplo se encuentra en la carpeta DB/ (DB_TPFinal.sql). "
        "A continuación se presenta el esquema conceptual de bloques y el detalle de cada tabla que compone la persistencia:"
    )

    p_img = doc.add_paragraph()
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    der_borrador_path = os.path.abspath("DB/Diagrama_DER_Borrador.png")
    if os.path.exists(der_borrador_path):
        r_img = p_img.add_run()
        r_img.add_picture(der_borrador_path, width=Inches(5.4))
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figura 1: Diagrama Conceptual y Bloques de Entidades (Borrador)")
    r_cap.font.name = 'Arial'
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_MUTED_GRAY

    # 2. tipo_recursos
    add_h1(doc, "2. Tabla: tipo_recursos", page_break_before=False)
    add_p(doc, "Almacena las categorías generales de los lugares que se pueden alquilar (ejemplos: Sala de Reuniones, Oficina Privada o Puesto de Trabajo).")
    t1 = doc.add_table(rows=3, cols=5)
    for j, h in enumerate(headers):
        t1.cell(0, j).paragraphs[0].text = h
    t1_data = [
        ["id_tipo_recurso", "INT", "NO", "PK (Auto Inc)", "Identificador numérico único de la categoría."],
        ["nombre_tipo", "VARCHAR(100)", "NO", "Ninguna", "Nombre de la categoría del espacio físico."]
    ]
    for i, row in enumerate(t1_data):
        for j, val in enumerate(row):
            t1.cell(i+1, j).paragraphs[0].text = val
    format_table(t1, [Inches(1.4), Inches(0.9), Inches(0.55), Inches(1.1), Inches(2.3)])

    # 3. recursos
    add_h1(doc, "3. Tabla: recursos", page_break_before=False)
    add_p(doc, "Contiene cada espacio físico específico que se puede alquilar, indicando su tarifa, ubicación y comodidades particulares.")
    t2 = doc.add_table(rows=10, cols=5)
    for j, h in enumerate(headers):
        t2.cell(0, j).paragraphs[0].text = h
    t2_data = [
        ["id_recurso", "INT", "NO", "PK (Auto Inc)", "Identificador numérico único de la sala, oficina o puesto."],
        ["nombre", "VARCHAR(100)", "NO", "Ninguna", "Nombre del lugar (ejemplo: 'Sala Innovación', 'Box 1')."],
        ["descripcion", "TEXT", "SÍ", "Ninguna", "Detalle de lo que incluye (pizarra, televisor, proyector)."],
        ["ubicacion", "VARCHAR(100)", "NO", "Ninguna", "Ubicación física dentro del edificio (ejemplo: 'Piso 1 - Sector A')."],
        ["precio_por_hora", "DECIMAL(10,2)", "NO", "Ninguna", "Precio base que se cobra por cada hora de uso."],
        ["mobiliario_incluido", "BOOLEAN", "SÍ", "Ninguna", "Aplica a oficinas: indica si incluye muebles o viene vacía."],
        ["cantidad_sillas", "INT", "SÍ", "Ninguna", "Aplica a salas: cantidad total de sillas disponibles."],
        ["nro_categoria", "INT", "SÍ", "Ninguna", "Aplica a puestos: nivel o categoría del box de trabajo (1, 2 o 3)."],
        ["id_tipo_recurso", "INT", "NO", "FK", "Apunta a tipo_recursos (indica qué clase de lugar es)."]
    ]
    for i, row in enumerate(t2_data):
        for j, val in enumerate(row):
            t2.cell(i+1, j).paragraphs[0].text = val
    format_table(t2, [Inches(1.4), Inches(0.9), Inches(0.55), Inches(1.1), Inches(2.3)])

    # 4. clientes
    add_h1(doc, "4. Tabla: clientes", page_break_before=False)
    add_p(doc, "Guarda la información de las personas que realizan alquileres en el coworking.")
    t3 = doc.add_table(rows=7, cols=5)
    for j, h in enumerate(headers):
        t3.cell(0, j).paragraphs[0].text = h
    t3_data = [
        ["id_cliente", "INT", "NO", "PK (Auto Inc)", "Identificador numérico único del cliente."],
        ["nombre", "VARCHAR(100)", "NO", "Ninguna", "Nombre de pila del cliente."],
        ["apellido", "VARCHAR(100)", "NO", "Ninguna", "Apellido del cliente."],
        ["telefono", "VARCHAR(20)", "NO", "Ninguna", "Teléfono para comunicarse con la persona."],
        ["mail", "VARCHAR(255)", "NO", "Ninguna", "Correo electrónico para confirmaciones y avisos."],
        ["fecha_registro", "DATETIME", "NO", "Default Now", "Fecha y hora en que se dio de alta al cliente en el sistema."]
    ]
    for i, row in enumerate(t3_data):
        for j, val in enumerate(row):
            t3.cell(i+1, j).paragraphs[0].text = val
    format_table(t3, [Inches(1.4), Inches(0.9), Inches(0.55), Inches(1.1), Inches(2.3)])

    # 5. reservas
    add_h1(doc, "5. Tabla: reservas (Tabla Intermedia / Pivote)", page_break_before=False)
    add_p(doc,
        "Es la tabla central del sistema. Une al cliente con el recurso contratado en una fecha y horario determinado. "
        "Representa una relación de muchos a muchos entre clientes y recursos."
    )
    t4 = doc.add_table(rows=8, cols=5)
    for j, h in enumerate(headers):
        t4.cell(0, j).paragraphs[0].text = h
    t4_data = [
        ["id_reserva", "INT", "NO", "PK (Auto Inc)", "Identificador numérico único de la reserva."],
        ["id_cliente", "INT", "NO", "FK", "Apunta a la tabla clientes (quién alquila)."],
        ["id_recurso", "INT", "NO", "FK", "Apunta a la tabla recursos (qué espacio alquiló)."],
        ["fecha_reserva", "DATETIME", "NO", "Ninguna", "Día y hora exactos para los que se reservó el lugar."],
        ["horas", "INT", "NO", "Default 1", "Cantidad de horas que dura el alquiler."],
        ["total", "DECIMAL(10,2)", "NO", "Ninguna", "Precio final calculado que debe abonar el cliente."],
        ["estado", "VARCHAR(20)", "NO", "Default Conf", "Estado de la reserva: 'Confirmada', 'Cancelada' o 'Pendiente'."]
    ]
    for i, row in enumerate(t4_data):
        for j, val in enumerate(row):
            t4.cell(i+1, j).paragraphs[0].text = val
    format_table(t4, [Inches(1.4), Inches(0.9), Inches(0.55), Inches(1.1), Inches(2.3)])

    # 6. auditoria_reservas
    add_h1(doc, "6. Tabla: auditoria_reservas", page_break_before=False)
    add_p(doc, "Tabla de control histórico. Se registra de manera automática mediante un trigger cuando alguien cancela una reserva.")
    t5 = doc.add_table(rows=6, cols=5)
    for j, h in enumerate(headers):
        t5.cell(0, j).paragraphs[0].text = h
    t5_data = [
        ["id_auditoria", "INT", "NO", "PK (Auto Inc)", "Identificador único del registro de auditoría."],
        ["id_reserva", "INT", "NO", "Ninguna", "Número de la reserva que fue cancelada."],
        ["accion", "VARCHAR(50)", "NO", "Ninguna", "Descripción del suceso ('Cancelacion de reserva')."],
        ["fecha_accion", "DATETIME", "NO", "Default Now", "Momento exacto en que se produjo la cancelación."],
        ["usuario", "VARCHAR(100)", "SÍ", "Default Sist", "Usuario que ejecutó la operación (por defecto 'Sistema')."]
    ]
    for i, row in enumerate(t5_data):
        for j, val in enumerate(row):
            t5.cell(i+1, j).paragraphs[0].text = val
    format_table(t5, [Inches(1.4), Inches(0.9), Inches(0.55), Inches(1.1), Inches(2.3)])

    # 7. Relaciones
    add_h1(doc, "7. Claves Foráneas y Relaciones entre Tablas", page_break_before=False)
    add_bullet(doc, "fk_recursos_tipo: Conecta recursos.id_tipo_recurso con tipo_recursos.id_tipo_recurso. No permite crear un recurso si no existe su categoría.", bold_prefix="fk_recursos_tipo: ")
    add_bullet(doc, "fk_reservas_cliente: Conecta reservas.id_cliente con clientes.id_cliente. Impide crear reservas para clientes inexistentes.", bold_prefix="fk_reservas_cliente: ")
    add_bullet(doc, "fk_reservas_recurso: Conecta reservas.id_recurso con recursos.id_recurso. Impide reservar un espacio que no existe en el catálogo.", bold_prefix="fk_reservas_recurso: ")

    # 8. Vistas
    add_h1(doc, "8. Vistas del Sistema", page_break_before=False)
    add_bullet(doc, "Combina las tablas reservas, clientes y recursos usando INNER JOIN. Muestra el nombre completo del cliente, correo, nombre del espacio, horas y estado, evitando tener que ver códigos numéricos.", bold_prefix="1. vw_detalle_reservas: ")
    add_bullet(doc, "Agrupa por cada recurso y calcula cuántas reservas confirmadas tuvo y cuánta plata total recaudó cada uno, usando sumas condicionales y GROUP BY.", bold_prefix="2. vw_resumen_recursos: ")

    # 9. Funciones
    add_h1(doc, "9. Funciones Almacenadas", page_break_before=False)
    add_p(doc,
        "fn_verificar_disponibilidad(p_id_recurso, p_fecha, p_horas): Recibe el ID del recurso, la fecha/hora de inicio y la duración en horas. "
        "Evalúa matemáticamente si existe solapamiento temporal ((nuevo_inicio < fin_existente) AND (nuevo_fin > inicio_existente)) frente a reservas confirmadas. "
        "Devuelve 1 si el espacio está libre durante todo el intervalo y 0 si existe superposición horaria."
    )

    # 10. Procedimientos
    add_h1(doc, "10. Procedimientos Almacenados (Stored Procedures)", page_break_before=False)
    add_bullet(doc, "Inserta un nuevo cliente con nombre, apellido, teléfono y mail.", bold_prefix="sp_alta_cliente: ")
    add_bullet(doc, "Busca a un cliente por su ID y actualiza sus datos de contacto.", bold_prefix="sp_modificar_cliente: ")
    add_bullet(doc, "Registra un nuevo espacio físico guardando nombre, precio y características.", bold_prefix="sp_alta_recurso: ")
    add_bullet(doc, "Actualiza los datos, ubicación o precios de un recurso existente.", bold_prefix="sp_modificar_recurso: ")
    add_bullet(doc, "Valida horas > 0, importe y existencia de cliente/recurso. Evalúa solapamiento de horarios mediante fn_verificar_disponibilidad y si el espacio está ocupado interrumpe la operación con SIGNAL SQLSTATE '45000'.", bold_prefix="sp_alta_reserva (Con SIGNAL 45000): ")
    add_bullet(doc, "Permite reprogramar fecha u horario de una reserva existente verificando disponibilidad frente a las demás reservas confirmadas.", bold_prefix="sp_modificar_reserva: ")
    add_bullet(doc, "Cambia el estado de una reserva a 'Cancelada'. Si la reserva no existe o ya estaba cancelada, emite alerta con SIGNAL 45000.", bold_prefix="sp_cancelar_reserva: ")
    add_bullet(doc, "Utiliza un CURSOR de MySQL para recorrer fila por fila todas las reservas confirmadas, acumulando los importes para devolver el monto total general recaudado.", bold_prefix="sp_calcular_total_recaudado_cursor (Cursor): ")

    # 11. Trigger
    add_h1(doc, "11. Trigger de Auditoría Automática", page_break_before=False)
    add_p(doc,
        "trg_auditoria_reservas: Disparador AFTER UPDATE sobre la tabla reservas. "
        "Compara si el nuevo estado es 'Cancelada' y el anterior no lo era. "
        "Si se cumple la condición, inserta automáticamente una fila en auditoria_reservas con el ID de la reserva, "
        "fecha y hora actual del sistema y el usuario que lo realizó."
    )

    save_doc_safely(doc, "Diccionario_de_Datos")


# =============================================================================
# 3. MANUAL DE USUARIO (Conforme a Pautas y A4)
# =============================================================================
def generate_manual():
    doc = Document()
    setup_document(doc)
    add_cover(doc, "MANUAL DE USUARIO", "")
    start_body_section(doc, "Manual de Usuario")

    manual_toc = [
        ("1. Requisitos previos para encender el sistema", "3", 1),
        ("2. Pantalla de Inicio de Sesión", "3", 1),
        ("2.1. Credenciales de acceso de Administrador", "3", 2),
        ("2.2. Control y validación de errores", "3", 2),
        ("2.3. Asistencia técnica y soporte por WhatsApp", "3", 2),
        ("3. Pantalla Principal del Sistema - Modo Operativo", "4", 1),
        ("3.1. Solapa 'CONTROL' (Crear una nueva reserva)", "4", 2),
        ("3.2. Solapa 'RESERVAS' (Consultar y cancelar reservas)", "4", 2),
        ("4. Modo Administrador (Solapa 'GESTIÓN')", "5", 1),
        ("4.1. Ingreso y desbloqueo de solapa de gestión", "5", 2),
        ("4.2. Alternancia rápida entre grilla de Usuarios y Recursos", "5", 2),
        ("4.3. Botones de acción (Crear, Modificar, Eliminar)", "5", 2),
        ("4.4. Cierre de sesión y protección de datos", "5", 2),
        ("5. Estado actual del proyecto y próximas etapas", "5", 1),
    ]
    add_toc(doc, manual_toc)

    # 1. Requisitos
    add_h1(doc, "1. Requisitos previos para encender el sistema", page_break_before=True)
    add_p(doc, "Antes de iniciar el programa en la computadora, se debe verificar lo siguiente:")
    add_bullet(doc, "Abrir el panel de control de XAMPP y hacer clic en 'Start' en el módulo de MySQL. Debe aparecer en color verde y con el puerto 3306 activo.", bold_prefix="Paso 1: ")
    add_bullet(doc, "Abrir phpMyAdmin o MySQL Workbench y ejecutar por única vez el script de creación ubicado en la carpeta DB/ (DB_TPFinal.sql) para crear la base de datos con las tablas y datos de prueba.", bold_prefix="Paso 2: ")
    add_bullet(doc, "Abrir la solución SistemaDeGestion.slnx en Visual Studio y presionar F5 (o hacer doble clic en el archivo .exe compilado).", bold_prefix="Paso 3: ")

    # 2. Login
    add_h1(doc, "2. Pantalla de Inicio de Sesión", page_break_before=False)
    add_p(doc,
        "Al iniciar el sistema o al seleccionar la opción de entrar como administrador desde el menú superior, se despliega la pantalla de acceso del sistema:"
    )

    add_h2(doc, "2.1. Credenciales de acceso de Administrador")
    add_p(doc,
        "El sistema cuenta con dos niveles de uso: el uso operativo regular (para registrar o consultar reservas) y el nivel de administración (para gestionar el catálogo de recursos y clientes). "
        "Para ingresar con permisos administrativos completos, se deben ingresar las siguientes credenciales en los casilleros de acceso:"
    )
    add_bullet(doc, "Escribir la palabra Admin (sin comillas ni espacios adicionales).", bold_prefix="Casilla 'Usuario': ")
    add_bullet(doc, "Escribir la clave 123456. Por motivos de seguridad, los caracteres se mostrarán protegidos con puntos o asteriscos mientras se escriben.", bold_prefix="Casilla 'Contraseña': ")
    add_p(doc, "Al hacer clic en el botón 'Ingresar', el sistema valida la información y muestra un mensaje de bienvenida, habilitando el acceso a las funciones completas.")

    add_h2(doc, "2.2. Control y validación de errores")
    add_p(doc,
        "Si los datos ingresados no coinciden con las credenciales registradas, el sistema muestra un cartel de advertencia claro para guiar al operador: "
        "'El Usuario es incorrecto' o 'La Contraseña es incorrecta'. "
        "De forma automática, el cursor se posiciona en el casillero correspondiente para que el operador pueda corregir el dato rápidamente sin tener que borrar todo de nuevo."
    )

    add_h2(doc, "2.3. Asistencia técnica y soporte por WhatsApp")
    add_p(doc,
        "Dado que el sistema no cuenta con un módulo de recuperación automática por correo electrónico (priorizando una operación sencilla, ágil y sin dependencias de servidores de correo externos), el restablecimiento de claves y la asistencia técnica se gestionan de forma directa a través de soporte."
    )
    add_p(doc,
        "En la parte inferior de la pantalla de inicio de sesión se encuentra el enlace interactivo: '¿Necesitas ayuda? Contactar soporte'. "
        "Al hacer clic sobre él, el sistema abre automáticamente la aplicación de WhatsApp o el navegador web con un mensaje preconfigurado dirigido a la línea de soporte técnico:"
    )
    add_bullet(doc, "+54 9 223 301-4626 (atención técnica directa).", bold_prefix="Línea de WhatsApp oficial: ")
    add_bullet(doc, "\"Hola, soy usuario de CoWorking, me contacto para pedir asesoramiento con respecto al usuario y la contraseña, ¡muchas gracias!\"", bold_prefix="Mensaje predeterminado: ")
    add_p(doc,
        "En caso de querer contactarse directamente con el equipo de desarrollo para solicitar o restablecer credenciales, asistencia o consultas técnicas, se encuentran disponibles las siguientes casillas de correo electrónico:"
    )
    add_bullet(doc, "shonimdp@gmail.com", bold_prefix="Jonathan Lester Tullo: ")
    add_bullet(doc, "davidortegaa86@gmail.com", bold_prefix="David Samuel Ortega: ")
    add_bullet(doc, "maximilianoscollo17@gmail.com", bold_prefix="Maximiliano Scollo: ")

    # 3. Principal
    add_h1(doc, "3. Pantalla Principal del Sistema - Modo Operativo", page_break_before=False)
    add_p(doc,
        "Cuando una persona abre el sistema sin ingresar como administrador, la pantalla principal le muestra las solapas operativas habilitadas para la jornada regular:"
    )

    add_h2(doc, "3.1. Solapa 'CONTROL' (Crear una nueva reserva)")
    add_p(doc, "Esta solapa permite ingresar una reserva en el momento:")
    add_bullet(doc, "Menú desplegable donde se selecciona qué cliente está realizando el alquiler.", bold_prefix="Selector de Cliente: ")
    add_bullet(doc, "Menú desplegable para elegir si alquila una Sala de Reuniones, una Oficina Privada o un Puesto de Trabajo.", bold_prefix="Tipo de Recurso: ")
    add_bullet(doc, "Permite seleccionar en un calendario interactivo el día y la hora de inicio del alquiler.", bold_prefix="Selector de Fecha: ")
    add_bullet(doc, "Casilla numérica con flechitas para indicar cuántas horas durará el uso del espacio.", bold_prefix="Selector de Horas: ")
    add_bullet(doc, "Muestra el importe total a cobrar según el recurso elegido y sus comodidades.", bold_prefix="Visor de Total: ")
    add_bullet(doc, "El botón 'Agregar' registra la reserva, mientras que el botón 'Cancelar' limpia los campos para empezar de nuevo.", bold_prefix="Botones Agregar y Cancelar: ")

    add_h2(doc, "3.2. Solapa 'RESERVAS' (Consultar y cancelar reservas)")
    add_p(doc,
        "En esta pestaña se encuentra una grilla amplia (DataGridView) donde se visualizan todas las reservas registradas. "
        "En la parte inferior se ubican dos botones de acción:"
    )
    add_bullet(doc, "Permite modificar la fecha o la cantidad de horas de una reserva seleccionada en la grilla.", bold_prefix="Botón 'Modificar Reserva': ")
    add_bullet(doc, "Cambia el estado de la reserva a Cancelada, disparando automáticamente el registro en la auditoría.", bold_prefix="Botón 'Eliminar Reserva': ")

    # 4. Admin
    add_h1(doc, "4. Modo Administrador (Solapa 'GESTIÓN')", page_break_before=False)
    add_p(doc,
        "Para realizar tareas de administración sobre las personas y los lugares del coworking:"
    )
    add_h2(doc, "4.1. Ingreso y desbloqueo de solapa de gestión")
    add_p(doc, "Hacer clic en el menú superior 'Menú' y seleccionar la opción 'Ingresar como Administrador'. Ingresar el usuario Admin y la contraseña 123456. Al presionar aceptar, se desbloquea de inmediato una nueva solapa llamada 'GESTIÓN'.")

    add_h2(doc, "4.2. Alternancia rápida entre grilla de Usuarios y Recursos")
    add_p(doc, "Dentro de la solapa Gestión se ubican dos botones de opción ('Radio Buttons'): uno dice 'Usuarios' y el otro dice 'Recursos'. Al marcar uno u otro, el título de la pantalla cambia automáticamente y la tabla conmuta entre la lista de Clientes y la lista de Espacios Físicos.")

    add_h2(doc, "4.3. Botones de acción (Crear, Modificar, Eliminar)")
    add_p(doc, "En esta pantalla se encuentran los botones 'Crear', 'Modificar' y 'Eliminar' para dar altas, actualizar datos o dar de baja clientes y recursos.")

    add_h2(doc, "4.4. Cierre de sesión y protección de datos")
    add_p(doc, "Desde el menú superior 'Menú', al presionar 'Cerrar sesión', el sistema pide confirmación y oculta de inmediato la solapa de Gestión para proteger los datos de modificaciones no autorizadas.")

    # 5. Proximas etapas
    add_h1(doc, "5. Estado actual del proyecto y próximas etapas", page_break_before=False)
    add_p(doc,
        "Para tener un registro claro del estado actual del sistema al día de hoy:"
    )
    add_bullet(doc, "La base de datos MySQL completa (tablas, relaciones, vistas, trigger, función y procedimientos almacenados con control SIGNAL 45000). Todas las clases del modelo en C# con programación orientada a objetos (clase abstracta, herencia, interfaces y polimorfismo). La clase gestora con LINQ. La interfaz gráfica completa con inicio de sesión, soporte por WhatsApp, navegación por solapas protegidas según rol y diseño prolijo con logos.", bold_prefix="Lo que ya está 100% terminado y funcional: ")
    add_bullet(doc, "Terminar de enlazar los botones de la pantalla de gestión con los procedimientos almacenados de MySQL a través de GestorDAO.cs, e incorporar el módulo de importación y exportación de reservas en archivos JSON para completar las funciones del sistema.", bold_prefix="Lo que se completará en la siguiente etapa: ")

    save_doc_safely(doc, "Manual_de_Usuario")


def export_all_to_pdf():
    # Exporta automaticamente a PDF usando Word COM segun Pautas de Entrega
    ps_script = """
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $files = @("Documentacion_Desarrollo", "Diccionario_de_Datos", "Manual_de_Usuario")
    foreach ($f in $files) {
        $docx = Resolve-Path "Documentacion\\$f.docx"
        $pdf = $docx.Path.Replace(".docx", ".pdf")
        $doc = $word.Documents.Open($docx.Path)
        $doc.SaveAs([ref]$pdf, [ref]17)
        $doc.Close(0)
        Write-Host "PDF generado: $pdf"
    }
    $word.Quit()
    """
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True, capture_output=True, text=True)
        print("Exportación a PDF completada exitosamente.")
    except Exception as e:
        print(f"Nota: No se pudo auto-exportar a PDF ({e}).")

if __name__ == "__main__":
    generate_desarrollo()
    generate_diccionario()
    generate_manual()
    export_all_to_pdf()
