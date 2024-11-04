# Script de ejemplo para iniciar servicios
# Iniciar backend
npm run start-backend &
BACKEND_PID=$!
sleep 5 # Esperar un tiempo prudente para asegurarte de que el backend esté listo

# Iniciar frontend
npm run start-frontend &
FRONTEND_PID=$!
sleep 5 # Esperar un tiempo prudente para asegurarte de que el frontend esté listo

# Ejecutar pruebas
npx playwright test --project=chromium

# Matar los procesos
kill $BACKEND_PID
kill $FRONTEND_PID
