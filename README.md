# 🔍 Buscador de Imágenes SHOWCast

Interfaz web para buscar imágenes generadas por **SHOWCast** a partir de fecha y hora. Las imágenes deben estar previamente almacenadas en la carpeta `Output`.

## 🚀 Características

- Búsqueda por satélite, producto, fecha y hora
- Vista previa de imágenes
- Opción para descargar resultados como archivo `.zip`
- Interfaz ligera basada en **Flask**

## 🧱 Requisitos

- Python 3.x
- Flask
- Gunicorn (opcional para producción)

Instalación rápida:

```bash
pip install flask gunicorn
````

## 🧱 Configuración


1. Clona el repositorio:
````bash
git clone https://github.com/wabarca/buscador_imagenes.git
cd buscador_imagenes
````

2. Edita el archivo ````app.py```` y actualiza la ruta base donde se almacenan las imágenes:
````python
BASE_DIR = "/ruta/a/tu/Output"
````
La estructura esperada del directorio es:
````php-template
Output/
  └── <satelite>/
      └── <producto>/
          └── imagenes_YYYYMMDDHHMM.webp
````
3. Asegúrate de tener permisos adecuados sobre estas rutas si corres el servicio en segundo plano.

## 🔄 Ejecución

🔧 Modo desarrollo (usando Flask directamente)
````bash
python app.py
````
Esto ejecutará el servidor en http://127.0.0.1:5000.

⚙️ Modo producción (con Gunicorn y systemd)
Instala Gunicorn:
````bash
pip install gunicorn
````
Usa el archivo .service incluido (buscador_imagenes.service) para habilitar el servicio automáticamente en Linux:
````bash
sudo cp buscador.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl enable buscador.service
sudo systemctl start buscador.service
````
Antes de activarlo, edita el archivo .service y ajusta:

- User=...
- WorkingDirectory=...
- ExecStart=... (la ruta completa a Gunicorn y app:app)