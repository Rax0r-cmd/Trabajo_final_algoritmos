# -*- coding: utf-8 -*-
import re
from PIL import Image, ImageDraw, ImageFont

W = 1800
H = 2050
img = Image.new("RGB", (W, H), color="#FFFFFF")
draw = ImageDraw.Draw(img)

# Fuentes
try:
    font_main_title = ImageFont.truetype("arialbd.ttf", 36)
    font_main_sub   = ImageFont.truetype("arial.ttf", 22)
    font_box_title  = ImageFont.truetype("arialbd.ttf", 21)
    font_text       = ImageFont.truetype("arial.ttf", 18)
    font_bold       = ImageFont.truetype("arialbd.ttf", 18)
    font_lbl        = ImageFont.truetype("arialbd.ttf", 17)
    font_lbl_reg    = ImageFont.truetype("arial.ttf", 17)
except:
    font_main_title = font_main_sub = font_box_title = font_text = font_bold = font_lbl = font_lbl_reg = ImageFont.load_default()

def draw_rich_text(draw, x, y, text, default_font, bold_font, color="#000000"):
    """
    Dibuja texto soportando etiquetas <b>...</b> para renderizar palabras
    específicas en negrita dentro de una misma línea fluida.
    """
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
    header_h = 38
    draw.rectangle([x, y, x + w, y + header_h], fill=fill_header, outline="#000000", width=2)
    
    # Titulo cabecera centrado (soporta <b>)
    # Medir largo total del titulo
    parts = re.split(r"(<b>.*?</b>)", title)
    total_w = 0
    for part in parts:
        if not part: continue
        f = font_box_title if (part.startswith("<b>") and part.endswith("</b>")) else font_box_title
        clean_part = part[3:-4] if (part.startswith("<b>") and part.endswith("</b>")) else part
        bbox = draw.textbbox((0, 0), clean_part, font=f)
        total_w += (bbox[2] - bbox[0])
    
    start_x = x + (w - total_w) / 2
    draw_rich_text(draw, start_x, y + 8, title, font_box_title, font_box_title)
    
    # Lineas de contenido
    curr_y = y + header_h + 10
    for line in lines:
        draw_rich_text(draw, x + 14, curr_y, line, font_text, font_bold)
        curr_y += 24

def draw_arrow_down(x, y1, y2, label=""):
    draw.line([x, y1, x, y2], fill="#000000", width=2)
    draw.polygon([(x, y2), (x - 7, y2 - 14), (x + 7, y2 - 14)], fill="#000000")
    if label:
        draw.text((x + 10, (y1 + y2) / 2 - 10), label, fill="#000000", font=font_lbl)

def draw_arrow_right(x1, y, x2, label=""):
    draw.line([x1, y, x2, y], fill="#000000", width=2)
    draw.polygon([(x2, y), (x2 - 14, y - 7), (x2 - 14, y + 7)], fill="#000000")
    if label:
        bbox = draw.textbbox((0, 0), label, font=font_lbl)
        tw = bbox[2] - bbox[0]
        draw.text(((x1 + x2 - tw) / 2, y - 24), label, fill="#000000", font=font_lbl)

# =========================================================================
# TÍTULO SUPERIOR
# =========================================================================
draw.text((W/2 - 370, 30), "SISTEMA DE GESTIÓN DE COWORKING", fill="#000000", font=font_main_title)
draw.text((W/2 - 270, 78), "Diagrama de Funcionamiento del Sistema", fill="#333333", font=font_main_sub)
draw.line([80, 118, W - 80, 118], fill="#000000", width=2)

# =========================================================================
# 1. PANTALLA PRINCIPAL Y ACCESO ADMINISTRADOR
# =========================================================================
draw_box(80, 145, 980, 130, "Ventana Principal (CoWorking - DASHBOARD)", [
    "• Inicia directamente aquí al abrir el programa en <b>Modo Estándar</b>.",
    "• Muestra inicialmente solo 2 solapas: <b>CONTROL</b> y <b>RESERVAS</b>.",
    "• Menú superior: opción para iniciar sesión como Administrador."
], border_w=3)

# Flecha hacia Login
draw_arrow_right(1060, 210, 1240, "Menú: Iniciar Sesión")

# Formulario Login
draw_box(1240, 145, 480, 130, "Acceso Administrador (FrmLogin)", [
    "• Usuario: <b>Admin</b>  |  Clave: <b>123456</b>",
    "• Validación estricta por teclado y enlace a WhatsApp.",
    "• Al ingresar: desbloquea las solapas de gestión administrativa."
])

