"""Generate Assignment 2 PDF: AES-128 CBC/CTR decryption report (B&W diagrams)."""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, white, Color

OUT = r"c:\Users\afnan\OneDrive\Desktop\IS A2\Assignment2_Report.pdf"
LIGHT = Color(0.92, 0.92, 0.92)
MED = Color(0.82, 0.82, 0.82)


def fmt8(h):
    """Split 32-char hex into two lines of 8+8 grouped nibbles."""
    h = h.replace(" ", "")
    if len(h) <= 12:
        # short block: group by 4
        parts = [h[i : i + 4] for i in range(0, len(h), 4)]
        return " ".join(parts), ""
    a, b = h[:16], h[16:]
    def g(s):
        return " ".join(s[i : i + 4] for i in range(0, len(s), 4))
    return g(a), g(b)


def draw_box(c, x, y, w, h, title, line1, line2="", fill=white, title_size=8, hex_size=7.5):
    c.setStrokeColor(black)
    c.setFillColor(fill)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", title_size)
    c.drawCentredString(x + w / 2, y + h - 12, title)
    c.setFont("Courier", hex_size)
    mid = y + h / 2 - 2
    if line2:
        c.drawCentredString(x + w / 2, mid + 5, line1)
        c.drawCentredString(x + w / 2, mid - 6, line2)
    else:
        c.drawCentredString(x + w / 2, mid - 2, line1)


def draw_xor(c, cx, cy, r=10):
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(1.4)
    c.circle(cx, cy, r, fill=1, stroke=1)
    c.line(cx - r * 0.55, cy, cx + r * 0.55, cy)
    c.line(cx, cy - r * 0.55, cx, cy + r * 0.55)


def arrow_down(c, x, y1, y2):
    c.setStrokeColor(black)
    c.setLineWidth(1.1)
    c.line(x, y1, x, y2 + 5)
    c.line(x, y2 + 5, x - 3.5, y2 + 11)
    c.line(x, y2 + 5, x + 3.5, y2 + 11)


def arrow_right(c, x1, y, x2):
    c.setStrokeColor(black)
    c.setLineWidth(1.1)
    c.line(x1, y, x2 - 5, y)
    c.line(x2 - 5, y, x2 - 11, y + 3.5)
    c.line(x2 - 5, y, x2 - 11, y - 3.5)


def dashed_h(c, x1, y, x2):
    c.setStrokeColor(black)
    c.setDash(3, 2)
    c.setLineWidth(1)
    c.line(x1, y, x2, y)
    c.setDash()


def dashed_v(c, x, y1, y2):
    c.setStrokeColor(black)
    c.setDash(3, 2)
    c.setLineWidth(1)
    c.line(x, y1, x, y2)
    c.setDash()


