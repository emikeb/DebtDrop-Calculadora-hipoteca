# Muestra la lista de comandos disponibles por defecto
default:
    @just --list

# Inicia la aplicación de forma completa con Docker Compose
up:
    docker compose up -d --build
    @echo "Servicios levantados. Puedes acceder a la calculadora en http://localhost"
    
alias run := up

# Muestra los logs en tiempo real de todos los contenedores
logs:
    docker compose logs -f

# Detiene los contenedores y los elimina
down:
    docker compose down
    @echo "Servicios detenidos"

# Realiza un apagado y un encendido forzoso limpio de la aplicación
restart:
    docker compose down
    docker compose up -d --build
