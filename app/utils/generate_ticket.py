
import base64
import os
import sys
import csv
import io
import argparse
from urllib import response
import requests
from PIL import Image, ImageDraw, ImageFont
import qrcode
from app.core.imagekit import upload_image_base64_url


FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Zones extraites du SVG officiel (595 × 238 px)
# QR code   : <rect x="197" y="105" width="67" height="68"/>
ZONE_QR = (197, 105, 67, 68)
# Barre verte : <rect x="432" y="19" width="201" height="43" transform="rotate(90 432 19)"/>
#               => après rotation : x=[389..432], y=[19..220]

ZONE_INFO = (475, 40, 42, 180)

# Couleurs
COL_NAME = (180, 230,  80, 255)  # vert lime
COL_ID = (160, 160, 160, 255)  # gris clair


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def make_qr_image(data: str, size: int, pass_type: str = "") -> Image.Image:
    qr = qrcode.QRCode(box_size=3, border=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    # upload qr to ImageKit
    buffered = io.BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(
        buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    upload_response = upload_image_base64_url(
        f"qr_{data.split('/')[-1]}.png", img_str, folder=f"pycontg26/qrcodes/{pass_type.lower() if pass_type else 'general'}")

    return qr.make_image(fill_color="black", back_color="white")\
             .convert("RGBA").resize((size, size), Image.LANCZOS), upload_response.url


def load_template(template_url: str) -> Image.Image:

    print(f"[INFO] Template local introuvable → téléchargement depuis ImageKit…")
    r = requests.get(template_url, timeout=15)
    r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGBA")


def generate_ticket(name: str, ticket_id: str, qr_data: str, template_url: str, name_color: tuple = COL_NAME, color_id: tuple = COL_ID, pass_type="") -> tuple[str, str]:

    name_safe = name.replace(" ", "_").lower()
    filename = f"ticket_{name_safe}_{ticket_id.lstrip('#')}.png"

    img = load_template(template_url)   # 595 × 238 px

    qx, qy, qw, qh = ZONE_QR
    pad = 3
    qr_img, qr_url = make_qr_image(qr_data, min(qw, qh), pass_type)
    white = Image.new("RGBA", (qw + pad*2, qh + pad*2), (255, 255, 255, 255))
    img.paste(white, (qx - pad, qy - pad))
    img.paste(qr_img, (qx, qy))

    # 3 ── ZONE INFOS (nom, ID) ─────────────────────────────────────────
    ix, iy, iw, ih = ZONE_INFO
    fn = load_font(FONT_BOLD, 14)
    fi = load_font(FONT_REG,  11)
    fd = load_font(FONT_REG,   9)

    canvas2 = Image.new("RGBA", (ih, iw), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(canvas2)
    y = 6
    d2.text((8, y), name, font=fn, fill=name_color)
    y += 18
    d2.text((8, y), f"Ticket ID  {ticket_id}", font=fi, fill=color_id)
    y += 14

    rot2 = canvas2.rotate(90, expand=True)
    img.paste(rot2, (ix, iy), rot2)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    upload_response = upload_image_base64_url(
        filename, img_str, folder=f"pycontg26/tickets/{pass_type.lower() if pass_type else 'general'}")

    uploaded_links = {
        "ticket_url": upload_response.url,
        "qr_url": qr_url
    }

    return uploaded_links["ticket_url"], uploaded_links["qr_url"]


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Générateur de tickets PyCon Togo 26")
    p.add_argument("--name",           default="Wassim Koffi",
                   help="Nom complet du participant")
    p.add_argument("--id",             default="#22R24SGS34")
    p.add_argument(
        "--qr",             default="https://pycon.pytogo.org/ticket/22R24SGSCS")
    p.add_argument("--no-day1",        action="store_true")
    p.add_argument("--no-day2",        action="store_true")
    args = p.parse_args()

    generate_ticket(
        name="Générateur de tickets PyCon Togo 26",
        ticket_id="#55T99AB",
        qr_data="https://pycon.pytogo.org/ticket/55T99AB",
        template_url="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/pycontg26_pro.svg?updatedAt=1780153986863"
    )