def draw_cbc_page(c):
    W, H = landscape(A4)
    c.setPageSize(landscape(A4))

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(18 * mm, H - 14 * mm, "Part A — AES-128-CBC Decryption")
    c.setFont("Helvetica", 10)
    c.drawString(
        18 * mm,
        H - 20 * mm,
        "Formula:  Pi = DK(Ci)  XOR  C(i-1)    with  C0 = IV",
    )
    c.setFont("Courier", 8)
    c.drawString(18 * mm, H - 26 * mm, "Key K = 26671722 51915cc4 4cfc2ec3 a88b4d89")

    # Layout metrics
    col_w = 145
    box_w = 128
    box_h = 38
    gap_y = 14
    top = H - 42 * mm
    cols_x = [95, 280, 465]  # left edges of columns
    labels = ["Block 1", "Block 2", "Block 3"]

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

    # Column headers
    for i, lx in enumerate(cols_x):
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(lx + box_w / 2, top + 8, labels[i])

    # IV box (left of XOR row)
    iv_y = top - 3 * (box_h + gap_y) - 8
    iv_x = 18
    iv_w = 70
    iv_h = 48
    l1, l2 = fmt8(IV)
    draw_box(c, iv_x, iv_y, iv_w, iv_h, "IV  (= C0)", l1, l2, fill=LIGHT, title_size=8, hex_size=6.5)

    # Draw three columns
    for i, lx in enumerate(cols_x):
        # Ciphertext
        y_c = top - box_h
        a, b = fmt8(C[i])
        draw_box(c, lx, y_c, box_w, box_h, f"Ciphertext C{i+1}", a, b, fill=white)

        # Arrow to AES
        y_aes = y_c - gap_y - box_h
        arrow_down(c, lx + box_w / 2, y_c, y_aes + box_h)

        # AES decrypt
        draw_box(
            c,
            lx,
            y_aes,
            box_w,
            box_h,
            "AES-128 Decrypt",
            "uses Key K",
            "",
            fill=MED,
            title_size=8,
            hex_size=8,
        )

        # Arrow to D_K
        y_d = y_aes - gap_y - box_h
        arrow_down(c, lx + box_w / 2, y_aes, y_d + box_h)

        a, b = fmt8(D[i])
        draw_box(c, lx, y_d, box_w, box_h, f"DK(C{i+1})  AES output", a, b, fill=LIGHT)

        # Arrow to XOR
        xor_y = y_d - gap_y - 8
        arrow_down(c, lx + box_w / 2, y_d, xor_y + 12)
        draw_xor(c, lx + box_w / 2, xor_y, 11)

        # Plaintext
        y_p = xor_y - gap_y - box_h - 4
        a, b = fmt8(P[i])
        note = ""
        title = f"Plaintext P{i+1}"
        draw_box(c, lx, y_p, box_w, box_h, title, a, b, fill=white)

        if i == 2:
            c.setFont("Helvetica-Oblique", 7.5)
            c.drawCentredString(
                lx + box_w / 2, y_p - 12, "11 trailing 00 bytes = padding"
            )

    # Chaining arrows: IV -> XOR1, C1 -> XOR2, C2 -> XOR3
    xor_centers_y = top - 3 * (box_h + gap_y) - 8  # approx same as xor_y from first col
    # Recompute xor_y consistently
    y_c0 = top - box_h
    y_aes0 = y_c0 - gap_y - box_h
    y_d0 = y_aes0 - gap_y - box_h
    xor_y = y_d0 - gap_y - 8

    # IV to XOR of block 1
    c.setStrokeColor(black)
    c.setDash(2, 2)
    c.setLineWidth(1)
    # from right of IV to left of XOR1
    xor1_x = cols_x[0] + box_w / 2
    c.line(iv_x + iv_w, iv_y + iv_h / 2, xor1_x - 14, xor_y)
    c.setDash()
    # small arrow head
    c.line(xor1_x - 14, xor_y, xor1_x - 20, xor_y + 4)
    c.line(xor1_x - 14, xor_y, xor1_x - 20, xor_y - 4)
    c.setFont("Helvetica", 7)
    c.drawString(iv_x + iv_w + 4, iv_y + iv_h / 2 + 4, "to XOR")

    # From each Ci box right-side down to next XOR (chain)
    for i in range(2):
        # start from bottom-right of Ci
        cx = cols_x[i] + box_w
        cy = y_c0 + box_h / 2
        nx = cols_x[i + 1] + box_w / 2
        # go right then down then left into XOR
        c.setDash(2, 2)
        c.setLineWidth(1)
        mid_x = (cx + cols_x[i + 1]) / 2
        c.line(cx, cy, mid_x, cy)
        c.line(mid_x, cy, mid_x, xor_y)
        c.line(mid_x, xor_y, nx - 14, xor_y)
        c.setDash()
        c.line(nx - 14, xor_y, nx - 20, xor_y + 4)
        c.line(nx - 14, xor_y, nx - 20, xor_y - 4)
        c.setFont("Helvetica", 7)
        c.drawString(mid_x + 2, (cy + xor_y) / 2, f"C{i+1}")

    # Arrow from XOR to plaintext for each (already have down arrow into xor; need out)
    for i, lx in enumerate(cols_x):
        y_p = xor_y - gap_y - box_h - 4
        arrow_down(c, lx + box_w / 2, xor_y - 11, y_p + box_h)

    # Footer note
    c.setFont("Helvetica", 8)
    c.drawString(
        18 * mm,
        12 * mm,
        "All values in hexadecimal. Diagram is original (monochrome). Chaining uses prior ciphertext (or IV), not prior plaintext.",
    )


