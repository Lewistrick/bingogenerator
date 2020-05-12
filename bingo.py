import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

SQSIZE = 60
SPACING = 15

def make_col(start, end, n=5):
    """Create a column of numbers."""
    nums = np.random.choice(np.arange(start, end+1), size=n, replace=False)
    return nums

def generate_card():
    """Create a bingo card and save it as PNG image."""

    # Create five columns
    cols = np.array([make_col(15*i + 1, 15*i + 15) for i in range(5)])

    # Replace the center cell by the median of the first column
    # so that it ends up in the middle when sorting the columns
    cols[2, 2] = np.median(np.r_[
        cols[2, :2],
        cols[2, 3:]
    ])

    # Sort the columns
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
    numfont = ImageFont.truetype(r"C:\Windows\Fonts\CALIST.TTF", size=SQSIZE // 2)

    for rowidx in range(5):
        # Show one letter from 'BINGO' at the top of the column
        x0 = SPACING + SQSIZE // 4 + (SPACING + SQSIZE) * rowidx
        y0 = SPACING
        draw.text((x0, y0), "BINGO"[rowidx], font=topfont, fill=textcolor)

        for colidx in range(5):
            # Create a square to put the number in
            x0 = SPACING + (SPACING + SQSIZE) * rowidx
            y0 = SPACING + (SPACING + SQSIZE) * (colidx + 1)
            x1 = x0 + SQSIZE
            y1 = y0 + SQSIZE
            draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0))

            # Create the text for the number
            text = str(rows[colidx, rowidx])
            textcoords = (x0+SPACING, y0+SPACING)

            # For single-digit numbers, move the text to center it
            if rows[colidx, rowidx] < 10:
                textcoords = (x0 + int(SPACING * 1.5), y0 + SPACING)

            font = numfont

            # For the center box: other text and font size
            if rowidx == colidx == 2:
                text = "BONUS"
                font = ImageFont.truetype(r"C:\Windows\Fonts\CALIST.TTF", size=SQSIZE // 5)
                textcoords = (x0 + SPACING // 2 + 1, y0 + int(SPACING * 1.5))

            # Put the number in the square
            draw.text(textcoords, text, font=numfont, fill=textcolor)

    # Create a filename with a number that doesn't exist yet
    bingodir = Path(__file__).parent
    volgnr = 0
    while True:
        fn = bingodir / f"kaart{volgnr:03d}.png"
        if not fn.is_file():
            break
        volgnr += 1

    # Finally, save the image
    img.save(fn)


if __name__ == "__main__":
    for _ in tqdm(range(150)):
        generate_card()
