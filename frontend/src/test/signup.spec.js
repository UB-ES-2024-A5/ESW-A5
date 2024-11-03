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

  it('sets valid name', async () => {
    wrapper.setData({ name: 'John' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.nameValid).toBe(true);
  });

  it('displays correct icon for valid name', async () => {
    wrapper.setData({ name: 'John' });
    wrapper.vm.validateName();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

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
    const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
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
    const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
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
    const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
    expect(errorIcon.exists()).toBe(true);
  });


  //SURNAME COMPROVATIONS

  it('sets valid surname', async () => {
    wrapper.setData({ surname: 'Pork' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.surnameValid).toBe(true);
  });

  it('displays correct icon for valid surname', async () => {
    wrapper.setData({surname: 'Pork' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets invalid surname for surname containing a number', async () => {
    wrapper.setData({ surname: 'Pork1' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.surnameValid).toBe(false);
  });

  it('displays incorrect icon for surname containing a number', async () => {
    wrapper.setData({ surname: 'Pork1' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets invalid surname for surname containing a symbol', async () => {
    wrapper.setData({ surname: 'Pork&' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.surnameValid).toBe(false);
  });

  it('displays incorrect icon for surname containing a symbol', async () => {
    wrapper.setData({ surname: 'Pork&&&' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
    expect(errorIcon.exists()).toBe(true);
  });
  
  it('sets valid surname for surname containing a space', async () => {
    wrapper.setData({ surname: 'Rizz Pork' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.surnameValid).toBe(true);
  });

  it('displays correct icon for surname containing a space', async () => {
    wrapper.setData({ surname: 'Rizz Pork' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

   it('sets invalid surname for surname being only a space', async () => {
    wrapper.setData({surname: ' '});
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.surnameValid).toBe(false);
   });

   it('displays incorrect icon for surname being only a space', async () => {
    wrapper.setData({surname: ' ' });
    wrapper.vm.validateSurname();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
    expect(errorIcon.exists()).toBe(true);
  });

  //MAIL COMPROVATIONS´
  it('sets valid mail', async() =>{
    wrapper.setData({email:'example@gmail.com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(true);
  });

  it('displays correct icon for mail', async () => {
    wrapper.setData({email: 'example@gmail.com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets invalid mail with mail without @', async () =>{
    wrapper.setData({email: 'asdasdasd.com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(false);
  });

  it('displays incorrect icon for mail without @', async () => {
    wrapper.setData({email: 'asdasdasd.com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets invalid mail with mail without .', async () =>{
    wrapper.setData({email: 'asdasdasd@com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(false);
  });

  it('displays incorrect icon for mail without .', async () => {
    wrapper.setData({email: 'asdasdasd@com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets invalid mail with mail without domain part', async () =>{
    wrapper.setData({email: 'asdasdasd@.com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(false);
  });

  it('displays incorrect icon for mail without domain part', async () => {
    wrapper.setData({email: 'asdasdasd@.com'});
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  //PASSWORD VALIDATION

  it('sets correct password', async() =>{
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(true);
  });

  it('displays incorrect icon for mail without @', async () => {
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect password for a password with less than 8 chars', async() =>{
    wrapper.setData({password:'Test#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
  });

  it('displays incorrect icon for a password with less than 8 chars', async () => {
    wrapper.setData({password:'Test#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect password for a password with more than 40 chars but with all the chars requisites', async() =>{
    wrapper.setData({password:'Testing#Testing#Testing#Testing#Testing#1'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
  });

  it('displays incorrect icon for a password with more than 40 chars but with all the chars requisites', async () => {
    wrapper.setData({password:'Testing#Testing#Testing#Testing#Testing#1'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect password for a password without a capital letter but with the correct length and a symbol', async() =>{
    wrapper.setData({password:'testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
  });

  it('displays incorrect icon for a password without a capital letter but with the correct length and a symbol', async () => {
    wrapper.setData({password:'testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect password for a password without a symbol but with the correct length and a capital letter', async() =>{
    wrapper.setData({password:'Testingg'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
  });

  it('displays incorrect icon for a password without a symbol but with the correct length and a capital letter', async () => {
    wrapper.setData({password:'Testingg'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect password for a password without a symbol or a capital letter but with the correct length ', async() =>{
    wrapper.setData({password:'testingg'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
  });

  it('displays incorrect icon for a password without a symbol or a capital letter but with the correct length ', async () => {
    wrapper.setData({password:'testingg'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('shows password when we click the toggle', async() =>{
    expect(wrapper.vm.showPassword).toBe(false)
    const toggleButton = wrapper.find('.toggle-password')
    await toggleButton.trigger('click')
    expect(wrapper.vm.showPassword).toBe(true)
    const passwordInput = wrapper.find('input[placeholder="Password"]')
    expect(passwordInput.attributes('type')).toBe('text')
  })



  //CONFIRM PASSWORD COMPROVATIONS
  it('sets correct confirm password for valid password', async() =>{
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(true);
  });

  it('displays correct icon for confirm password for valid password', async () => {
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets correct confirm password for invalid password', async() =>{
    wrapper.setData({password:'Testing'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(true);
  });

  it('displays correct icon for confirm password for valid password', async () => {
    wrapper.setData({password:'Testing'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect confirm password when are not the same but password is valid', async() =>{
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing1#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(false);
  });

  it('displays incorrect icon for confirm password when are not the same but password is valid', async () => {
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing1#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[title="Passwords do not match."]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('sets incorrect confirm password when they were the same but password is changed', async() =>{
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({password:'Testing1#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(false);
  });

  it('displays incorrect icon for confirm password when they were the same but password is changed', async () => {
    wrapper.setData({password:'Testing#'});
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({confirmPassword:'Testing#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({password:'Testing1#'});
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    const errorIcon = wrapper.find('img[title="Passwords do not match."]');
    expect(errorIcon.exists()).toBe(true);
  });

  it('shows password when we click the toggle', async() =>{
    expect(wrapper.vm.showConfirmPassword).toBe(false)
    const toggleButton = wrapper.find('.toggle-confirm-password');
    await toggleButton.trigger('click')
    expect(wrapper.vm.showConfirmPassword).toBe(true)
    const confirmPasswordInput = wrapper.find('input[placeholder="Confirm Password"]')
    expect(confirmPasswordInput.attributes('type')).toBe('text')
  });

  //TERMS AND CONDITIONS COMPROVATIONS
  it('sets true terms and conditions when checkbox is clicked',async() =>{
    expect(wrapper.vm.agreedToTerms).toBe(false);
    const checkbox = wrapper.find('input[type="checkbox"]');
    await checkbox.setChecked();
    expect(wrapper.vm.agreedToTerms).toBe(true);
  });

});