def draw_ctr_page(c):
    W, H = landscape(A4)
    c.setPageSize(landscape(A4))

    c.setFont("Helvetica-Bold", 14)
    c.drawString(14 * mm, H - 12 * mm, "Part B — AES-128-CTR Decryption")
    c.setFont("Helvetica", 10)
    c.drawString(
        14 * mm,
        H - 18 * mm,
        "Formulas:  Ti = CTR + (i - 1)     Pi = Ci  XOR  EK(Ti)",
    )
    c.setFont("Courier", 8)
    c.drawString(14 * mm, H - 24 * mm, "Key K = 53153913 a1623f8a 089ee173 60fb9ac9")

    # Row data
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

    bw = 118
    bh = 40
    aes_w = 100
    start_x = 18
    row_tops = [H - 48 * mm, H - 105 * mm, H - 162 * mm]

    for ri, row in enumerate(rows):
        y = row_tops[ri] - bh
        c.setFont("Helvetica-Bold", 10)
        c.drawString(start_x, y + bh + 6, row["label"])

        # Counter
        x = start_x
        a, b = fmt8(row["T"])
        draw_box(c, x, y, bw, bh, row["t_title"], a, b, fill=LIGHT, title_size=7, hex_size=6.5)

        # Arrow to AES
        x2 = x + bw + 12
        arrow_right(c, x + bw, y + bh / 2, x2)

        # AES encrypt
        draw_box(
            c,
            x2,
            y,
            aes_w,
            bh,
            "AES-128 Encrypt",
            "uses Key K",
            "",
            fill=MED,
            title_size=7.5,
            hex_size=8,
        )

        # Arrow to keystream
        x3 = x2 + aes_w + 12
        arrow_right(c, x2 + aes_w, y + bh / 2, x3)

        a, b = fmt8(row["KS"])
        ks_title = f"Keystream EK(T{ri+1})"
        draw_box(c, x3, y, bw, bh, ks_title, a, b, fill=LIGHT, title_size=7, hex_size=6.5)

        if row["partial"]:
            c.setFont("Helvetica-Oblique", 6.5)
            c.drawCentredString(
                x3 + bw / 2,
                y - 10,
                "only first 6 bytes used: c5e999dd 4e4f  (rest unused)",
            )

        # Arrow to XOR
        xor_x = x3 + bw + 22
        xor_y = y + bh / 2
        arrow_right(c, x3 + bw, xor_y, xor_x - 11)
        draw_xor(c, xor_x, xor_y, 11)

        # Ciphertext above XOR
        cw = 110 if not row["partial"] else 90
        ch = 34
        cx = xor_x - cw / 2
        cy = y + bh + 8
        a, b = fmt8(row["C"])
        draw_box(
            c,
            cx,
            cy,
            cw,
            ch,
            f"Ciphertext C{ri+1}",
            a,
            b if b else "",
            fill=white,
            title_size=7,
            hex_size=6.5,
        )
        # arrow down from C to XOR
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.line(xor_x, cy, xor_x, xor_y + 11)

        # Arrow to plaintext
        px = xor_x + 22
        arrow_right(c, xor_x + 11, xor_y, px)

        pw = 118 if not row["partial"] else 100
        a, b = fmt8(row["P"])
        draw_box(
            c,
            px,
            y,
            pw,
            bh,
            f"Plaintext P{ri+1}",
            a,
            b if b else "",
            fill=white,
            title_size=7.5,
            hex_size=6.5,
        )

        if row["partial"]:
            c.setFont("Helvetica-Oblique", 7)
            c.drawCentredString(px + pw / 2, y - 10, "6 bytes — no padding needed")

    # +1 dashed links between counters (pointing downward)
    for ri in range(2):
        y_from = row_tops[ri] - bh  # bottom of upper counter
        y_to = row_tops[ri + 1]  # top of lower label / just above counter
        y_lower_box = row_tops[ri + 1] - bh
        cx = start_x + bw / 2
        dashed_v(c, cx, y_from, y_lower_box + bh)
        # arrow head pointing down into next counter
        tip = y_lower_box + bh
        c.setStrokeColor(black)
        c.setFillColor(black)
        c.setLineWidth(1)
        path = c.beginPath()
        path.moveTo(cx, tip)
        path.lineTo(cx - 4, tip + 8)
        path.lineTo(cx + 4, tip + 8)
        path.close()
        c.drawPath(path, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(cx + 8, (y_from + tip) / 2 - 3, "+1")

    c.setFont("Helvetica", 8)
    c.drawString(
        14 * mm,
        10 * mm,
        "All values in hexadecimal. Counter increments by 1 each block. Block 3 ciphertext is only 6 bytes.",
    )


def draw_answers_page(c):
    W, H = A4
    c.setPageSize(A4)
    margin = 20 * mm
    y = H - 20 * mm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "CS3002 — Assignment 2: Block Cipher Modes Decryption")
    y -= 8 * mm
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Recovered plaintexts and discussion answers")
    y -= 12 * mm

    # CBC plaintext
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Recovered Plaintext — Message 1 (AES-128-CBC)")
    y -= 7 * mm
    c.setFont("Courier", 8.5)
    pt_cbc = (
        "dead1111 1beef222 2cafe333 3333dead "
        "44444bee f66cafe7 7777dead 888beef9 "
        "999999ca fe000000 00000000 00000000"
    )
    # wrap
    for line in [
        "dead11111beef2222cafe3333333dead",
        "44444beef66cafe77777dead888beef9",
        "999999cafe0000000000000000000000",
    ]:
        a, b = fmt8(line)
        c.drawString(margin + 4, y, a + "  " + b)
        y -= 5 * mm
    c.setFont("Helvetica", 9)
    y -= 2 * mm
    c.setFont("Courier", 7)
    c.drawString(
        margin,
        y,
        "Full (48 bytes): dead11111beef2222cafe3333333dead44444beef66cafe77777dead888beef9999999cafe0000000000000000000000",
    )
    y -= 5 * mm
    c.setFont("Helvetica", 9)
    c.drawString(
        margin,
        y,
        "Last 11 bytes are 00 padding so the final CBC block is a full 16 bytes.",
    )
    y -= 12 * mm

    # Q4
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Question 4 — Can CBC decryption be parallelized?")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    q4 = (
        "Yes. CBC encryption must run in order because each new ciphertext block needs the previous "
        "ciphertext. CBC decryption is different. All ciphertext blocks C1, C2, C3 are already known "
        "as inputs. Each AES decrypt step DK(Ci) only needs that block Ci and the shared key, so those "
        "AES operations can run at the same time. After that, XOR with IV or C(i-1) also uses only "
        "known ciphertext. The CBC diagram shows each AES decrypt box taking only its own Ci — it does "
        "not wait for the previous plaintext. So the sequential limit of CBC encryption does not apply "
        "to decryption in the same way."
    )
    y = draw_wrapped(c, q4, margin, y, W - 2 * margin, 10, 13)
    y -= 12 * mm

    # CTR plaintext
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Recovered Plaintext — Message 2 (AES-128-CTR)")
    y -= 7 * mm
    c.setFont("Courier", 8.5)
    for line in [
        "badface11111111111c0ffee11111111",
        "1111deaf11111111111feed1111111de",
        "cade111faced",
    ]:
        a, b = fmt8(line)
        text = a + (("  " + b) if b else "")
        c.drawString(margin + 4, y, text)
        y -= 5 * mm
    c.setFont("Helvetica", 9)
    y -= 2 * mm
    c.drawString(
        margin,
        y,
        "Full CTR plaintext (hex): badface11111111111c0ffee111111111111deaf11111111111feed1111111decade111faced",
    )
    y -= 5 * mm
    c.drawString(margin, y, "Length: 38 bytes. No padding bytes.")
    y -= 12 * mm

    # Q6
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Question 6 — Why is padding not required in CTR mode?")
    y -= 7 * mm
    c.setFont("Helvetica", 10)
    q6 = (
        "CTR mode turns AES into a stream cipher. It encrypts a counter to make a keystream, then "
        "XORs that keystream with the data. The ciphertext can be the same length as the plaintext. "
        "If the last piece is shorter than 16 bytes, only that many keystream bytes are used. In this "
        "message the last ciphertext is 0f3788c2e2a2 (6 bytes), so only the first 6 keystream bytes "
        "are XORed and the rest are unused. CBC works on full 16-byte blocks, so leftover space must "
        "be filled with padding (here trailing zero bytes on the CBC plaintext). CTR does not need that."
    )
    y = draw_wrapped(c, q6, margin, y, W - 2 * margin, 10, 13)

    y -= 14 * mm
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        margin,
        y,
        "Method: AES-128 block encrypt/decrypt with CBC chaining and CTR counter increment, plus XOR.",
    )


def draw_wrapped(c, text, x, y, max_w, font_size, leading):
    c.setFont("Helvetica", font_size)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, "Helvetica", font_size) <= max_w:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


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
