# -*- coding: utf-8 -*-
import re
from PIL import Image, ImageDraw, ImageFont

# Canvas amplio de alta resolucion (2100 x 2550)
W = 2100
H = 2550
img = Image.new("RGB", (W, H), color="#FFFFFF")
draw = ImageDraw.Draw(img)

# Fuentes
try:
    font_main_title = ImageFont.truetype("arialbd.ttf", 36)
    font_main_sub   = ImageFont.truetype("arial.ttf", 22)
    font_box_title  = ImageFont.truetype("arialbd.ttf", 20)
    font_text       = ImageFont.truetype("arial.ttf", 17)
    font_bold       = ImageFont.truetype("arialbd.ttf", 17)
    font_lbl        = ImageFont.truetype("arialbd.ttf", 16)
    font_lbl_reg    = ImageFont.truetype("arial.ttf", 16)
except:
    font_main_title = font_main_sub = font_box_title = font_text = font_bold = font_lbl = font_lbl_reg = ImageFont.load_default()

def draw_rich_text(draw, x, y, text, default_font, bold_font, color="#000000"):
    """Dibuja texto soportando etiquetas <b>...</b> para negrita."""
    parts = re.split(r"(<b>.*?</b>)", text)
    curr_x = x
    for part in parts:
        if not part:
            continue
        if part.startswith("<b>") and part.endswith("</b>"):
            clean_part = part[3:-4]
            f = bold_font
        else:
            clean_part = part
            f = default_font
        draw.text((curr_x, y), clean_part, fill=color, font=f)
        bbox = draw.textbbox((0, 0), clean_part, font=f)
        curr_x += (bbox[2] - bbox[0])

def draw_box(x, y, w, h, title, lines=[], fill_header="#F5F5F5", border_w=2):
    draw.rectangle([x, y, x + w, y + h], fill="#FFFFFF", outline="#000000", width=border_w)
    header_h = 36
    draw.rectangle([x, y, x + w, y + header_h], fill=fill_header, outline="#000000", width=2)
    
    # Titulo cabecera centrado
    parts = re.split(r"(<b>.*?</b>)", title)
    total_w = 0
    for part in parts:
        if not part: continue
        clean_part = part[3:-4] if (part.startswith("<b>") and part.endswith("</b>")) else part
        bbox = draw.textbbox((0, 0), clean_part, font=font_box_title)
        total_w += (bbox[2] - bbox[0])
    
    start_x = x + (w - total_w) / 2
    draw_rich_text(draw, start_x, y + 8, title, font_box_title, font_box_title)
    
    # Lineas
    curr_y = y + header_h + 10
    for line in lines:
        draw_rich_text(draw, x + 12, curr_y, line, font_text, font_bold)
        curr_y += 24

def draw_arrow_down(x, y1, y2, label=""):
    draw.line([x, y1, x, y2], fill="#000000", width=2)
    draw.polygon([(x, y2), (x - 6, y2 - 12), (x + 6, y2 - 12)], fill="#000000")
    if label:
        draw_rich_text(draw, x + 10, (y1 + y2) / 2 - 10, label, font_lbl_reg, font_lbl)

def draw_arrow_right(x1, y, x2, label=""):
    draw.line([x1, y, x2, y], fill="#000000", width=2)
    draw.polygon([(x2, y), (x2 - 12, y - 6), (x2 - 12, y + 6)], fill="#000000")
    if label:
        bbox = draw.textbbox((0, 0), label.replace("<b>", "").replace("</b>", ""), font=font_lbl)
        tw = bbox[2] - bbox[0]
        draw_rich_text(draw, (x1 + x2 - tw) / 2, y - 24, label, font_lbl_reg, font_lbl)

# =========================================================================
# TÍTULO SUPERIOR
# =========================================================================
draw.text((W/2 - 420, 25), "SISTEMA DE GESTIÓN DE COWORKING", fill="#000000", font=font_main_title)
draw.text((W/2 - 380, 72), "Diagrama Integral: Pantallas, Lógica en C# y Objetos de Base de Datos", fill="#333333", font=font_main_sub)
draw.line([60, 110, W - 60, 110], fill="#000000", width=2)