# Flecha desde Login que baja a desbloquear solapas admin
draw.line([1480, 275, 1480, 315], fill="#000000", width=2)
draw_arrow_down(1480, 315, 365, "Desbloquea solapas")

# =========================================================================
# 2. SOLAPAS DE LA VENTANA PRINCIPAL
# =========================================================================
draw.line([320, 275, 320, 320], fill="#000000", width=2)
draw.line([840, 275, 840, 320], fill="#000000", width=2)

draw_arrow_down(320, 320, 365, "Visible al inicio")
draw_arrow_down(840, 320, 365, "Visible al inicio")

# SOLAPA 1: CONTROL (Crear Reserva)
draw_box(80, 365, 520, 250, "Solapa: CONTROL (Crear reserva)", [
    "• Formulario activo al iniciar el programa:",
    "  - Cliente (selector de clientes registrados)",
    "  - Tipo de Recurso (sala, oficina o puesto)",
    "  - Fecha y Horario de inicio del turno",
    "  - Horas de uso (duración de la reserva)",
    "  - Valor a abonar (calculado automáticamente)",
    "",
    "<b>BOTÓN: [ AGREGAR ]</b>"
], fill_header="#EAEAEA", border_w=3)

# SOLAPA 2: RESERVAS (Grilla conectada a la Vista)
draw_box(630, 365, 440, 150, "Solapa: RESERVAS (Listado)", [
    "• Muestra la tabla de reservas confirmadas.",
    "• Consulta la Vista: <b>vw_detalle_reservas</b>.",
    "• Permite revisar los turnos agendados.",
    "• Si es Admin: permite modificar o cancelar."
])

# SOLAPAS DESBLOQUEADAS POR ADMIN
draw_box(1100, 365, 300, 110, "Solapa: CLIENTES (Admin)", [
    "• Padrón de clientes registrados.",
    "• Botón 'Nuevo Cliente' / 'Modificar'."
])
draw_arrow_down(1250, 475, 515, "Abre ventana")
draw_box(1100, 515, 300, 100, "Editor de Clientes (Modal)", [
    "• Formulario para cargar o cambiar datos.",
    "• Al guardar: actualiza la lista sola."
])

draw_box(1430, 365, 300, 110, "Solapa: RECURSOS (Admin)", [
    "• Catálogo de salas y oficinas.",
    "• Botón 'Nuevo Recurso' / 'Modificar'."
])
draw_arrow_down(1580, 475, 515, "Abre ventana")
draw_box(1430, 515, 300, 100, "Editor de Recursos (Modal)", [
    "• Configura precios, sillas y categoría.",
    "• Al guardar: actualiza la lista sola."
])

# =========================================================================
# 3. LÓGICA DEL SISTEMA
# =========================================================================
# Flecha directa desde el botón [ Agregar ] en la solapa CONTROL
draw_arrow_down(340, 615, 725, "Presiona botón [ AGREGAR ]")

draw_box(80, 725, 1650, 130, "Lógica del Sistema (Capa Gestora y Modelos C#)", [
    "• Recibe los datos cargados en la solapa <b>CONTROL</b> (cliente, espacio, fecha y horas).",
    "• Aplica la fórmula de tarifas según el tipo de espacio mediante el método <b>CalcularCosto()</b>.",
    "• Abre la conexión centralizada con la base de datos a través de <b>Conexion.cs</b> y despacha el Procedimiento."
], border_w=3)

# =========================================================================
# 4. BASE DE DATOS Y COMPROBACIÓN DE HORARIOS
# =========================================================================
draw_arrow_down(900, 855, 925, "Ejecuta el Procedimiento Almacenado")

draw_box(440, 925, 920, 120, "Base de Datos (Procedimiento: <b>sp_alta_reserva</b>)", [
    "• Recibe los parámetros enviados: cliente, espacio, fecha, horas e importe.",
    "• Antes de registrar la reserva, invoca la Función: <b>fn_verificar_disponibilidad</b>.",
    "• Evalúa matemáticamente si el rango solicitado se superpone con turnos ya confirmados."
])

draw_arrow_down(900, 1045, 1100, "Retorna 1 (Libre) o 0 (Ocupado)")

