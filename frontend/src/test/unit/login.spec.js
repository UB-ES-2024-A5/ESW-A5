import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import Login from '../../components/login.vue';
import userServices from '../../services/UserServices';
import WishlistServices from '../../services/WishlistServices';
import Swal from 'sweetalert2';


import axios from 'axios';
function flushPromises() {
  return new Promise(resolve => setImmediate(resolve));
}

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
          Authorization: '',
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

jest.mock('../../services/WishlistServices', () => ({
  createWishlistOnLogin : jest.fn(),
}))
  
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
        WishlistServices.createWishlistOnLogin = jest.fn().mockResolvedValue()

        userServices.getActualUser = jest.fn().mockResolvedValue({
          email: 'test@example.com',
          is_editor: false
        });

        const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();
      
        await wrapper.setData({
          email: 'test@example.com',
          password: 'correctpassword'
        });
    
        await wrapper.find('form').trigger('submit.prevent');
        await wrapper.vm.$nextTick();
      
        expect(axios.post).toHaveBeenCalledWith(
            `${process.env.API_URL}/api/v1/login/access-token`, 
            'username=test@example.com&password=correctpassword',
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
          );
       
        await wrapper.vm.$nextTick();
        
        expect(WishlistServices.createWishlistOnLogin).toHaveBeenCalled();
        await wrapper.vm.$nextTick();
        await flushPromises();

        expect(SwalMock).toHaveBeenCalledWith({
          icon: 'success',
          title: 'Welcome!',
          text: "Redirecting to the user's page...",
          timer: 2000,
          showConfirmButton: false
        });

        SwalMock.mockRestore();
      
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
            path: '/mainPage_user',
            query: { email: 'test@example.com', token: 'dummy_token' }
          });
      });

      it('should login successfully and redirect to editor page', async () => {

        axios.post.mockResolvedValue({ data: { access_token: 'dummy_token' } });
        WishlistServices.createWishlistOnLogin = jest.fn().mockResolvedValue()

        userServices.getActualUser = jest.fn().mockResolvedValue({
          email: 'test@example.com',
          is_editor: true
        });

        const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();
      
        await wrapper.setData({
          email: 'test@example.com',
          password: 'correctpassword'
        });
    
        await wrapper.find('form').trigger('submit.prevent');
        await wrapper.vm.$nextTick();
      
        expect(axios.post).toHaveBeenCalledWith(
            `${process.env.API_URL}/api/v1/login/access-token`, 
            'username=test@example.com&password=correctpassword',
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
          );
       
        await wrapper.vm.$nextTick();

        expect(SwalMock).toHaveBeenCalledWith({
          icon: 'success',
          title: 'Welcome!',
          text: "Redirecting to the publisher's page...",
          timer: 2000,
          showConfirmButton: false
        });
      
        SwalMock.mockRestore();

        expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
            path: '/mainPage_publisher',
            query: { email: 'test@example.com', token: 'dummy_token' }
          });
      });

      it('should show error if login fails', async () => {
        axios.post.mockRejectedValue(new Error('Invalid credentials'));

        const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();

        await wrapper.setData({
          email: 'test@example.com',
          password: 'incorrectpassword'
        });
        await wrapper.find('form').trigger('submit.prevent');
        await wrapper.vm.$nextTick();

        expect(SwalMock).toHaveBeenCalledWith({
          icon: 'error',
          title: 'Login Failed',
          text: 'Email or Password incorrect. Please try again.'
        });
      
        SwalMock.mockRestore()
      
    });

    it('should redirect to sign up page when sign up link is clicked', async () => {
        const signupLink = wrapper.find('.signup-link-text');
        expect(signupLink.attributes('to')).toBe('/signup');
    });
  });