# =========================================================================
# 1. PANTALLA PRINCIPAL Y ACCESO ADMINISTRADOR
# =========================================================================
draw_box(60, 130, 1160, 120, "Ventana Principal (CoWorking - DASHBOARD)", [
    "• Inicia directamente aquí al abrir el software en <b>Modo Estándar</b>.",
    "• Muestra inicialmente solo las solapas: <b>CONTROL</b> y <b>RESERVAS</b>.",
    "• Menú superior: botón para iniciar sesión como Administrador."
], border_w=3)

draw_arrow_right(1220, 190, 1420, "Menú: Iniciar Sesión")

draw_box(1420, 130, 620, 120, "Acceso Administrador (FrmLogin)", [
    "• Usuario: <b>Admin</b>  |  Clave: <b>123456</b>",
    "• Control estricto por teclado y soporte WhatsApp.",
    "• Al ingresar: desbloquea solapas de gestión administrativa."
])

# Flecha desde Login hacia solapas admin
draw.line([1730, 250, 1730, 280], fill="#000000", width=2)
draw_arrow_down(1730, 280, 325, "Desbloquea solapas")

# Flecha desde FrmPrincipal hacia las 2 solapas iniciales
draw.line([300, 250, 300, 285], fill="#000000", width=2)
draw.line([830, 250, 830, 285], fill="#000000", width=2)
draw_arrow_down(300, 285, 325, "Visible al inicio")
draw_arrow_down(830, 285, 325, "Visible al inicio")

# =========================================================================
# 2. SOLAPAS DE LA VENTANA PRINCIPAL (UI)
# =========================================================================
# SOLAPA 1: CONTROL (Crear Reserva)
draw_box(60, 325, 480, 245, "Solapa: CONTROL (Crear reserva)", [
    "• Formulario activo al iniciar el sistema:",
    "  - Cliente (selector de clientes)",
    "  - Tipo de Recurso (sala, oficina o puesto)",
    "  - Fecha y Horario de inicio del turno",
    "  - Horas de uso (duración 1 a 24 hs)",
    "  - Valor a abonar (calculado en tiempo real)",
    "",
    "<b>BOTÓN: [ AGREGAR ]</b>"
], fill_header="#EAEAEA", border_w=3)

# SOLAPA 2: RESERVAS (Grilla y Acciones de turno)
draw_box(570, 325, 520, 245, "Solapa: RESERVAS (Gestión de turnos)", [
    "• Muestra tabla de reservas confirmadas.",
    "• Consulta la Vista: <b>vw_detalle_reservas</b>.",
    "• Botón <b>Modificar Reserva</b> (abre modal):",
    "  Aplica cambios con <b>sp_modificar_reserva</b>.",
    "• Botón <b>Cancelar Reserva</b>:",
    "  Cancela turno con <b>sp_cancelar_reserva</b>.",
    "  (Activa auditoría automática en MySQL)."
], fill_header="#EAEAEA", border_w=2)

# SOLAPAS DESBLOQUEADAS POR ADMIN (Derecha)
draw_box(1120, 325, 440, 115, "Solapa: CLIENTES (Admin)", [
    "• Padrón de clientes registrados.",
    "• Botones: Nuevo / Modificar / Eliminar."
])
draw_arrow_down(1340, 440, 475, "Abre ventana modal")
draw_box(1120, 475, 440, 95, "Editor de Clientes (FrmEditorClientes)", [
    "• Ejecuta: <b>sp_alta_cliente</b>,",
    "  <b>sp_modificar_cliente</b> y <b>sp_eliminar_cliente</b>."
])

draw_box(1590, 325, 450, 115, "Solapa: RECURSOS (Admin)", [
    "• Catálogo de salas, oficinas y escritorios.",
    "• Botones: Nuevo / Modificar / Eliminar."
])
draw_arrow_down(1815, 440, 475, "Abre ventana modal")
draw_box(1590, 475, 450, 95, "Editor de Recursos (FrmEditorRecursos)", [
    "• Ejecuta: <b>sp_alta_recurso</b>,",
    "  <b>sp_modificar_recurso</b> y <b>sp_eliminar_recurso</b>."
])

# =========================================================================
# 3. LÓGICA DE NEGOCIO (C# .NET)
# =========================================================================
draw_arrow_down(300, 570, 630, "Presiona botón [ AGREGAR ]")

