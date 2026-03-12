# 🖼️ ImageConvert

Conversor de imágenes web construido con **Python + Flask**. Permite convertir entre los formatos más comunes desde una interfaz moderna con tema oscuro, drag & drop y descarga instantánea.

![Python](https://img.shields.io/badge/Python-3.8+-3b82f6?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-3b82f6?style=flat-square&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-6366f1?style=flat-square&logo=bootstrap&logoColor=white)

---

## ✨ Características

- 🔄 Conversión entre **JPEG, PNG, GIF, BMP, TIFF y SVG**
- 🖱️ **Drag & drop** o selección manual de archivos
- 👁️ **Vista previa** de la imagen antes de convertir
- ⚡ Descarga instantánea del archivo convertido
- 🌙 Interfaz oscura moderna con Bootstrap 5
- 🔒 Sin servidores externos — todo se procesa localmente

---

## 📦 Requisitos

- Python 3.8 o superior
- pip

---

## 🚀 Instalación y uso

**1. Clona el repositorio**
```bash
git clone https://github.com/EvePulido/convertidorImagenes.git
cd convertidorImagenes
```

**2. Instala las dependencias**
```bash
pip install flask pillow
```

**3. Ejecuta la aplicación**
```bash
python convertidor.py
```

**4. Abre en el navegador**
```
http://localhost:5000
```

---

## 📁 Estructura del proyecto

```
imageconvert/
├── convertidor.py        # Servidor Flask + lógica de conversión
├── templates/
│   └── index.html        # Interfaz de usuario
└── README.md
```

---

## 🔧 Formatos soportados

| Entrada | Salida |
|---------|--------|
| JPEG / JPG | ✅ |
| PNG | ✅ |
| GIF | ✅ |
| BMP | ✅ |
| TIFF | ✅ |
| SVG | ✅ (SVG → SVG o raster → SVG) |

> ⚠️ La conversión de SVG a formatos rasterizados (JPEG, PNG, etc.) requiere instalar Cairo. En Windows es complejo; se recomienda usar otro formato de entrada para esos casos.

---

## 🛠️ Tecnologías

- **[Flask](https://flask.palletsprojects.com/)** — servidor web ligero en Python
- **[Pillow](https://python-pillow.org/)** — procesamiento de imágenes
- **[Bootstrap 5](https://getbootstrap.com/)** — estilos y componentes UI

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.