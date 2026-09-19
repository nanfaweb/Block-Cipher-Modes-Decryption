"""Generate Assignment 2 PDF: AES-128 CBC/CTR decryption report (B&W)."""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame

OUT = r"c:\Users\afnan\OneDrive\Desktop\IS A2\Assignment2_Report.pdf"
LIGHT = Color(0.93, 0.93, 0.93)
MED = Color(0.84, 0.84, 0.84)

pdfmetrics.registerFont(TTFont("TNR", r"C:\Windows\Fonts\times.ttf"))
pdfmetrics.registerFont(TTFont("TNR-Bold", r"C:\Windows\Fonts\timesbd.ttf"))
pdfmetrics.registerFont(TTFont("TNR-Italic", r"C:\Windows\Fonts\timesi.ttf"))
pdfmetrics.registerFont(TTFont("TNR-BI", r"C:\Windows\Fonts\timesbi.ttf"))
pdfmetrics.registerFont(TTFont("CourierNew", r"C:\Windows\Fonts\cour.ttf"))
pdfmetrics.registerFont(TTFont("CourierNew-Bold", r"C:\Windows\Fonts\courbd.ttf"))
pdfmetrics.registerFontFamily(
    "TNR",
    normal="TNR",
    bold="TNR-Bold",
    italic="TNR-Italic",
    boldItalic="TNR-BI",
)


def hex_lines(h):
    """Return 1–2 readable hex lines (groups of 4)."""
    h = h.replace(" ", "").lower()
    g = " ".join(h[i : i + 4] for i in range(0, len(h), 4))
    if len(h) <= 16:
        return [g]
    mid = len(g) // 2
    # split near middle space
    sp = g.find(" ", mid - 4)
    if sp < 0:
        sp = mid
    return [g[:sp].strip(), g[sp:].strip()]


def draw_box(c, x, y, w, h, title, hex_str, fill=white, title_size=8, hex_size=7):
    """Draw a labeled box. Hex is centered and clipped to fit."""
    c.setStrokeColor(black)
    c.setFillColor(fill)
    c.setLineWidth(1.15)
    c.rect(x, y, w, h, fill=1, stroke=1)

    c.setFillColor(black)
    c.setFont("TNR-Bold", title_size)
    c.drawCentredString(x + w / 2.0, y + h - 11, title)

    lines = hex_lines(hex_str) if hex_str else []
    c.setFont("CourierNew", hex_size)
    if len(lines) == 0:
        return
    if len(lines) == 1:
        c.drawCentredString(x + w / 2.0, y + 12, lines[0])
    else:
        c.drawCentredString(x + w / 2.0, y + 18, lines[0])
        c.drawCentredString(x + w / 2.0, y + 7, lines[1])


def draw_op_box(c, x, y, w, h, title, subtitle, fill=MED):
    c.setStrokeColor(black)
    c.setFillColor(fill)
    c.setLineWidth(1.15)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("TNR-Bold", 8)
    c.drawCentredString(x + w / 2.0, y + h / 2.0 + 4, title)
    c.setFont("TNR", 7)
    c.drawCentredString(x + w / 2.0, y + h / 2.0 - 8, subtitle)


def draw_xor(c, cx, cy, r=9):
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(1.3)
    c.circle(cx, cy, r, fill=1, stroke=1)
    c.line(cx - r * 0.55, cy, cx + r * 0.55, cy)
    c.line(cx, cy - r * 0.55, cx, cy + r * 0.55)


