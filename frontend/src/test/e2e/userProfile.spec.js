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
    expect(bookDataResponse.title).toBe(bookData.title);

    const userData2 = {
        email: 'testuser2@example.com',
        name: 'John',
        password: 'testpassword',
        is_editor: false,
        surname: 'Doe',
      };
  
      let response2 = await fetch(`${apiUrl}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData2),
      });
  
      expect(response2.status).toBe(200);
      const userDataResponse2 = await response2.json();
  
      const accountData2 = {
        id: userDataResponse2.id,
      };
  
      response = await fetch(`${apiUrl}/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(accountData2),
      });
  });
});

test.describe('User profile', () => {
  test('Should be redirected if user is not logged', async ({ page }) => {
    await page.goto('http://localhost:8080/user_profile');

    await expect(page).toHaveURL('http://localhost:8080/login'); 

  });

  test('Should see the user details', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');

    await page.click('button.login-button');

    await expect(page).toHaveURL(new RegExp('/mainPage_user'));

    const userProfileIcon = page.locator('[data-testid="user-profile-icon"]');
    await expect(userProfileIcon).toBeVisible();

    await userProfileIcon.click();

    await expect(page).toHaveURL(new RegExp('/user_profile'));

    await page.waitForTimeout(100);

    const userName = await page.textContent('.user-info h1');
    const userEmail = await page.textContent('.user-info p');
    
    await expect(userName).toContain('John Doe');
    await expect(userEmail).toContain('testuser2@example.com');

  
  });

  test('should edit the bio correctly', async ({page}) => {

    await page.goto('http://localhost:8080/login');
    await expect(page).toHaveURL('http://localhost:8080/login'); 

    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');

    await page.click('button.login-button');

    await expect(page).toHaveURL(new RegExp('/mainPage_user'));

    const userProfileIcon = page.locator('[data-testid="user-profile-icon"]');
    await expect(userProfileIcon).toBeVisible();

    await userProfileIcon.click();

    await expect(page).toHaveURL(new RegExp('/user_profile'));
    

    await page.click('.edit-bio-btn');

    const bioTextarea = await page.locator('.bio-textarea');
    await expect(bioTextarea).toBeVisible();

    const newBio = 'Esta es una nueva biografía editada para el test.';
    await bioTextarea.fill(newBio); 
    await page.click('.edit-bio-btn');

    const updatedBioText = await page.textContent('.biography-section p');
    expect(updatedBioText).toBe(newBio);

  });


  test('Should upload profile image correctly', async ({ page }) => {
    await page.goto('http://localhost:8080/login');
    await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
    await page.fill('input[placeholder="Password"]', 'testpassword');
    await page.click('button.login-button');
    await expect(page).toHaveURL('http://localhost:8080/mainPage_user');
  
    const userProfileIcon = page.locator('[data-testid="user-profile-icon"]');
    await expect(userProfileIcon).toBeVisible();

    await userProfileIcon.click();

    await expect(page).toHaveURL(new RegExp('/user_profile'));
    
    await expect(page).toHaveURL('http://localhost:8080/user_profile');
      
    const imagePath = 'src/test/assets/prueba.jpg';

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(imagePath);

    const updatedProfileImage = page.locator('.profile-image');
    await expect(updatedProfileImage).toHaveAttribute('src', /data:image\/jpeg/);

    const successMessage = page.locator('.swal2-container');
    await expect(successMessage).toBeVisible();
  });
  

});