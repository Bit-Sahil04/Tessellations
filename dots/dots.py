from PIL import Image, ImageDraw
import time

IMAGE = "flower.jpg"
CHUNK_SIZE = 20         # maximum size of dots
FILL = True            # use color or grayscale image
PALETTE = (0, 0, 0)     # background color
INVERTED = False        # size of dots inversely proportional to its brightness


def get_avg_color(img_data2d, area):
    R, G, B = 0, 0, 0
    x_min, y_min, x_max, y_max = area
    w = x_max - x_min
    h = y_max - y_min
    for height in range(y_min, y_max):
        for width in range(x_min, x_max):
            R += img_data2d[height][width][0]
            G += img_data2d[height][width][1]
            B += img_data2d[height][width][2]

    R = int(R / (w * h))
    G = int(G / (w * h))
    B = int(B / (w * h))
    # avg = int(R + G + B) // 3
    avg = int(0.3 * R + 0.59 * G + 0.11 * B)
    return (R, G, B) if FILL else (avg, avg, avg)


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
    br = brightness[0] * 0.3 + brightness[1] * 0.59 + brightness[2] * .11
    radius = custom_map(br, 0, 255, CHUNK_SIZE // 8, CHUNK_SIZE // 2.01)

    if INVERTED:
        radius = CHUNK_SIZE // 2 - radius
    x_mid = x_min + (x_max - x_min) // 2
    y_mid = y_min + (y_max - y_min) // 2

    circle_region = (x_mid - radius, y_mid - radius, x_mid + radius, y_mid + radius)
    img_draw.ellipse(circle_region, fill=brightness, width=1)


def dotify(img):
    width, height = img.size
    img_data = list(img.getdata().convert("RGB"))

    # fill image with a solid color
    if FILL:
        img.paste(PALETTE[0], (0, 0, width, height))
    else:
        img.paste((0, 0, 0), (0, 0, width, height))

    img_data_2d = [[img_data[y * width + x] for x in range(width)] for y in range(height)]
    chunks = chunkify_img(height, width)

    img_draw = ImageDraw.Draw(img)

    for area in chunks:
        brightness = img_data_2d[area[1]][area[0]]
        draw_circle(img_draw, area, brightness)

    return img


def custom_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def main():
    img = Image.open(IMAGE)
    dt = time.time()
    chunkified_img = get_chunkified_img(img)
    dots = dotify(chunkified_img)
    print(time.time() - dt)
    dots.show()
    dots.save(f"{CHUNK_SIZE}_{IMAGE}", format="JPEG")


main()
