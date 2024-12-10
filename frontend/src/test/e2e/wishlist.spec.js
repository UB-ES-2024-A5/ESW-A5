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
        db.run('DELETE FROM link')
        db.run('DELETE FROM book')
        db.run('DELETE FROM account');
        console.log("account deleted");
        db.run('DELETE FROM user'); 
        console.log("user deleted");
    });

    db.close();
  }
}
let bookId;
let bookId2;
test.describe('Set up books', () => {
    test('Create books with user, account, and login', async () => {
      await clearUserDatabase();
      const apiUrl = 'http://127.0.0.1:8000/api/v1';
  
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
  
      const loginData = {
        username: userData.email,
        password: userData.password,
      };
  
      response = await fetch(`${apiUrl}/login/access-token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(loginData),
      });
  
      expect(response.status).toBe(200);
      const loginResponse = await response.json();
      const accessToken = loginResponse.access_token;
  
      const bookData = {
        title: 'The Great Book',
        author: 'Jane Author',
        gender_main: 'Fiction',
        gender_secondary: 'Drama',
        synopsis: 'A gripping novel about...',
        publication_year: 2024,
        isbn: '9781234567890',
        price: 19.99,
        img: 'path/to/book/image.jpg',
        links: ['http://example.com'],
      };
  
      response = await fetch(`${apiUrl}/books`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(bookData),
      });
  
      expect(response.status).toBe(200);
      const bookDataResponse = await response.json();
  
      expect(bookDataResponse).toHaveProperty('id');
      bookId = bookDataResponse.id;
      expect(bookDataResponse.title).toBe(bookData.title);
    });
  });
  test('Create a normal user', async () => {
    const apiUrl = 'http://127.0.0.1:8000/api/v1';

    const userData = {
      email: 'testuser2@example.com',
      name: 'John',
      password: 'testpassword',
      is_editor: false,
      surname: 'Doe',
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
  test('Should toggle the star, and when we come back it should stay toggled', async ({ page }) => {
    await page.goto('http://localhost:8080/login');

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');
    await page.click('button.login-button');

    await page.waitForURL('http://localhost:8080/mainPage_user');

    const firstImage = await page.locator('.carousel-image').first();

    const src = await firstImage.getAttribute('src');

    await firstImage.click();

    await page.waitForURL(`http://localhost:8080/book?bookId=${bookId}`);

    const star = await page.locator('.title-container .star');

    await expect(star).not.toHaveClass('selected');

    await star.click();

    await expect(star).toHaveClass('star selected');

    await page.goBack();

    await expect(page).toHaveURL('http://localhost:8080/mainPage_user');

    await firstImage.click();

    await expect(star).toHaveClass('star selected');
    });

  test('Should toggle the star, and when we come back it should stay toggled', async ({ page }) => {
    await page.goto('http://localhost:8080/login');

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');
    await page.click('button.login-button');

    await page.waitForURL('http://localhost:8080/mainPage_user');

      

  });



