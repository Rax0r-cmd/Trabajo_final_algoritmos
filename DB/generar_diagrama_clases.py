import math
from PIL import Image, ImageDraw, ImageFont

def create_uml_diagram(output_path="DB/Diagrama_Clases_UML.png"):
    W, H = 1800, 1150
    img = Image.new("RGB", (W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fuentes
    f_title = ImageFont.truetype("arialbd.ttf", 22)
    f_subtitle = ImageFont.truetype("ariali.ttf", 13)
    f_class_name = ImageFont.truetype("arialbd.ttf", 15)
    f_class_stereo = ImageFont.truetype("ariali.ttf", 12)
    f_text = ImageFont.truetype("arial.ttf", 12)
    f_text_bold = ImageFont.truetype("arialbd.ttf", 12)
    f_text_italic = ImageFont.truetype("ariali.ttf", 12)

    # Colores institucionales
    NAVY = (11, 43, 74)         # #0B2B4A
    NAVY2 = (26, 75, 109)       # #1A4B6D
    BORDER_COLOR = (40, 70, 100)
    HEADER_BG = (235, 243, 250)
    BOX_BG = (255, 255, 255)
    TEXT_COLOR = (25, 30, 40)
    LINE_COLOR = (50, 80, 110)
    SHADOW_COLOR = (225, 230, 238)

    # Encabezado institucional superior del diagrama
    draw.rectangle([(0, 0), (W, 70)], fill=NAVY)
    draw.text((35, 15), "DIAGRAMA DE CLASES SIMPLIFICADO — SISTEMA DE GESTIÓN DE COWORKING", fill=(255, 255, 255), font=f_title)
    draw.text((35, 45), "Modelo de Dominio Orientado a Objetos (POO) · C# .NET Framework 4.7.2 · Arquitectura en Capas", fill=(245, 176, 66), font=f_subtitle)

    def draw_box(x, y, w, h, stereo, name, attributes, methods, is_abstract=False, is_interface=False, is_static=False, is_enum=False):
        # Sombra suave
        draw.rectangle([(x + 4, y + 4), (x + w + 4, y + h + 4)], fill=SHADOW_COLOR)
        # Fondo
        draw.rectangle([(x, y), (x + w, y + h)], fill=BOX_BG, outline=BORDER_COLOR, width=2)

        # Header de la clase
        header_h = 42 if stereo else 32
        draw.rectangle([(x, y), (x + w, y + header_h)], fill=HEADER_BG, outline=BORDER_COLOR, width=1)
        
        # Estereotipo
        curr_y = y + 4
        if stereo:
            s_w = draw.textlength(stereo, font=f_class_stereo)
            draw.text((x + (w - s_w) / 2, curr_y), stereo, fill=NAVY2, font=f_class_stereo)
            curr_y += 16

        # Nombre
        n_font = f_class_name
        n_w = draw.textlength(name, font=n_font)
        draw.text((x + (w - n_w) / 2, curr_y), name, fill=NAVY, font=n_font)

        # Divisor de atributos
        curr_y = y + header_h
        draw.line([(x, curr_y), (x + w, curr_y)], fill=BORDER_COLOR, width=1)

        # Atributos
        curr_y += 8
        for attr in attributes:
            draw.text((x + 12, curr_y), attr, fill=TEXT_COLOR, font=f_text)
            curr_y += 18

        # Divisor de métodos
        curr_y += 4
        draw.line([(x, curr_y), (x + w, curr_y)], fill=BORDER_COLOR, width=1)

        # Métodos
        curr_y += 8
        for m in methods:
            m_font = f_text_italic if ("abstract" in m or is_abstract and "CalcularCosto" in m) else f_text
            draw.text((x + 12, curr_y), m, fill=TEXT_COLOR, font=m_font)
            curr_y += 18

    # 1. IReservable (Interfaz)
    draw_box(
        x=50, y=100, w=300, h=110,
        stereo="<<interface>>",
        name="IReservable",
        attributes=[],
        methods=["+ PuedeReservarse(fecha: DateTime): bool"],
        is_interface=True
    )

    # 2. Recurso (Clase abstracta)
    draw_box(
        x=440, y=100, w=370, h=220,
        stereo="<<abstract>>",
        name="Recurso",
        attributes=[
            "+ IdRecurso: int",
            "+ Nombre: string",
            "+ Descripcion: string",
            "+ Ubicacion: string",
            "+ PrecioPorHora: decimal",
            "+ IdTipoRecurso: int"
        ],
        methods=[
            "+ Recurso()",
            "+ Recurso(id, nom, desc, ubic, precio, tipo)",
            "+ PuedeReservarse(fecha: DateTime): bool",
            "+ CalcularCosto(horas: int): decimal  {abstract}"
        ],
        is_abstract=True
    )

    # 3. Clases derivadas de Recurso
    # 3.1 Sala
    draw_box(
        x=70, y=380, w=340, h=160,
        stereo="",
        name="Sala",
        attributes=[
            "+ CantSillas: int"
        ],
        methods=[
            "+ Sala()",
            "+ Sala(id, nom, desc, ubic, precio, sillas)",
            "+ CalcularCosto(horas: int): decimal  {override}",
            "+ PuedeReservarse(fecha: DateTime): bool  {override}"
        ]
    )

    # 3.2 OficinaPrivada
    draw_box(
        x=455, y=380, w=340, h=160,
        stereo="",
        name="OficinaPrivada",
        attributes=[
            "+ MobiliarioIncluido: bool"
        ],
        methods=[
            "+ OficinaPrivada()",
            "+ OficinaPrivada(id, nom, desc, ubic, precio, mob)",
            "+ CalcularCosto(horas: int): decimal  {override}",
            "+ PuedeReservarse(fecha: DateTime): bool  {override}"
        ]
    )

    # 3.3 PuestoTrabajo
    draw_box(
        x=840, y=380, w=340, h=160,
        stereo="",
        name="PuestoTrabajo",
        attributes=[
            "+ NroCategoria: int"
        ],
        methods=[
            "+ PuestoTrabajo()",
            "+ PuestoTrabajo(id, nom, desc, ubic, precio, cat)",
            "+ CalcularCosto(horas: int): decimal  {override}",
            "+ PuedeReservarse(fecha: DateTime): bool  {override}"
        ]
    )

    # 4. Cliente
    draw_box(
        x=1360, y=100, w=380, h=200,
        stereo="",
        name="Cliente",
        attributes=[
            "+ IdCliente: int",
            "+ Nombre: string",
            "+ Apellido: string",
            "+ Telefono: string",
            "+ Mail: string",
            "+ FechaRegistro: DateTime"
        ],
        methods=[
            "+ Cliente()",
            "+ Cliente(id, nombre, apellido, tel, mail)",
            "+ ToString(): string"
        ]
    )

    # 5. EstadoReserva (Enum)
    draw_box(
        x=900, y=100, w=220, h=140,
        stereo="<<enumeration>>",
        name="EstadoReserva",
        attributes=[
            "Pendiente",
            "Confirmada",
            "Cancelada",
            "Finalizada"
        ],
        methods=[],
        is_enum=True
    )

    # 6. Reserva
    draw_box(
        x=1290, y=380, w=450, h=220,
        stereo="",
        name="Reserva",
        attributes=[
            "+ IdReserva: int",
            "+ IdCliente: int",
            "+ IdRecurso: int",
            "+ Fecha: DateTime",
            "+ Horas: int",
            "+ Total: decimal",
            "+ EstadoReserva: EstadoReserva"
        ],
        methods=[
            "+ Reserva()",
            "+ Reserva(id, idCli, idRec, fecha, hs, tot, estado)",
            "+ Reserva(id, idCli, idRec, fecha, hs, tot)"
        ]
    )

    # 7. GestoraCoworking (Capa de Negocio en Memoria)
    draw_box(
        x=980, y=680, w=480, h=230,
        stereo="",
        name="GestoraCoworking",
        attributes=[
            "- ListaReservas: List<Reserva>"
        ],
        methods=[
            "+ AgregarReserva(reserva: Reserva): void",
            "+ CancelarReserva(idReserva: int): void",
            "+ ConfirmarReserva(idReserva: int): void",
            "+ ModificarReserva(id, fecha: DateTime, hs: int): void",
            "+ ObtenerReservasPorFecha(fecha: DateTime): List<Reserva>",
            "+ ObtenerReservasPorCliente(cliente: Cliente): List<Reserva>",
            "+ ObtenerReservasPorRecurso(recurso: Recurso): List<Reserva>",
            "+ ObtenerReservasPorEstado(estado: EstadoReserva): List<Reserva>"
        ]
    )

    # 8. Conexion (Capa de Conexión)
    draw_box(
        x=70, y=680, w=340, h=130,
        stereo="<<static>>",
        name="Conexion",
        attributes=[
            "- cadenaConexion: string"
        ],
        methods=[
            "+ CrearConexion(): MySqlConnection"
        ],
        is_static=True
    )

    # 9. GestorDAO (Capa de Acceso a Datos / DAO)
    draw_box(
        x=455, y=680, w=480, h=250,
        stereo="",
        name="GestorDAO",
        attributes=[
            "/* Operaciones con MySQL mediante Stored Procedures */"
        ],
        methods=[
            "+ AgregarCliente(nom, ape, tel, mail): bool",
            "+ ModificarCliente(id, nom, ape, tel, mail): bool",
            "+ EliminarCliente(idCliente: int): bool",
            "+ AgregarRecurso(nom, desc, ubic, precio, tipo, ...): bool",
            "+ ModificarRecurso(id, nom, desc, ubic, precio, ...): bool",
            "+ EliminarRecurso(idRecurso: int): bool",
            "+ AltaReserva(idCli, idRec, fecha, hs, tot, estado): bool",
            "+ ModificarReserva(idRes, fecha, hs, tot): bool",
            "+ CancelarReserva(idReserva: int): bool"
        ]
    )

    # =========================================================================
    # FLECHAS Y CONEXIONES UML
    # =========================================================================
    def draw_triangle(tip_x, tip_y, size=14, direction="up", fill_color=(255, 255, 255), outline_color=LINE_COLOR):
        if direction == "up":
            pts = [(tip_x, tip_y), (tip_x - size/2, tip_y + size), (tip_x + size/2, tip_y + size)]
        elif direction == "down":
            pts = [(tip_x, tip_y), (tip_x - size/2, tip_y - size), (tip_x + size/2, tip_y - size)]
        elif direction == "left":
            pts = [(tip_x, tip_y), (tip_x + size, tip_y - size/2), (tip_x + size, tip_y + size/2)]
        elif direction == "right":
            pts = [(tip_x, tip_y), (tip_x - size, tip_y - size/2), (tip_x - size, tip_y + size/2)]
        draw.polygon(pts, fill=fill_color, outline=outline_color)

    # A) Recurso IMPLEMENTA IReservable (Flecha discontinua con triángulo hueco apuntando a IReservable)
    # De Recurso (x=440, y=155) a IReservable (x=350, y=155)
    # Dibujar linea de guiones
    x_start = 440
    x_end = 350 + 14
    y_pos = 155
    step = 8
    cur_x = x_start
    while cur_x > x_end:
        draw.line([(cur_x, y_pos), (max(cur_x - step, x_end), y_pos)], fill=LINE_COLOR, width=2)
        cur_x -= step * 2
    draw_triangle(350, 155, size=14, direction="left")
    draw.text((365, 135), "<<implements>>", fill=NAVY2, font=f_class_stereo)

    # B) Sala, OficinaPrivada y PuestoTrabajo HEREDAN de Recurso
    # Triángulo hueco arriba apuntando a Recurso (bottom: x=625, y=320)
    draw_triangle(625, 320, size=14, direction="up")
    # Línea vertical desde el triángulo hasta barra horizontal intermedia y=350
    draw.line([(625, 334), (625, 350)], fill=LINE_COLOR, width=2)
    # Barra horizontal que une las tres clases derivadas (de x=240 a x=1010)
    draw.line([(240, 350), (1010, 350)], fill=LINE_COLOR, width=2)
    # Bajada a Sala (x=240, y=380)
    draw.line([(240, 350), (240, 380)], fill=LINE_COLOR, width=2)
    # Bajada a OficinaPrivada (x=625, y=380)
    draw.line([(625, 350), (625, 380)], fill=LINE_COLOR, width=2)
    # Bajada a PuestoTrabajo (x=1010, y=350)
    draw.line([(1010, 350), (1010, 380)], fill=LINE_COLOR, width=2)
    draw.text((635, 333), "<<extends>>", fill=NAVY2, font=f_class_stereo)

    # C) Reserva ASOCIA con Cliente y Recurso
    # De Reserva (top: x=1550, y=380) a Cliente (bottom: x=1550, y=300)
    draw.line([(1550, 380), (1550, 300)], fill=LINE_COLOR, width=2)
    draw.text((1560, 310), "1", fill=NAVY, font=f_text_bold)
    draw.text((1560, 360), "0..*", fill=NAVY, font=f_text_bold)
    draw.text((1560, 335), "solicita", fill=NAVY2, font=f_class_stereo)

    # De Reserva (left: x=1290, y=420) a Recurso (bottom right: via linea a x=810, y=210)
    draw.line([(1290, 420), (1240, 420)], fill=LINE_COLOR, width=2)
    draw.line([(1240, 420), (1240, 210)], fill=LINE_COLOR, width=2)
    draw.line([(1240, 210), (810, 210)], fill=LINE_COLOR, width=2)
    draw.text((820, 190), "1", fill=NAVY, font=f_text_bold)
    draw.text((1250, 425), "0..*", fill=NAVY, font=f_text_bold)
    draw.text((1050, 190), "asigna recurso", fill=NAVY2, font=f_class_stereo)

    # D) GestoraCoworking AGREGA Reservas (Agregación: rombo hueco en Gestora)
    # De GestoraCoworking (x=1290, y=680) a Reserva (x=1350, y=600)
    # Rombo en (1290, 680)
    draw.line([(1350, 680), (1350, 600)], fill=LINE_COLOR, width=2)
    # Rombo hueco en (1350, 680)
    pts_diamond = [(1350, 666), (1358, 674), (1350, 682), (1342, 674)]
    draw.polygon(pts_diamond, fill=(255, 255, 255), outline=LINE_COLOR)
    draw.text((1360, 640), "1..* en memoria", fill=NAVY2, font=f_class_stereo)

    # E) GestorDAO USA Conexion (Dependencia: flecha discontinua hacia Conexion)
    # De GestorDAO (left: x=455, y=745) a Conexion (right: x=410, y=745)
    cur_x = 455
    target_x = 410 + 10
    y_pos = 745
    while cur_x > target_x:
        draw.line([(cur_x, y_pos), (max(cur_x - step, target_x), y_pos)], fill=LINE_COLOR, width=2)
        cur_x -= step * 2
    # Flecha abierta
    draw.line([(410, 745), (420, 740)], fill=LINE_COLOR, width=2)
    draw.line([(410, 745), (420, 750)], fill=LINE_COLOR, width=2)
    draw.text((415, 725), "<<uses>>", fill=NAVY2, font=f_class_stereo)

    # Pie de pagina técnico del diagrama
    draw.rectangle([(0, H - 45), (W, H)], fill=(245, 248, 252))
    draw.line([(0, H - 45), (W, H - 45)], fill=BORDER_COLOR, width=1)
    footer_text = "Algoritmos II · Trabajo Práctico Final 2026 · Instituto Argentino de la Empresa · Tullo, Jonathan Lester — Ortega, David Samuel — Scollo, Maximiliano"
    f_ft = ImageFont.truetype("arial.ttf", 12)
    draw.text((35, H - 32), footer_text, fill=NAVY2, font=f_ft)

    img.save(output_path, dpi=(300, 300))
    print(f"Diagrama UML generado con éxito en: {output_path}")

if __name__ == "__main__":
    create_uml_diagram()
