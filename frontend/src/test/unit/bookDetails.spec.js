import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import MainPageUser from '../../components/mainPageUser.vue';
import BookDetails from '../../components/book.vue';
import BookServices from '../../services/BookServices';
import axios from 'axios';
import UserServices from '../../services/UserServices';
import WishlistService from '../../services/WishlistServices';
import Swal from 'sweetalert2';

function flushPromises() {
    return new Promise(resolve => setImmediate(resolve));
  }

  jest.mock('../../services/UserServices', () => ({
    getActualUser: jest.fn(),
    getUserById2: jest.fn(),
  }));
  
  jest.mock('../../services/WishlistServices', () => ({
    getMyWishlists: jest.fn(),
    getWishlistsBooks: jest.fn(),
    addBookWishlist: jest.fn(),
    deleteBookWishlist: jest.fn(),
  }));

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
    getBookById: jest.fn(),
    getBookPublisher: jest.fn(),
    getReviews: jest.fn().mockResolvedValue({ data: [] }),
    createReviewComments: jest.fn(),
    createReviewPoints: jest.fn(),
  }));

const localVue = createLocalVue();
localVue.use(VueRouter);

describe('BookDetails', () => {
  let router;

  beforeEach(() => {
    BookServices.getAllBooks.mockResolvedValue([
        { id: '47a550e7-679d-4e30-8b78-635530c186ca', img: 'book1.png' },
        { id: 'b74c50f4-21f7-4b60-b678-d2b8d4b30f59', img: 'book2.png' },
      ]);
      UserServices.getActualUser.mockResolvedValue({
        data: { id: 1, name: 'Test User' },
      });

      BookServices.getBookPublisher.mockResolvedValue({
        data: {
          publisher: 'Test Publisher'
        },
      });

      BookServices.getReviews.mockResolvedValue({
        data: [],
      });
    
      // Simula una respuesta exitosa para `getMyWishlists`
      WishlistService.getMyWishlists.mockResolvedValue({
        data: [{ id: 'wishlist-id' }],
      });
    
      // Simula una respuesta exitosa para `getWishlistsBooks`
      WishlistService.getWishlistsBooks.mockResolvedValue({
        data: [{ isbn: '1234567890', title: 'Test Book' }],
      });
    const routes = [
      { path: '/mainPage_user', component: MainPageUser },
      { path: '/book', component: BookDetails },
    ];
    router = new VueRouter({ mode: 'history', routes });
  });

  it('should fetch and display book details when authenticated and accessing /book', async () => {
    const mockToken = 'valid-token';
    localStorage.setItem('auth_token', mockToken);

    BookServices.getBookById.mockResolvedValue({
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
      }
    });


    router.push({ path: '/book', query: { bookId: '47a550e7-679d-4e30-8b78-635530c186ca' } });

    await localVue.nextTick();

    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });

    await wrapper.vm.fetchBookDetails();

    await wrapper.vm.$nextTick();

    await new Promise(resolve => setTimeout(resolve, 300));

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

  it('adds a book to the wishlist when the star is toggled on', async () => {

    
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

    router.push({ path: '/book', query: { bookId: 'b74c50f4-21f7-4b60-b678-d2b8d4b30f59' } });

    await localVue.nextTick();

    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });

    await wrapper.vm.fetchBookDetails();

    await wrapper.vm.$nextTick();
  
    wrapper.setData({ starSelected: false, wishlistId: 'wishlist-id', bookid2: 'book-id' });
  
    await wrapper.vm.toggleStar('wishlist-id', 'book-id');
  
    expect(WishlistService.addBookWishlist).toHaveBeenCalledWith('wishlist-id', 'book-id');
    expect(wrapper.vm.starSelected).toBe(true);
  });

  it('removes a book from the wishlist when the star is toggled off', async () => {
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

    router.push({ path: '/book', query: { bookId: 'b74c50f4-21f7-4b60-b678-d2b8d4b30f59' } });

    await localVue.nextTick();

    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });

    await wrapper.vm.fetchBookDetails();

    await wrapper.vm.$nextTick();
  
    wrapper.setData({ starSelected: true, wishlistId: 'wishlist-id', bookid2: 'book-id' });
  
    await wrapper.vm.toggleStar('wishlist-id', 'book-id');
  
    expect(WishlistService.deleteBookWishlist).toHaveBeenCalledWith('wishlist-id', 'book-id');
    expect(wrapper.vm.starSelected).toBe(false);
  });

  it('shows an error when trying to comment without rating the book', async () => {
    
    const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();

    BookServices.getReviews.mockResolvedValue({
      data: [],
    });
    UserServices.getUserById2.mockResolvedValue({});

    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });
    await wrapper.vm.fetchComments2('some-id');
    await wrapper.vm.$nextTick();

    wrapper.setData({ rating: 0, comment: 'This is my comment' });
  
    await wrapper.vm.submitReview();
  
    expect(SwalMock).toHaveBeenCalledWith({
      icon: 'warning',
      title: 'Valoració Incompleta',
      text: 'No es pot crear la valoració sense indicar el nombre de estrelles.',
    });
  });
  
  it('successfully rates and comments on a book', async () => {

    const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();

    BookServices.getReviews.mockResolvedValue({
      data: [],
    });
    UserServices.getUserById2.mockResolvedValue({});
    BookServices.createReviewComments.mockResolvedValue({ message: 'Comentario creado correctamente' });
    BookServices.createReviewPoints.mockResolvedValue({ message: 'Puntos creados correctamente' });

    
    const data = {
      text: 'This is an amazing book!',
    };
    const data2 = {
      point_book: 5,
    };
    
    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });
  
    wrapper.setData({
      rating: 5,
      comment: 'This is an amazing book!',
    });
    wrapper.setData({bookid2 : '1'})
  
    BookServices.addReview = jest.fn().mockResolvedValue({
      data: { success: true },
    });

    wrapper.setData({valoracioUsuari : false});
  
    await wrapper.vm.submitReview();

    expect(BookServices.createReviewComments).toHaveBeenCalledWith(data, wrapper.vm.bookid2);
    expect(BookServices.createReviewPoints).toHaveBeenCalledWith(data2, wrapper.vm.bookid2);
  
    expect(SwalMock).toHaveBeenCalledWith({
      icon: 'success',
      title: 'Success!',
      text: 'Grácies per la teva valoració!'
    });
  });
  
  it('shows an error when trying to comment on a book that already has a comment by the same user', async () => {
    const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();

    BookServices.getReviews.mockResolvedValue({
      data: [],
    });
    UserServices.getUserById2.mockResolvedValue({});
    const wrapper = mount(BookDetails, {
      localVue,
      router,
    });
  
    wrapper.setData({
      rating: 4,
      comment: 'Another comment',
      valoracioUsuari: true,
    });
  
    await wrapper.vm.submitReview();
  
    expect(SwalMock).toHaveBeenCalledWith({
      icon: 'warning',
      title: 'Valoració ja registrada',
      text: 'Aquest usuari ja te una valoració en aquest llibre.'
    });;
  });

});
