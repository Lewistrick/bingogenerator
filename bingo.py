import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

SQSIZE = 60
SPACING = 15

def make_col(start, end, n=5):
    """Maak een kolom met getallen."""
    nums = np.random.choice(np.arange(start, end+1), size=n, replace=False)
    return nums

def generate_card():
    """Maak een bingokaart en sla 'm als afbeelding op."""

    # Maak 5 kolommen
    cols = np.array([make_col(15*i + 1, 15*i + 15) for i in range(5)])

    # Vervang het middelste element door de mediaan van de middelste kolom
    # zodat die in het midden eindigt als je de kolom sorteert
    cols[2, 2] = np.median(np.r_[
        cols[2, :2],
        cols[2, 3:]
    ])

    # Sorteer de kolommen
    rows = np.sort(cols.T, axis=0)
    rows[2, 2] = -1

    cols = rows.T

    # Create the bingo image and fill the background with a light color
    bgcolor = tuple(np.random.randint(200, 255) for _ in range(3))
    textcolor = tuple(np.random.randint(50, 150) for _ in range(3))
    img_width = 5 * SQSIZE + 6 * SPACING
    img_height = 6 * SQSIZE + 7 * SPACING
    img = Image.new("RGB", (img_width, img_height), color=bgcolor)

    draw = ImageDraw.Draw(img)
    topfont = ImageFont.truetype(r"C:\Windows\Fonts\CALIST.TTF", size=int(SQSIZE * 0.75))

    for rowidx in range(5):
        # Toon een letter van BINGO bovenaan
        x0 = SPACING + SQSIZE // 4 + (SPACING + SQSIZE) * rowidx
        y0 = SPACING
        draw.text((x0, y0), "BINGO"[rowidx], font=topfont, fill=textcolor)

        for colidx in range(5):
            # Maak een vierkantje
            x0 = SPACING + (SPACING + SQSIZE) * rowidx
            y0 = SPACING + (SPACING + SQSIZE) * (colidx + 1)
            x1 = x0 + SQSIZE
            y1 = y0 + SQSIZE
            draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0))

            # Toon het getal
            text = str(rows[colidx, rowidx])
            font = ImageFont.truetype(r"C:\Windows\Fonts\CALIST.TTF", size=SQSIZE // 2)
            textcoords = (x0+SPACING, y0+SPACING)

            # Centreer getallen kleiner dan 10
            if rows[colidx, rowidx] < 10:
                textcoords = (x0 + int(SPACING * 1.5), y0 + SPACING)

            # Voor het middelste vakje: andere tekst, andere grootte
            if rowidx == colidx == 2:
                text = "BONUS"
                font = ImageFont.truetype(r"C:\Windows\Fonts\CALIST.TTF", size=SQSIZE // 5)
                textcoords = (x0 + SPACING // 2 + 1, y0 + int(SPACING * 1.5))

            # Zet de tekst op de afbeelding
            draw.text(textcoords, text, font=font, fill=textcolor)

    # Maak een bestandsnaam met volgnr
    bingodir = Path(__file__).parent
    volgnr = 0
    while True:
        fn = bingodir / f"kaart{volgnr:03d}.png"
        if not fn.is_file():
            break
        volgnr += 1

    img.save(fn)

if __name__ == "__main__":
    for _ in tqdm(range(150)):
        generate_card()
