import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import WelcomePage from '../../components/welcomePage.vue';
import MainPagePublisher from '../../components/mainPagePublisher.vue';
import BookServices from '../../services/BookServices';
import UserServices from '../../services/UserServices';


jest.mock('../../services/BookServices', () => ({
  getAllBooks: jest.fn(),
}));

jest.mock('../../services/UserServices', () => ({
  getActualUser: jest.fn(),
}));

describe('Check info in MainPagePublisher', () => {
  let router;
  const localVue = createLocalVue();
  localVue.use(VueRouter);

  beforeEach(() => {
    UserServices.getActualUser.mockResolvedValue({ data: { id: 1, name: 'Test User' } });
    BookServices.getAllBooks.mockResolvedValue([
      { id: 1, img: 'book1.png' },
      { id: 2, img: 'book2.png' },
    ]);
    const routes = [
      { path: '/', component: WelcomePage },
      { path: '/guest', component: MainPagePublisher },
    ];

    router = new VueRouter({
      mode: 'history',
      routes,
    });
  });

  it('should display a list of books in the carousel', async () => {
    const wrapper = mount(MainPagePublisher, {
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

    const wrapper = mount(MainPagePublisher, {
      localVue,
      router,
    });

    const userIcon = wrapper.find('.user-icon')
    expect(userIcon.exists()).toBe(true)

  });

  it('should check for + button', () => {

    const wrapper = mount(MainPagePublisher, {
      localVue,
      router,
    });

    const addButton = wrapper.find('.add-button')
    expect(addButton.exists()).toBe(true);
  });

});



