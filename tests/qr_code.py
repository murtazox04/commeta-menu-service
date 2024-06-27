import qrcode
import qrcode.image.styledpil
from PIL import Image


def generate_custom_qr_code(data, logo_path, output_path, qr_color=(0, 0, 0), back_color=(255, 255, 255),
                            logo_size=(60, 60)):
    # Create a QR Code instance with custom styling
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Add data to the QR Code
    qr.add_data(data)
    qr.make(fit=True)

    # Create a custom styled QR Code image
    img = qr.make_image(
        image_factory=qrcode.image.styledpil.StyledPilImage,
        module_drawer=qrcode.image.styledpil.SquareModuleDrawer(),
        color_mask=qrcode.image.styledpil.SolidFillColorMask(back_color=back_color, front_color=qr_color)
    ).convert('RGB')

    # Open the logo image
    logo = Image.open(logo_path)

    # Resize the logo image
    logo.thumbnail(logo_size, Image.Resampling.LANCZOS)

    # Calculate the position to place the logo at the center of the QR Code
    qr_width, qr_height = img.size
    logo_width, logo_height = logo.size
    x = (qr_width - logo_width) // 2
    y = (qr_height - logo_height) // 2

    # Check if the logo image has an alpha channel
    if logo.mode in ('RGBA', 'LA') or (logo.mode == 'P' and 'transparency' in logo.info):
        img.paste(logo, (x, y), logo)
    else:
        img.paste(logo, (x, y))

    # Save the final QR Code image
    img.save(output_path)


# Example usage
data = "https://www.example.com"
logo_path = "media/logo.png"
output_path = "media/qr_code_with_logo.png"
generate_custom_qr_code(data, logo_path, output_path)
