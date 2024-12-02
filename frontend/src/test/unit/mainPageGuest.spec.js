import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import WelcomePage from '../../components/WelcomePage.vue';
import MainPageGuest from '../../components/MainPageGuest.vue';
import BookServices from '../../services/BookServices';

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
      { path: '/guest', component: MainPageGuest },
    ];

    router = new VueRouter({
      mode: 'history',
      routes,
    });
  });

  it('should navigate from Welcome Page to MainPageGuest on Guest Access click', async () => {
    const wrapper = mount(WelcomePage, {
      localVue,
      router,
    });

    await wrapper.vm.$nextTick();

    const button = wrapper.find('.sign-up-btn[href="/mainpage_guest"]');
    expect(button.exists()).toBe(true);


    await button.trigger('click');
    await wrapper.vm.$nextTick();

    expect(router.currentRoute.path).toBe('/mainpage_guest');
  });
});

describe('Checking MainPage guest', () => {
  let router;
  const localVue = createLocalVue();
  localVue.use(VueRouter);

  beforeEach(() => {
    const routes = [];
    router = new VueRouter({ mode: 'history', routes });
  });

  it('should display a list of books in the carousel', async () => {
    const wrapper = mount(MainPageGuest, {
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

  it('should display a login button and not show a profile icon', () => {
    const wrapper = mount(MainPageGuest, {
      localVue,
      router,
    });

    const loginButton = wrapper.find('.sign-in-btn');
    expect(loginButton.exists()).toBe(true);
    expect(loginButton.text()).toBe('Sign in');

    const profileIcon = wrapper.find('.profile-icon');
    expect(profileIcon.exists()).toBe(false);
  });

});



