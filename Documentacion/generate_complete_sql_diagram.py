# -*- coding: utf-8 -*-
import re
from PIL import Image, ImageDraw, ImageFont

# Canvas amplio de alta resolucion (2100 x 2650)
W = 2100
H = 2650
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

def draw_auto_box(x, y, w, title, lines=[], fill_header="#F5F5F5", border_w=2, line_spacing=26):
    """
    Dibuja una caja calculando su altura EXACTA de forma automática
    para que JAMÁS ningún texto desborde ni sea cortado por el borde inferior.
    """
    header_h = 38
    content_h = 14 + len(lines) * line_spacing + 14
    total_h = header_h + content_h
    
    # Fondo y bordes
    draw.rectangle([x, y, x + w, y + total_h], fill="#FFFFFF", outline="#000000", width=border_w)
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
    
    # Lineas de contenido
    curr_y = y + header_h + 12
    for line in lines:
        draw_rich_text(draw, x + 14, curr_y, line, font_text, font_bold)
        curr_y += line_spacing
        
    return total_h

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
h_main = draw_auto_box(60, 130, 1160, "Ventana Principal (CoWorking - DASHBOARD)", [
    "• Inicia directamente aquí al abrir el software en <b>Modo Estándar</b>.",
    "• Muestra inicialmente solo las solapas: <b>CONTROL</b> y <b>RESERVAS</b>.",
    "• Menú superior: botón para iniciar sesión como Administrador."
], border_w=3)

draw_arrow_right(1220, 190, 1420, "Menú: Iniciar Sesión")

h_login = draw_auto_box(1420, 130, 620, "Acceso Administrador (FrmLogin)", [
    "• Usuario: <b>Admin</b>  |  Clave: <b>123456</b>",
    "• Control estricto por teclado y soporte WhatsApp.",
    "• Al ingresar: desbloquea solapas de gestión administrativa."
])

# Flechas desde Login que bifurcan a AMBAS solapas de administracion (Clientes y Recursos)
y_branch_admin = 280
draw.line([1730, 130 + h_login, 1730, y_branch_admin], fill="#000000", width=2)
# Linea horizontal conectando el centro de CLIENTES (x=1340) y RECURSOS (x=1815)
draw.line([1340, y_branch_admin, 1815, y_branch_admin], fill="#000000", width=2)

draw_arrow_down(1340, y_branch_admin, 320, "Desbloquea solapa")
draw_arrow_down(1815, y_branch_admin, 320, "Desbloquea solapa")

# Flecha desde FrmPrincipal hacia las 2 solapas iniciales
draw.line([300, 130 + h_main, 300, 280], fill="#000000", width=2)
draw.line([830, 130 + h_main, 830, 280], fill="#000000", width=2)
draw_arrow_down(300, 280, 320, "Visible al inicio")
draw_arrow_down(830, 280, 320, "Visible al inicio")

