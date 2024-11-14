const { test, expect } = require('@playwright/test');
const sqlite3 = require('sqlite3').verbose();


async function clearUserDatabase() {
  const environment = process.env.ENVIRONMENT;

  if (environment === 'staging') {
    const client = new Client({
      user: process.env.DB_USER,
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      password: process.env.DB_PASSWORD,
      port: 5432,
    });

    try {
      await client.connect();
      const res = await client.query('DELETE FROM "user"');
      console.log('Número de filas afectadas:', res.rowCount);
    } catch (err) {
      console.error('Error al conectar o limpiar la base de datos PostgreSQL', err.stack);
    } finally {
      await client.end();
    }
  } else {
    const path = require('path');
    const dbPath = path.resolve(__dirname, '../../../../test_db.sqlite');
    const db = new sqlite3.Database(dbPath);
    await db.serialize(() => {
        db.run('DELETE FROM user'); 
    });

    db.close();
}


test.beforeEach(async ({ page }) => {
  await clearUserDatabase();  
});

test.describe('Signup Page Tests', () => {
  
  test('should successfully create a new user account', async ({ page }) => {

    await clearUserDatabase();
    await page.goto('http://localhost:8080/#/');
    await page.click('text=Sign up as user');
    await page.fill('input[placeholder="Name"]', 'John');
    await page.fill('input[placeholder="Surname"]', 'Doe');
    await page.fill('input[placeholder="Email"]', 'john.doe@example.com');
    await page.fill('input[placeholder="Password"]', 'Password!123');
    await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
    await page.check('input[type="checkbox"]');    
    await page.click('button.signup-button');
    const dialogPromise = new Promise(resolve => {
      page.on('dialog', async dialog => {
        console.log('Diálogo detectado con mensaje:', dialog.message()); // Log para ver el mensaje
        expect(dialog.message()).toBe('La cuenta se ha creado correctamente. Por favor inicie sesión.');
        await dialog.accept();
        resolve(); // Resuelve la promesa una vez aceptado el diálogo
      });
    });
    await dialogPromise;

    await expect(page).toHaveURL('http://localhost:8080/#/login');
    
  });

  test('should show error for missing terms acceptance', async ({ page }) => {
    await page.goto('http://localhost:8080/#/');
    await page.click('text=Sign up as user');
    await page.fill('input[placeholder="Name"]', 'John');
    await page.fill('input[placeholder="Surname"]', 'Doe');
    await page.fill('input[placeholder="Email"]', 'john.doe@example.com');
    await page.fill('input[placeholder="Password"]', 'Password!123');
    await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
    await page.click('button.signup-button');
    page.on('dialog', async dialog => {
        console.log(dialog.message());
        expect(dialog.message()).toBe('Please correct the errors in the form.');
        await dialog.accept();
      });
  });
  test('should show error for email already registered', async ({ page }) => {
    await page.goto('http://localhost:8080/#/');
    await page.click('text=Sign up as user');
    await page.fill('input[placeholder="Name"]', 'John');
    await page.fill('input[placeholder="Surname"]', 'Doe');
    await page.fill('input[placeholder="Email"]', 'john.doe@example.com');
    await page.fill('input[placeholder="Password"]', 'Password!123');
    await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
    await page.check('input[type="checkbox"]');
    await page.click('button.signup-button');
    page.on('dialog', async dialog => {
        expect(dialog.message()).toBe('Hubo un error al crear la cuenta.');
        await dialog.accept();
      });
  });

});