draw_box(60, 630, 1980, 125, "Lógica del Sistema (Capa Gestora y Modelos C#)", [
    "• Recibe los datos cargados en la pantalla (cliente, espacio, fecha y horas).",
    "• Aplica tarifas mediante el método polimórfico <b>CalcularCosto()</b> según el tipo de recurso (Sala, Oficina o Puesto).",
    "• Administra la conexión mediante <b>Conexion.cs</b> y despacha los Procedimientos Almacenados hacia la Base de Datos."
], border_w=3)

# =========================================================================
# 4. BASE DE DATOS RELACIONAL (MySQL - tp_final_db)
# =========================================================================
draw_arrow_down(750, 755, 810, "Ejecuta Procedimiento Almacenado")

# Procedimiento sp_alta_reserva
draw_box(250, 810, 1000, 115, "Procedimiento Almacenado: <b>sp_alta_reserva</b>", [
    "• Recibe los parámetros: cliente, espacio, fecha, horas e importe total.",
    "• Invoca la Función: <b>fn_verificar_disponibilidad</b> para comprobar el horario.",
    "• Si el horario está libre guarda la fila; si no, interrumpe con <b>SIGNAL 45000</b>."
], border_w=2)

draw_arrow_down(750, 925, 980, "Evalúa disponibilidad")

# Rombo de decisión disponibilidad
rx, ry, rw, rh = 750, 1090, 720, 210
rombo_pts = [(rx, ry - rh/2), (rx + rw/2, ry), (rx, ry + rh/2), (rx - rw/2, ry)]
draw.polygon(rombo_pts, fill="#FBFBFB", outline="#000000")
draw.line(rombo_pts + [rombo_pts[0]], fill="#000000", width=3)

draw.text((rx - 170, ry - 32), "¿El horario está libre?", fill="#000000", font=font_main_title)

# Subtexto rombo
func_txt = "(Función: <b>fn_verificar_disponibilidad</b>)"
parts = re.split(r"(<b>.*?</b>)", func_txt)
tw = 0
for p in parts:
    clean_p = p[3:-4] if (p.startswith("<b>") and p.endswith("</b>")) else p
    f = font_lbl if (p.startswith("<b>") and p.endswith("</b>")) else font_lbl_reg
    bbox = draw.textbbox((0, 0), clean_p, font=f)
    tw += (bbox[2] - bbox[0])
draw_rich_text(draw, rx - tw / 2, ry + 12, func_txt, font_lbl_reg, font_lbl)

# -------------------------------------------------------------------------
# RAMA SÍ: LIBRE = 1 (Izquierda)
# -------------------------------------------------------------------------
draw.line([rx - rw/2, ry, 260, ry], fill="#000000", width=2)
draw_arrow_down(260, ry, 1260, "")
draw.rectangle([270, ry - 30, 440, ry - 5], fill="#FFFFFF", outline="#000000", width=1)
draw.text((285, ry - 26), "SÍ (Libre = 1)", fill="#000000", font=font_lbl)

draw_box(60, 1260, 480, 125, "Guarda Reserva (<b>INSERT</b>)", [
    "• Ejecuta <b>INSERT INTO reservas</b>.",
    "• Guarda con estado: 'Confirmada'.",
    "• Transacción finalizada con éxito."
], fill_header="#EAEAEA", border_w=3)

draw_arrow_down(260, 1385, 1450, "")
draw_box(60, 1450, 480, 130, "Resultado: Grilla Actualizada", [
    "• C# consulta la Vista: <b>vw_detalle_reservas</b>.",
    "• Aparece la nueva reserva en la tabla.",
    "• Cartel: 'Reserva confirmada con éxito'."
], border_w=2)

# -------------------------------------------------------------------------
# RAMA NO: OCUPADO = 0 (Centro / Derecha)
# -------------------------------------------------------------------------
draw.line([rx + rw/2, ry, 1240, ry], fill="#000000", width=2)
draw_arrow_down(1240, ry, 1260, "")
draw.rectangle([1030, ry - 30, 1220, ry - 5], fill="#FFFFFF", outline="#000000", width=1)
draw.text((1045, ry - 26), "NO (Ocupado = 0)", fill="#000000", font=font_lbl)

draw_box(1000, 1260, 480, 125, "Alerta: Horario Ocupado", [
    "• Detecta solapamiento (resultado = <b>0</b>).",
    "• Dispara <b>SIGNAL SQLSTATE '45000'</b>.",
    "• Cancela la operación sin guardar nada."
], fill_header="#EAEAEA", border_w=3)

