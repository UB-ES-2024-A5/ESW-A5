import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import MainPageUser from '../../components/mainPageUser.vue';
import BookDetails from '../../components/book.vue';
import BookServices from '../../services/BookServices';
import axios from 'axios';


function flushPromises() {
    return new Promise(resolve => setImmediate(resolve));
  }


jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
  create: jest.fn(() => ({
    interceptors: {
      request: { use: jest.fn(), eject: jest.fn() },
      response: { use: jest.fn(), eject: jest.fn() },
    },
  })),
  defaults: {
    headers: {
      common: {
        Authorization: '',
      },
    },
  },
  interceptors: {
    request: { use: jest.fn(), eject: jest.fn() },
    response: { use: jest.fn(), eject: jest.fn() },
  },
}));

jest.mock('../../services/BookServices', () => ({
    getAllBooks: jest.fn(),
  }));

const localVue = createLocalVue();
localVue.use(VueRouter);

describe('Navigation from MainPageGuest to BookDetails', () => {
  let router;

  beforeEach(() => {
    BookServices.getAllBooks.mockResolvedValue([
        { id: '47a550e7-679d-4e30-8b78-635530c186ca', img: 'book1.png' },
        { id: 'b74c50f4-21f7-4b60-b678-d2b8d4b30f59', img: 'book2.png' },
      ]);
    const routes = [
      { path: '/mainPage_user', component: MainPageUser },
      { path: '/book', component: BookDetails },
    ];
    router = new VueRouter({ mode: 'history', routes });
  });

  it('should fetch and display book details when authenticated and accessing /book', async () => {
    // Simulate authentication token in localStorage
    const mockToken = 'valid-token';
    localStorage.setItem('auth_token', mockToken);

    // Use jest.fn() to mock the axios.get method directly
    axios.get.mockResolvedValue({
      data: {
        title: 'Test Book',
        author: 'Author Test',
        gender_main: 'Fiction',
        publication_year: 2021,
        isbn: '1234567890',
        price: '20',
        synopsis: 'A great book about testing.',
        img: 'test-book.png',
        list_links: ['http://example.com'],
        account_id: 1,
      },
    });

    // Navigate to the /book route with a bookId query parameter
    router.push({ path: '/book', query: { bookId: '47a550e7-679d-4e30-8b78-635530c186ca' } });

    // Ensure the Vue component updates after the route change
    await localVue.nextTick();

    // Mount the BookDetails component with the router
    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });

    // Wait for the component to fetch the book details
    await wrapper.vm.fetchBookDetails();

    await wrapper.vm.$nextTick();


    // Verify that the book details were correctly assigned to the component's data
    expect(wrapper.vm.book.title).toBe('Test Book');
    expect(wrapper.vm.book.author).toBe('Author Test');
    expect(wrapper.vm.book.isbn).toBe('1234567890');
    expect(wrapper.vm.book.price).toBe('20');

    // Check if the book details are displayed correctly in the component's template
    expect(wrapper.find('.title').text()).toBe('Test Book');
    expect(wrapper.find('.info').text()).toContain('Author: Author Test');
    expect(wrapper.find('.image-container img').attributes('src')).toBe('test-book.png');
  });
});
