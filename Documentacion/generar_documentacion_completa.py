# -*- coding: utf-8 -*-
"""
Generador Maestro Integral de Documentación Institucional y Académica
Algoritmos II — Trabajo Práctico Final 2026
Instituto Argentino de la Empresa

Estilo estricto: Texto 100% color negro en todas las fuentes y elementos.
"""

import os
import subprocess
import win32com.client
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Texto estrictamente en color negro (0, 0, 0)
COLOR_TEXT_BLACK = RGBColor(0, 0, 0)
HEX_BORDER = "CCCCCC"
HEX_HEADER_BG = "F2F2F2"

def setup_document(doc):
    """Configura márgenes reglamentarios A4 (2.54 cm en los cuatro lados) y estilo normal Arial 11pt 1.5."""
    sec = doc.sections[0]
    sec.page_width = Inches(8.27)    # 210 mm
    sec.page_height = Inches(11.69)  # 297 mm
    sec.top_margin = Inches(1.0)     # 2.54 cm
    sec.bottom_margin = Inches(1.0)  # 2.54 cm
    sec.left_margin = Inches(1.0)    # 2.54 cm
    sec.right_margin = Inches(1.0)   # 2.54 cm
    sec.different_first_page_header_footer = False
    sec.footer.paragraphs[0].text = ""

    # Actualización automática de campos en Word (números de página, TOC)
    settings = doc.settings.element
    if settings.find(docx.oxml.ns.qn('w:updateFields')) is None:
        settings.append(parse_xml(f'<w:updateFields {nsdecls("w")} w:val="true"/>'))

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_TEXT_BLACK
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_after = Pt(4)

def start_body_section(doc, doc_short_title):
    """Inicializa la sección 2 (a partir de pág. 2) con pie de página anclado al fondo en números arábigos."""
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.0)
    sec2.right_margin = Inches(1.0)
    sec2.footer_distance = Inches(0.5)
    sec2.different_first_page_header_footer = False

    sec2.footer.is_linked_to_previous = False
    p_ft = sec2.footer.paragraphs[0]
    p_ft.text = ""
    p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ft.paragraph_format.space_after = Pt(0)
    
    r_ft = p_ft.add_run(f"Algoritmos II · {doc_short_title}  |  Pág. ")
    r_ft.font.name = 'Arial'
    r_ft.font.size = Pt(9)
    r_ft.font.color.rgb = COLOR_TEXT_BLACK

    # Campo de página con valor por defecto visible para evitar campo en blanco al abrir
    fld_page = parse_xml(
        r'<w:fldSimple %s w:instr="PAGE"><w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:color w:val="000000"/><w:sz w:val="18"/></w:rPr><w:t>2</w:t></w:r></w:fldSimple>' % nsdecls('w')
    )
    p_ft._p.append(fld_page)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_TEXT_BLACK
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_after = Pt(4)

