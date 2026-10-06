from PIL import Image, ImageDraw, ImageOps


def add_rounded_corners(img, radius=30):
    """Apply rounded corners to an image."""
    # Ensure image is in RGBA mode
    img = img.convert("RGBA")

    # 1. Create mask with exact bounds [(0,0), (w-1, h-1)]
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=radius, fill=255)

    # 2. Fit and apply alpha mask
    rounded = ImageOps.fit(img, (w, h))
    rounded.putalpha(mask)
    return rounded


def circular_crop(image, size, border=5, border_color=(255, 255, 255)):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    output = ImageOps.fit(image, size, centering=(0.5, 0.5))
    output.putalpha(mask)

    # add border
    border_img = Image.new("RGBA", (size[0] + border * 2, size[1] + border * 2), border_color)
    mask_border = Image.new("L", (size[0] + border * 2, size[1] + border * 2), 0)
    draw = ImageDraw.Draw(mask_border)
    draw.ellipse((0, 0, size[0] + border * 2, size[1] + border * 2), fill=255)
    border_img.putalpha(mask_border)
    border_img.paste(output, (border, border), output)
    return border_img