import base64
from io import BytesIO

import segno


class GenerateQR:
    @staticmethod
    def gen_file(short_url, name_qr, scale=10, border=2):
        qr = segno.make_qr(short_url)
        qr.save(f'{name_qr}.svg', scale=scale, border=border)

    @staticmethod
    def gen_text(short_url, scale=10, border=2):
        qr = segno.make(short_url)
        svg_buffer = BytesIO()
        qr.save(svg_buffer, kind='svg', scale=scale, border=border)
        svg_data = svg_buffer.getvalue()
        svg_buffer.close()
        svg_data_base64 = base64.b64encode(svg_data).decode('utf-8')

        return svg_data_base64
