import { mount } from '@vue/test-utils';
import Signup from '../components/signup.vue';
import UserService from '../services/UserServices';

// Mockear UserService
jest.mock('../services/UserServices', () => ({
  create: jest.fn(),
}));

describe('signup.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(Signup, {
      stubs: {
        'router-link': true
      }
    });
  });

  it('renders correctly', () => {
    expect(wrapper.exists()).toBe(true);
  });


    //NAME COMPROVATIONS

  it('sets invalid name for name containing a number', async () => {
    wrapper.setData({ name: 'John1' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.nameValid).toBe(false);
  });

  it('displays incorrect icon for name containing a number', async () => {
    wrapper.setData({ name: 'John123' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets invalid name for name containing a symbol', async () => {
    wrapper.setData({ name: 'John&' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.nameValid).toBe(false);
  });

  it('displays incorrect icon for name containing a symbol', async () => {
    wrapper.setData({ name: 'John&&&' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });
  
  it('sets valid name for name containing a space', async () => {
    wrapper.setData({ name: 'John Pork' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.nameValid).toBe(true);
  });

  it('displays correct icon for name containing a space', async () => {
    wrapper.setData({ name: 'John Pork' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

   it('sets invalid name for name being only a space', async () => {
    wrapper.setData({name: ' '});
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.nameValid).toBe(false);
   });

   it('displays incorrect icon for name being only a space', async () => {
    wrapper.setData({ name: ' ' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });


  

  
});
