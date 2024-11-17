import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import Login from '../../components/login.vue';
import userServices from '../../services/UserServices';

import axios from 'axios';


const localVue = createLocalVue();
localVue.use(VueRouter);
const router = new VueRouter();
jest.mock('axios', () => {
  return {
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
          Authorization: '', // Mocking Authorization header
        },
      },
    },
    interceptors: {
      request: { use: jest.fn(), eject: jest.fn() },
      response: { use: jest.fn(), eject: jest.fn() },
    },
  };
});

jest.mock('../../services/UserServices', () => ({
  getActualUser: jest.fn(),
}));
  
  describe('login.vue', () => {
    let wrapper;
  
    beforeEach(() => {
      wrapper = mount(Login, {
        stubs: {
          'router-link': true,
        },
      });
  
      // Mock the $router.push method
      wrapper.vm.$router = {
        push: jest.fn(), // Mock the push function
      };
    });
  
    it('renders correctly', () => {
      expect(wrapper.exists()).toBe(true);
    });

    it('should login successfully and redirect to main page', async () => {

        axios.post.mockResolvedValue({ data: { access_token: 'dummy_token' } });

        userServices.getActualUser = jest.fn().mockResolvedValue({
          email: 'test@example.com',
          is_editor: false
        });
      
        await wrapper.setData({
          email: 'test@example.com',
          password: 'correctpassword'
        });
    
        await wrapper.find('.login-button').trigger('click');
        await wrapper.vm.$nextTick();
      
        expect(axios.post).toHaveBeenCalledWith(
            `${process.env.API_URL}/api/v1/login/access-token`, 
            'username=test@example.com&password=correctpassword',
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
          );
       
        await wrapper.vm.$nextTick();
      
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
            path: '/mainPage_user',
            query: { email: 'test@example.com', token: 'dummy_token' }
          });
      });

      it('should show error if login fails', async () => {
        axios.post.mockRejectedValue(new Error('Invalid credentials'));

        window.alert = jest.fn();

        await wrapper.setData({
          email: 'test@example.com',
          password: 'incorrectpassword'
        });
        await wrapper.find('.login-button').trigger('click');
        await wrapper.vm.$nextTick();

        expect(window.alert).toHaveBeenCalledWith('Email or Password incorrect');
      
    });

    it('should redirect to sign up page when sign up link is clicked', async () => {
        const signupLink = wrapper.find('.signup-link-text');
        expect(signupLink.attributes('to')).toBe('/signup');
    });
  });