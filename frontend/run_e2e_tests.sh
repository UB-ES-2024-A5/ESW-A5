# Script de ejemplo para iniciar servicios
# Iniciar backend
cd ..
cd backend || exit
poetry run uvicorn app.main:app --reload &

sleep 5

cd ..
cd frontend || exit
npm run dev &

sleep 5
npx playwright test --project=chromium
sleep 5
