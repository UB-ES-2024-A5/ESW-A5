Projecte ES grup A5 2024

## COMANDOS PARA EJECUTAR LOS TESTS:

### BACKEND

Si es la primera vez que los ejecutas o ha habido un cambio en la base de datos(nuevas tablas, etc ...) y se necesita crearla de nuevo:

**En la terminal:**

$env:ENVIRONMENT = "testing"

y luego dentro de poetry shell

alembic upgrade head

Luego IMPORTANTE volver a cambiar a produccion para que las nuevas migraciones se hagan donde toca:

**$env:ENVIRONMENT = "production"**

Para ejecutar los test de backend:

**poetry run pytest**

### FRONTEND

Para ejecutar los tests de frontend con jest:

**cd frontend** 

**npm update**

**npm run test**


### END2END

IMPORTANTE:

**cd frontend**

**npm update**

IMPORTANTE: tendreis que tener la base de datos de test_db.sqlite. Si no la tenéis, leed el paso 1 donde explico los test de backend.
Para ejecutar y comprobar los test hay que iniciar tanto el backend y el frontend. y cuando ya lo tengais haceis desde el directorio frontend:

**npx playwright test --project=chromium**

**Si no funciona** importante hacer desde cd frontend:

**npx playwright install**

Tambien hay un comando para hacerlo más facil:

desde la terminal en cd frontend se puede escribir

**npm run test:e2e**

Luego hay que cerrar los procesos a mano desde el administrador de tareas ya que se quedan abiertos.