def set_cell_shading(cell, fill_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_padding(cell, top=50, bottom=50, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def format_table(table, col_widths=None):
    """Aplica formato formal según APA 7 (bordes superior e inferior, sin bordes verticales)."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="10" w:space="0" w:color="{HEX_BORDER}"/>'
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
                        run.font.size = Pt(9.5)
                        run.font.color.rgb = COLOR_TEXT_BLACK
            else:
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_after = Pt(0)
                    for run in p.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(9.0)
                        run.font.color.rgb = COLOR_TEXT_BLACK

def add_institutional_cover(doc, doc_specific_title=None, doc_subtitle=None):
    """Portada institucional estricta según Sección 2 de Pautas de Presentación con texto 100% negro."""
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.space_before = Pt(14)
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("INSTITUTO ARGENTINO DE LA EMPRESA")
    r_inst.font.name = 'Arial'
    r_inst.font.bold = True
    r_inst.font.size = Pt(12)
    r_inst.font.color.rgb = COLOR_TEXT_BLACK

    p_car = doc.add_paragraph()
    p_car.paragraph_format.space_before = Pt(0)
    p_car.paragraph_format.space_after = Pt(2)
    p_car.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_car = p_car.add_run("Carrera: Analista de Sistemas de Información")
    r_car.font.name = 'Arial'
    r_car.font.size = Pt(10)
    r_car.font.color.rgb = COLOR_TEXT_BLACK

    p_asig = doc.add_paragraph()
    p_asig.paragraph_format.space_before = Pt(0)
    p_asig.paragraph_format.space_after = Pt(2)
    p_asig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_asig = p_asig.add_run("Asignatura: Algoritmos II")
    r_asig.font.name = 'Arial'
    r_asig.font.size = Pt(10)
    r_asig.font.color.rgb = COLOR_TEXT_BLACK

    p_ciclo = doc.add_paragraph()
    p_ciclo.paragraph_format.space_before = Pt(0)
    p_ciclo.paragraph_format.space_after = Pt(12)
    p_ciclo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ciclo = p_ciclo.add_run("Ciclo Lectivo: 2026")
    r_ciclo.font.name = 'Arial'
    r_ciclo.font.size = Pt(10)
    r_ciclo.font.color.rgb = COLOR_TEXT_BLACK

    # Logo
    logo_path = os.path.abspath("src/Img/Logo/Logo_coWorking_para_fondo_blanco.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.abspath("src/Img/Logo/Logo_coWorking_con_lema_turquesa_y_blanco.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(14)
        p_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(2.7))

    # Título principal reglamentario: 18 pt · negrita · centrado · negro
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("TRABAJO PRÁCTICO FINAL")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_TEXT_BLACK

    # Tema del trabajo
    p_theme = doc.add_paragraph()
    p_theme.paragraph_format.space_before = Pt(0)
    p_theme.paragraph_format.space_after = Pt(8)
    p_theme.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_theme = p_theme.add_run("Sistema de Gestión de Coworking y Reservas")
    r_theme.font.name = 'Arial'
    r_theme.font.size = Pt(14)
    r_theme.font.bold = True
    r_theme.font.color.rgb = COLOR_TEXT_BLACK

    if doc_specific_title:
        p_specific = doc.add_paragraph()
        p_specific.paragraph_format.space_before = Pt(2)
        p_specific.paragraph_format.space_after = Pt(4)
        p_specific.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_specific = p_specific.add_run(doc_specific_title.upper())
        r_specific.font.name = 'Arial'
        r_specific.font.size = Pt(11)
        r_specific.font.bold = True
        r_specific.font.color.rgb = COLOR_TEXT_BLACK

    if doc_subtitle:
        p_sub = doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(14)
        p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_sub = p_sub.add_run(doc_subtitle)
        r_sub.font.name = 'Arial'
        r_sub.font.size = Pt(10)
        r_sub.font.italic = True
        r_sub.font.color.rgb = COLOR_TEXT_BLACK

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(14)
    p_div.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("—" * 40)
    r_div.font.color.rgb = COLOR_TEXT_BLACK

    # 5. Metadatos institucionales claros y ordenados verticalmente (uno abajo del otro)
    # A) Titulo de integrantes en su propia linea
    p_int_title = doc.add_paragraph()
    p_int_title.paragraph_format.space_before = Pt(4)
    p_int_title.paragraph_format.space_after = Pt(4)
    p_int_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_it = p_int_title.add_run("Integrantes del Equipo:")
    r_it.font.name = 'Arial'
    r_it.font.bold = True
    r_it.font.size = Pt(10)
    r_it.font.color.rgb = COLOR_TEXT_BLACK

    # B) Cada integrante en su propia linea con sangria y viñeta
    integrantes = [
        ("Tullo, Jonathan Lester", "shonimdp@gmail.com"),
        ("Ortega, David Samuel", "davidortegaa86@gmail.com"),
        ("Scollo, Maximiliano", "maximilianoscollo17@gmail.com")
    ]
    for nom, mail in integrantes:
        p_miembro = doc.add_paragraph()
        p_miembro.paragraph_format.left_indent = Inches(0.25)
        p_miembro.paragraph_format.space_before = Pt(0)
        p_miembro.paragraph_format.space_after = Pt(3)
        p_miembro.paragraph_format.line_spacing = 1.15
        p_miembro.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

        r_dot = p_miembro.add_run("- ")
        r_dot.font.name = 'Arial'
        r_dot.font.bold = True
        r_dot.font.size = Pt(9.5)
        r_dot.font.color.rgb = COLOR_TEXT_BLACK

        r_n = p_miembro.add_run(nom)
        r_n.font.name = 'Arial'
        r_n.font.bold = True
        r_n.font.size = Pt(9.5)
        r_n.font.color.rgb = COLOR_TEXT_BLACK

        r_m = p_miembro.add_run(f" ({mail})")
        r_m.font.name = 'Arial'
        r_m.font.size = Pt(9.0)
        r_m.font.color.rgb = COLOR_TEXT_BLACK

    # C) Los demas campos institucionales bien espaciados y uno abajo del otro
    otros_metadatos = [
        ("Docente a cargo", "Lic. Adrián Aroca"),
        ("Comisión / Curso", "2º Año · Modalidad Regular"),
        ("Ciclo lectivo", "2026"),
        ("Fecha de entrega", "Noviembre de 2026"),
        ("Versión del documento", "Versión 1.0 (Entrega Integrada Final)")
    ]

    for i, (label, val) in enumerate(otros_metadatos):
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_before = Pt(6 if i == 0 else 3)
        p_m.paragraph_format.space_after = Pt(3)
        p_m.paragraph_format.line_spacing = 1.15
        p_m.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

        r_l = p_m.add_run(f"{label}: ")
        r_l.font.name = 'Arial'
        r_l.font.bold = True
        r_l.font.size = Pt(10)
        r_l.font.color.rgb = COLOR_TEXT_BLACK

        r_v = p_m.add_run(val)
        r_v.font.name = 'Arial'
        r_v.font.size = Pt(10)
        r_v.font.color.rgb = COLOR_TEXT_BLACK

def add_toc(doc, items):
    """Índice de contenidos con tabulación derecha y puntos guía reglamentarios APA 7, texto negro."""
    p_head = doc.add_paragraph()
    p_head.paragraph_format.page_break_before = False
    p_head.paragraph_format.space_before = Pt(14)
    p_head.paragraph_format.space_after = Pt(6)
    p_head.paragraph_format.keep_with_next = True
    p_head.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_h = p_head.add_run("ÍNDICE DE CONTENIDOS")
    r_h.font.name = 'Arial'
    r_h.font.size = Pt(14)
    r_h.font.bold = True
    r_h.font.color.rgb = COLOR_TEXT_BLACK

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(8)
    r_div = p_div.add_run("—" * 40)
    r_div.font.color.rgb = COLOR_TEXT_BLACK

    # Posición objetivo común en el margen derecho: 6.00 pulgadas (432 pt, perfectamente dentro del margen útil)
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
        elif level == 3:
            indent = Inches(0.44)
            p.paragraph_format.left_indent = indent

        # Tab stop nativo de python-docx: esquema OpenXML válido con puntos guía continuos
        p.paragraph_format.tab_stops.add_tab_stop(
            target_right + indent,
            WD_TAB_ALIGNMENT.RIGHT,
            WD_TAB_LEADER.DOTS
        )

        r1 = p.add_run(title)
        r1.font.name = 'Arial'
        r1.font.size = Pt(10.0 if level == 1 else 9.5)
        r1.font.bold = (level == 1)
        r1.font.color.rgb = COLOR_TEXT_BLACK

        r_tab = p.add_run('\t')
        r_tab.font.name = 'Arial'

        r2 = p.add_run(str(page_num))
        r2.font.name = 'Arial'
        r2.font.size = Pt(10.0 if level == 1 else 9.5)
        r2.font.bold = (level == 1)
        r2.font.color.rgb = COLOR_TEXT_BLACK

def add_h1(doc, text, page_break_before=True):
    """Sección principal: 16 pt negrita, negro."""
    p = doc.add_paragraph()
    if page_break_before:
        p.paragraph_format.page_break_before = True
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEXT_BLACK
    return p

def add_h2(doc, text):
    """Subsección: 13 pt negrita, negro."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEXT_BLACK
    return p

def add_h3(doc, text):
    """Tercer nivel: 11 pt negrita, negro."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEXT_BLACK
    return p

def add_p(doc, text, bold_prefix=None, italic=False):
    """Párrafo de texto formal en Arial 11 pt interlineado 1,5 justificado en negro."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Arial'
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_TEXT_BLACK
    r_t = p.add_run(text)
    r_t.font.name = 'Arial'
    r_t.font.italic = italic
    r_t.font.color.rgb = COLOR_TEXT_BLACK
    return p

def add_bullet(doc, text, bold_prefix=None):
    """Viñeta técnica formal justificada en negro."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Arial'
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_TEXT_BLACK
    r_t = p.add_run(text)
    r_t.font.name = 'Arial'
    r_t.font.color.rgb = COLOR_TEXT_BLACK
    return p

def add_figure_apa7(doc, img_path, fig_num, title, note_text=None, width=Inches(6.0)):
    """Inserta figura rotulada según APA 7.ª edición con texto negro."""
    if not os.path.exists(img_path):
        return

    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.keep_with_next = True
    p_num.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_num = p_num.add_run(f"Figura {fig_num}")
    r_num.font.name = 'Arial'
    r_num.font.bold = True
    r_num.font.size = Pt(10)
    r_num.font.color.rgb = COLOR_TEXT_BLACK

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.keep_with_next = True
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_title = p_title.add_run(title)
    r_title.font.name = 'Arial'
    r_title.font.italic = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = COLOR_TEXT_BLACK

    p_img = doc.add_paragraph()
    p_img.paragraph_format.space_before = Pt(0)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=width)

    if note_text:
        p_note = doc.add_paragraph()
        p_note.paragraph_format.space_before = Pt(0)
        p_note.paragraph_format.space_after = Pt(10)
        p_note.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_nlabel = p_note.add_run("Nota. ")
        r_nlabel.font.name = 'Arial'
        r_nlabel.font.italic = True
        r_nlabel.font.size = Pt(9)
        r_nlabel.font.color.rgb = COLOR_TEXT_BLACK
        r_ntext = p_note.add_run(note_text)
        r_ntext.font.name = 'Arial'
        r_ntext.font.size = Pt(9)
        r_ntext.font.color.rgb = COLOR_TEXT_BLACK

def add_code_snippet(doc, code_text, caption=None):
    """Inserta código formateado limpiamente con tipografía monospace Consolas,
    sangría izquierda, saltos de línea e indentación real, SIN cajas ni tablas grises."""
    lines = code_text.strip().splitlines()
    for i, line in enumerate(lines):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.space_before = Pt(4 if i == 0 else 0)
        p.paragraph_format.space_after = Pt(4 if i == len(lines) - 1 else 0)
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

        run = p.add_run(line if line else " ")
        run.font.name = 'Consolas'
        run.font.size = Pt(8.5)
        run.font.color.rgb = COLOR_TEXT_BLACK

    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.left_indent = Inches(0.4)
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Arial'
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_TEXT_BLACK

def save_doc_safely(doc, base_name):
    target_path = os.path.join("Documentacion", f"{base_name}.docx")
    try:
        doc.save(target_path)
        print(f"Documento Word guardado exitosamente: {target_path}")
    except PermissionError:
        alt_path = os.path.join("Documentacion", f"{base_name}_Nuevo.docx")
        doc.save(alt_path)
        print(f"Aviso: {target_path} se encuentra abierto. Guardado alternativo en: {alt_path}")


# =============================================================================
# 1. DOCUMENTO INTEGRADO OFICIAL: TP_Final_AlgoritmosII_Grupo2
# =============================================================================
def generate_master_document():
    doc = Document()
    setup_document(doc)
    add_institutional_cover(doc, "DOCUMENTO TÉCNICO Y MEMORIA INTEGRADORA", "Arquitectura POO, Persistencia MySQL, Manejo de Errores y Manual de Operación")
    start_body_section(doc, "Informe Integrador Final")

    master_toc = [
        ("1. Introducción y Objetivo General del Sistema", "3", 1),
        ("2. Tecnologías, Herramientas y Lenguajes Utilizados", "4", 1),
        ("3. Organización y Distribución del Trabajo en Equipo", "5", 1),
        ("4. Modelo de Datos y Persistencia en MySQL", "6", 1),
        ("4.1. Esquema Relacional y Restricciones de Integridad", "6", 2),
        ("4.2. Diagramas Entidad-Relación (DER Workbench y Conceptual)", "6", 2),
        ("4.3. Diccionario de Datos: Estructura de Tablas", "7", 2),
        ("4.4. Vistas del Sistema y Funciones Almacenadas", "9", 2),
        ("4.5. Procedimientos Almacenados y Reglas de Negocio con SIGNAL 45000", "9", 2),
        ("4.6. Trigger de Auditoría Automática", "10", 2),
        ("5. Arquitectura del Software y Programación Orientada a Objetos", "11", 1),
        ("5.1. Arquitectura en Capas del Sistema", "11", 2),
        ("5.2. Diagrama de Clases Simplificado (UML)", "11", 2),
        ("5.3. Interfaz de Dominio (IReservable.cs)", "12", 2),
        ("5.4. Enumerador Tipado (EstadoReserva.cs)", "12", 2),
        ("5.5. Clase Abstracta Base (Recurso.cs) y Justificación de Diseño", "12", 2),
        ("5.6. Clases Derivadas Especializadas (Sala, OficinaPrivada, PuestoTrabajo)", "13", 2),
        ("5.7. Justificación del Polimorfismo: CalcularCosto(horas)", "13", 2),
        ("5.8. Clases de Entidad (Cliente.cs y Reserva.cs)", "14", 2),
        ("5.9. Clase Gestora en Memoria (GestoraCoworking.cs) y Consultas LINQ", "14", 2),
        ("5.10. Evolución hacia el Patrón DAO (GestorDAO.cs)", "15", 2),
        ("6. Manejo de Errores, Estrategia de Conexión y Decisiones de Diseño", "16", 1),
        ("6.1. Estrategia de Conexión Centralizada (Conexion.cs) y App.config", "16", 2),
        ("6.2. Flujo de Captura del Error 45000 de MySQL a través de MySqlException", "16", 2),
        ("6.3. Manejo General de Excepciones y Ausencia de Bloques Vacíos", "17", 2),
        ("6.4. Funcionalidad y Esquema de Intercambio de Datos JSON", "17", 2),
        ("6.5. Justificación de Decisiones Técnicas y Alternativas Analizadas", "18", 2),
        ("7. Manual de Usuario y Guía de Operación del Sistema", "19", 1),
        ("7.1. Requisitos Previos para el Encendido del Sistema", "19", 2),
        ("7.2. Autenticación de Usuarios (FrmLogin) y Asistencia vía WhatsApp", "19", 2),
        ("7.3. Pantalla Principal (FrmPrincipal): Control Operativo y Reservas", "19", 2),
        ("7.4. Módulo de Administración: Gestión de Usuarios y Recursos", "20", 2),
        ("8. Guía de Ejecución y Puesta en Marcha", "21", 1),
        ("9. Referencias Bibliográficas (Normas APA 7.ª edición)", "22", 1),
        ("10. Checklist Institucional de Control Previo a la Entrega", "23", 1),
    ]
    add_toc(doc, master_toc)

    # 1. Introducción
    add_h1(doc, "1. Introducción y Objetivo General del Sistema", page_break_before=True)
    add_p(doc,
        "El presente proyecto corresponde al Trabajo Práctico Final integrador de la asignatura Algoritmos II, perteneciente a la carrera de Analista de Sistemas de Información del Instituto Argentino de la Empresa. "
        "Consiste en el diseño, desarrollo e implementación de una aplicación de escritorio completa construida en el lenguaje C# bajo la plataforma .NET Framework 4.7.2 con interfaz gráfica en Windows Forms, conectada a un motor de base de datos relacional MySQL/MariaDB bajo el entorno XAMPP."
    )
    add_p(doc,
        "El propósito del sistema es administrar de forma integral las actividades operativas y administrativas de un espacio de trabajo colaborativo (Coworking). "
        "Permite gestionar el padrón de clientes, catalogar los espacios físicos disponibles para alquiler (salas de reuniones, oficinas privadas y puestos de trabajo individuales) y registrar reservas horarias con control riguroso de concurrencia y disponibilidad."
    )
    add_p(doc,
        "La solución resuelve integralmente las reglas críticas del negocio: impide la superposición o solapamiento horario de reservas sobre un mismo recurso mediante lógica matemática encapsulada en procedimientos y funciones almacenadas de MySQL (emitiendo excepciones controladas vía SIGNAL SQLSTATE '45000'), calcula dinámicamente las tarifas aplicando polimorfismo orientado a objetos según las comodidades específicas de cada espacio, y audita automáticamente toda cancelación de servicio a través de un disparador (trigger) en la base de datos."
    )

    # 2. Tecnologías
    add_h1(doc, "2. Tecnologías, Herramientas y Lenguajes Utilizados", page_break_before=True)
    add_p(doc, "Para la construcción de la solución se adoptaron tecnologías estandarizadas, garantizando robustez, mantenibilidad y rendimiento óptimo:")
    add_bullet(doc, "Lenguaje principal de desarrollo con tipado estático riguroso, programación orientada a objetos (clases abstractas, interfaces, herencia y polimorfismo), colecciones genéricas y lenguaje de consulta integrado (LINQ).", bold_prefix="C# (.NET Framework 4.7.2): ")
    add_bullet(doc, "Framework para la construcción de la interfaz gráfica de usuario en entornos Windows, empleando formularios desacoplados, grillas de datos (DataGridView), selectores de fecha gráficos (DateTimePicker), controles de pestañas (TabControl) y controles numéricos (NumericUpDown).", bold_prefix="Windows Forms (WinForms): ")
    add_bullet(doc, "Sistema gestor de bases de datos relacionales alojado en localhost:3306 bajo XAMPP, responsable de la persistencia de datos, integridad referencial (claves primarias y foráneas), vistas analíticas, funciones determinísticas, disparadores de auditoría y procedimientos almacenados.", bold_prefix="MySQL / MariaDB (v10.4+): ")
    add_bullet(doc, "Conector oficial de Oracle para ADO.NET (v9.5.0), utilizado para la administración de conexiones (MySqlConnection), ejecución de comandos parametrizados (MySqlCommand), manejo de parámetros de entrada/salida y captura de excepciones específicas (MySqlException).", bold_prefix="MySql.Data: ")
    add_bullet(doc, "Entorno de desarrollo integrado utilizado para la escritura de código, diseño de formularios, depuración paso a paso, compilación mediante MSBuild y gestión de paquetes vía NuGet.", bold_prefix="Microsoft Visual Studio 2022: ")
    add_bullet(doc, "Herramientas oficiales de diseño relacional y administración de base de datos para la diagramación del modelo (mwb) y la ejecución del script de despliegue (DB_TPFinal.sql).", bold_prefix="MySQL Workbench 8.0 CE y phpMyAdmin: ")
    add_bullet(doc, "Sistema de control de versiones distribuido y repositorio remoto para la sincronización colaborativa y trazabilidad histórica de cambios del equipo.", bold_prefix="Git y GitHub: ")
    add_bullet(doc, "Mecanismo de enlace URI (wa.me) para derivar consultas operativas directamente a la línea de asistencia técnica del coworking.", bold_prefix="Protocolo Web WhatsApp: ")

    # 3. Organización
    add_h1(doc, "3. Organización y Distribución del Trabajo en Equipo", page_break_before=True)
    add_p(doc, "El desarrollo se articuló en módulos funcionales asignados a cada integrante del equipo, promoviendo la especialización técnica y la integración continua:")
    add_bullet(doc, "Diseño relacional y programación del script completo de base de datos MySQL (DB_TPFinal.sql): tablas, restricciones, vistas, funciones, procedimientos almacenados y trigger de auditoría. Configuración del proyecto base en Visual Studio 2022 (.NET 4.7.2), resolución de dependencias NuGet (MySql.Data), programación de la clase centralizada de conexión (Conexion.cs) y desarrollo del modelo base (Recurso.cs, IReservable.cs, EstadoReserva.cs).", bold_prefix="Jonathan Lester Tullo (shonimdp@gmail.com): ")
    add_bullet(doc, "Programación de las clases derivadas del modelo (Sala.cs, OficinaPrivada.cs, PuestoTrabajo.cs) con implementación del cálculo polimórfico de costos (CalcularCosto) y disponibilidad (PuedeReservarse). Desarrollo de los modelos Cliente.cs y Reserva.cs, implementación de la clase gestora en memoria con LINQ (GestoraCoworking.cs) y diagramación del modelo relacional en MySQL Workbench.", bold_prefix="Maximiliano Scollo (maximilianoscollo17@gmail.com): ")
    add_bullet(doc, "Diseño e implementación de la interfaz gráfica en Windows Forms: desarrollo de la pantalla de autenticación (FrmLogin) con control de credenciales y asistencia técnica vía WhatsApp, preparación de recursos gráficos y maquetado de la pantalla principal (FrmPrincipal) con solapas operativas (Control y Reservas) y solapa administrativa protegida por roles (Gestión).", bold_prefix="David Samuel Ortega (davidortegaa86@gmail.com): ")

    # 4. Base de Datos
    add_h1(doc, "4. Modelo de Datos y Persistencia en MySQL", page_break_before=True)
    add_p(doc,
        "La persistencia del sistema está gobernada por la base de datos tp_final_db alojada en MySQL. "
        "El diseño respeta rigurosamente la Tercera Forma Normal (3NF), garantizando la no duplicación de información y la preservación de la integridad referencial."
    )

    add_h2(doc, "4.1. Esquema Relacional y Restricciones de Integridad")
    add_p(doc,
        "El modelo relacional vincula clientes, recursos físicos y sus reservas temporales. "
        "Se aplican claves foráneas con restricciones estrictas de integridad: no es posible generar reservas asociadas a clientes inexistentes ni a recursos que no figuren en el catálogo general."
    )

    add_h2(doc, "4.2. Diagramas Entidad-Relación (DER Workbench y Conceptual)")
    add_p(doc, "A continuación se presentan el diagrama exportado de MySQL Workbench y el diagrama conceptual de entidades:")

    add_figure_apa7(
        doc,
        img_path=os.path.abspath("DB/Diagrama_DER.png"),
        fig_num="1",
        title="Diagrama Entidad-Relación (DER) del Modelo Relacional en MySQL Workbench",
        note_text="Exportación directa del modelo de datos de la base tp_final_db generada en MySQL Workbench 8.0 CE.",
        width=Inches(6.2)
    )

    add_figure_apa7(
        doc,
        img_path=os.path.abspath("DB/Diagrama_DER_Borrador.png"),
        fig_num="2",
        title="Diagrama Conceptual de Bloques y Flujo de Entidades del Negocio",
        note_text="Esquema conceptual inicial consensuado por el equipo de desarrollo para modelar las interacciones de coworking.",
        width=Inches(5.6)
    )

    add_h2(doc, "4.3. Diccionario de Datos: Estructura de Tablas")
    headers = ["Campo", "Tipo de Dato", "Nulo", "Clave", "Descripción"]

    add_h3(doc, "Tabla: tipo_recursos (Categorización de espacios)")
    t1 = doc.add_table(rows=3, cols=5)
    for j, h in enumerate(headers): t1.cell(0, j).paragraphs[0].text = h
    t1_data = [
        ["id_tipo_recurso", "INT", "NO", "PK (AI)", "Identificador unívoco del tipo de espacio físico."],
        ["nombre_tipo", "VARCHAR(100)", "NO", "-", "Denominación de la categoría (Sala, Oficina, Puesto)."]
    ]
    for i, r in enumerate(t1_data):
        for j, val in enumerate(r): t1.cell(i+1, j).paragraphs[0].text = val
    format_table(t1, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h3(doc, "Tabla: recursos (Espacios físicos comercializables)")
    t2 = doc.add_table(rows=10, cols=5)
    for j, h in enumerate(headers): t2.cell(0, j).paragraphs[0].text = h
    t2_data = [
        ["id_recurso", "INT", "NO", "PK (AI)", "Identificador unívoco del recurso físico."],
        ["nombre", "VARCHAR(100)", "NO", "-", "Nombre comercial del espacio (ej. Sala Innovación)."],
        ["descripcion", "TEXT", "SÍ", "-", "Descripción de comodidades y equipamiento disponible."],
        ["ubicacion", "VARCHAR(100)", "NO", "-", "Sector y nivel edilicio (ej. Piso 2 - Sector B)."],
        ["precio_por_hora", "DECIMAL(10,2)", "NO", "-", "Tarifa monetaria base por hora de uso."],
        ["mobiliario_incluido", "BOOLEAN", "SÍ", "-", "Aplica a oficinas: indica si incluye mobiliario completo."],
        ["cantidad_sillas", "INT", "SÍ", "-", "Aplica a salas: capacidad total de sillas instaladas."],
        ["nro_categoria", "INT", "SÍ", "-", "Aplica a puestos: nivel del box de trabajo (categorías 1, 2 o 3)."],
        ["id_tipo_recurso", "INT", "NO", "FK", "Referencia foránea a tipo_recursos.id_tipo_recurso."]
    ]
    for i, r in enumerate(t2_data):
        for j, val in enumerate(r): t2.cell(i+1, j).paragraphs[0].text = val
    format_table(t2, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h3(doc, "Tabla: clientes (Padrón de usuarios del coworking)")
    t3 = doc.add_table(rows=7, cols=5)
    for j, h in enumerate(headers): t3.cell(0, j).paragraphs[0].text = h
    t3_data = [
        ["id_cliente", "INT", "NO", "PK (AI)", "Identificador unívoco del cliente."],
        ["nombre", "VARCHAR(100)", "NO", "-", "Nombre de pila del cliente."],
        ["apellido", "VARCHAR(100)", "NO", "-", "Apellido del cliente."],
        ["telefono", "VARCHAR(20)", "NO", "-", "Teléfono de contacto directo."],
        ["mail", "VARCHAR(255)", "NO", "-", "Dirección de correo electrónico institucional o personal."],
        ["fecha_registro", "DATETIME", "NO", "Default Now", "Estampa temporal de alta del cliente en el sistema."]
    ]
    for i, r in enumerate(t3_data):
        for j, val in enumerate(r): t3.cell(i+1, j).paragraphs[0].text = val
    format_table(t3, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h3(doc, "Tabla: reservas (Tabla relacional pivote de transacciones)")
    t4 = doc.add_table(rows=8, cols=5)
    for j, h in enumerate(headers): t4.cell(0, j).paragraphs[0].text = h
    t4_data = [
        ["id_reserva", "INT", "NO", "PK (AI)", "Identificador unívoco de la reserva."],
        ["id_cliente", "INT", "NO", "FK", "Referencia foránea al cliente titular (clientes.id_cliente)."],
        ["id_recurso", "INT", "NO", "FK", "Referencia foránea al espacio asignado (recursos.id_recurso)."],
        ["fecha_reserva", "DATETIME", "NO", "-", "Fecha y hora pactada para el inicio del alquiler."],
        ["horas", "INT", "NO", "Default 1", "Duración en horas del período de uso contratado."],
        ["total", "DECIMAL(10,2)", "NO", "-", "Importe total facturado calculado para la operación."],
        ["estado", "VARCHAR(20)", "NO", "Default Conf", "Estado operativo: 'Confirmada', 'Cancelada' o 'Pendiente'."]
    ]
    for i, r in enumerate(t4_data):
        for j, val in enumerate(r): t4.cell(i+1, j).paragraphs[0].text = val
    format_table(t4, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h3(doc, "Tabla: auditoria_reservas (Trazabilidad y registro de cancelaciones)")
    t5 = doc.add_table(rows=6, cols=5)
    for j, h in enumerate(headers): t5.cell(0, j).paragraphs[0].text = h
    t5_data = [
        ["id_auditoria", "INT", "NO", "PK (AI)", "Identificador secuencial del evento de auditoría."],
        ["id_reserva", "INT", "NO", "-", "Número de la reserva afectada por la cancelación."],
        ["accion", "VARCHAR(50)", "NO", "-", "Descripción del suceso ('Cancelacion de reserva')."],
        ["fecha_accion", "DATETIME", "NO", "Default Now", "Fecha y hora exacta en la que se produjo la baja."],
        ["usuario", "VARCHAR(100)", "SÍ", "Default Sist", "Identificador de usuario o sistema que ejecutó la baja."]
    ]
    for i, r in enumerate(t5_data):
        for j, val in enumerate(r): t5.cell(i+1, j).paragraphs[0].text = val
    format_table(t5, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h2(doc, "4.4. Vistas del Sistema y Funciones Almacenadas")
    add_bullet(doc, "Combina mediante INNER JOIN las tablas reservas, clientes y recursos, proyectando nombres, apellidos, denominación del espacio físico, fecha, duración y estado en texto claro, desacoplando a la capa de presentación de la complejidad relacional de IDs.", bold_prefix="vw_detalle_reservas: ")
    add_bullet(doc, "Agrupa por recurso mediante GROUP BY calculando la cantidad acumulada de reservas confirmadas y el monto total recaudado, proporcionando resúmenes analíticos directos.", bold_prefix="vw_resumen_recursos: ")
    add_bullet(doc, "Recibe el identificador del recurso, la fecha/hora de inicio y la duración requerida. Evalúa la superposición de intervalos temporales aplicando la fórmula matemática estricta: (nuevo_inicio < fin_existente) AND (nuevo_fin > inicio_existente) frente a reservas confirmadas. Retorna 1 si el espacio se encuentra disponible o 0 en caso de conflicto.", bold_prefix="fn_verificar_disponibilidad: ")

    add_h2(doc, "4.5. Procedimientos Almacenados y Reglas de Negocio con SIGNAL 45000")
    add_p(doc,
        "Las operaciones de modificación de estado en la base de datos se ejecutan exclusivamente a través de Stored Procedures. "
        "En particular, sp_alta_reserva implementa una barrera de integridad de negocio inquebrantable:"
    )

    sp_code = """-- Procedimiento Almacenado con validación de disponibilidad y SIGNAL 45000
DELIMITER $$
CREATE PROCEDURE sp_alta_reserva(
    IN p_id_cliente INT,
    IN p_id_recurso INT,
    IN p_fecha DATETIME,
    IN p_horas INT,
    IN p_total DECIMAL(10,2),
    IN p_estado VARCHAR(20)
)
BEGIN
    -- Validación de horas e importe
    IF p_horas <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La cantidad de horas debe ser mayor a cero.';
    END IF;

    -- Validación matemática de superposición de intervalos
    IF fn_verificar_disponibilidad(p_id_recurso, p_fecha, p_horas) = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El recurso ya se encuentra reservado u ocupado en ese intervalo de horario.';
    END IF;

    -- Inserción si pasa todas las reglas de negocio
    INSERT INTO reservas (id_cliente, id_recurso, fecha_reserva, horas, total, estado)
    VALUES (p_id_cliente, p_id_recurso, p_fecha, p_horas, p_total, IFNULL(p_estado, 'Confirmada'));
END$$
DELIMITER ;"""
    add_code_snippet(doc, sp_code, caption="Código 1: sp_alta_reserva con validación de solapamiento y emisión de SIGNAL SQLSTATE '45000'")

    add_h2(doc, "4.6. Trigger de Auditoría Automática")
    add_p(doc,
        "El trigger trg_auditoria_reservas opera de manera reactiva tras una actualización (AFTER UPDATE) en la tabla reservas. "
        "Examina si el estado mutó a 'Cancelada' habiendo estado previamente en otro estado. "
        "De cumplirse, inserta automáticamente un registro histórico en auditoria_reservas, garantizando trazabilidad inmutable sin depender del código de la interfaz."
    )

    # 5. POO y C#
    add_h1(doc, "5. Arquitectura del Software y Programación Orientada a Objetos", page_break_before=True)
    add_p(doc,
        "El desarrollo del software en C# adopta los principios fundamentales de la Programación Orientada a Objetos (POO): abstracción, encapsulamiento, herencia funcional y polimorfismo dinámico."
    )

    add_h2(doc, "5.1. Arquitectura en Capas del Sistema")
    add_bullet(doc, "Formularios FrmLogin y FrmPrincipal. Capturan interacciones de usuario, configuran controles y muestran respuestas visuales sin contener lógica relacional.", bold_prefix="Capa de Presentación (UI): ")
    add_bullet(doc, "Clases gestoras (GestoraCoworking) que procesan listas en memoria, aplican filtros LINQ y coordinan reglas de negocio.", bold_prefix="Capa de Negocio (BLL): ")
    add_bullet(doc, "Clases de dominio (Recurso, Sala, OficinaPrivada, PuestoTrabajo, Cliente, Reserva) que modelan las entidades y encapsulan sus atributos y cálculos.", bold_prefix="Capa de Modelos (Entidades): ")
    add_bullet(doc, "Clase GestorDAO encargada de aislar el consumo de procedimientos almacenados, comandos y parámetros ADO.NET.", bold_prefix="Capa de Acceso a Datos (DAO): ")
    add_bullet(doc, "Clase estática Conexion responsable de fabricar instancias MySqlConnection hacia el servidor MySQL.", bold_prefix="Capa de Infraestructura / Conexión: ")

    add_h2(doc, "5.2. Diagrama de Clases Simplificado (UML)")
    add_figure_apa7(
        doc,
        img_path=os.path.abspath("DB/Diagrama_Clases_UML.png"),
        fig_num="3",
        title="Diagrama de Clases Simplificado del Dominio (UML)",
        note_text="Diagrama UML con especificación de atributos, métodos, jerarquía de herencia (Recurso) e implementación de interfaz (IReservable).",
        width=Inches(6.2)
    )

    add_h2(doc, "5.3. Interfaz de Dominio (IReservable.cs)")
    add_p(doc,
        "La interfaz IReservable define el contrato formal bool PuedeReservarse(DateTime fecha). "
        "Su utilización desacopla la capacidad de reserva de la jerarquía de herencia de clases: cualquier recurso físico, servicio adicional o equipamiento tecnológico que deba validar disponibilidad en una fecha determinada implementa esta interfaz de forma uniforme."
    )

    add_h2(doc, "5.4. Enumerador Tipado (EstadoReserva.cs)")
    add_p(doc,
        "El enumerador EstadoReserva (con valores Pendiente, Confirmada, Cancelada, Finalizada) elimina la utilización de cadenas literales arbitrarias en el código, mitigando errores de tipeo y dotando a la lógica de negocio de fuerte tipado estático en tiempo de compilación."
    )

    add_h2(doc, "5.5. Clase Abstracta Base (Recurso.cs) y Justificación de Diseño")
    add_p(doc,
        "La clase Recurso se define con el modificador abstract porque en el mundo real no existe un 'recurso genérico' que un cliente pueda alquilar; los clientes alquilan espacios concretos con características físicas determinadas (una sala de conferencias con cierta cantidad de sillas, una oficina amueblada o un puesto individual de categoría específica). "
        "Recurso reúne los atributos comunes (IdRecurso, Nombre, Descripcion, Ubicacion, PrecioPorHora, IdTipoRecurso), implementa la interfaz IReservable y establece la firma abstracta obligatoria public abstract decimal CalcularCosto(int horas); forzando a que cada subclase provea su propio algoritmo de cálculo."
    )

    add_h2(doc, "5.6. Clases Derivadas Especializadas")
    add_p(doc, "Las subclases especializan el comportamiento base incorporando atributos diferenciales del negocio:")
    add_bullet(doc, "Añade la propiedad CantSillas. En el cálculo de costo, evalúa la capacidad de asistentes para incorporar cargos de mantenimiento y limpieza.", bold_prefix="Sala (IdTipoRecurso = 1): ")
    add_bullet(doc, "Añade la propiedad booleana MobiliarioIncluido. Si la oficina cuenta con equipamiento ergonómico y mobiliario ejecutivo completo, incorpora un canon fijo adicional.", bold_prefix="OficinaPrivada (IdTipoRecurso = 2): ")
    add_bullet(doc, "Añade la propiedad numérica NroCategoria (1, 2 o 3). Aplica un plus tarifario escalonado según el nivel de comodidades tecnológicas del box.", bold_prefix="PuestoTrabajo (IdTipoRecurso = 3): ")

    add_h2(doc, "5.7. Justificación del Polimorfismo: CalcularCosto(horas)")
    add_p(doc,
        "El polimorfismo constituye el pilar arquitectónico central del subsistema de tarifación. "
        "Al definir CalcularCosto(int horas) como método abstracto en la clase base Recurso y sobrescribirlo mediante override en cada clase hija, el sistema permite que cualquier componente (como el formulario de reservas o la clase gestora) invoque el método sobre una referencia genérica Recurso sin necesidad de inspeccionar el tipo concreto en tiempo de ejecución."
    )
    add_p(doc,
        "Esta decisión técnica aporta dos ventajas críticas: elimina por completo el uso de estructuras condicionales acopladas (switch o if-else encadenados basados en tipos) y cumple de manera estricta con el Principio Abierto/Cerrado (OCP - Open/Closed Principle) de SOLID. "
        "Si en el futuro se incorporara una nueva clase de recurso (por ejemplo, CabinaDeStreaming o TerrazaDeEventos), bastará con crear una nueva clase derivada de Recurso que sobreescriba CalcularCosto, sin tener que alterar ni una sola línea del código de cálculo existente."
    )

    poly_code = """// Implementación de polimorfismo dinámico en las clases del dominio
public abstract class Recurso : IReservable
{
    public decimal PrecioPorHora { get; set; }
    // Método abstracto: obliga a la implementación en cada derivada
    public abstract decimal CalcularCosto(int horas);
}

public class Sala : Recurso
{
    public int CantSillas { get; set; }
    public override decimal CalcularCosto(int horas)
    {
        decimal costo = PrecioPorHora * horas;
        if (CantSillas > 60) costo += 16000;
        else if (CantSillas > 30) costo += 8000;
        return costo;
    }
}

public class OficinaPrivada : Recurso
{
    public bool MobiliarioIncluido { get; set; }
    public override decimal CalcularCosto(int horas)
    {
        decimal costo = PrecioPorHora * horas;
        return MobiliarioIncluido ? costo + 1500 : costo;
    }
}

public class PuestoTrabajo : Recurso
{
    public int NroCategoria { get; set; }
    public override decimal CalcularCosto(int horas)
    {
        decimal costo = PrecioPorHora * horas;
        if (NroCategoria == 1) return costo + 3500;
        if (NroCategoria == 2) return costo + 5500;
        if (NroCategoria == 3) return costo + 8000;
        return costo;
    }
}"""
    add_code_snippet(doc, poly_code, caption="Código 2: Sobrescritura polimórfica del método CalcularCosto(horas) en clases derivadas")

    add_h2(doc, "5.8. Clases de Entidad (Cliente.cs y Reserva.cs)")
    add_p(doc,
        "Cliente modela los datos de filiación del titular (IdCliente, Nombre, Apellido, Telefono, Mail, FechaRegistro).\n"
        "Reserva actúa como entidad relacional pura, vinculando al cliente con el espacio rentado, la estampa temporal de inicio, la duración en horas, el monto total facturado y el estado operativo tipado mediante EstadoReserva."
    )

    add_h2(doc, "5.9. Clase Gestora en Memoria (GestoraCoworking.cs) y Consultas LINQ")
    add_p(doc,
        "GestoraCoworking administra una colección genérica List<Reserva> en memoria principal. "
        "Aplica el encapsulamiento de datos y expone métodos de consulta basados en expresiones lambda y Language Integrated Query (LINQ):"
    )
    add_bullet(doc, "ListaReservas.Where(r => r.Fecha.Date == fecha.Date).ToList()", bold_prefix="Búsqueda por fecha: ")
    add_bullet(doc, "ListaReservas.Where(r => r.IdCliente == cliente.IdCliente).ToList()", bold_prefix="Filtrado por cliente: ")
    add_bullet(doc, "ListaReservas.Where(r => r.EstadoReserva == estado).ToList()", bold_prefix="Filtrado por estado: ")
    add_bullet(doc, "ListaReservas.FirstOrDefault(r => r.IdReserva == idReserva)", bold_prefix="Localización unívoca: ")

    add_h2(doc, "5.10. Evolución hacia el Patrón DAO (GestorDAO.cs)")
    add_p(doc,
        "Para culminar el desacoplamiento entre la capa visual y el motor relacional conforme a las consignas evolutivas de la cátedra, el sistema incorpora GestorDAO.cs. "
        "Esta clase asume la responsabilidad exclusiva de interactuar con MySQL mediante comandos parametrizados (MySqlCommand con CommandType.StoredProcedure), liberando a los formularios de cualquier instrucción SQL o referencia a ADO.NET y respetando el Principio de Responsabilidad Única (SRP)."
    )

    # 6. Manejo de Errores
    add_h1(doc, "6. Manejo de Errores, Estrategia de Conexión y Decisiones de Diseño", page_break_before=True)
    add_h2(doc, "6.1. Estrategia de Conexión Centralizada (Conexion.cs) y App.config")
    add_p(doc,
        "La clase Conexion se declara con el modificador static debido a que representa un servicio utilitario de infraestructura sin estado que no debe ser instanciado como objeto de negocio. "
        "Implementa el patrón de factoría simple a través de su método CrearConexion(), el cual retorna una nueva instancia configurada de MySqlConnection pero sin invocar anticipadamente .Open()."
    )
    add_p(doc,
        "Cada método que interactúa con la base de datos envuelve la conexión en un bloque using. "
        "Al finalizar el bloque (incluso si se produjera una excepción no controlada), el entorno de ejecución de .NET invoca automáticamente el método Dispose(), cerrando la conexión hacia MySQL y devolviendo el recurso al pool de conexiones del sistema operativo sin riesgo de fugas de memoria o conexiones huérfanas."
    )
    add_p(doc,
        "Asimismo, se prevé la migración de la cadena de conexión hacia el archivo de configuración externa App.config mediante ConfigurationManager.ConnectionStrings[\"CoworkingDB\"], permitiendo modificar el host, puerto o credenciales de acceso sin requerir la recompilación del código fuente."
    )

    add_h2(doc, "6.2. Flujo de Captura del Error 45000 de MySQL a través de MySqlException")
    add_p(doc,
        "Cuando el procedimiento almacenado sp_alta_reserva detecta una violación de disponibilidad mediante fn_verificar_disponibilidad, interrumpe la transacción emitiendo la instrucción SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El recurso ya se encuentra reservado...'. "
        "El proveedor ADO.NET captura dicha señal y arroja una excepción MySqlException hacia la aplicación C#."
    )

    err_code = """// Captura y tratamiento controlado de excepciones provenientes de MySQL
try
{
    using (MySqlConnection conn = Conexion.CrearConexion())
    {
        conn.Open();
        using (MySqlCommand cmd = new MySqlCommand("sp_alta_reserva", conn))
        {
            cmd.CommandType = CommandType.StoredProcedure;
            cmd.Parameters.AddWithValue("p_id_cliente", idCliente);
            cmd.Parameters.AddWithValue("p_id_recurso", idRecurso);
            cmd.Parameters.AddWithValue("p_fecha", fecha);
            cmd.Parameters.AddWithValue("p_horas", horas);
            cmd.Parameters.AddWithValue("p_total", total);
            cmd.Parameters.AddWithValue("p_estado", "Confirmada");

            cmd.ExecuteNonQuery();
            MessageBox.Show("Reserva confirmada con éxito.", "Operación Exitosa", 
                            MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}
catch (MySqlException ex)
{
    // Código 1644 / SQLSTATE 45000 corresponde a errores de negocio emitidos por SIGNAL
    if (ex.Number == 1644 || ex.SqlState == "45000")
    {
        MessageBox.Show("Aviso de Negocio: " + ex.Message, 
                        "Conflicto de Disponibilidad", MessageBoxButtons.OK, MessageBoxIcon.Warning);
    }
    else
    {
        MessageBox.Show("Falla de Base de Datos [Código " + ex.Number + "]: " + ex.Message, 
                        "Error Técnico", MessageBoxButtons.OK, MessageBoxIcon.Error);
    }
}
catch (Exception ex)
{
    MessageBox.Show("Error inesperado en el sistema: " + ex.Message, 
                    "Error General", MessageBoxButtons.OK, MessageBoxIcon.Error);
}"""
    add_code_snippet(doc, err_code, caption="Código 3: Bloque estructurado de captura diferenciada de MySqlException (SIGNAL 45000)")

    add_h2(doc, "6.3. Manejo General de Excepciones y Ausencia de Bloques Vacíos")
    add_p(doc,
        "En estricto cumplimiento de las directivas institucionales de la cátedra, la totalidad de los bloques catch implementan una respuesta activa (presentando un mensaje explicativo al usuario y preservando la trazabilidad de la pila de llamadas mediante ex.Message). "
        "Se garantiza la inexistencia de bloques catch vacíos en todo el proyecto."
    )

    add_h2(doc, "6.4. Funcionalidad y Esquema de Intercambio de Datos JSON")
    add_p(doc,
        "Conforme a los requerimientos evolutivos del proyecto, se definió el formato estándar de intercambio de datos mediante JSON (JavaScript Object Notation). "
        "Este módulo permite exportar e importar tanto el catálogo de recursos como los lotes históricos de reservas para interoperabilidad con sistemas externos y respaldo de seguridad:"
    )

    json_sample = """[
  {
    "IdReserva": 101,
    "Cliente": {
      "IdCliente": 1,
      "NombreCompleto": "Juan Pérez",
      "Mail": "juan.perez@empresa.com"
    },
    "Recurso": {
      "IdRecurso": 2,
      "Nombre": "Oficina Ejecutiva A",
      "Tipo": "OficinaPrivada",
      "PrecioPorHora": 4500.00
    },
    "Fecha": "2026-11-15T09:00:00",
    "Horas": 4,
    "TotalCalculado": 19500.00,
    "Estado": "Confirmada"
  }
]"""
    add_code_snippet(doc, json_sample, caption="Código 4: Estructura del archivo JSON de intercambio para exportación/importación de reservas")

    add_h2(doc, "6.5. Justificación de Decisiones Técnicas y Alternativas Analizadas")
    add_bullet(doc, "Se priorizó el uso de procedimientos almacenados sobre sentencias SQL embebidas en el código C# para prevenir vulnerabilidades de Inyección SQL (SQL Injection), reducir el tráfico en la red local y permitir optimizaciones en el plan de ejecución dentro del motor de base de datos.", bold_prefix="Persistencia vía Stored Procedures vs SQL Dinámico: ")
    add_bullet(doc, "Se resolvió delegar la comprobación de disponibilidad a la función fn_verificar_disponibilidad en el motor relacional en lugar de calcularla en memoria del cliente. Esto previene condiciones de carrera (race conditions) en escenarios multiusuario donde dos operadores intentasen reservar simultáneamente el mismo espacio.", bold_prefix="Validación de Disponibilidad en Motor vs Cliente: ")
    add_bullet(doc, "Se implementó una autenticación ágil basada en roles (Usuario Operativo y Administrador). Para el restablecimiento de credenciales, se descartó deliberadamente el envío automático de correos (que requería configurar servidores SMTP propensos a bloqueos) y se optó por un enlace interactivo vía WhatsApp, garantizando asistencia humana inmediata.", bold_prefix="Mecanismo de Login y Soporte Técnico: ")

    # 7. Manual de Usuario
    add_h1(doc, "7. Manual de Usuario y Guía de Operación del Sistema", page_break_before=True)
    add_h2(doc, "7.1. Requisitos Previos para el Encendido del Sistema")
    add_bullet(doc, "Iniciar el panel de control de XAMPP y activar el servicio de MySQL en el puerto 3306 (debe visualizarse en color verde).", bold_prefix="1. Servidor de Persistencia: ")
    add_bullet(doc, "Abrir MySQL Workbench o phpMyAdmin y ejecutar por única vez el script DB/DB_TPFinal.sql para inicializar el esquema tp_final_db con tablas, vistas, funciones, procedimientos y datos de muestra.", bold_prefix="2. Inicialización de Datos: ")
    add_bullet(doc, "Abrir la solución SistemaDeGestion.slnx en Microsoft Visual Studio 2022 y compilar con F5 (o ejecutar el binario compilado SistemaDeGestion.exe).", bold_prefix="3. Lanzamiento: ")

    add_h2(doc, "7.2. Autenticación de Usuarios (FrmLogin) y Asistencia vía WhatsApp")
    add_p(doc,
        "Al pulsar la opción 'Ingresar como Administrador' desde el menú superior, se despliega el formulario modal FrmLogin. "
        "Las credenciales autorizadas de nivel directivo son Usuario: Admin y Contraseña: 123456. "
        "Si los datos ingresados no concuerdan, el sistema notifica el campo erróneo y sitúa el foco del cursor para su corrección rápida. "
        "En la parte inferior se encuentra el enlace '¿Necesitas ayuda? Contactar soporte', el cual invoca el navegador web o la app de WhatsApp derivando un mensaje tipificado al número de atención oficial (+54 9 223 301-4626)."
    )

    add_h2(doc, "7.3. Pantalla Principal (FrmPrincipal): Control Operativo y Reservas")
    add_bullet(doc, "Dispone de selectores vinculados para Cliente (ComboBox), Tipo de Recurso (ComboBox), fecha de inicio (DateTimePicker) y horas de uso (NumericUpDown). El visor de importe calcula el monto total a pagar considerando tarifas base y recargos por equipamiento. El botón 'Agregar' envía la solicitud de reserva al motor.", bold_prefix="Solapa CONTROL: ")
    add_bullet(doc, "Exhibe una grilla completa (DataGridView) con el listado de reservas vigentes. Permite reprogramar turnos mediante el botón 'Modificar Reserva' o registrar la baja mediante 'Eliminar Reserva', disparando la auditoría automática en MySQL.", bold_prefix="Solapa RESERVAS: ")

    add_h2(doc, "7.4. Módulo de Administración: Gestión de Usuarios y Recursos")
    add_p(doc,
        "Una vez validada la clave de administrador, se desbloquea dinámicamente la solapa 'GESTIÓN'. "
        "Esta pantalla cuenta con botones de opción mutuamente excluyentes (RadioButtons: 'Usuarios' y 'Recursos') que conmutan instantáneamente la grilla activa entre el catálogo de Clientes y el catálogo de Espacios Físicos. "
        "Desde allí, los botones 'Crear', 'Modificar' y 'Eliminar' permiten ejecutar el mantenimiento integral del padrón. "
        "La opción 'Cerrar sesión' en el menú superior oculta la solapa administrativa para resguardar la seguridad de la información."
    )

    # 8. Guía de Ejecución
    add_h1(doc, "8. Guía de Ejecución y Puesta en Marcha", page_break_before=True)
    add_p(doc, "Para reproducir el entorno y ejecutar las pruebas de validación académica en cualquier equipo de prueba, siga los pasos estandarizados:")
    add_bullet(doc, "Clonar o descomprimir el repositorio del proyecto en una ruta local accesible (ej. c:\\xampp\\htdocs\\TP_FINAL_ALGORITMOS).", bold_prefix="Paso 1 (Descarga de Fuentes): ")
    add_bullet(doc, "Abrir XAMPP Control Panel, inicializar el servicio MySQL en el puerto 3306, ingresar a phpMyAdmin (http://localhost/phpmyadmin) o MySQL Workbench, abrir el archivo DB/DB_TPFinal.sql y hacer clic en 'Ejecutar'. Verificar la creación de la base tp_final_db y sus 5 tablas.", bold_prefix="Paso 2 (Despliegue de Base de Datos): ")
    add_bullet(doc, "Abrir Visual Studio 2022 y cargar el archivo de solución SistemaDeGestion.slnx ubicado en la carpeta del proyecto.", bold_prefix="Paso 3 (Apertura de Solución): ")
    add_bullet(doc, "Hacer clic derecho sobre la solución en el Explorador de Soluciones y seleccionar 'Restaurar paquetes NuGet' para garantizar que MySql.Data se encuentre debidamente vinculado.", bold_prefix="Paso 4 (Restauración de Dependencias): ")
    add_bullet(doc, "Seleccionar la configuración 'Debug' / 'AnyCPU' y presionar la tecla F5 (o el botón Iniciar). La aplicación compilará sin errores y desplegará la pantalla de inicio.", bold_prefix="Paso 5 (Compilación y Ejecución): ")

    # 9. Referencias Bibliográficas
    add_h1(doc, "9. Referencias Bibliográficas (Normas APA 7.ª edición)", page_break_before=True)
    add_p(doc, "A continuación se listan las fuentes técnicas y bibliográficas formales consultadas para el desarrollo del software y la redacción de la presente memoria técnica, conforme a las pautas de citación APA 7.ª edición:")

    references = [
        ("Freeman, E., & Robson, E. (2020). ", "Head First Design Patterns: Building Extensible and Maintainable Object-Oriented Software", " (2.ª ed.). O'Reilly Media."),
        ("Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). ", "Design Patterns: Elements of Reusable Object-Oriented Software", ". Addison-Wesley Professional."),
        ("Martin, R. C. (2018). ", "Clean Architecture: A Craftsman's Guide to Software Structure and Design", ". Prentice Hall."),
        ("Microsoft Corporation. (2023). ", "Documentación de C# y Guía de Arquitectura de .NET Framework", ". Microsoft Learn. https://learn.microsoft.com/es-es/dotnet/csharp/"),
        ("Oracle Corporation. (2024). ", "MySQL 8.0 Reference Manual: Stored Procedures, Triggers and Functions", ". Oracle Help Center. https://dev.mysql.com/doc/refman/8.0/en/"),
        ("Troelsen, A., & Japikse, P. (2022). ", "Pro C# 10 with .NET 6: Foundational Principles and Practices in Programming", " (11.ª ed.). Apress.")
    ]

    for authors, book_title, rest in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.2
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        r1 = p_ref.add_run(authors)
        r1.font.name = 'Arial'
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEXT_BLACK
        
        r2 = p_ref.add_run(book_title)
        r2.font.name = 'Arial'
        r2.font.italic = True
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_TEXT_BLACK
        
        r3 = p_ref.add_run(rest)
        r3.font.name = 'Arial'
        r3.font.size = Pt(10)
        r3.font.color.rgb = COLOR_TEXT_BLACK

    # 10. Checklist
    add_h1(doc, "10. Checklist Institucional de Control Previo a la Entrega", page_break_before=True)
    add_p(doc, "Tabla de control de conformidad previa respecto a las Pautas de Presentación de la Cátedra:")

    chk_headers = ["Requisito Institucional", "Criterio de Evaluación", "Estado"]
    t_chk = doc.add_table(rows=11, cols=3)
    for j, h in enumerate(chk_headers): t_chk.cell(0, j).paragraphs[0].text = h
    chk_rows = [
        ["Portada Reglamentaria", "Instituto, carrera, materia, docente, año, versión y datos completos de todos los integrantes.", "CUMPLE (100%)"],
        ["Formato de Documento", "Hoja tamaño A4, márgenes de 2,54 cm en los cuatro costados, texto justificado.", "CUMPLE (100%)"],
        ["Tipografía y Estilo", "Arial 11 pt, interlineado 1,5, jerarquía de títulos estricta (18 pt, 16 pt, 13 pt, 11 pt).", "CUMPLE (100%)"],
        ["Normas APA 7.ª Edición", "Rotulado formal de figuras, tablas sin bordes verticales y sección final de referencias.", "CUMPLE (100%)"],
        ["Índice y Paginación", "Tabla de contenidos con puntos guía y numeración de página arábiga en pie de página.", "CUMPLE (100%)"],
        ["Modelo de Base de Datos", "DER exportado de Workbench, script DB_TPFinal.sql, tablas, vistas, función y trigger.", "CUMPLE (100%)"],
        ["Validación SIGNAL 45000", "Control estricto de disponibilidad y captura diferenciada vía MySqlException en C#.", "CUMPLE (100%)"],
        ["Arquitectura POO y C#", "Clase abstracta Recurso, interfaz IReservable, herencia y polimorfismo en CalcularCosto.", "CUMPLE (100%)"],
        ["Gestión y Capas (DAO)", "Uso de GestoraCoworking con LINQ y desacoplamiento progresivo mediante GestorDAO.", "CUMPLE (100%)"],
        ["Código y Evidencias", "Bloques de código con tipografía monospace sin capturas innecesarias de texto.", "CUMPLE (100%)"]
    ]
    for i, r in enumerate(chk_rows):
        for j, val in enumerate(r): t_chk.cell(i+1, j).paragraphs[0].text = val
    format_table(t_chk, [Inches(2.0), Inches(3.6), Inches(1.3)])

    save_doc_safely(doc, "TP_Final_AlgoritmosII_Grupo2")


# =============================================================================
# 2. DOCUMENTO MODULAR: Documentacion_Desarrollo
# =============================================================================
def generate_desarrollo():
    doc = Document()
    setup_document(doc)
    add_institutional_cover(doc, "DOCUMENTACIÓN DEL DESARROLLO", "Arquitectura en Capas, Programación Orientada a Objetos y Manejo de Errores")
    start_body_section(doc, "Documentación del Desarrollo")

    desarrollo_toc = [
        ("1. Objetivo y Descripción del Sistema", "3", 1),
        ("2. Tecnologías, Herramientas y Lenguajes Utilizados", "3", 1),
        ("3. Organización del Trabajo en Equipo", "4", 1),
        ("4. Arquitectura del Sistema por Capas", "4", 1),
        ("5. Diagrama de Clases Simplificado (UML)", "5", 1),
        ("6. Programación Orientada a Objetos y Clases C#", "6", 1),
        ("6.1. Conexión centralizada (Conexion.cs)", "6", 2),
        ("6.2. Interfaz de disponibilidad (IReservable.cs)", "6", 2),
        ("6.3. Enumerador de estado (EstadoReserva.cs)", "6", 2),
        ("6.4. Clase base abstracta (Recurso.cs) y justificación", "6", 2),
        ("6.5. Clases derivadas especializadas (Sala, Oficina, Puesto)", "7", 2),
        ("6.6. Polimorfismo: Justificación de CalcularCosto(horas)", "7", 2),
        ("6.7. Clases de entidad (Cliente.cs y Reserva.cs)", "8", 2),
        ("6.8. Gestión en memoria con LINQ (GestoraCoworking.cs)", "8", 2),
        ("6.9. Evolución hacia el patrón DAO (GestorDAO.cs)", "9", 2),
        ("7. Manejo de Errores y Excepciones (MySQL + C#)", "9", 1),
        ("8. Requerimientos Evolutivos (JSON y Configuración Externa)", "10", 1),
        ("9. Instrucciones para la Ejecución del Proyecto", "10", 1),
        ("10. Referencias Bibliográficas (APA 7.ª edición)", "11", 1)
    ]
    add_toc(doc, desarrollo_toc)

    add_h1(doc, "1. Objetivo y Descripción del Sistema", page_break_before=True)
    add_p(doc,
        "Este proyecto consiste en el desarrollo de una aplicación de escritorio programada en C# con Windows Forms, conectada de manera centralizada a una base de datos MySQL alojada en el entorno de XAMPP. "
        "El objetivo principal es administrar de forma integral un espacio de coworking, permitiendo la gestión de clientes, el catálogo de recursos alquilables (salas de reunión, oficinas privadas y puestos de trabajo) y el control de reservas por fecha y horario."
    )
    add_p(doc,
        "El sistema resuelve los problemas operativos fundamentales del negocio: asegura que no existan reservas duplicadas para un mismo recurso en el mismo horario mediante validaciones estrictas en la base de datos (SIGNAL SQLSTATE '45000'), calcula automáticamente los costos de alquiler aplicando tarifas base y recargos polimórficos por comodidades, y mantiene un registro automático de auditoría para cada cancelación."
    )

    add_h1(doc, "2. Tecnologías, Herramientas y Lenguajes Utilizados", page_break_before=False)
    add_bullet(doc, "C# (.NET Framework 4.7.2): POO estricto, herencia, interfaces, colecciones genéricas y LINQ.", bold_prefix="Lenguaje: ")
    add_bullet(doc, "Windows Forms (WinForms): Formularios FrmLogin y FrmPrincipal con DataGridView, ComboBox, TabControl.", bold_prefix="Interfaz: ")
    add_bullet(doc, "MySQL / MariaDB en XAMPP: Motor relacional en localhost:3306 con Stored Procedures, vistas, funciones y triggers.", bold_prefix="Persistencia: ")
    add_bullet(doc, "MySql.Data (v9.5.0): Conector oficial de ADO.NET para administración de conexiones y parámetros.", bold_prefix="Conector: ")
    add_bullet(doc, "Microsoft Visual Studio 2022: IDE de desarrollo, compilación y gestión NuGet.", bold_prefix="IDE: ")
    add_bullet(doc, "Git y GitHub: Control de versiones distribuido y trabajo colaborativo.", bold_prefix="Control de Versiones: ")

    add_h1(doc, "3. Organización del Trabajo en Equipo", page_break_before=False)
    add_bullet(doc, "Jonathan Lester Tullo: Base de datos MySQL completa, solución en Visual Studio, NuGet MySql.Data, clase Conexion.cs, clase abstracta Recurso.cs e interfaz IReservable.cs.", bold_prefix="Base de Datos y Núcleo: ")
    add_bullet(doc, "Maximiliano Scollo: Clases derivadas (Sala, OficinaPrivada, PuestoTrabajo), implementación de polimorfismo en CalcularCosto, modelos Cliente y Reserva, GestoraCoworking con LINQ y diagrama DER.", bold_prefix="Lógica y POO: ")
    add_bullet(doc, "David Samuel Ortega: Interfaz Windows Forms, pantalla de login FrmLogin con WhatsApp, FrmPrincipal con solapas Control, Reservas y Gestión protegida por perfil.", bold_prefix="Interfaz y Experiencia de Usuario: ")

    add_h1(doc, "4. Arquitectura del Sistema por Capas", page_break_before=False)
    add_bullet(doc, "Capa de Presentación: Formularios FrmLogin y FrmPrincipal.", bold_prefix="4.1. UI: ")
    add_bullet(doc, "Capa de Negocio: GestoraCoworking administra colecciones List<Reserva> en memoria con consultas LINQ.", bold_prefix="4.2. BLL: ")
    add_bullet(doc, "Capa de Modelos: Clases Recurso, Sala, OficinaPrivada, PuestoTrabajo, Cliente, Reserva y EstadoReserva.", bold_prefix="4.3. Entidades: ")
    add_bullet(doc, "Capa de Acceso a Datos: GestorDAO desacopla el consumo de procedimientos almacenados de MySQL.", bold_prefix="4.4. DAO: ")
    add_bullet(doc, "Capa de Conexión: Conexion.cs provee instancias MySqlConnection bajo bloques using.", bold_prefix="4.5. Infraestructura: ")

    add_h1(doc, "5. Diagrama de Clases Simplificado (UML)", page_break_before=True)
    add_figure_apa7(
        doc,
        img_path=os.path.abspath("DB/Diagrama_Clases_UML.png"),
        fig_num="1",
        title="Diagrama de Clases Simplificado del Dominio (UML)",
        note_text="Diagrama UML exhibiendo la jerarquía de herencia de Recurso, la interfaz IReservable y la relación con la capa DAO.",
        width=Inches(6.2)
    )

    add_h1(doc, "6. Programación Orientada a Objetos y Clases C#", page_break_before=True)
    add_h2(doc, "6.1. Conexión centralizada (Conexion.cs)")
    add_p(doc, "Clase static con método CrearConexion(). Entrega instancias de MySqlConnection que se abren puntualmente con using, garantizando su cierre automático con Dispose().")

    add_h2(doc, "6.2. Interfaz de disponibilidad (IReservable.cs)")
    add_p(doc, "Contrato formal bool PuedeReservarse(DateTime fecha). Desacopla la verificación de disponibilidad de la jerarquía de herencia.")

    add_h2(doc, "6.3. Enumerador de estado (EstadoReserva.cs)")
    add_p(doc, "Enum con valores Pendiente, Confirmada, Cancelada y Finalizada, asegurando fuerte tipado.")

    add_h2(doc, "6.4. Clase base abstracta (Recurso.cs) y justificación")
    add_p(doc, "No se instancian recursos genéricos porque los clientes alquilan tipos específicos de espacios. Agrupa propiedades comunes y declara el método abstracto CalcularCosto(int horas).")

    add_h2(doc, "6.5. Clases derivadas especializadas")
    add_bullet(doc, "Sala: Propiedad CantSillas. Adicional de $8.000 (>30 sillas) o $16.000 (>60 sillas).", bold_prefix="Sala: ")
    add_bullet(doc, "OficinaPrivada: Propiedad MobiliarioIncluido. Canon fijo adicional de $1.500 si viene amueblada.", bold_prefix="OficinaPrivada: ")
    add_bullet(doc, "PuestoTrabajo: Propiedad NroCategoria. Plus de $3.500 (cat 1), $5.500 (cat 2) u $8.000 (cat 3).", bold_prefix="PuestoTrabajo: ")

    add_h2(doc, "6.6. Polimorfismo: Justificación de CalcularCosto(horas)")
    add_p(doc,
        "Permite que una referencia de tipo Recurso invoque CalcularCosto dinámicamente en tiempo de ejecución sin switch ni condicionales acoplados, respetando el Principio Abierto/Cerrado (OCP)."
    )

    poly_code = """public override decimal CalcularCosto(int horas)
{
    decimal costo = PrecioPorHora * horas;
    if (CantSillas > 60) costo += 16000;
    else if (CantSillas > 30) costo += 8000;
    return costo;
}"""
    add_code_snippet(doc, poly_code, caption="Código 1: Sobrescritura polimórfica en Sala.cs")

    add_h2(doc, "6.7. Clases de entidad (Cliente.cs y Reserva.cs)")
    add_p(doc, "Modelan los datos del cliente y la reserva intermedia que conecta cliente, espacio y horario.")

    add_h2(doc, "6.8. Gestión en memoria con LINQ (GestoraCoworking.cs)")
    add_p(doc, "Administra List<Reserva> en memoria principal mediante consultas LINQ (Where, FirstOrDefault).")

    add_h2(doc, "6.9. Evolución hacia el patrón DAO (GestorDAO.cs)")
    add_p(doc, "Desacopla a los formularios de cualquier instrucción ADO.NET o procedimiento SQL, aplicando Responsabilidad Única.")

    add_h1(doc, "7. Manejo de Errores y Excepciones (MySQL + C#)", page_break_before=True)
    add_p(doc, "Se implementa captura diferenciada de excepciones mediante MySqlException:")

    err_code = """try
{
    // Ejecución de procedimiento almacenado sp_alta_reserva
}
catch (MySqlException ex)
{
    if (ex.Number == 1644 || ex.SqlState == "45000")
        MessageBox.Show("Aviso de Negocio: " + ex.Message, "Disponibilidad", MessageBoxButtons.OK, MessageBoxIcon.Warning);
    else
        MessageBox.Show("Error Técnico MySQL: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
}
catch (Exception ex)
{
    MessageBox.Show("Error Inesperado: " + ex.Message, "Error General", MessageBoxButtons.OK, MessageBoxIcon.Error);
}"""
    add_code_snippet(doc, err_code, caption="Código 2: Captura estructurada de SIGNAL 45000 y errores generales")

    add_h1(doc, "8. Requerimientos Evolutivos (JSON y Configuración Externa)", page_break_before=False)
    add_p(doc, "Se documenta el esquema JSON de intercambio para exportación de catálogos y la migración de la cadena a App.config.")

    add_h1(doc, "9. Instrucciones para la Ejecución del Proyecto", page_break_before=False)
    add_bullet(doc, "Iniciar MySQL en XAMPP (puerto 3306).", bold_prefix="1. Persistencia: ")
    add_bullet(doc, "Ejecutar DB/DB_TPFinal.sql en phpMyAdmin o Workbench.", bold_prefix="2. Carga BD: ")
    add_bullet(doc, "Abrir SistemaDeGestion.slnx en Visual Studio 2022 y compilar con F5.", bold_prefix="3. Compilación: ")

    add_h1(doc, "10. Referencias Bibliográficas (APA 7.ª edición)", page_break_before=True)
    references = [
        ("Freeman, E., & Robson, E. (2020). ", "Head First Design Patterns", " (2.ª ed.). O'Reilly Media."),
        ("Martin, R. C. (2018). ", "Clean Architecture: A Craftsman's Guide to Software Structure and Design", ". Prentice Hall."),
        ("Microsoft Corporation. (2023). ", "Documentación de C# y .NET", ". Microsoft Learn. https://learn.microsoft.com/es-es/dotnet/csharp/"),
        ("Oracle Corporation. (2024). ", "MySQL 8.0 Reference Manual", ". Oracle Help Center. https://dev.mysql.com/doc/refman/8.0/en/")
    ]
    for authors, book_title, rest in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r1 = p_ref.add_run(authors)
        r1.font.color.rgb = COLOR_TEXT_BLACK
        r2 = p_ref.add_run(book_title)
        r2.font.italic = True
        r2.font.color.rgb = COLOR_TEXT_BLACK
        r3 = p_ref.add_run(rest)
        r3.font.color.rgb = COLOR_TEXT_BLACK

    save_doc_safely(doc, "Documentacion_Desarrollo")


# =============================================================================
# 3. DOCUMENTO MODULAR: Diccionario_de_Datos
# =============================================================================
def generate_diccionario():
    doc = Document()
    setup_document(doc)
    add_institutional_cover(doc, "DICCIONARIO DE DATOS", "Estructura de Base de Datos MySQL, Tablas, Vistas, Funciones y Procedimientos")
    start_body_section(doc, "Diccionario de Datos")

    diccionario_toc = [
        ("1. Información General y Esquema Relacional", "3", 1),
        ("2. Diagramas Entidad-Relación (DER)", "3", 1),
        ("3. Estructura Detallada de Tablas", "4", 1),
        ("3.1. Tabla: tipo_recursos", "4", 2),
        ("3.2. Tabla: recursos", "4", 2),
        ("3.3. Tabla: clientes", "5", 2),
        ("3.4. Tabla: reservas", "5", 2),
        ("3.5. Tabla: auditoria_reservas", "6", 2),
        ("4. Relaciones y Claves Foráneas", "6", 1),
        ("5. Vistas del Sistema", "7", 1),
        ("6. Funciones Almacenadas", "7", 1),
        ("7. Procedimientos Almacenados con SIGNAL 45000", "8", 1),
        ("8. Trigger de Auditoría Automática", "8", 1),
        ("9. Referencias Bibliográficas (APA 7.ª edición)", "9", 1)
    ]
    add_toc(doc, diccionario_toc)

    add_h1(doc, "1. Información General y Esquema Relacional", page_break_before=True)
    add_p(doc,
        "La base de datos tp_final_db se encuentra implementada sobre el motor relacional MySQL/MariaDB bajo XAMPP. "
        "Consta de 5 tablas normalizadas en Tercera Forma Normal (3NF), 2 vistas analíticas, 1 función determinística de disponibilidad, 1 trigger de auditoría y 8 procedimientos almacenados."
    )

    add_h1(doc, "2. Diagramas Entidad-Relación (DER)", page_break_before=False)
    add_figure_apa7(
        doc,
        img_path=os.path.abspath("DB/Diagrama_DER.png"),
        fig_num="1",
        title="Diagrama Entidad-Relación (DER) en MySQL Workbench",
        note_text="Exportación relacional directa desde MySQL Workbench 8.0 CE.",
        width=Inches(6.2)
    )

    add_figure_apa7(
        doc,
        img_path=os.path.abspath("DB/Diagrama_DER_Borrador.png"),
        fig_num="2",
        title="Diagrama Conceptual de Bloques y Entidades",
        note_text="Esquema conceptual previo consensuado por el equipo de desarrollo.",
        width=Inches(5.6)
    )

    add_h1(doc, "3. Estructura Detallada de Tablas", page_break_before=True)
    headers = ["Campo", "Tipo de Dato", "Nulo", "Clave", "Descripción"]

    add_h2(doc, "3.1. Tabla: tipo_recursos")
    t1 = doc.add_table(rows=3, cols=5)
    for j, h in enumerate(headers): t1.cell(0, j).paragraphs[0].text = h
    t1_data = [
        ["id_tipo_recurso", "INT", "NO", "PK (AI)", "Identificador unívoco del tipo de espacio."],
        ["nombre_tipo", "VARCHAR(100)", "NO", "-", "Nombre de la categoría (Sala, Oficina, Puesto)."]
    ]
    for i, r in enumerate(t1_data):
        for j, val in enumerate(r): t1.cell(i+1, j).paragraphs[0].text = val
    format_table(t1, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h2(doc, "3.2. Tabla: recursos")
    t2 = doc.add_table(rows=10, cols=5)
    for j, h in enumerate(headers): t2.cell(0, j).paragraphs[0].text = h
    t2_data = [
        ["id_recurso", "INT", "NO", "PK (AI)", "Identificador unívoco del espacio físico."],
        ["nombre", "VARCHAR(100)", "NO", "-", "Nombre del espacio (ej. Sala Innovación)."],
        ["descripcion", "TEXT", "SÍ", "-", "Detalle de equipamiento y comodidades."],
        ["ubicacion", "VARCHAR(100)", "NO", "-", "Ubicación edilicia (Piso y sector)."],
        ["precio_por_hora", "DECIMAL(10,2)", "NO", "-", "Tarifa base monetaria por hora."],
        ["mobiliario_incluido", "BOOLEAN", "SÍ", "-", "Aplica a oficinas: indica si incluye muebles."],
        ["cantidad_sillas", "INT", "SÍ", "-", "Aplica a salas: cantidad total de sillas."],
        ["nro_categoria", "INT", "SÍ", "-", "Aplica a puestos: nivel del box (1, 2 o 3)."],
        ["id_tipo_recurso", "INT", "NO", "FK", "Referencia a tipo_recursos."]
    ]
    for i, r in enumerate(t2_data):
        for j, val in enumerate(r): t2.cell(i+1, j).paragraphs[0].text = val
    format_table(t2, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h2(doc, "3.3. Tabla: clientes")
    t3 = doc.add_table(rows=7, cols=5)
    for j, h in enumerate(headers): t3.cell(0, j).paragraphs[0].text = h
    t3_data = [
        ["id_cliente", "INT", "NO", "PK (AI)", "Identificador unívoco del cliente."],
        ["nombre", "VARCHAR(100)", "NO", "-", "Nombre de pila."],
        ["apellido", "VARCHAR(100)", "NO", "-", "Apellido."],
        ["telefono", "VARCHAR(20)", "NO", "-", "Teléfono de contacto."],
        ["mail", "VARCHAR(255)", "NO", "-", "Correo electrónico."],
        ["fecha_registro", "DATETIME", "NO", "Default Now", "Fecha y hora de alta."]
    ]
    for i, r in enumerate(t3_data):
        for j, val in enumerate(r): t3.cell(i+1, j).paragraphs[0].text = val
    format_table(t3, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h2(doc, "3.4. Tabla: reservas")
    t4 = doc.add_table(rows=8, cols=5)
    for j, h in enumerate(headers): t4.cell(0, j).paragraphs[0].text = h
    t4_data = [
        ["id_reserva", "INT", "NO", "PK (AI)", "Identificador unívoco de la reserva."],
        ["id_cliente", "INT", "NO", "FK", "Cliente titular (clientes.id_cliente)."],
        ["id_recurso", "INT", "NO", "FK", "Espacio reservado (recursos.id_recurso)."],
        ["fecha_reserva", "DATETIME", "NO", "-", "Día y hora de inicio."],
        ["horas", "INT", "NO", "Default 1", "Duración en horas."],
        ["total", "DECIMAL(10,2)", "NO", "-", "Monto final facturado."],
        ["estado", "VARCHAR(20)", "NO", "Default Conf", "'Confirmada', 'Cancelada' o 'Pendiente'."]
    ]
    for i, r in enumerate(t4_data):
        for j, val in enumerate(r): t4.cell(i+1, j).paragraphs[0].text = val
    format_table(t4, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h2(doc, "3.5. Tabla: auditoria_reservas")
    t5 = doc.add_table(rows=6, cols=5)
    for j, h in enumerate(headers): t5.cell(0, j).paragraphs[0].text = h
    t5_data = [
        ["id_auditoria", "INT", "NO", "PK (AI)", "Identificador secuencial."],
        ["id_reserva", "INT", "NO", "-", "ID de la reserva cancelada."],
        ["accion", "VARCHAR(50)", "NO", "-", "Descripción ('Cancelacion de reserva')."],
        ["fecha_accion", "DATETIME", "NO", "Default Now", "Momento exacto de la baja."],
        ["usuario", "VARCHAR(100)", "SÍ", "Default Sist", "Usuario que ejecutó la operación."]
    ]
    for i, r in enumerate(t5_data):
        for j, val in enumerate(r): t5.cell(i+1, j).paragraphs[0].text = val
    format_table(t5, [Inches(1.5), Inches(1.1), Inches(0.6), Inches(1.0), Inches(2.3)])

    add_h1(doc, "4. Relaciones y Claves Foráneas", page_break_before=False)
    add_bullet(doc, "fk_recursos_tipo: Une recursos.id_tipo_recurso con tipo_recursos.id_tipo_recurso.", bold_prefix="fk_recursos_tipo: ")
    add_bullet(doc, "fk_reservas_cliente: Une reservas.id_cliente con clientes.id_cliente.", bold_prefix="fk_reservas_cliente: ")
    add_bullet(doc, "fk_reservas_recurso: Une reservas.id_recurso con recursos.id_recurso.", bold_prefix="fk_reservas_recurso: ")

    add_h1(doc, "5. Vistas del Sistema", page_break_before=False)
    add_bullet(doc, "Combina reservas, clientes y recursos mediante INNER JOIN proyectando nombres legibles.", bold_prefix="vw_detalle_reservas: ")
    add_bullet(doc, "Agrupa por recurso calculando reservas confirmadas y monto total acumulado con GROUP BY.", bold_prefix="vw_resumen_recursos: ")

    add_h1(doc, "6. Funciones Almacenadas", page_break_before=False)
    add_p(doc,
        "fn_verificar_disponibilidad(p_id_recurso, p_fecha, p_horas): Evalúa la condición estricta de solapamiento de intervalos temporales ((nuevo_inicio < fin_existente) AND (nuevo_fin > inicio_existente)) sobre reservas confirmadas. Devuelve 1 si el espacio está libre y 0 si existe conflicto."
    )

    add_h1(doc, "7. Procedimientos Almacenados con SIGNAL 45000", page_break_before=True)
    add_bullet(doc, "Inserta un nuevo cliente en el padrón.", bold_prefix="sp_alta_cliente: ")
    add_bullet(doc, "Actualiza datos de contacto de un cliente existente.", bold_prefix="sp_modificar_cliente: ")
    add_bullet(doc, "Registra un nuevo espacio físico con tarifas y comodidades.", bold_prefix="sp_alta_recurso: ")
    add_bullet(doc, "Modifica la información o tarifas de un recurso existente.", bold_prefix="sp_modificar_recurso: ")
    add_bullet(doc, "Valida horas e invoca fn_verificar_disponibilidad. Si hay superposición emite SIGNAL SQLSTATE '45000'.", bold_prefix="sp_alta_reserva (Con SIGNAL 45000): ")
    add_bullet(doc, "Permite reprogramar fecha u horario comprobando disponibilidad con las demás reservas confirmadas.", bold_prefix="sp_modificar_reserva: ")
    add_bullet(doc, "Pasa la reserva a 'Cancelada'. Si no existe o ya estaba cancelada emite SIGNAL 45000.", bold_prefix="sp_cancelar_reserva: ")
    add_bullet(doc, "Cursor de MySQL que totaliza los montos facturados de reservas confirmadas.", bold_prefix="sp_calcular_total_recaudado_cursor (Cursor): ")

    add_h1(doc, "8. Trigger de Auditoría Automática", page_break_before=False)
    add_p(doc, "trg_auditoria_reservas: Disparador AFTER UPDATE en reservas. Inserta en auditoria_reservas cuando una reserva muta a 'Cancelada'.")

    add_h1(doc, "9. Referencias Bibliográficas (APA 7.ª edición)", page_break_before=False)
    add_p(doc, "Oracle Corporation. (2024). MySQL 8.0 Reference Manual. Oracle Help Center. https://dev.mysql.com/doc/refman/8.0/en/")

    save_doc_safely(doc, "Diccionario_de_Datos")


# =============================================================================
# 4. DOCUMENTO MODULAR: Manual_de_Usuario
# =============================================================================
def generate_manual():
    doc = Document()
    setup_document(doc)
    add_institutional_cover(doc, "MANUAL DE USUARIO", "Guía de Operación del Sistema para Perfiles Operativo y Administrador")
    start_body_section(doc, "Manual de Usuario")

    manual_toc = [
        ("1. Requisitos Previos para el Encendido del Sistema", "3", 1),
        ("2. Pantalla de Inicio de Sesión (FrmLogin)", "3", 1),
        ("2.1. Credenciales de Nivel Administrador", "3", 2),
        ("2.2. Validación de Credenciales y Control de Errores", "3", 2),
        ("2.3. Asistencia Técnica Directa vía WhatsApp", "4", 2),
        ("3. Pantalla Principal (FrmPrincipal) — Modo Operativo", "4", 1),
        ("3.1. Solapa CONTROL: Registro de Nuevas Reservas", "4", 2),
        ("3.2. Solapa RESERVAS: Consulta, Reprogramación y Cancelación", "5", 2),
        ("4. Módulo de Administración (Solapa GESTIÓN)", "5", 1),
        ("4.1. Desbloqueo y Acceso al Módulo Administrativo", "5", 2),
        ("4.2. Alternancia Dinámica entre Usuarios y Recursos", "5", 2),
        ("4.3. Operaciones de Mantenimiento (Crear, Modificar, Eliminar)", "6", 2),
        ("4.4. Cierre de Sesión y Protección de Datos", "6", 2),
        ("5. Estado de Avance del Proyecto y Próximas Etapas", "6", 1)
    ]
    add_toc(doc, manual_toc)

    add_h1(doc, "1. Requisitos Previos para el Encendido del Sistema", page_break_before=True)
    add_bullet(doc, "Iniciar XAMPP Control Panel y presionar 'Start' en MySQL (puerto 3306 en verde).", bold_prefix="Paso 1: ")
    add_bullet(doc, "Ejecutar por única vez el script DB/DB_TPFinal.sql en phpMyAdmin o MySQL Workbench para inicializar tablas y datos.", bold_prefix="Paso 2: ")
    add_bullet(doc, "Abrir la solución SistemaDeGestion.slnx en Visual Studio 2022 y presionar F5.", bold_prefix="Paso 3: ")

    add_h1(doc, "2. Pantalla de Inicio de Sesión (FrmLogin)", page_break_before=False)
    add_h2(doc, "2.1. Credenciales de Nivel Administrador")
    add_bullet(doc, "Admin", bold_prefix="Usuario: ")
    add_bullet(doc, "123456 (caracteres protegidos visualmente por asteriscos).", bold_prefix="Contraseña: ")

    add_h2(doc, "2.2. Validación de Credenciales y Control de Errores")
    add_p(doc, "Si se ingresa un dato erróneo, el sistema advierte específicamente si falló el Usuario o la Contraseña y posiciona automáticamente el foco del cursor para su corrección rápida.")

    add_h2(doc, "2.3. Asistencia Técnica Directa vía WhatsApp")
    add_p(doc, "El enlace '¿Necesitas ayuda? Contactar soporte' abre WhatsApp con un mensaje predefinido dirigido a la línea de soporte oficial (+54 9 223 301-4626), facilitando la asistencia humana inmediata.")

    add_h1(doc, "3. Pantalla Principal (FrmPrincipal) — Modo Operativo", page_break_before=True)
    add_h2(doc, "3.1. Solapa CONTROL: Registro de Nuevas Reservas")
    add_bullet(doc, "Selector de Cliente: Menú desplegable con los clientes registrados.", bold_prefix="Cliente: ")
    add_bullet(doc, "Tipo de Recurso: Selector de Sala, Oficina o Puesto.", bold_prefix="Recurso: ")
    add_bullet(doc, "Fecha y Horas: Calendario gráfico y control numérico con flechas.", bold_prefix="Período: ")
    add_bullet(doc, "Total y Botones: Visor con el importe calculado automáticamente y botón Agregar.", bold_prefix="Confirmación: ")

    add_h2(doc, "3.2. Solapa RESERVAS: Consulta, Reprogramación y Cancelación")
    add_p(doc, "Grilla amplia (DataGridView) con todas las reservas registradas. Los botones 'Modificar Reserva' y 'Eliminar Reserva' permiten reprogramar o dar de baja un turno con auditoría automática.")

    add_h1(doc, "4. Módulo de Administración (Solapa GESTIÓN)", page_break_before=True)
    add_h2(doc, "4.1. Desbloqueo y Acceso al Módulo Administrativo")
    add_p(doc, "Desde el menú superior 'Menú' -> 'Ingresar como Administrador'. Tras validar la clave, se inserta dinámicamente la solapa GESTIÓN.")

    add_h2(doc, "4.2. Alternancia Dinámica entre Usuarios y Recursos")
    add_p(doc, "Dos RadioButtons ('Usuarios' y 'Recursos') conmutan instantáneamente el título y la tabla visible entre Clientes y Espacios Físicos.")

    add_h2(doc, "4.3. Operaciones de Mantenimiento (Crear, Modificar, Eliminar)")
    add_p(doc, "Botones de acción que permiten dar altas, modificaciones y bajas sobre el catálogo activo.")

    add_h2(doc, "4.4. Cierre de Sesión y Protección de Datos")
    add_p(doc, "La opción 'Cerrar sesión' en el menú superior oculta la solapa administrativa, protegiendo los datos de accesos no autorizados.")

    add_h1(doc, "5. Estado de Avance del Proyecto y Próximas Etapas", page_break_before=False)
    add_bullet(doc, "Base de datos completa con reglas SIGNAL 45000, trigger y función. Modelos C# con clase abstracta, herencia funcional, polimorfismo en CalcularCosto, interfaz IReservable y gestora con LINQ. Interfaz Windows Forms con login, roles, control de permisos y asistencia por WhatsApp.", bold_prefix="100% Funcional hoy: ")
    add_bullet(doc, "Completar la vinculación con MySQL mediante GestorDAO.cs e incorporar el módulo de exportación/importación JSON.", bold_prefix="Próximas etapas: ")

    save_doc_safely(doc, "Manual_de_Usuario")


# =============================================================================
# EXPORTACIÓN AUTOMÁTICA A PDF MEDIANTE WORD COM
# =============================================================================
def export_docs_to_pdf():
    ps_script = """
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $files = @("TP_Final_AlgoritmosII_Grupo2", "Documentacion_Desarrollo", "Diccionario_de_Datos", "Manual_de_Usuario")
    foreach ($f in $files) {
        $docxPath = Join-Path (Get-Location) "Documentacion\\$f.docx"
        if (Test-Path $docxPath) {
            $pdfPath = $docxPath.Replace(".docx", ".pdf")
            $doc = $word.Documents.Open($docxPath)
            $doc.SaveAs([ref]$pdfPath, [ref]17)
            $doc.Close(0)
            Write-Host "PDF generado exitosamente: $pdfPath"
        }
    }
    $word.Quit()
    """
    try:
        res = subprocess.run(["powershell", "-Command", ps_script], check=True, capture_output=True, text=True)
        print(res.stdout)
        print("Exportación a PDF completada exitosamente.")
    except Exception as e:
        print(f"Aviso durante la exportación a PDF: {e}")

if __name__ == "__main__":
    generate_master_document()
    generate_desarrollo()
    generate_diccionario()
    generate_manual()
    export_docs_to_pdf()
