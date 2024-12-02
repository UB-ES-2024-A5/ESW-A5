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
        db.run('DELETE FROM account');
        db.run('DELETE FROM user'); 
    });

    db.close();
  }
}


async function verifyUserAndAccount(email) {
    let userExists = false;
    let accountExists = false;
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
  
        const userQuery = `SELECT * FROM "user" WHERE email = $1`;
        const userResult = await client.query(userQuery, [email]);
        userExists = userResult.rows.length > 0;

        if (userExists) {
          const accountQuery = `SELECT * FROM "account" WHERE id = $1`;
          const accountResult = await client.query(accountQuery, [userResult.rows[0].id]);
          accountExists = accountResult.rows.length > 0;
        }
      } finally {
        await client.end();
      }
    } else {
      const path = require('path');
      const dbPath = path.resolve(__dirname, '../../../../test_db.sqlite');
      const db = new sqlite3.Database(dbPath);
  
      await new Promise((resolve, reject) => {

        db.get(`SELECT * FROM user WHERE email = ?`, [email], (err, userRow) => {
          if (err) return reject(err);
          userExists = !!userRow;
  
          if (userExists) {
            db.get(`SELECT * FROM account`,(err, accountRow) => {
            
              if (err){
                return reject(err);
              }
              if(accountRow.id == userRow.id){
                accountExists = !!accountRow;
              }
              resolve();
            });
          } else {
            resolve();
          }
        });
      });
  
      db.close();
    }
  
    return { userExists, accountExists };
  }

test.describe('Account creation Tests', () => {

    test('should successfully create a new account with same id as publisher user', async ({ page }) => {

        const testEmail = 'john.doe@example.com';

        await clearUserDatabase();
        await page.goto('http://localhost:8080/#/');
        await page.click('text=Sign up as publisher');
        await page.fill('input[placeholder="Name"]', 'John');
        await page.fill('input[placeholder="CIF"]', 'G90909090');
        await page.fill('input[placeholder="Email"]', testEmail);
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

        await new Promise(resolve => setTimeout(resolve, 100));
        
        
        const { userExists, accountExists } = await verifyUserAndAccount(testEmail);
        expect(userExists).toBe(true);
        expect(accountExists).toBe(true);
        

        await expect(page).toHaveURL('http://localhost:8080/#/login');


    });

    test('should successfully create a new account with same id as user', async ({ page }) => {

        const testEmail = 'john.doe2@example.com';

        await clearUserDatabase();
        await page.goto('http://localhost:8080/#/');
        await page.click('text=Sign up as user');
        await page.fill('input[placeholder="Name"]', 'John');
        await page.fill('input[placeholder="Surname"]', 'Doe');
        await page.fill('input[placeholder="Email"]', testEmail);
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

        await new Promise(resolve => setTimeout(resolve, 100));
        
        
        const { userExists, accountExists } = await verifyUserAndAccount(testEmail);
        expect(userExists).toBe(true);
        expect(accountExists).toBe(true);
        

        await expect(page).toHaveURL('http://localhost:8080/#/login');


    });
  


});