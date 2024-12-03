import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import MainPageUser from '../../components/MainPageUser.vue'; // Asegúrate de importar el componente correcto
import Login from '../../components/login.vue';
import Swal from 'sweetalert2';
import BookServices from '../../services/BookServices';
import WelcomePage from '../../components/welcomePage.vue';

jest.mock('../../services/BookServices', () => ({
  getAllBooks: jest.fn(),
}));

describe('Navigation from Welcome Page to MainPageGuest', () => {
  let router;
  const localVue = createLocalVue();
  localVue.use(VueRouter);

  beforeEach(() => {
    BookServices.getAllBooks.mockResolvedValue([
      { id: 1, img: 'book1.png' },
      { id: 2, img: 'book2.png' },
    ]);
    const routes = [
      { path: '/', component: WelcomePage },
      { path: '/mainPage_user', component: MainPageUser },
    ];

    router = new VueRouter({
      mode: 'history',
      routes,
    });
  });

  it('should display a list of books in the carousel', async () => {
    const wrapper = mount(MainPageUser, {
      localVue,
      router,
    });

    wrapper.setData({
      books: [
        { id: 1, img: 'book1.png' },
        { id: 2, img: 'book2.png' },
      ],
    });

    await wrapper.vm.$nextTick();

    const images = wrapper.findAll('.carousel-image');
    expect(images.length).toBe(2);
    expect(images.at(0).attributes('src')).toBe('book1.png');
  });


  it('should display the user icon', () => {

    const wrapper = mount(MainPageUser, {
      localVue,
      router,
    });

    const userIcon = wrapper.find('.user-icon')
    expect(userIcon.exists()).toBe(true)

  });

  
});
