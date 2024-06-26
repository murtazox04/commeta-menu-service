import qrcode
from PIL import Image


def generate_qr_code(data: str, file_path: str):
    logo = Image.open('media/logo.png')

    base_with = 75
    w_percent = (base_with / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(w_percent)))
    logo = logo.resize((base_with, hsize))

    qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)

    qr_big.add_data(data)
    qr_big.make(fit=True)
    img_qr_big = qr_big.make_image(fill_color='black', back_color='white').convert('RGBA')
    pos = ((img_qr_big.size[0] - logo.size[0]) // 2, (img_qr_big.size[1] - logo.size[1]) // 2)
    img_qr_big.paste(logo, pos)

    img_qr_big.save(file_path)
