const { test, expect } = require('@playwright/test');
const sqlite3 = require('sqlite3').verbose();
const { Client } = require('pg');
const { user } = require('pg/lib/defaults');
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
      const res7 = await client.query('DELETE FROM "comment"')
      const res8 = await client.query('DELETE FROM "review"')
      const res9 = await client.query('DELETE FROM "forumreaction"')
      const res10 = await client.query('DELETE FROM "forum"')      
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
let userId;
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
    userId = userDataResponse.id

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

    const bookData2 = {
        title: 'Test Book 2',
        author: 'Perico',
        gender_main: 'Fiction',
        gender_secondary: 'Drama',
        synopsis: 'A gripping novel about...',
        publication_year: 2024,
        isbn: '9781234567891',
        price: 19.99,
        img: 'path/to/book/image.jpg',
        links: ['http://example.es'],
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
      const bookDataResponse2 = await response.json();
      bookId2 = bookDataResponse2.id
  });
  test('Create a normal user', async () => {
    const apiUrl = 'http://127.0.0.1:8000/api/v1';

    const userData = {
      email: 'testuser2@example.com',
      name: 'Peter',
      password: 'testpassword',
      is_editor: false,
      surname: 'Jackson',
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

test.describe('Search bar testing:', () => {
  test('Should display The Great Book in the search bar if we search Great', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');

    await page.click('button.login-button');

    await expect(page).toHaveURL(new RegExp('/mainPage_user'));

    const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
    await searchBar.fill('Great');

    await page.waitForSelector('.dropdown-item');

    const resultTitle = await page.textContent('.dropdown-item .result-title');
    const resultType = await page.textContent('.dropdown-item .result-type');
    const resultImageSrc = await page.getAttribute('.dropdown-item .result-image', 'src');

    expect(resultTitle).toBe('The Great Book');
    expect(resultType).toBe('Book');
    expect(resultImageSrc).toBe('path/to/book/image.jpg');
  });
  test('Should display Test Book 2 in the search bar if we search Perico who is its author', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');

    await page.click('button.login-button');

    await expect(page).toHaveURL(new RegExp('/mainPage_user'));

    const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
    await searchBar.fill('Perico');

    await page.waitForSelector('.dropdown-item');

    const resultTitle = await page.textContent('.dropdown-item .result-title');
    const resultType = await page.textContent('.dropdown-item .result-type');
    const resultImageSrc = await page.getAttribute('.dropdown-item .result-image', 'src');

    expect(resultTitle).toBe('Test Book 2');
    expect(resultType).toBe('Book');
    expect(resultImageSrc).toBe('path/to/book/image.jpg');

 });

 test('Should display Test Book 2 and John Doe in the search bar if we search Test', async ({ page }) => {
  await page.goto('http://localhost:8080/login');
  await expect(page).toHaveURL('http://localhost:8080/login'); 

  await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
  await page.fill('input[placeholder="Password"]', 'testpassword');

  await page.click('button.login-button');

  await expect(page).toHaveURL(new RegExp('/mainPage_user'));

  const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
  await searchBar.fill('Test');

  await page.waitForSelector('.dropdown-item');

  const dropdownItems = page.locator('.dropdown-item');

  const itemCount = await dropdownItems.count();
  expect(itemCount).toBe(2);

  const firstResultTitle = await dropdownItems.nth(0).locator('.result-title').textContent();
  const firstResultType = await dropdownItems.nth(0).locator('.result-type').textContent();
  const firstResultImageSrc = await dropdownItems.nth(0).locator('.result-image').getAttribute('src');

  expect(firstResultTitle).toBe('Test Book 2');
  expect(firstResultType).toBe('Book');
  expect(firstResultImageSrc).toBe('path/to/book/image.jpg');

  const secondResultTitle = await dropdownItems.nth(1).locator('.result-title').textContent();
  const secondResultType = await dropdownItems.nth(1).locator('.result-type').textContent();

  expect(secondResultTitle).toBe('John Doe');
  expect(secondResultType).toBe('User');

  });
  test('Should display nothing in the search bar if we search Testqwdu8qsd0sd9aauasdsduads', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 
  
    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');
  
    await page.click('button.login-button');
  
    await expect(page).toHaveURL(new RegExp('/mainPage_user'));
  
    const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
    await searchBar.fill('Testqwdu8qsd0sd9aauasdsduads');
  
    const dropdownItems = page.locator('.dropdown-item');
    const isVisible = await dropdownItems.isVisible();

    expect(isVisible).toBe(false);
  
  });
  test('Should display nothing if we search ourselves', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 
  
    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');
  
    await page.click('button.login-button');
  
    await expect(page).toHaveURL(new RegExp('/mainPage_user'));
  
    const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
    await searchBar.fill('testuser2');
  
    const dropdownItems = page.locator('.dropdown-item');
    const isVisible = await dropdownItems.isVisible();

    expect(isVisible).toBe(false);
  
  });
  test('Should navigate to Test Book 2 if we click the result', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');

    await page.click('button.login-button');

    await expect(page).toHaveURL(new RegExp('/mainPage_user'));

    const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
    await searchBar.fill('Perico');

    await page.waitForSelector('.dropdown-item');
    const dropdownItems = page.locator('.dropdown-item');

    await dropdownItems.first().click();

    await expect(page).toHaveURL(`http://localhost:8080/book?bookId=${bookId2}`);

 });

 test('Should navigate to user John Doe if we click the result', async ({ page }) => {
  await page.goto('http://localhost:8080/login');
  await expect(page).toHaveURL('http://localhost:8080/login'); 

  await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
  await page.fill('input[placeholder="Password"]', 'testpassword');

  await page.click('button.login-button');

  await expect(page).toHaveURL(new RegExp('/mainPage_user'));

  const searchBar = page.locator('input.search-bar[placeholder="Search for a publication or user"]');
  await searchBar.fill('testuser');

  await page.waitForSelector('.dropdown-item');
  const dropdownItems = page.locator('.dropdown-item');

  await dropdownItems.first().click();

  await expect(page).toHaveURL(`http://localhost:8080/search_publisher_profile?userID=${userId}`);

  });
});