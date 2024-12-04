const { test, expect } = require('@playwright/test');
const sqlite3 = require('sqlite3').verbose();
const { Client } = require('pg');


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
      const res5 = await client.query('DELETE FROM "wishlistbooklink"')
      const res4 = await client.query('DELETE FROM "wishlist"')
      const res3 = await client.query('DELETE FROM "link"')
      const res2 = await client.query('DELETE FROM "book"')
      const res6 = await client.query('DELETE FROM "follower"')
      const res1 = await client.query('DELETE FROM  "account"')
      const res = await client.query('DELETE FROM "user"');
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
}

test.describe('Signup Page Tests', () => {
  
  test('should successfully create a new user account', async ({ page }) => {

    await clearUserDatabase();
    await page.goto('http://localhost:8080');
    await page.click('text=Sign up as user');
    await page.fill('input[placeholder="Name"]', 'John');
    await page.fill('input[placeholder="Surname"]', 'Doe');
    await page.fill('input[placeholder="Email"]', 'john.doe@example.com');
    await page.fill('input[placeholder="Password"]', 'Password!123');
    await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
    await page.check('input[type="checkbox"]');    
    await page.click('button.signup-button');

    const swal = page.locator('.swal2-container');
    await expect(swal).toBeVisible();

    const swalTitle = swal.locator('.swal2-title');
    const swalText = swal.locator('.swal2-html-container');
    await expect(swalTitle).toHaveText('Account Created!');
    await expect(swalText).toHaveText('La cuenta se ha creado correctamente. Por favor inicie sesión.');

    const confirmButton = swal.locator('.swal2-confirm');
    await confirmButton.click();
    await expect(page).toHaveURL('http://localhost:8080/login');
    
  });

  test('should show error for missing terms acceptance', async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.click('text=Sign up as user');
    await page.fill('input[placeholder="Name"]', 'John');
    await page.fill('input[placeholder="Surname"]', 'Doe');
    await page.fill('input[placeholder="Email"]', 'john.doe@example.com');
    await page.fill('input[placeholder="Password"]', 'Password!123');
    await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
    await page.click('button.signup-button');
    const swal = page.locator('.swal2-container');
    await expect(swal).toBeVisible();

    const swalTitle = swal.locator('.swal2-title');
    const swalText = swal.locator('.swal2-html-container');
    await expect(swalTitle).toHaveText('Form Error');
    await expect(swalText).toHaveText('Please correct the errors in the form.');

    const confirmButton = swal.locator('.swal2-confirm');
    await confirmButton.click();
  });
  test('should show error for email already registered', async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.click('text=Sign up as user');
    await page.fill('input[placeholder="Name"]', 'John');
    await page.fill('input[placeholder="Surname"]', 'Doe');
    await page.fill('input[placeholder="Email"]', 'john.doe@example.com');
    await page.fill('input[placeholder="Password"]', 'Password!123');
    await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
    await page.check('input[type="checkbox"]');
    await page.click('button.signup-button');
    const swal = page.locator('.swal2-container');
    await expect(swal).toBeVisible();

    const swalTitle = swal.locator('.swal2-title');
    const swalText = swal.locator('.swal2-html-container');
    await expect(swalTitle).toHaveText('Oops...');
    await expect(swalText).toHaveText('There was an error creating your account.');
    const confirmButton = swal.locator('.swal2-confirm');
    await confirmButton.click();
  });

});