def arrow_v(c, x, y_top, y_bot):
    """Arrow pointing down from y_top to y_bot."""
    c.setStrokeColor(black)
    c.setFillColor(black)
    c.setLineWidth(1.0)
    tip = y_bot + 1
    c.line(x, y_top, x, tip + 7)
    p = c.beginPath()
    p.moveTo(x, tip)
    p.lineTo(x - 3.2, tip + 7)
    p.lineTo(x + 3.2, tip + 7)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def arrow_h(c, x_left, y, x_right):
    """Arrow pointing right from x_left to x_right."""
    c.setStrokeColor(black)
    c.setFillColor(black)
    c.setLineWidth(1.0)
    tip = x_right - 1
    c.line(x_left, y, tip - 7, y)
    p = c.beginPath()
    p.moveTo(tip, y)
    p.lineTo(tip - 7, y + 3.2)
    p.lineTo(tip - 7, y - 3.2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def draw_cbc_page(c):
    W, H = landscape(A4)
    c.setPageSize(landscape(A4))

    # Title block
    c.setFont("TNR-Bold", 16)
    c.drawCentredString(W / 2, H - 16 * mm, "Part A: AES-128-CBC Decryption")
    c.setFont("TNR", 10)
    c.drawCentredString(
        W / 2,
        H - 22 * mm,
        "Formula:  Pi = DK(Ci) XOR C(i-1) ,   where C0 = IV",
    )
    c.setFont("CourierNew", 8)
    c.drawCentredString(
        W / 2,
        H - 27.5 * mm,
        "Key K = 26671722 51915cc4 4cfc2ec3 a88b4d89",
    )

    C = [
        "9a8460ce302b68a3feb172a2fd89a5b2",
        "8f203e5e67ad1bc5022fa2837a2b8222",
        "77cc0976ac42593dc8b5b4e70816ec87",
    ]
    D = [
        "732e20d42a775e0534ea4c9c7035b8c5",
        "dec02b20c647c74489c6ac0f75024b4b",
        "16b9a79499ad1bc5022fa2837a2b8222",
    ]
    P = [
        "dead11111beef2222cafe3333333dead",
        "44444beef66cafe77777dead888beef9",
        "999999cafe0000000000000000000000",
    ]
    IV = "ad8331c53199ac271845afaf43066668"

    # Geometry — leave left strip for IV; three equal columns
    left_margin = 12 * mm
    right_margin = 12 * mm
    iv_w = 78
    gap_iv = 14
    usable_left = left_margin + iv_w + gap_iv
    usable_right = W - right_margin
    col_span = usable_right - usable_left
    col_gap = 22
    box_w = (col_span - 2 * col_gap) / 3.0
    box_h = 42
    v_gap = 11
    xor_r = 9

    top = H - 36 * mm
    cols_x = [usable_left + i * (box_w + col_gap) for i in range(3)]

    # Column titles
    for i, lx in enumerate(cols_x):
        c.setFont("TNR-Bold", 11)
        c.drawCentredString(lx + box_w / 2, top + 4, f"Block {i + 1}")

    # Vertical positions (shared)
    y_c = top - box_h
    y_aes = y_c - v_gap - box_h
    y_d = y_aes - v_gap - box_h
    xor_cy = y_d - v_gap - xor_r - 2
    y_p = xor_cy - xor_r - v_gap - box_h

    # Draw columns
    for i, lx in enumerate(cols_x):
        cx = lx + box_w / 2

        draw_box(c, lx, y_c, box_w, box_h, f"Ciphertext C{i + 1}", C[i], fill=white, title_size=8, hex_size=6.8)
        arrow_v(c, cx, y_c, y_aes + box_h)

        draw_op_box(c, lx, y_aes, box_w, box_h, "AES-128 Decrypt", "uses Key K", fill=MED)
        arrow_v(c, cx, y_aes, y_d + box_h)

        draw_box(c, lx, y_d, box_w, box_h, f"DK(C{i + 1})  AES output", D[i], fill=LIGHT, title_size=8, hex_size=6.8)
        arrow_v(c, cx, y_d, xor_cy + xor_r)

        draw_xor(c, cx, xor_cy, xor_r)
        arrow_v(c, cx, xor_cy - xor_r, y_p + box_h)

        draw_box(c, lx, y_p, box_w, box_h, f"Plaintext P{i + 1}", P[i], fill=white, title_size=8, hex_size=6.8)

        if i == 2:
            c.setFont("TNR-Italic", 8)
            c.drawCentredString(cx, y_p - 11, "11 trailing 00 bytes = padding")

    # IV box aligned with XOR row
    iv_h = 50
    iv_x = left_margin
    iv_y = xor_cy - iv_h / 2
    draw_box(c, iv_x, iv_y, iv_w, iv_h, "IV  (= C0)", IV, fill=LIGHT, title_size=8, hex_size=6.2)

    # IV -> XOR1 (dashed)
    c.setStrokeColor(black)
    c.setDash(2.5, 2)
    c.setLineWidth(1)
    x1 = cols_x[0] + box_w / 2
    c.line(iv_x + iv_w, xor_cy, x1 - xor_r - 1, xor_cy)
    c.setDash()
    c.setFont("TNR", 7)
    c.drawCentredString((iv_x + iv_w + x1 - xor_r) / 2, xor_cy + 5, "to XOR")

    # Chain C1 -> XOR2, C2 -> XOR3 (dashed, in the column gutters)
    for i in range(2):
        src_right = cols_x[i] + box_w
        src_cy = y_c + box_h / 2
        dst_cx = cols_x[i + 1] + box_w / 2
        gutter = cols_x[i] + box_w + col_gap / 2

        c.setDash(2.5, 2)
        c.setLineWidth(1)
        c.line(src_right, src_cy, gutter, src_cy)
        c.line(gutter, src_cy, gutter, xor_cy)
        c.line(gutter, xor_cy, dst_cx - xor_r - 1, xor_cy)
        c.setDash()

        c.setFont("TNR-Bold", 7)
        # place label to the right of the vertical gutter line, away from boxes
        c.drawString(gutter + 3, (src_cy + xor_cy) / 2 - 2, f"C{i + 1}")

    # Footer
    c.setFont("TNR", 8)
    c.drawCentredString(
        W / 2,
        10 * mm,
        "All values are hexadecimal. Chaining uses the previous ciphertext (or IV), not the previous plaintext.",
    )


def draw_ctr_page(c):
    W, H = landscape(A4)
    c.setPageSize(landscape(A4))

    c.setFont("TNR-Bold", 16)
    c.drawCentredString(W / 2, H - 14 * mm, "Part B: AES-128-CTR Decryption")
    c.setFont("TNR", 10)
    c.drawCentredString(
        W / 2,
        H - 20 * mm,
        "Formulas:  Ti = CTR + (i - 1)     and     Pi = Ci XOR EK(Ti)",
    )
    c.setFont("CourierNew", 8)
    c.drawCentredString(
        W / 2,
        H - 25.5 * mm,
        "Key K = 53153913 a1623f8a 089ee173 60fb9ac9",
    )

    rows = [
        {
            "label": "Block 1",
            "t_title": "Counter T1 = CTR + 0",
            "T": "d441e7c1fa329130bbaea83918ea5cc9",
            "KS": "c85aa5eb370e9ea2b27664c2aa8de851",
            "C": "7285090a261f8fb3a3b69b2cbb9cf940",
            "P": "badface11111111111c0ffee11111111",
            "partial": False,
        },
        {
            "label": "Block 2",
            "t_title": "Counter T2 = CTR + 1",
            "T": "d441e7c1fa329130bbaea83918ea5cca",
            "KS": "48c325d3ef2ea51f37542e0fd9d81cc4",
            "C": "59d2fb7cfe3fb40e264bc0dec8c90d1a",
            "P": "1111deaf11111111111feed1111111de",
            "partial": False,
        },
        {
            "label": "Block 3 (partial)",
            "t_title": "Counter T3 = CTR + 2",
            "T": "d441e7c1fa329130bbaea83918ea5ccb",
            "KS": "c5e999dd4e4f994359c4875a1339077d",
            "C": "0f3788c2e2a2",
            "P": "cade111faced",
            "partial": True,
        },
    ]

    # Horizontal layout with reserved bands so C boxes never collide with next row
    margin_x = 12 * mm
    bw = 128          # counter / keystream / plaintext width
    aes_w = 92
    c_w = 128
    bh = 40
    c_h = 36
    xor_r = 9
    h_gap = 10

    # Total content width check
    # counter + gap + aes + gap + ks + gap + xor + gap + p  (+ C sits above xor/p area)
    start_x = margin_x

    # Vertical: header ends ~ H-28mm; footer at 10mm; 3 equal bands
    band_top = H - 32 * mm
    band_bottom = 18 * mm
    band_h = (band_top - band_bottom) / 3.0

    counter_centers_x = []
    counter_bottoms = []

    for ri, row in enumerate(rows):
        band_y0 = band_top - (ri + 1) * band_h   # bottom of this band
        band_y1 = band_top - ri * band_h         # top of this band

        # Layout inside band (top to bottom):
        #   label
        #   ciphertext box (centered over XOR column)
        #   main row: T -> AES -> KS -> XOR -> P
        #   optional note under KS / P
        label_y = band_y1 - 11
        c.setFont("TNR-Bold", 10)
        c.drawString(start_x, label_y, row["label"])

        main_y = band_y0 + 16   # bottom of main boxes
        if row["partial"]:
            main_y = band_y0 + 20

        # X positions
        x_t = start_x
        x_aes = x_t + bw + h_gap
        x_ks = x_aes + aes_w + h_gap
        xor_x = x_ks + bw + h_gap + xor_r + 4
        x_p = xor_x + xor_r + h_gap + 4

        mid_y = main_y + bh / 2

        # Counter
        draw_box(c, x_t, main_y, bw, bh, row["t_title"], row["T"], fill=LIGHT, title_size=7.5, hex_size=6.5)
        counter_centers_x.append(x_t + bw / 2)
        counter_bottoms.append(main_y)

        arrow_h(c, x_t + bw, mid_y, x_aes)

        draw_op_box(c, x_aes, main_y, aes_w, bh, "AES-128 Encrypt", "uses Key K", fill=MED)
        arrow_h(c, x_aes + aes_w, mid_y, x_ks)

        draw_box(c, x_ks, main_y, bw, bh, f"Keystream EK(T{ri + 1})", row["KS"], fill=LIGHT, title_size=7.5, hex_size=6.5)
        arrow_h(c, x_ks + bw, mid_y, xor_x - xor_r)

        draw_xor(c, xor_x, mid_y, xor_r)

        # Ciphertext ABOVE XOR, inside this band only
        c_box_y = main_y + bh + 6
        # ensure it stays below the label
        max_c_top = label_y - 3
        if c_box_y + c_h > max_c_top:
            c_box_y = max_c_top - c_h
        c_box_x = xor_x - c_w / 2
        draw_box(
            c,
            c_box_x,
            c_box_y,
            c_w,
            c_h,
            f"Ciphertext C{ri + 1}",
            row["C"],
            fill=white,
            title_size=7.5,
            hex_size=6.5,
        )
        # line from C down to XOR
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.line(xor_x, c_box_y, xor_x, mid_y + xor_r)

        arrow_h(c, xor_x + xor_r, mid_y, x_p)

        pw = bw if not row["partial"] else 108
        draw_box(
            c,
            x_p,
            main_y,
            pw,
            bh,
            f"Plaintext P{ri + 1}",
            row["P"],
            fill=white,
            title_size=7.5,
            hex_size=6.5,
        )

        if row["partial"]:
            c.setFont("TNR-Italic", 7)
            c.drawCentredString(
                x_ks + bw / 2,
                main_y - 10,
                "only first 6 bytes used: c5e999dd 4e4f (rest unused)",
            )
            c.drawCentredString(x_p + pw / 2, main_y - 10, "6 bytes - no padding needed")

    # +1 links between counters
    for ri in range(2):
        cx = counter_centers_x[ri]
        y_from = counter_bottoms[ri]
        y_to = counter_bottoms[ri + 1] + bh
        c.setDash(2.5, 2)
        c.setLineWidth(1)
        c.setStrokeColor(black)
        c.line(cx, y_from, cx, y_to)
        c.setDash()
        # arrow down
        c.setFillColor(black)
        p = c.beginPath()
        p.moveTo(cx, y_to)
        p.lineTo(cx - 3.5, y_to + 7)
        p.lineTo(cx + 3.5, y_to + 7)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.setFont("TNR-Bold", 9)
        c.drawString(cx + 6, (y_from + y_to) / 2 - 2, "+1")

    c.setFont("TNR", 8)
    c.drawCentredString(
        W / 2,
        8 * mm,
        "All values are hexadecimal. The counter increments by 1 for each block. Block 3 ciphertext is 6 bytes.",
    )


def make_styles():
    return {
        "title": ParagraphStyle(
            "title",
            fontName="TNR-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontName="TNR-Italic",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="TNR-Bold",
            fontSize=13,
            leading=17,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="TNR-Bold",
            fontSize=12,
            leading=15,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="TNR",
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "hex": ParagraphStyle(
            "hex",
            fontName="CourierNew",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            leftIndent=8,
            spaceAfter=3,
        ),
        "note": ParagraphStyle(
            "note",
            fontName="TNR",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="TNR-Italic",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            spaceBefore=12,
        ),
    }


def draw_answers_page(c):
    W, H = A4
    c.setPageSize(A4)
    styles = make_styles()
    margin = 20 * mm

    story = []
    story.append(Paragraph("CS3002 - Assignment 2", styles["title"]))
    story.append(Paragraph("Block Cipher Modes Decryption", styles["title"]))
    story.append(Paragraph("Recovered Plaintexts and Discussion Answers", styles["subtitle"]))

    story.append(Paragraph("1. Recovered Plaintext - Message 1 (AES-128-CBC)", styles["h1"]))
    story.append(Paragraph("P1: dead1111 1beef222 2cafe333 3333dead", styles["hex"]))
    story.append(Paragraph("P2: 44444bee f66cafe7 7777dead 888beef9", styles["hex"]))
    story.append(Paragraph("P3: 999999ca fe000000 00000000 00000000", styles["hex"]))
    story.append(Paragraph("Full plaintext (48 bytes, hex):", styles["note"]))
    story.append(
        Paragraph(
            "dead1111 1beef222 2cafe333 3333dead "
            "44444bee f66cafe7 7777dead 888beef9 "
            "999999ca fe000000 00000000 00000000",
            styles["hex"],
        )
    )
    story.append(
        Paragraph(
            "The last eleven bytes are 00 padding. CBC requires full 16-byte blocks, so padding "
            "was added to complete the final block.",
            styles["body"],
        )
    )

    story.append(Paragraph("2. Question 4 - Can CBC Decryption Be Parallelized?", styles["h1"]))
    story.append(
        Paragraph(
            "Yes. CBC encryption must run in order because each new ciphertext block needs the "
            "previous ciphertext. CBC decryption is different. All ciphertext blocks C1, C2 and C3 "
            "are already known as inputs. Each AES decrypt step DK(Ci) only needs that block Ci and "
            "the shared key, so those AES operations can run at the same time. After that, XOR with "
            "IV or C(i-1) also uses only known ciphertext. The CBC diagram shows each AES decrypt "
            "box taking only its own Ci; it does not wait for the previous plaintext. Therefore the "
            "sequential limit of CBC encryption does not apply to decryption in the same way.",
            styles["body"],
        )
    )

    story.append(Paragraph("3. Recovered Plaintext - Message 2 (AES-128-CTR)", styles["h1"]))
    story.append(Paragraph("P1: badface1 11111111 11c0ffee 11111111", styles["hex"]))
    story.append(Paragraph("P2: 1111deaf 11111111 111feed1 111111de", styles["hex"]))
    story.append(Paragraph("P3: cade 111f aced", styles["hex"]))
    story.append(Paragraph("Full plaintext (38 bytes, hex):", styles["note"]))
    story.append(
        Paragraph(
            "badface1 11111111 11c0ffee 11111111 "
            "1111deaf 11111111 111feed1 111111de "
            "cade111f aced",
            styles["hex"],
        )
    )
    story.append(
        Paragraph(
            "Length: 38 bytes. There are no padding bytes.",
            styles["body"],
        )
    )

    story.append(Paragraph("4. Question 6 - Why Is Padding Not Required in CTR Mode?", styles["h1"]))
    story.append(
        Paragraph(
            "CTR mode turns AES into a stream cipher. It encrypts a counter to make a keystream, "
            "then XORs that keystream with the data. The ciphertext can be the same length as the "
            "plaintext. If the last piece is shorter than 16 bytes, only that many keystream bytes "
            "are used. In this message the last ciphertext is 0f3788c2e2a2 (6 bytes), so only the "
            "first 6 keystream bytes are XORed and the rest are unused. CBC works on full 16-byte "
            "blocks, so leftover space must be filled with padding (here trailing zero bytes on the "
            "CBC plaintext). CTR does not need that.",
            styles["body"],
        )
    )

    story.append(
        Paragraph(
            "Method: AES-128 block encrypt/decrypt with CBC chaining and CTR counter increment, plus XOR.",
            styles["footer"],
        )
    )

    frame = Frame(margin, margin, W - 2 * margin, H - 2 * margin, showBoundary=0)
    frame.addFromList(story, c)


def main():
    c = canvas.Canvas(OUT, pagesize=landscape(A4))
    draw_cbc_page(c)
    c.showPage()
    draw_ctr_page(c)
    c.showPage()
    draw_answers_page(c)
    c.save()
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
