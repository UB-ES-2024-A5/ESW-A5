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
let wishlistId;
let userId;
let userId2;
let publisherId;
test.describe('Set up db', () => {
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
      publisherId = userDataResponse.id
  
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
  test('Create normal users', async () => {
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

    const userData2 = {
      email: 'testuser3@example.com',
      name: 'Luke',
      password: 'testpassword',
      is_editor: false,
      surname: 'Garcia',
    };

    let response2 = await fetch(`${apiUrl}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData2),
    });

    expect(response2.status).toBe(200);
    const userDataResponse2 = await response2.json();
    userId2 = userDataResponse2.id

    const accountData2 = {
      id: userDataResponse2.id,
    };

    response = await fetch(`${apiUrl}/accounts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(accountData2),
    });

    expect(response2.status).toBe(200);

    const loginData = {
        username: userData2.email,
        password: userData2.password,
      };
  
      response = await fetch(`${apiUrl}/login/access-token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(loginData),
      });
  
      expect(response.status).toBe(200);
      const loginResponse = await response.json();
      const accessToken = loginResponse.access_token;

      const wishlistData = {
        name: 'Wishlist'
      }

      response = await fetch(`${apiUrl}/wishlists`, {
        method : 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
          },
          body: JSON.stringify(wishlistData),
        
        });
        expect(response.status).toBe(200);
        const wishlistResponse = await response.json();
        wishlistId = wishlistResponse.id

        response = await fetch(`${apiUrl}/wishlists/${wishlistId}/${bookId}`, {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            },
          });
          
          expect(response.status).toBe(200);
  });
});

  test.describe('Follow and unfollow', () => {
    test('Follow a user and see his wishlist', async ({page}) => {
      await page.goto('http://localhost:8080/login');
      await expect(page).toHaveURL('http://localhost:8080/login'); 
    
      await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
      await page.fill('input[placeholder="Password"]', 'testpassword');
    
      await page.click('button.login-button');
    
      await expect(page).toHaveURL(new RegExp('/mainPage_user'));

      await page.goto(`http://localhost:8080/search_user_profile?userID=${userId2}`);

      await expect(page).toHaveURL(`http://localhost:8080/search_user_profile?userID=${userId2}`);

      const followButton = await page.locator('button.follow-button');
      await expect(followButton).toBeVisible();
      await expect(followButton).toHaveText('Follow');
      await followButton.click();

      await expect(followButton).toHaveText('Unfollow');

      const wishlistButton = await page.locator('button.wishlist-btn:not(.disabled)');
      await expect(wishlistButton).toBeVisible();
      await wishlistButton.click();

      const wishlistPopup = page.locator('.wishlist-popup');
      await expect(wishlistPopup).toBeVisible();
      await expect(wishlistPopup.locator('li')).toContainText('The Great Book');
      await expect(wishlistPopup.locator('li')).toContainText('Jane Author');

      const closeButton = await page.locator('.wishlist-popup .close-button');
      await closeButton.click();
      await expect(wishlistPopup).toBeHidden();
    });

    test('See the followed and following users of one user', async ({page}) => {
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

      const followersText = await page.locator('.follow-item').nth(0).textContent();
      expect(followersText).toContain('0 followers');

      const followingText = await page.locator('.follow-item').nth(1).textContent();
      expect(followingText).toContain('1 followed');
    });

    test('Unfollow a user', async ({page}) => {
      await page.goto('http://localhost:8080/login');
      await expect(page).toHaveURL('http://localhost:8080/login'); 

      await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
      await page.fill('input[placeholder="Password"]', 'testpassword');
      await page.click('button.login-button');

      await expect(page).toHaveURL(new RegExp('/mainPage_user'));
    
      await page.goto(`http://localhost:8080/search_user_profile?userID=${userId2}`);
      await expect(page).toHaveURL(`http://localhost:8080/search_user_profile?userID=${userId2}`);

      const followButton = await page.locator('button.follow-button');
      await expect(followButton).toBeVisible();
      await expect(followButton).toHaveText('Unfollow');
      await followButton.click();
      await expect(followButton).toHaveText('Follow');

      await page.goBack();
    

      const userProfileIcon = page.locator('[data-testid="user-profile-icon"]');
      await expect(userProfileIcon).toBeVisible();

      await userProfileIcon.click();

      await expect(page).toHaveURL(new RegExp('/user_profile'));

      await page.waitForTimeout(100);

      const followersText = await page.locator('.follow-item').nth(0).textContent();
      expect(followersText).toContain('0 followers');

      const followingText = await page.locator('.follow-item').nth(1).textContent();
      expect(followingText).toContain('0 followed');
    });

    test('Follow a publisher and see his publications', async ({page}) => {     


      await page.goto('http://localhost:8080/login');
      await expect(page).toHaveURL('http://localhost:8080/login'); 
    
      await page.fill('input[placeholder="Email"]', 'testuser2@example.com');
      await page.fill('input[placeholder="Password"]', 'testpassword');
    
      await page.click('button.login-button');
    
      await expect(page).toHaveURL(new RegExp('/mainPage_user'));

      await page.goto(`http://localhost:8080/search_publisher_profile?userID=${publisherId}`);

      await expect(page).toHaveURL(`http://localhost:8080/search_publisher_profile?userID=${publisherId}`);

      await page.click('button.follow-button');
  
      const bookImage = page.locator('.carousel-image[src="path/to/book/image.jpg"]');
      await expect(bookImage).toBeVisible();


    });





  });