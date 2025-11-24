# Proyecto `evaluacion` — Instrucciones de puesta en marcha

Este README explica cómo dejar funcionando el proyecto Django localmente después de clonarlo, conectarlo a MariaDB (local — Docker recomendado) y ejecutar las migraciones. Está pensado para Windows (PowerShell) pero los pasos son adaptables a Linux/macOS.

## Requisitos
- Python 3.10+ instalado (usa la misma versión que ejecutarás con `python`).
- `pip` disponible.
- (Recomendado) Docker si quieres levantar MariaDB rápidamente.

## Archivos importantes
- `evaluacion/settings.py` — configuración principal; usa variables de entorno para la DB.
- `.env` — archivo con variables de conexión (ya existe en este repo con valores de ejemplo).
- `requirements.txt` — contiene `PyMySQL` (driver usado en Windows para MySQL/MariaDB).

## Pasos rápidos (PowerShell)

1) Clonar y entrar al proyecto
```powershell
git clone <repo-url>
cd evaluacion
```

2) Crear y activar un virtualenv (recomendado)
```powershell
python -m venv .venv
\# permitir ejecución en esta sesión si da error:
\# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

3) Instalar dependencias
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4) Levantar MariaDB con Docker (opcional, rápido)
```powershell
\# Esto crea un contenedor con DB 'evaluacion_db', usuario 'usuario' y contraseña 'password'
docker pull mariadb:10.11
docker run --name mariadb-evaluacion -e MARIADB_ROOT_PASSWORD=rootpass -e MARIADB_DATABASE=evaluacion_db -e MARIADB_USER=usuario -e MARIADB_PASSWORD=password -p 3306:3306 -d mariadb:10.11
```

Si no usas Docker, asegúrate de tener MariaDB/MySQL instalado y accesible.

5) Configurar variables de entorno / `.env`
- El proyecto incluye un `.env` en la raíz con valores de ejemplo. Puedes editarlo con tus credenciales.
- Alternativamente, exporta las variables para la sesión actual (PowerShell):
```powershell
$env:DB_NAME = 'evaluacion_db'
$env:DB_USER = 'root'
$env:DB_PASSWORD = 'Lumaco2426'
$env:DB_HOST = '127.0.0.1'
$env:DB_PORT = '3306'
```
Nota: si prefieres que Django lea `.env` automáticamente, instala `python-dotenv` o `django-environ` y añade la carga en `settings.py`. Actualmente `settings.py` usa `os.environ.get(...)`, por lo que definir las variables del entorno funciona.

6) (Opcional) Crear usuario `usuario` si usas la configuración por defecto
```powershell
\# dentro del contenedor Docker
docker exec -i mariadb-evaluacion mysql -u root -prootpass -e "CREATE USER IF NOT EXISTS 'usuario'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON evaluacion_db.* TO 'usuario'@'%'; FLUSH PRIVILEGES;"
```

7) Migraciones y arranque
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

8) Uso básico
- Abre `http://127.0.0.1:8000/` para ver la pantalla de login. Ingresa las credenciales de tu base de datos (por ejemplo `root` / `Lumaco2426` si usaste el `.env` del repo).
- Después podrás crear `Responsable`, `Maquina` y `Mantencion` desde la interfaz.

## Exportar/importar datos desde `db.sqlite3` (si tienes datos existentes)
- Exportar desde SQLite (en tu copia actual):
```powershell
python manage.py dumpdata --natural-primary --natural-foreign --indent 2 > data.json
```
- Después de apuntar a MariaDB y ejecutar `migrate` en la nueva BD, importa:
```powershell
python manage.py loaddata data.json
```
Ten cuidado con `contenttypes` y `auth` — revisa el JSON si hay errores.

## Solución de problemas comunes
- ModuleNotFoundError: No module named 'pymysql'
  - Asegúrate de instalar `PyMySQL` en el mismo entorno Python: `python -m pip install PyMySQL`.
- django.db.utils.OperationalError: (1045, "Access denied...")
  - Comprueba `DB_USER`/`DB_PASSWORD`/`DB_HOST`/`DB_PORT` y que el usuario existe en MariaDB.
  - Si usas Docker con `-p 3306:3306`, conecta a `127.0.0.1:3306`.
- Activación de virtualenv en PowerShell falla por política de ejecución
  - Ejecuta: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` en la sesión y vuelve a activar.
- Si el puerto 3306 está en uso, cambia el mapeo Docker (`-p 3307:3306`) y ajusta `DB_PORT`.

## Comandos útiles (detener/eliminar contenedor)
```powershell
docker stop mariadb-evaluacion
docker rm mariadb-evaluacion
```

## Seguridad y recomendaciones
- No uses `root` en producción. Crea un usuario con privilegios limitados.
- No subas `.env` a repositorios públicos. Añádelo a `.gitignore`.
- Usa `DEBUG = False` y configura `ALLOWED_HOSTS` cuando despliegues.

¿Problemas? Pega aquí el error completo (traceback) y te ayudo a solucionarlo.
