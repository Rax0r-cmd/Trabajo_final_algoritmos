import math
from PIL import Image, ImageDraw, ImageFont

def create_uml_diagram(output_path="DB/Diagrama_Clases_UML.png"):
    # Dimensiones optimizadas para ancho completo de hoja A4 en Word con texto GRANDE y legible
    W, H = 1400, 1020
    img = Image.new("RGB", (W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fuentes GRANDES para legibilidad perfecta en hoja A4 (sin necesidad de hacer zoom)
    f_title = ImageFont.truetype("arialbd.ttf", 22)
    f_subtitle = ImageFont.truetype("arial.ttf", 14)
    f_class_name = ImageFont.truetype("arialbd.ttf", 19)
    f_class_stereo = ImageFont.truetype("ariali.ttf", 15)
    f_text = ImageFont.truetype("arial.ttf", 16)
    f_text_bold = ImageFont.truetype("arialbd.ttf", 16)
    f_text_italic = ImageFont.truetype("ariali.ttf", 16)

    COLOR_BLACK = (0, 0, 0)
    BORDER_COLOR = (0, 0, 0)
    HEADER_BG = (240, 240, 240)
    BOX_BG = (255, 255, 255)
    SHADOW_COLOR = (225, 225, 225)
    LINE_COLOR = (0, 0, 0)

    # Encabezado superior claro y visible
    draw.rectangle([(0, 0), (W, 60)], fill=(245, 245, 245), outline=BORDER_COLOR, width=2)
    draw.text((25, 12), "DIAGRAMA DE CLASES SIMPLIFICADO - DOMINIO Y POO", fill=COLOR_BLACK, font=f_title)
    draw.text((25, 38), "Jerarquía de Herencia, Interfaz IReservable y Capas del Sistema (C# .NET)", fill=(60, 60, 60), font=f_subtitle)

    def draw_box(x, y, w, h, stereo, name, attributes, methods, is_abstract=False):
        # Sombra
        draw.rectangle([(x + 4, y + 4), (x + w + 4, y + h + 4)], fill=SHADOW_COLOR)
        # Borde exterior
        draw.rectangle([(x, y), (x + w, y + h)], fill=BOX_BG, outline=BORDER_COLOR, width=2)

        # Header
        header_h = 48 if stereo else 36
        draw.rectangle([(x, y), (x + w, y + header_h)], fill=HEADER_BG, outline=BORDER_COLOR, width=1)
        
        curr_y = y + 4
        if stereo:
            s_w = draw.textlength(stereo, font=f_class_stereo)
            draw.text((x + (w - s_w) / 2, curr_y), stereo, fill=COLOR_BLACK, font=f_class_stereo)
            curr_y += 18

        n_w = draw.textlength(name, font=f_class_name)
        draw.text((x + (w - n_w) / 2, curr_y), name, fill=COLOR_BLACK, font=f_class_name)

        # Divisor de atributos
        curr_y = y + header_h
        draw.line([(x, curr_y), (x + w, curr_y)], fill=BORDER_COLOR, width=1)

        # Atributos
        curr_y += 8
        for attr in attributes:
            draw.text((x + 12, curr_y), attr, fill=COLOR_BLACK, font=f_text)
            curr_y += 24

        # Divisor de métodos
        curr_y += 4
        draw.line([(x, curr_y), (x + w, curr_y)], fill=BORDER_COLOR, width=1)

        # Métodos
        curr_y += 8
        for m in methods:
            m_font = f_text_italic if ("abstract" in m or is_abstract and "CalcularCosto" in m) else f_text
            draw.text((x + 12, curr_y), m, fill=COLOR_BLACK, font=m_font)
            curr_y += 24

    # =========================================================================
    # 1. FILA SUPERIOR: IReservable + Recurso (Abstracta) + EstadoReserva
    # =========================================================================
    # 1.1 IReservable (Interfaz)
    draw_box(
        x=40, y=90, w=350, h=110,
        stereo="<<interface>>",
        name="IReservable",
        attributes=[],
        methods=["+ PuedeReservarse(fecha): bool"]
    )

    # 1.2 Recurso (Clase abstracta base)
    draw_box(
        x=480, y=90, w=450, h=190,
        stereo="<<abstract>>",
        name="Recurso",
        attributes=[
            "+ IdRecurso: int",
            "+ Nombre: string",
            "+ PrecioPorHora: decimal"
        ],
        methods=[
            "+ PuedeReservarse(fecha): bool",
            "+ CalcularCosto(horas: int): decimal  {abstract}"
        ],
        is_abstract=True
    )

    # 1.3 EstadoReserva (Enum)
    draw_box(
        x=1020, y=90, w=340, h=140,
        stereo="<<enumeration>>",
        name="EstadoReserva",
        attributes=[
            "Pendiente",
            "Confirmada",
            "Cancelada"
        ],
        methods=[]
    )

    # =========================================================================
    # 2. FILA INTERMEDIA: Las 3 Clases Derivadas de Recurso
    # =========================================================================
    # 2.1 Sala
    draw_box(
        x=40, y=370, w=400, h=150,
        stereo="",
        name="Sala",
        attributes=[
            "+ CantSillas: int"
        ],
        methods=[
            "+ CalcularCosto(horas): decimal  {override}",
            "+ PuedeReservarse(fecha): bool  {override}"
        ]
    )

    # 2.2 OficinaPrivada
    draw_box(
        x=500, y=370, w=410, h=150,
        stereo="",
        name="OficinaPrivada",
        attributes=[
            "+ MobiliarioIncluido: bool"
        ],
        methods=[
            "+ CalcularCosto(horas): decimal  {override}",
            "+ PuedeReservarse(fecha): bool  {override}"
        ]
    )

    # 2.3 PuestoTrabajo
    draw_box(
        x=960, y=370, w=400, h=150,
        stereo="",
        name="PuestoTrabajo",
        attributes=[
            "+ NroCategoria: int"
        ],
        methods=[
            "+ CalcularCosto(horas): decimal  {override}",
            "+ PuedeReservarse(fecha): bool  {override}"
        ]
    )

    # =========================================================================
    # 3. FILA INFERIOR: Cliente, Reserva y Capas (Gestora / DAO)
    # =========================================================================
    # 3.1 Cliente
    draw_box(
        x=40, y=600, w=360, h=160,
        stereo="",
        name="Cliente",
        attributes=[
            "+ IdCliente: int",
            "+ NombreCompleto: string",
            "+ Mail: string",
            "+ Telefono: string"
        ],
        methods=[
            "+ ToString(): string"
        ]
    )

    # 3.2 Reserva
    draw_box(
        x=470, y=600, w=440, h=190,
        stereo="",
        name="Reserva",
        attributes=[
            "+ IdReserva: int",
            "+ IdCliente: int",
            "+ IdRecurso: int",
            "+ Fecha: DateTime",
            "+ Horas: int",
            "+ Total: decimal",
            "+ Estado: EstadoReserva"
        ],
        methods=[]
    )

    # 3.3 GestoraCoworking & DAO (Capa de Negocio y Persistencia)
    draw_box(
        x=960, y=600, w=400, h=200,
        stereo="<<capas>>",
        name="Gestora & GestorDAO",
        attributes=[
            "GestoraCoworking: List<Reserva>",
            "+ AgregarReserva(r): void",
            "+ CancelarReserva(id): void",
            "+ ObtenerPorFecha(f): List"
        ],
        methods=[
            "GestorDAO (Persistencia MySQL):",
            "+ AltaReserva(...) : bool",
            "+ CancelarReserva(...) : bool"
        ]
    )

    # =========================================================================
    # FLECHAS Y CONEXIONES UML (Líneas gruesas de 2px y triángulos nítidos)
    # =========================================================================
    def draw_triangle(tip_x, tip_y, size=16, direction="up", fill_color=(255, 255, 255), outline_color=LINE_COLOR):
        if direction == "up":
            pts = [(tip_x, tip_y), (tip_x - size/2, tip_y + size), (tip_x + size/2, tip_y + size)]
        elif direction == "left":
            pts = [(tip_x, tip_y), (tip_x + size, tip_y - size/2), (tip_x + size, tip_y + size/2)]
        draw.polygon(pts, fill=fill_color, outline=outline_color, width=2)

    # A) Recurso IMPLEMENTA IReservable (Flecha discontinua a la izquierda)
    x_start = 480
    x_end = 390 + 16
    y_pos = 145
    step = 10
    cur_x = x_start
    while cur_x > x_end:
        draw.line([(cur_x, y_pos), (max(cur_x - step, x_end), y_pos)], fill=LINE_COLOR, width=2)
        cur_x -= step * 2
    draw_triangle(390, 145, size=16, direction="left")
    draw.text((395, 115), "<<implements>>", fill=COLOR_BLACK, font=f_class_stereo)

    # B) Sala, Oficina y Puesto HEREDAN de Recurso
    # Triángulo en bottom center de Recurso (x=705, y=280)
    draw_triangle(705, 280, size=16, direction="up")
    draw.line([(705, 296), (705, 330)], fill=LINE_COLOR, width=2)
    # Barra horizontal de conexión
    draw.line([(240, 330), (1160, 330)], fill=LINE_COLOR, width=2)
    # Bajadas a cada clase
    draw.line([(240, 330), (240, 370)], fill=LINE_COLOR, width=2)
    draw.line([(705, 330), (705, 370)], fill=LINE_COLOR, width=2)
    draw.line([(1160, 330), (1160, 370)], fill=LINE_COLOR, width=2)
    draw.text((715, 305), "<<extends>>", fill=COLOR_BLACK, font=f_class_stereo)

    # C) Reserva ASOCIA con Cliente (Horizontal directa)
    draw.line([(400, 680), (470, 680)], fill=LINE_COLOR, width=2)
    draw.text((408, 655), "1", fill=COLOR_BLACK, font=f_text_bold)
    draw.text((445, 655), "0..*", fill=COLOR_BLACK, font=f_text_bold)

    # D) Gestora ASOCIA con Reserva (Horizontal directa)
    draw.line([(910, 680), (960, 680)], fill=LINE_COLOR, width=2)
    draw.text((915, 655), "1..*", fill=COLOR_BLACK, font=f_text_bold)

    # Pie institucional del diagrama
    draw.rectangle([(0, H - 40), (W, H)], fill=(245, 245, 245), outline=BORDER_COLOR, width=1)
    footer_text = "Algoritmos II - Trabajo Practico Final 2026 - Instituto Argentino de la Empresa - Modelo POO Simplificado"
    f_ft = ImageFont.truetype("arial.ttf", 13)
    draw.text((25, H - 28), footer_text, fill=COLOR_BLACK, font=f_ft)

    img.save(output_path, dpi=(300, 300))
    print(f"Diagrama UML simplificado con texto GRANDE generado en: {output_path}")

if __name__ == "__main__":
    create_uml_diagram()
