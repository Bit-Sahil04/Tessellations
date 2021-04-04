from PIL import Image, ImageDraw
import time

CHUNK_SIZE = 64
FILL = False
PALETTE = [(255, 255, 255), (42, 44, 5)]
INVERTED = False


def get_avg_color(img_data2d, area):
    R, G, B = 0, 0, 0
    x_min, y_min, x_max, y_max = area

    for height in range(y_min, y_max):
        for width in range(x_min, x_max):
            R += img_data2d[height][width][0]
            G += img_data2d[height][width][1]
            B += img_data2d[height][width][2]

    R = int(R / ((x_max - x_min) * (y_max - y_min)))
    G = int(G / ((x_max - x_min) * (y_max - y_min)))
    B = int(B / ((x_max - x_min) * (y_max - y_min)))
    avg = (R + G + B) // 3
    print(R - G, R - B)
    return (R, G, B) if FILL else avg


def set_color(img_data2d, area, color):
    x_min, y_min, x_max, y_max = area

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            img_data2d[y][x] = color


def chunkify_img(height, width):
    chunks = []
    for y in range(height // CHUNK_SIZE):
        for x in range(width // CHUNK_SIZE):
            area = (
                x * CHUNK_SIZE,
                y * CHUNK_SIZE,
                x * CHUNK_SIZE + CHUNK_SIZE,
                y * CHUNK_SIZE + CHUNK_SIZE
            )
            chunks.append(area)

    return chunks


def get_chunkified_img(img):
    width, height = img.size
    img_data = list(img.getdata().convert("RGB"))
    img_data_2d = [[img_data[y * width + x] for x in range(width)] for y in range(height)]
    chunks = chunkify_img(height, width)

    for area in chunks:
        color = get_avg_color(img_data_2d, area)
        set_color(img_data_2d, area, color)

    new_img_data_1d = []
    for i in range(height):
        for j in range(width):
            new_img_data_1d.append(img_data_2d[i][j])

    chunkified_gray_image = Image.new("RGB", img.size)
    chunkified_gray_image.putdata(new_img_data_1d)

    return chunkified_gray_image


def draw_circle(img_draw: ImageDraw, area, brightness):
    x_min, y_min, x_max, y_max = area
    off = (CHUNK_SIZE * (-1 * INVERTED + brightness / 255)) // 2
    circle_region = (x_min + off, y_min + off, x_max - off, y_max - off)
    img_draw.ellipse(circle_region, fill=brightness, width=1)


def dotify(img):
    width, height = img.size
    img_data = list(img.getdata().convert("RGB"))

    # fill image with a solid color
    if FILL:
        img.paste(PALETTE[0], (0, 0, width, height))

    img_data_2d = [[img_data[y * width + x] for x in range(width)] for y in range(height)]
    chunks = chunkify_img(height, width)

    img_draw = ImageDraw.Draw(img)

    for area in chunks:
        brightness = img_data_2d[area[1]][area[0]]
        draw_circle(img_draw, area, brightness[2])

    return img


def main():
    img = Image.open("Aditya.jpeg")
    dt = time.time()
    chunkified_img = get_chunkified_img(img).show()
    dots = dotify(chunkified_img)
    print(time.time() - dt)
    dots.show()


main()
