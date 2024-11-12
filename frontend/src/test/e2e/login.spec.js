const { test, expect } = require('@playwright/test');
const sqlite3 = require('sqlite3').verbose();

async function clearUserDatabase() {
    const path = require('path');
    const dbPath = path.resolve(__dirname, '../../../../es_db.sqlite');
    const db = new sqlite3.Database(dbPath);
    await db.serialize(() => {
        db.run('DELETE FROM user'); 
    });

    db.close();
}

test.afterEach(async ({page}) => {
  await clearUserDatabase();
});

  
  
  test.describe('Login Page Tests', () => {
    test('should successfully log in with the created user', async ({ page }) => {


      await page.goto('http://localhost:8080/#/');

      await page.click('text=Sign up as user');
      await page.fill('input[placeholder="Name"]', 'John');
      await page.fill('input[placeholder="Surname"]', 'Doe');
      await page.fill('input[placeholder="Email"]', 'john.doe2@example.com');
      await page.fill('input[placeholder="Password"]', 'Password!123');
      await page.fill('input[placeholder="Confirm Password"]', 'Password!123');
      await page.check('input[type="checkbox"]');
      await page.click('button.signup-button');

      // Esperar al diálogo que confirma que la cuenta se ha creado
      const dialogPromise = new Promise((resolve) => {
        page.on('dialog', async (dialog) => {
          console.log('Diálogo detectado con mensaje:', dialog.message());
          expect(dialog.message()).toBe('La cuenta se ha creado correctamente. Por favor inicie sesión.');
          await dialog.accept();
          resolve();
        });
      });
      await dialogPromise;

      // Asegurarse de que redirige a la página de login
      await expect(page).toHaveURL('http://localhost:8080/#/login');
      

      await page.goto('http://localhost:8080/#/login');  
      await page.fill('input[placeholder="Email"]', 'john.doe2@example.com');
      await page.fill('input[placeholder="Password"]', 'Password!123');
  
      await page.click('button.login-button');

      await expect(page).toHaveURL(new RegExp('/mainpage_user'));

    });

    test('should display an error message for invalid credentials', async ({ page }) => {
  
      await page.goto('http://localhost:8080/#/login');
  
      await page.fill('input[placeholder="Email"]', 'wrong.email@example.com');
      await page.fill('input[placeholder="Password"]', 'wrongPassword!');
      await page.click('button.login-button');
  
      const dialogPromise = new Promise(resolve => {
        page.on('dialog', async dialog => {
          console.log('Diálogo detectado con mensaje:', dialog.message());
          expect(dialog.message()).toBe('Email or Password incorrect');
          
          await dialog.accept();
          resolve();
        });
      });
      await dialogPromise;
      await expect(page).toHaveURL('http://localhost:8080/#/login');
    });
    test('should navigate to the signup page when "Sign Up" link is clicked', async ({ page }) => {

      await page.goto('http://localhost:8080/#/login');
  
      await page.click('text=Sign Up');      
  
      await expect(page).toHaveURL('http://localhost:8080/#/signup');
    });
  });