draw_arrow_down(1240, 1385, 1450, "")
draw_box(1000, 1450, 480, 130, "Resultado: Aviso en Pantalla", [
    "• C# captura la alerta (<b>catch MySqlException</b>).",
    "• La aplicación no falla ni se cierra.",
    "• Cuadro emergente (MessageBox): aviso."
], border_w=2)

# =========================================================================
# 5. MÓDULO DE AUDITORÍA Y CANCELACIONES (MySQL)
# =========================================================================
draw.line([60, 1630, W - 60, 1630], fill="#000000", width=2)
draw.text((80, 1650), "AUDITORÍA, CANCELACIÓN Y REPORTES EN LA BASE DE DATOS", fill="#000000", font=font_box_title)

# Flujo Cancelar -> Trigger
draw_box(60, 1690, 600, 160, "Cancelación: <b>sp_cancelar_reserva</b>", [
    "• Se ejecuta al hacer clic en 'Cancelar Reserva'.",
    "• Valida que la reserva exista y no esté ya cancelada.",
    "• Actualiza el estado a <b>'Cancelada'</b> en la tabla.",
    "• Este cambio de estado activa el Trigger."
], border_w=2)

draw_arrow_right(660, 1770, 770, "Dispara Trigger")

# Trigger Auditoria
draw_box(770, 1690, 640, 160, "Trigger: <b>trg_auditoria_reservas</b>", [
    "• Trigger automático: <b>AFTER UPDATE ON reservas</b>.",
    "• Se ejecuta solo en MySQL (no lo llama C#).",
    "• Inserta en la tabla <b>auditoria_reservas</b>:",
    "  - ID de la reserva cancelada.",
    "  - Acción: 'Cancelacion de reserva'.",
    "  - Fecha/hora exacta (NOW) y Usuario activo."
], fill_header="#EAEAEA", border_w=3)

# Flujo Vistas y Cursor (Derecha)
draw_box(1450, 1690, 590, 160, "Vista Analítica y Cursor (Reportes)", [
    "• Vista: <b>vw_resumen_recursos</b>:",
    "  Calcula total facturado y cantidad de turnos.",
    "• Procedimiento con Cursor:",
    "  <b>sp_calcular_total_recaudado_cursor</b>:",
    "  Recorre fila por fila sumando montos de reservas",
    "  confirmadas para calcular el total general."
], border_w=2)

# =========================================================================
# CUADRO DE RESUMEN DE OBJETOS SQL (PIE DE PÁGINA)
# =========================================================================
draw.line([60, 1900, W - 60, 1900], fill="#000000", width=2)

draw_box(60, 1930, 1980, 160, "MAPA DE OBJETOS FUNCIONALES DEL ARCHIVO SQL (tp_final_db)", [
    "• <b>Vistas (2):</b> <b>vw_detalle_reservas</b> (grilla principal con nombres reales)  |  <b>vw_resumen_recursos</b> (reporte de ingresos por sala).",
    "• <b>Función (1):</b> <b>fn_verificar_disponibilidad</b> (cálculo matemático de superposición de turnos: retorna 1 si está libre, 0 si está ocupado).",
    "• <b>Procedimientos (8):</b> <b>sp_alta_reserva</b>, <b>sp_modificar_reserva</b>, <b>sp_cancelar_reserva</b>, <b>sp_alta_cliente</b>, <b>sp_modificar_cliente</b>, <b>sp_eliminar_cliente</b>, <b>sp_alta_recurso</b>, <b>sp_modificar_recurso</b>.",
    "• <b>Cursor (1):</b> <b>sp_calcular_total_recaudado_cursor</b> (recorrido secuencial con cursor para suma total de reservas confirmadas).",
    "• <b>Trigger (1):</b> <b>trg_auditoria_reservas</b> (registro inmutable automático en tabla <b>auditoria_reservas</b> ante cada cancelación)."
], fill_header="#F0F0F0", border_w=2)

final_h = 2140
img_clean = img.crop((0, 0, W, final_h))

output_png = r"c:\xampp\htdocs\ALGORITMOS2\Trabajo_final_algoritmos\Documentacion\diagrama_imprimible.png"
img_clean.save(output_png, "PNG", dpi=(300, 300))
print("Diagrama con el 100% de los objetos SQL guardado exitosamente en:", output_png)
