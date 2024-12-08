const { test, expect } = require('@playwright/test');
const sqlite3 = require('sqlite3').verbose();
const { Client } = require('pg');

async function clearUserDatabase() {
  const environment = process.env.ENVIRONMENT;

  if (environment === 'staging') {
    console.log('API_URL:', process.env.API_URL);
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



  
  
  test.describe('Login Page Tests', () => {
    test('should successfully log in with the created user', async ({ page }) => {

      await clearUserDatabase();
      await page.goto('http://localhost:8080');

      await page.click('text=Sign up as user');
      await page.fill('input[placeholder="Name"]', 'John');
      await page.fill('input[placeholder="Surname"]', 'Doe');
      await page.fill('input[placeholder="Email"]', 'john.doe2@example.com');
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
      

      await page.goto('http://localhost:8080/login');  
      await page.fill('input[placeholder="Email"]', 'john.doe2@example.com');
      await page.fill('input[placeholder="Password"]', 'Password!123');
  
      await page.click('button.login-button');

      await expect(page).toHaveURL(new RegExp('/mainPage_user'));

    });

    test('should display an error message for invalid credentials', async ({ page }) => {
  
      await page.goto('http://localhost:8080/login');
  
      await page.fill('input[placeholder="Email"]', 'wrong.email@example.com');
      await page.fill('input[placeholder="Password"]', 'wrongPassword!');
      await page.click('button.login-button');
  
      const swal = page.locator('.swal2-container');
      await expect(swal).toBeVisible();

      const swalTitle = swal.locator('.swal2-title');
      const swalText = swal.locator('.swal2-html-container');
      await expect(swalTitle).toHaveText('Login Failed');
      await expect(swalText).toHaveText('Email or Password incorrect. Please try again.');

      const confirmButton = swal.locator('.swal2-confirm');
      await confirmButton.click();
      
      await expect(page).toHaveURL('http://localhost:8080/login');
    });
    test('should navigate to the signup page when "Sign Up" link is clicked', async ({ page }) => {

      await page.goto('http://localhost:8080/login');
  
      await page.click('text=Sign Up');      
  
      await expect(page).toHaveURL('http://localhost:8080/signup');
    });
  });
