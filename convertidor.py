from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'svg'}
OUTPUT_FORMATS = ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'SVG']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', formats=OUTPUT_FORMATS)

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No se subió ningún archivo'}), 400
    file = request.files['file']
    output_format = request.form.get('format', 'PNG').upper()
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Formato de archivo no soportado'}), 400
    try:
        file_bytes = file.read()
        input_ext = file.filename.rsplit('.', 1)[1].lower()
        if input_ext == 'svg':
            if output_format == 'SVG':
                b64 = base64.b64encode(file_bytes).decode('utf-8')
                original_name = file.filename.rsplit('.', 1)[0]
                return jsonify({'success': True, 'data': b64, 'mime': 'image/svg+xml',
                                'filename': f"{original_name}_convertido.svg", 'format': 'SVG'})
            else:
                return jsonify({'error': 'Conversión SVG a raster no soportada sin Cairo.'}), 400
        img = Image.open(io.BytesIO(file_bytes))
        if output_format == 'SVG':
            buf = io.BytesIO()
            img_copy = img.copy()
            if img_copy.mode not in ('RGB', 'RGBA'):
                img_copy = img_copy.convert('RGBA')
            img_copy.save(buf, format='PNG')
            buf.seek(0)
            b64_inner = base64.b64encode(buf.read()).decode('utf-8')
            w, h = img.size
            svg_content = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                           f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                           f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
                           f'  <image xlink:href="data:image/png;base64,{b64_inner}" width="{w}" height="{h}"/>\n</svg>')
            output_bytes = svg_content.encode('utf-8')
            mime = 'image/svg+xml'
            ext = 'svg'
        else:
            output_bytes, mime = process_image(img, output_format)
            ext = {'JPEG': 'jpg', 'PNG': 'png', 'GIF': 'gif', 'BMP': 'bmp', 'TIFF': 'tif'}[output_format]
        b64 = base64.b64encode(output_bytes).decode('utf-8')
        original_name = file.filename.rsplit('.', 1)[0]
        return jsonify({'success': True, 'data': b64, 'mime': mime,
                        'filename': f"{original_name}_convertido.{ext}", 'format': output_format})
    except Exception as e:
        return jsonify({'error': f'Error al convertir: {str(e)}'}), 500

def process_image(img, output_format):
    fmt_map = {'JPEG': ('JPEG', 'image/jpeg'), 'PNG': ('PNG', 'image/png'),
               'GIF': ('GIF', 'image/gif'), 'BMP': ('BMP', 'image/bmp'), 'TIFF': ('TIFF', 'image/tiff')}
    pil_format, mime = fmt_map[output_format]
    if pil_format == 'JPEG':
        if img.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P': img = img.convert('RGBA')
            if img.mode in ('RGBA', 'LA'): bg.paste(img, mask=img.split()[-1])
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
    elif pil_format == 'GIF':
        img = img.convert('P')
    else:
        if img.mode not in ('RGB', 'RGBA', 'L', 'LA'):
            img = img.convert('RGBA')
    buf = io.BytesIO()
    img.save(buf, format=pil_format, **({'quality': 95} if pil_format == 'JPEG' else {}))
    buf.seek(0)
    return buf.read(), mime

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)