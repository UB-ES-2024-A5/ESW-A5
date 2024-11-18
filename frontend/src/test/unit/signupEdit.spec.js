import { mount } from '@vue/test-utils';
import Signup from '../../components/signupEdit.vue';
import UserService from '../../services/UserServices';

jest.mock('../../services/UserServices', () => ({
    create: jest.fn(() => Promise.resolve()),
  }));

  describe('signup.vue', () => {
    let wrapper;
  
    beforeEach(() => {
      wrapper = mount(Signup, {
        stubs: {
          'router-link': true
        }
      });
      wrapper.vm.$router = { push: jest.fn() };
    });

    it('renders correctly', () => {
        expect(wrapper.exists()).toBe(true);
      });

    



  });