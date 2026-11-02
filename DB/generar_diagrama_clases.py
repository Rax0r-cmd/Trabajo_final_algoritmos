# -*- coding: utf-8 -*-
"""
Generador del Diagrama de Clases UML Simplificado del Dominio y POO
Algoritmos II — Trabajo Práctico Final 2026
Instituto Argentino de la Empresa

Diseño optimizado:
- Tipografía GRANDE y nítida (17-24 pt) para lectura directa al 100% en hojas A4 sin zoom.
- Dimensionamiento dinámico de cajas: el texto NUNCA se desborda ni pisa los bordes.
- Separación clara entre GestoraCoworking (negocio) y GestorDAO (persistencia MySQL).
- Relaciones estándar UML (herencia, interfaces, agregación, multiplicidades 1 a 0..*).
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_uml_diagram(output_path="DB/Diagrama_Clases_UML.png"):
    W, H = 1260, 1310
    img = Image.new("RGB", (W, H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Tipografía grande y de alta definición
    f_title = ImageFont.truetype("arialbd.ttf", 23)
    f_sub = ImageFont.truetype("arial.ttf", 14)
    f_name = ImageFont.truetype("arialbd.ttf", 20)
    f_stereo = ImageFont.truetype("ariali.ttf", 16)
    f_txt = ImageFont.truetype("arial.ttf", 17)
    f_txt_bold = ImageFont.truetype("arialbd.ttf", 17)
    f_txt_italic = ImageFont.truetype("ariali.ttf", 17)
    f_card = ImageFont.truetype("arialbd.ttf", 15)
    f_note = ImageFont.truetype("ariali.ttf", 13)

    COLOR_BLACK = (0, 0, 0)
    BORDER_COLOR = (0, 0, 0)
    HEADER_BG = (242, 242, 242)
    BOX_BG = (255, 255, 255)
    SHADOW_COLOR = (225, 225, 225)
    LINE_COLOR = (0, 0, 0)

    # 1. Encabezado institucional superior
    draw.rectangle([(0, 0), (W, 60)], fill=(245, 245, 245), outline=BORDER_COLOR, width=2)
    draw.text((25, 10), "DIAGRAMA DE CLASES SIMPLIFICADO — MODELO DE DOMINIO Y POO", fill=COLOR_BLACK, font=f_title)
    draw.text((25, 36), "Jerarquía de Herencia, Implementación de Interfaz y Capas del Sistema (C# .NET / MySQL)", fill=(70, 70, 70), font=f_sub)

    # 2. Función de dibujo de clases con cálculo dinámico exacto de altura
    def draw_box(x, y, w, stereo, name, attributes, methods, is_abstract=False):
        line_h = 28
        header_h = 56 if stereo else 44
        attr_h = (len(attributes) * line_h) + (16 if attributes else 0)
        meth_h = (len(methods) * line_h) + (16 if methods else 0)
        total_h = header_h + attr_h + meth_h + (10 if (not attributes and not methods) else 6)

        # Sombra
        draw.rectangle([(x + 4, y + 4), (x + w + 4, y + total_h + 4)], fill=SHADOW_COLOR)
        # Borde exterior de la caja
        draw.rectangle([(x, y), (x + w, y + total_h)], fill=BOX_BG, outline=BORDER_COLOR, width=2)
        # Cabecera
        draw.rectangle([(x, y), (x + w, y + header_h)], fill=HEADER_BG, outline=BORDER_COLOR, width=2)

        curr_y = y + 5
        if stereo:
            s_w = draw.textlength(stereo, font=f_stereo)
            draw.text((x + (w - s_w) / 2, curr_y), stereo, fill=COLOR_BLACK, font=f_stereo)
            curr_y += 22

        n_w = draw.textlength(name, font=f_name)
        draw.text((x + (w - n_w) / 2, curr_y), name, fill=COLOR_BLACK, font=f_name)

        curr_y = y + header_h
        if attributes:
            draw.line([(x, curr_y), (x + w, curr_y)], fill=BORDER_COLOR, width=1)
            curr_y += 8
            for attr in attributes:
                draw.text((x + 14, curr_y), attr, fill=COLOR_BLACK, font=f_txt)
                curr_y += line_h
            curr_y += 8

        if methods:
            draw.line([(x, curr_y), (x + w, curr_y)], fill=BORDER_COLOR, width=1)
            curr_y += 8
            for m in methods:
                m_font = f_txt_italic if ("abstract" in m or (is_abstract and "CalcularCosto" in m)) else f_txt
                draw.text((x + 14, curr_y), m, fill=COLOR_BLACK, font=m_font)
                curr_y += line_h

        return total_h

    # =========================================================================
    # FILA 1: CONTRATO E INTERFAZ BASE Y CLASE ABSTRACTA RECURSO
    # =========================================================================
    h_ires = draw_box(
        x=70, y=85, w=480,
        stereo="<<interface>>",
        name="IReservable",
        attributes=[],
        methods=["+ PuedeReservarse(fecha: DateTime): bool"]
    )

    h_rec = draw_box(
        x=610, y=85, w=570,
        stereo="<<abstract>>",
        name="Recurso",
        attributes=[
            "+ IdRecurso: int",
            "+ Nombre: string",
            "+ PrecioPorHora: decimal"
        ],
        methods=[
            "+ PuedeReservarse(fecha: DateTime): bool",
            "+ CalcularCosto(horas: int): decimal  {abstract}"
        ],
        is_abstract=True
    )

    # Flecha discontinua de implementación (Recurso implementa IReservable)
    # Triángulo hueco apuntando a IReservable
    y_imp = 138
    draw.polygon([(550, y_imp), (568, y_imp - 8), (568, y_imp + 8)], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    cur_x = 610
    while cur_x > 568:
        nxt = max(cur_x - 8, 568)
        draw.line([(cur_x, y_imp), (nxt, y_imp)], fill=LINE_COLOR, width=2)
        cur_x -= 16
    draw.text((554, 112), "<<implements>>", fill=COLOR_BLACK, font=f_note)

    # =========================================================================
    # FILA 2: LAS 3 CLASES DERIVADAS POLIMÓRFICAS (HERENCIA DE RECURSO)
    # =========================================================================
    y_row2 = 390
    h_sala = draw_box(
        x=60, y=y_row2, w=360,
        stereo="",
        name="Sala",
        attributes=["+ CantSillas: int"],
        methods=[
            "+ CalcularCosto(horas: int): decimal",
            "+ PuedeReservarse(fecha: DateTime): bool"
        ]
    )

    h_ofic = draw_box(
        x=450, y=y_row2, w=370,
        stereo="",
        name="OficinaPrivada",
        attributes=["+ MobiliarioIncluido: bool"],
        methods=[
            "+ CalcularCosto(horas: int): decimal",
            "+ PuedeReservarse(fecha: DateTime): bool"
        ]
    )

    h_pues = draw_box(
        x=850, y=y_row2, w=350,
        stereo="",
        name="PuestoTrabajo",
        attributes=["+ NroCategoria: int"],
        methods=[
            "+ CalcularCosto(horas: int): decimal",
            "+ PuedeReservarse(fecha: DateTime): bool"
        ]
    )

    # Conexión de Herencia UML (Árbol con triángulo cerrado en la base de Recurso)
    rec_center_x = 610 + 570 // 2  # 895
    rec_bottom_y = 85 + h_rec      # 319
    # Triángulo cerrado de herencia
    draw.polygon([(rec_center_x, rec_bottom_y), (rec_center_x - 10, rec_bottom_y + 18), (rec_center_x + 10, rec_bottom_y + 18)], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    # Tronco vertical
    draw.line([(rec_center_x, rec_bottom_y + 18), (rec_center_x, 358)], fill=LINE_COLOR, width=2)
    # Barra horizontal colectora
    draw.line([(240, 358), (1025, 358)], fill=LINE_COLOR, width=2)
    # Bajadas a cada clase derivada
    draw.line([(240, 358), (240, y_row2)], fill=LINE_COLOR, width=2)
    draw.line([(635, 358), (635, y_row2)], fill=LINE_COLOR, width=2)
    draw.line([(1025, 358), (1025, y_row2)], fill=LINE_COLOR, width=2)
    draw.text((rec_center_x + 14, rec_bottom_y + 20), "<<extends>>", fill=COLOR_BLACK, font=f_note)

    # =========================================================================
    # FILA 3: ENTIDADES DEL NEGOCIO (CLIENTE, RESERVA Y ESTADORESERVA)
    # =========================================================================
    y_row3 = 620
    h_cli = draw_box(
        x=60, y=y_row3, w=340,
        stereo="",
        name="Cliente",
        attributes=[
            "+ IdCliente: int",
            "+ NombreCompleto: string",
            "+ Mail: string",
            "+ Telefono: string"
        ],
        methods=["+ ToString(): string"]
    )

    h_res = draw_box(
        x=430, y=y_row3, w=440,
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
        methods=["+ ToString(): string"]
    )

    h_est = draw_box(
        x=900, y=y_row3, w=300,
        stereo="<<enumeration>>",
        name="EstadoReserva",
        attributes=[
            "Pendiente = 0",
            "Confirmada = 1",
            "Cancelada = 2"
        ],
        methods=[]
    )

    # Asociación Cliente — Reserva (Multiplicidad 1 a 0..*)
    draw.line([(400, 710), (430, 710)], fill=LINE_COLOR, width=2)
    draw.text((404, 686), "1", fill=COLOR_BLACK, font=f_card)
    draw.text((404, 716), "0..*", fill=COLOR_BLACK, font=f_card)

    # Asociación Reserva — EstadoReserva (Uso tipado con flecha discontinua)
    draw.line([(870, 700), (900, 700)], fill=LINE_COLOR, width=2)
    draw.polygon([(900, 700), (890, 695), (890, 705)], fill=LINE_COLOR, outline=LINE_COLOR)
    draw.text((874, 676), "1", fill=COLOR_BLACK, font=f_card)

    # =========================================================================
    # FILA 4: ARQUITECTURA EN CAPAS (GESTORA DE NEGOCIO Y GESTOR DAO MYSQL)
    # =========================================================================
    y_row4 = 980
    h_gest = draw_box(
        x=70, y=y_row4, w=520,
        stereo="<<capa de negocio>>",
        name="GestoraCoworking",
        attributes=["- listaReservas: List<Reserva>"],
        methods=[
            "+ AgregarReserva(r: Reserva): void",
            "+ CancelarReserva(idReserva: int): void",
            "+ ObtenerReservasPorFecha(f: DateTime): List"
        ]
    )

    h_dao = draw_box(
        x=660, y=y_row4, w=520,
        stereo="<<capa de datos / persistencia>>",
        name="GestorDAO",
        attributes=["- cadenaConexion: string"],
        methods=[
            "+ AltaReserva(r: Reserva): bool",
            "+ CancelarReserva(idReserva: int): bool",
            "+ ConsultarDisponibilidad(id, f, h): bool"
        ]
    )

    # Agregación GestoraCoworking <>---- Reserva (Colección en memoria)
    # Línea en ángulo recto con rombo vacío en GestoraCoworking
    gest_top_x = 70 + 520 // 2     # 330
    res_bot_x = 430 + 440 // 2     # 650
    res_bot_y = y_row3 + h_res     # 926

    # Rombo vacío en la cabecera de GestoraCoworking
    diamond = [(gest_top_x, y_row4), (gest_top_x - 8, y_row4 - 12), (gest_top_x, y_row4 - 24), (gest_top_x + 8, y_row4 - 12)]
    draw.polygon(diamond, fill=(255, 255, 255), outline=LINE_COLOR, width=2)

    # Trazado de conexión de agregación
    draw.line([(gest_top_x, y_row4 - 24), (gest_top_x, 952)], fill=LINE_COLOR, width=2)
    draw.line([(gest_top_x, 952), (res_bot_x - 40, 952)], fill=LINE_COLOR, width=2)
    draw.line([(res_bot_x - 40, 952), (res_bot_x - 40, res_bot_y)], fill=LINE_COLOR, width=2)
    draw.text((gest_top_x + 12, y_row4 - 20), "1", fill=COLOR_BLACK, font=f_card)
    draw.text((res_bot_x - 30, res_bot_y + 6), "1..*", fill=COLOR_BLACK, font=f_card)

    # Dependencia GestorDAO ..> MySQL Stored Procedures
    dao_top_x = 660 + 520 // 2     # 920
    draw.text((dao_top_x - 140, y_row4 - 26), "<<ejecuta Stored Procedures en MySQL>>", fill=COLOR_BLACK, font=f_note)

    # 4. Pie institucional del diagrama
    draw.rectangle([(0, H - 40), (W, H)], fill=(245, 245, 245), outline=BORDER_COLOR, width=1)
    footer_text = "Algoritmos II — Trabajo Práctico Final 2026 — Instituto Argentino de la Empresa — Modelo de Clases UML Simplificado"
    draw.text((25, H - 28), footer_text, fill=COLOR_BLACK, font=f_sub)

    img.save(output_path, dpi=(300, 300))
    print(f"Diagrama UML simplificado de alta legibilidad generado en: {output_path}")

if __name__ == "__main__":
    create_uml_diagram()
