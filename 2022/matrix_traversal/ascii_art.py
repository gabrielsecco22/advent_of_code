from PIL import Image, ImageDraw, ImageFont
from svg import ascii_to_svg

img_path = "img-vit-gab.jpg"
FONT = ImageFont.truetype("cour.ttf", 12)


def generate_img(char, font):
    img = Image.new("L", (6, 13), 255)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, font=font)
    return img


def get_chr_density(char, font=FONT):
    img = generate_img(char, font)
    pixels = list(img.getdata())
    # img.show()
    return sum(pixels) / len(pixels)


def get_intesity_list(font=FONT):
    ascii_chars = [chr(x) for x in range(0, 256) if chr(x).isprintable()]
    # print(ascii_chars)
    # img = generate_img(ascii_chars[32], font)
    # print(get_chr_density(ascii_chars[32], font))
    return [(char, get_chr_density(char, font)) for char in ascii_chars]


def normalize_intensity_list(intensity_list, r=(0, 255)):
    min_intensity = min([x[1] for x in intensity_list])
    max_intensity = max([x[1] for x in intensity_list])
    return [(x[0], int((x[1] - min_intensity) / (max_intensity - min_intensity) * (r[1] - r[0]) + r[0])) for x in intensity_list]


def get_intensity_to_char_map(intensity_list, interpolate=True):
    js = {x[1]: x[0] for x in intensity_list}
    if interpolate:
        min_key = min(js.keys())
        max_key = max(js.keys())
        curr = js[min_key]
        for i in range(min_key, max_key):
            if i not in js:
                js[i] = curr
            else:
                curr = js[i]
    js = sorted(js.items(), key=lambda x: x[0])
    js = {x[0]: x[1] for x in js}
    return js


il = get_intesity_list()
il_norm = normalize_intensity_list(il)
intensity_to_char_map = get_intensity_to_char_map(il_norm)


def ascii_art(img_path, i2c_map):
    img = Image.open(img_path)
    # img = img.convert("RGB")
    img = img.convert("L")
    pixels = list(img.getdata())
    width, height = img.size
    new_img = Image.new("L", (width * 6, height * 13), 255)
    draw = ImageDraw.Draw(new_img)
    for i in range(height):
        for j in range(width):
            char = i2c_map[pixels[i * width + j]]
            draw.text((j * 6, i * 13), char, font=FONT)
    return new_img


def ascii_art_svg(img_path, i2c_map, dest_file):
    img = Image.open(img_path)
    # img = img.convert("RGB")
    img = img.convert("L")
    pixels = list(img.getdata())
    width, height = img.size
    new_img = Image.new("L", (width * 6, height * 13), 255)
    draw = ImageDraw.Draw(new_img)
    txt = []
    for i in range(height):
        line = []
        for j in range(width):
             line.append(i2c_map[pixels[i * width + j]])
        txt.append("".join(line))
    txt = "\n".join(txt)
    with open(dest_file, "w") as f:
        svg = ascii_to_svg(txt)
        f.write(svg)



# new_img = ascii_art(img_path, intensity_to_char_map)
# new_img.show()
ascii_art_svg(img_path, intensity_to_char_map, "art.svg")


