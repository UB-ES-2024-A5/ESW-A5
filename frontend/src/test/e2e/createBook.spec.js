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
          db.run('DELETE FROM link')
          db.run('DELETE FROM book')
          db.run('DELETE FROM account');
          db.run('DELETE FROM user'); 
      });
  
      db.close();
    }
  }

  test.describe('Set up publisher account', () => {
    test('Create a user and a account', async () => {
      await clearUserDatabase();
      const apiUrl = 'http://localhost:8000/api/v1';
  
      const userData = {
        email: 'testuser@example.com',
        name: 'John Doe',
        password: 'testpassword',
        is_editor: true,
        cif: 'G12345678',
      };
  
      let response = await fetch(`${apiUrl}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });
  
      expect(response.status).toBe(200);
      const userDataResponse = await response.json();
  
      const accountData = {
        id: userDataResponse.id,
      };
  
      response = await fetch(`${apiUrl}/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(accountData),
      });
  
      expect(response.status).toBe(200);
      const accountDataResponse = await response.json();
    });
  });

  test.describe('E2E Book Page', () => {
    test('Should redirect to login if not authenticated and trying to access /mainPage_user', async ({ page }) => {
    await page.goto('http://localhost:8080')
    await page.goto('http://localhost:8080/mainPage_publisher');
  
    await expect(page).toHaveURL('http://localhost:8080/login');

    });
});