import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import WelcomePage from '../../components/welcomePage.vue';
import MainPagePublisher from '../../components/mainPagePublisher.vue';
import BookServices from '../../services/BookServices';
import UserServices from '../../services/UserServices';
import SearchServices from '../../services/SearchServices';


jest.mock('../../services/BookServices', () => ({
  getAllBooks: jest.fn(),
}));

jest.mock('../../services/UserServices', () => ({
  getActualUser: jest.fn(),
}));
jest.mock('../../services/SearchServices', () => ({
  search: jest.fn(),
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
  it('updates searchQuery on input and calls search method', async () => {
    const wrapper = mount(MainPagePublisher, {
      localVue,
      router,
    });

    const searchInput = wrapper.find('.search-bar');
    await searchInput.setValue('Test query');

    expect(wrapper.vm.searchQuery).toBe('Test query');
    expect(SearchServices.search).toHaveBeenCalledWith('Test query', 20);
  });

  it('shows dropdown with search results when populated', async () => {
    const wrapper = mount(MainPagePublisher, {
      localVue,
      router,
    });

    await wrapper.setData({
      searchResults: [
        { id: 3, name: 'User 1' },
        { id: 4, title: 'Book 1' },
      ],
      showDropdown: true,
    });

    await wrapper.vm.$nextTick();

    const dropdownItems = wrapper.findAll('.dropdown-item');
    expect(dropdownItems.length).toBe(2);
    expect(dropdownItems.at(0).text()).toContain('User 1');
    expect(dropdownItems.at(1).text()).toContain('Book 1');
  });

});