# Rombo de decisión
rx, ry, rw, rh = 900, 1215, 750, 215
rombo_pts = [(rx, ry - rh/2), (rx + rw/2, ry), (rx, ry + rh/2), (rx - rw/2, ry)]
draw.polygon(rombo_pts, fill="#FBFBFB", outline="#000000")
draw.line(rombo_pts + [rombo_pts[0]], fill="#000000", width=3)

draw.text((rx - 170, ry - 32), "¿El horario está libre?", fill="#000000", font=font_main_title)

# Subtexto rombo con la funcion en negrita
func_label = "(Función: "
bbox1 = draw.textbbox((0, 0), func_label, font=font_lbl_reg)
w1 = bbox1[2] - bbox1[0]
func_name = "fn_verificar_disponibilidad"
bbox2 = draw.textbbox((0, 0), func_name, font=font_lbl)
w2 = bbox2[2] - bbox2[0]
func_close = ")"
bbox3 = draw.textbbox((0, 0), func_close, font=font_lbl_reg)
w3 = bbox3[2] - bbox3[0]

total_func_w = w1 + w2 + w3
start_func_x = rx - total_func_w / 2
draw.text((start_func_x, ry + 12), func_label, fill="#444444", font=font_lbl_reg)
draw.text((start_func_x + w1, ry + 12), func_name, fill="#000000", font=font_lbl)
draw.text((start_func_x + w1 + w2, ry + 12), func_close, fill="#444444", font=font_lbl_reg)

# -------------------------------------------------------------------------
# RAMA SÍ: LIBRE = 1 (Izquierda)
# -------------------------------------------------------------------------
draw.line([rx - rw/2, ry, 360, ry], fill="#000000", width=2)
draw_arrow_down(360, ry, 1385, "")
draw.rectangle([360, ry - 30, 540, ry - 5], fill="#FFFFFF", outline="#000000", width=1)
draw.text((375, ry - 26), "SÍ (Libre = 1)", fill="#000000", font=font_lbl)

draw_box(100, 1385, 520, 130, "Guarda Reserva (<b>INSERT</b>)", [
    "• Ejecuta <b>INSERT INTO reservas</b> con estado 'Confirmada'.",
    "• La transacción en MySQL finaliza con éxito.",
    "• Devuelve confirmación de guardado a C#."
], fill_header="#EAEAEA", border_w=3)

draw_arrow_down(360, 1515, 1595, "")
draw_box(100, 1595, 520, 135, "Resultado: Grilla Actualizada", [
    "• C# consulta la Vista: <b>vw_detalle_reservas</b>.",
    "• Se actualiza la tabla en la solapa <b>RESERVAS</b>.",
    "• Muestra mensaje: 'Reserva confirmada con éxito'."
], border_w=2)

# -------------------------------------------------------------------------
# RAMA NO: OCUPADO = 0 (Derecha)
# -------------------------------------------------------------------------
draw.line([rx + rw/2, ry, 1440, ry], fill="#000000", width=2)
draw_arrow_down(1440, ry, 1385, "")
draw.rectangle([1230, ry - 30, 1430, ry - 5], fill="#FFFFFF", outline="#000000", width=1)
draw.text((1245, ry - 26), "NO (Ocupado = 0)", fill="#000000", font=font_lbl)

draw_box(1180, 1385, 520, 130, "Alerta: Horario Ocupado", [
    "• Detecta conflicto de turnos (resultado = <b>0</b>).",
    "• MySQL aborta con <b>SIGNAL SQLSTATE '45000'</b>.",
    "• No guarda nada para evitar solapamientos."
], fill_header="#EAEAEA", border_w=3)

draw_arrow_down(1440, 1515, 1595, "")
draw_box(1180, 1595, 520, 135, "Resultado: Aviso en Pantalla", [
    "• C# captura la alerta (<b>catch MySqlException</b>).",
    "• La aplicación no falla ni se congela.",
    "• Muestra mensaje: 'Horario no disponible, elija otro'."
], border_w=2)

# Recortar canvas al contenido exacto con margen inferior limpio
final_h = 1780
img_clean = img.crop((0, 0, W, final_h))

output_png = r"c:\xampp\htdocs\ALGORITMOS2\Trabajo_final_algoritmos\Documentacion\diagrama_imprimible.png"
img_clean.save(output_png, "PNG", dpi=(300, 300))
print("Diagrama con nombres técnicos en negrita guardado con éxito:", output_png)