# =========================================================================
# 2. SOLAPAS DE LA VENTANA PRINCIPAL (UI)
# =========================================================================
# SOLAPA 1: CONTROL (Crear Reserva)
h_tab1 = draw_auto_box(60, 320, 480, "Solapa: CONTROL (Crear reserva)", [
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
h_tab2 = draw_auto_box(570, 320, 520, "Solapa: RESERVAS (Gestión de turnos)", [
    "• Muestra tabla de reservas confirmadas.",
    "• Consulta la Vista: <b>vw_detalle_reservas</b>.",
    "• Botón <b>Modificar Reserva</b> (abre modal):",
    "  Aplica cambios con <b>sp_modificar_reserva</b>.",
    "• Botón <b>Cancelar Reserva</b>:",
    "  Cancela turno con <b>sp_cancelar_reserva</b>.",
    "  (Activa auditoría automática en MySQL)."
], fill_header="#EAEAEA", border_w=2)

# SOLAPAS DESBLOQUEADAS POR ADMIN (Derecha)
draw_auto_box(1120, 320, 440, "Solapa: CLIENTES (Admin)", [
    "• Padrón de clientes registrados.",
    "• Botones: Nuevo / Modificar / Eliminar."
])
draw_arrow_down(1340, 435, 470, "Abre ventana modal")
draw_auto_box(1120, 470, 440, "Editor de Clientes (FrmEditorClientes)", [
    "• Ejecuta: <b>sp_alta_cliente</b>,",
    "  <b>sp_modificar_cliente</b> y <b>sp_eliminar_cliente</b>."
])

draw_auto_box(1590, 320, 450, "Solapa: RECURSOS (Admin)", [
    "• Catálogo de salas, oficinas y escritorios.",
    "• Botones: Nuevo / Modificar / Eliminar."
])
draw_arrow_down(1815, 435, 470, "Abre ventana modal")
draw_auto_box(1590, 470, 450, "Editor de Recursos (FrmEditorRecursos)", [
    "• Ejecuta: <b>sp_alta_recurso</b>,",
    "  <b>sp_modificar_recurso</b> y <b>sp_eliminar_recurso</b>."
])

# =========================================================================
# 3. LÓGICA DE NEGOCIO (C# .NET)
# =========================================================================
y_logica = 320 + h_tab1 + 60
draw_arrow_down(300, 320 + h_tab1, y_logica, "Presiona botón [ AGREGAR ]")

h_logica = draw_auto_box(60, y_logica, 1980, "Lógica del Sistema (Capa Gestora y Modelos C#)", [
    "• Recibe los datos cargados en la pantalla (cliente, espacio, fecha y horas).",
    "• Aplica tarifas mediante el método polimórfico <b>CalcularCosto()</b> según el tipo de recurso (Sala, Oficina o Puesto).",
    "• Administra la conexión mediante <b>Conexion.cs</b> y despacha los Procedimientos Almacenados hacia la Base de Datos."
], border_w=3)

# =========================================================================
# 4. BASE DE DATOS RELACIONAL (MySQL - tp_final_db)
# =========================================================================
y_sp = y_logica + h_logica + 50
draw_arrow_down(750, y_logica + h_logica, y_sp, "Ejecuta Procedimiento Almacenado")

# Procedimiento sp_alta_reserva
h_sp = draw_auto_box(250, y_sp, 1000, "Procedimiento Almacenado: <b>sp_alta_reserva</b>", [
    "• Recibe los parámetros: cliente, espacio, fecha, horas e importe total.",
    "• Invoca la Función: <b>fn_verificar_disponibilidad</b> para comprobar el horario.",
    "• Si el horario está libre guarda la fila; si no, interrumpe con <b>SIGNAL 45000</b>."
], border_w=2)

y_rombo_conn = y_sp + h_sp
draw_arrow_down(750, y_rombo_conn, y_rombo_conn + 55, "Evalúa disponibilidad")

# Rombo de decisión disponibilidad
rx = 750
ry = y_rombo_conn + 165
rw = 720
rh = 210
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
y_branches = ry + rh/2 + 55
draw.line([rx - rw/2, ry, 260, ry], fill="#000000", width=2)
draw_arrow_down(260, ry, y_branches, "")
draw.rectangle([270, ry - 30, 440, ry - 5], fill="#FFFFFF", outline="#000000", width=1)
draw.text((285, ry - 26), "SÍ (Libre = 1)", fill="#000000", font=font_lbl)

h_insert = draw_auto_box(60, y_branches, 480, "Guarda Reserva (<b>INSERT</b>)", [
    "• Ejecuta <b>INSERT INTO reservas</b>.",
    "• Guarda con estado: 'Confirmada'.",
    "• Transacción finalizada con éxito."
], fill_header="#EAEAEA", border_w=3)

y_grid_res = y_branches + h_insert + 35
draw_arrow_down(260, y_branches + h_insert, y_grid_res, "")
draw_auto_box(60, y_grid_res, 480, "Resultado: Grilla Actualizada", [
    "• C# consulta la Vista: <b>vw_detalle_reservas</b>.",
    "• Aparece la nueva reserva en la tabla.",
    "• Cartel: 'Reserva confirmada con éxito'."
], border_w=2)

# -------------------------------------------------------------------------
# RAMA NO: OCUPADO = 0 (Centro / Derecha)
# -------------------------------------------------------------------------
draw.line([rx + rw/2, ry, 1240, ry], fill="#000000", width=2)
draw_arrow_down(1240, ry, y_branches, "")
draw.rectangle([1030, ry - 30, 1220, ry - 5], fill="#FFFFFF", outline="#000000", width=1)
draw.text((1045, ry - 26), "NO (Ocupado = 0)", fill="#000000", font=font_lbl)

h_alerta = draw_auto_box(1000, y_branches, 480, "Alerta: Horario Ocupado", [
    "• Detecta solapamiento (resultado = <b>0</b>).",
    "• Dispara <b>SIGNAL SQLSTATE '45000'</b>.",
    "• Cancela la operación sin guardar nada."
], fill_header="#EAEAEA", border_w=3)

draw_arrow_down(1240, y_branches + h_alerta, y_grid_res, "")
draw_auto_box(1000, y_grid_res, 480, "Resultado: Aviso en Pantalla", [
    "• C# captura la alerta (<b>catch MySqlException</b>).",
    "• La aplicación no falla ni se cierra.",
    "• Cuadro emergente (MessageBox): aviso."
], border_w=2)

# =========================================================================
# 5. MÓDULO DE AUDITORÍA Y CANCELACIONES (MySQL)
# =========================================================================
y_audit_section = y_grid_res + 160
draw.line([60, y_audit_section, W - 60, y_audit_section], fill="#000000", width=2)
draw.text((80, y_audit_section + 15), "AUDITORÍA, CANCELACIÓN Y REPORTES EN LA BASE DE DATOS", fill="#000000", font=font_box_title)

y_audit_boxes = y_audit_section + 55

# Caja 1: Cancelación
w_c1 = 570
x_c1 = 60
h_c1 = draw_auto_box(x_c1, y_audit_boxes, w_c1, "Cancelación: <b>sp_cancelar_reserva</b>", [
    "• Se ejecuta al hacer clic en 'Cancelar Reserva'.",
    "• Valida que la reserva exista y no esté ya cancelada.",
    "• Actualiza el estado a <b>'Cancelada'</b> en la tabla.",
    "• Este cambio de estado activa el Trigger."
], border_w=2)

# Flecha con espacio amplio entre cajas (de 630 a 810 = 180 px de espacio despejado)
x_arrow_start = x_c1 + w_c1
x_arrow_end = x_arrow_start + 180
y_arrow_mid = y_audit_boxes + h_c1 / 2

draw_arrow_right(x_arrow_start, y_arrow_mid, x_arrow_end, "Dispara Trigger")

# Caja 2: Trigger Auditoría (altura automática con espacio suficiente para las 6 líneas)
w_c2 = 680
x_c2 = x_arrow_end
h_c2 = draw_auto_box(x_c2, y_audit_boxes, w_c2, "Trigger: <b>trg_auditoria_reservas</b>", [
    "• Trigger automático: <b>AFTER UPDATE ON reservas</b>.",
    "• Se ejecuta solo en MySQL (no lo llama C#).",
    "• Inserta en la tabla <b>auditoria_reservas</b>:",
    "  - ID de la reserva cancelada.",
    "  - Acción: 'Cancelacion de reserva'.",
    "  - Fecha/hora exacta (NOW) y Usuario activo."
], fill_header="#EAEAEA", border_w=3, line_spacing=26)

# Caja 3: Vista Analítica y Cursor (altura automática con espacio amplio)
x_c3 = x_c2 + w_c2 + 50
w_c3 = W - 60 - x_c3
h_c3 = draw_auto_box(x_c3, y_audit_boxes, w_c3, "Vista Analítica y Cursor (Reportes)", [
    "• Vista: <b>vw_resumen_recursos</b>:",
    "  Calcula total facturado y cantidad de turnos.",
    "• Procedimiento con Cursor:",
    "  <b>sp_calcular_total_recaudado_cursor</b>:",
    "  Recorre fila por fila sumando montos de reservas",
    "  confirmadas para calcular el total general."
], border_w=2, line_spacing=26)

# =========================================================================
# CUADRO DE RESUMEN DE OBJETOS SQL (PIE DE PÁGINA)
# =========================================================================
max_h_audit = max(h_c1, h_c2, h_c3)
y_map_section = y_audit_boxes + max_h_audit + 45
draw.line([60, y_map_section, W - 60, y_map_section], fill="#000000", width=2)

y_map_box = y_map_section + 25
h_map = draw_auto_box(60, y_map_box, 1980, "MAPA DE OBJETOS FUNCIONALES DEL ARCHIVO SQL (tp_final_db)", [
    "• <b>Vistas (2):</b> <b>vw_detalle_reservas</b> (grilla principal con nombres reales)  |  <b>vw_resumen_recursos</b> (reporte de ingresos por sala).",
    "• <b>Función (1):</b> <b>fn_verificar_disponibilidad</b> (cálculo de superposición horaria: retorna 1 si está libre, 0 si está ocupado).",
    "• <b>Procedimientos (8):</b> <b>sp_alta_reserva</b>, <b>sp_modificar_reserva</b>, <b>sp_cancelar_reserva</b>, <b>sp_alta_cliente</b>, <b>sp_modificar_cliente</b>, <b>sp_eliminar_cliente</b>, <b>sp_alta_recurso</b>, <b>sp_modificar_recurso</b>.",
    "• <b>Cursor (1):</b> <b>sp_calcular_total_recaudado_cursor</b> (recorrido secuencial con cursor para suma total de reservas confirmadas).",
    "• <b>Trigger (1):</b> <b>trg_auditoria_reservas</b> (registro inmutable automático en tabla <b>auditoria_reservas</b> ante cada cancelación)."
], fill_header="#F0F0F0", border_w=2, line_spacing=30)

final_h = y_map_box + h_map + 60
img_clean = img.crop((0, 0, W, final_h))

output_png = r"c:\xampp\htdocs\ALGORITMOS2\Trabajo_final_algoritmos\Documentacion\Diagrama_de_Flujo_Funcional.png"
img_clean.save(output_png, "PNG", dpi=(300, 300))
print("Diagrama 100% corregido y con alturas dinamicas guardado en:", output_png)
