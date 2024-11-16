import { mount } from '@vue/test-utils';
import Login from '../../components/login.vue';
import LoginService from '../../services/LoginServices';

import axios from 'axios';

jest.mock('axios', () => ({
  post: jest.fn(),
  create : jest.fn()
}));
  
  describe('login.vue', () => {
    let wrapper;
  
    beforeEach(() => {
      wrapper = mount(Login, {
        stubs: {
          'router-link': true
        }
      });
      wrapper.vm.$router = { push: jest.fn() };
    });
  
    it('renders correctly', () => {
      expect(wrapper.exists()).toBe(true);
    });

    it('should login successfully and redirect to main page', async () => {

        axios.post.mockResolvedValue({ data: { access_token: 'dummy_token' } });
      
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
       
      
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith({
            path: '/mainpage_user',
            query: { email: 'test@example.com', logged: true, token: 'dummy_token' }
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