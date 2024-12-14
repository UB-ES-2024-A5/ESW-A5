const { test, expect } = require('@playwright/test');
const sqlite3 = require('sqlite3').verbose();
const { Client } = require('pg');
const { unescape } = require('querystring');


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

test.describe('Set up book', () => {
  test('Create a book with user, account, and login', async () => {
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
      publication_year: 2022,
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
    expect(bookDataResponse.title).toBe(bookData.title);

    const bookData2 = {
      title: 'The Great Book 2',
      author: 'Jane Author',
      gender_main: 'Fantasy',
      synopsis: 'A gripping novel about...',
      publication_year: 2022,
      isbn: '9781234567891',
      price: 30,
      img: 'path/to/book/image2.jpg',
      links: ['http://example.cat'],
    };

    response = await fetch(`${apiUrl}/books`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(bookData2),
    });

    expect(response.status).toBe(200);
    const bookDataResponse2 = await response.json()

    const bookData3 = {
      title: 'The Great Book 3',
      author: 'Jane Author',
      gender_main: 'Fantasy',
      synopsis: 'A gripping novel about...',
      publication_year: 2024,
      isbn: '9781234567892',
      price: 1,
      img: 'path/to/book/image3.jpg',
      links: ['http://example.es'],
    };

    response = await fetch(`${apiUrl}/books`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(bookData3),
    });

    expect(response.status).toBe(200);
    const bookDataResponse3 = await response.json()


    const bookData4 = {
      title: 'The Great Book 4',
      author: 'Jane Author',
      gender_main: 'Fantasy',
      synopsis: 'A gripping novel about...',
      publication_year: 1999,
      isbn: '9781234567893',
      price: 3,
      img: 'path/to/book/image4.jpg',
      links: ['http://example.org'],
    };

    response = await fetch(`${apiUrl}/books`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(bookData4),
    });

    expect(response.status).toBe(200);
    const bookDataResponse4 = await response.json()


  });
});

test.describe('E2E Book Page', () => {
  test('Should be able to enter as a guest and get the books', async ({ page }) => {
    await page.goto('http://localhost:8080');

    await page.click('text=Guest access');
    await expect(page).toHaveURL('http://localhost:8080/mainpage_guest'); 
  
    const firstImage = await page.locator('.carousel-image').first(); 
    const imageUrl = await firstImage.getAttribute('src');
    expect(imageUrl).toBe('path/to/book/image.jpg');
  });
  test('Should have a visible Sign In button', async ({ page }) => {
    await page.goto('http://localhost:8080/mainpage_guest');
    const signInButton = await page.locator('.sign-in-btn');
    expect(await signInButton.isVisible()).toBeTruthy()
  });


});

test.describe('Filters functionality in MainPageGuest', () => {

  test.beforeEach(async ({ page }) => {
    // Navega a la página principal antes de cada test
    await page.goto('http://localhost:8080/mainpage_guest'); // Cambia esto por la URL correcta de tu aplicación
  });

  test('should filter books by genre', async ({ page }) => {
    await page.selectOption('select', { label: 'Fiction' });

    await page.waitForTimeout(500); 
    const images = await page.locator('.carousel-image');

    expect(await images.count()).toBeGreaterThan(0);
    const firstImage = await page.locator('.carousel-image').first(); 
    const imageUrl = await firstImage.getAttribute('src');
    expect(imageUrl).toBe('path/to/book/image.jpg');
  });

  test('should filter books by minPrice', async ({ page }) => {
    await page.fill('input[placeholder="Min Price"]', '26');

    await page.waitForTimeout(500); 
    const images = await page.locator('.carousel-image');

    expect(await images.count()).toBeGreaterThan(0);
    const firstImage = await page.locator('.carousel-image').first(); 
    const imageUrl = await firstImage.getAttribute('src');
    expect(imageUrl).toBe('path/to/book/image2.jpg');
  });
  test('should filter books by maxPrice', async ({ page }) => {
    await page.fill('input[placeholder="Max Price"]', '2');

    await page.waitForTimeout(500); 
    const images = await page.locator('.carousel-image');

    expect(await images.count()).toBeGreaterThan(0);
    const firstImage = await page.locator('.carousel-image').first(); 
    const imageUrl = await firstImage.getAttribute('src');
    expect(imageUrl).toBe('path/to/book/image3.jpg');
  });
  test('should filter books by minYear', async ({ page }) => {
    await page.fill('input[placeholder="Min Year"]', '2024');

    await page.waitForTimeout(500); 
    const images = await page.locator('.carousel-image');

    expect(await images.count()).toBeGreaterThan(0);
    const firstImage = await page.locator('.carousel-image').first(); 
    const imageUrl = await firstImage.getAttribute('src');
    expect(imageUrl).toBe('path/to/book/image3.jpg');
  });
  test('should filter books by maxYear', async ({ page }) => {
    await page.fill('input[placeholder="Max Year"]', '2000');

    await page.waitForTimeout(500); 
    const images = await page.locator('.carousel-image');

    expect(await images.count()).toBeGreaterThan(0);
    const firstImage = await page.locator('.carousel-image').first(); 
    const imageUrl = await firstImage.getAttribute('src');
    expect(imageUrl).toBe('path/to/book/image4.jpg');
  });

});
