# -*- coding: utf-8 -*-

import qrcode
from django.conf import settings
from PIL import Image


# 二维码生成函数
def generate_qrcode(data, logo, path, image_name):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    if logo:
        img = img.convert("RGBA")

        icon = Image.open(logo)  # 二维码logo

        img_w, img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img.paste(icon, (w, h), icon)

    img.save(path + image_name)
    return path + image_name
