import { mount } from '@vue/test-utils';
import Signup from '../../components/signupEdit.vue';
import UserService from '../../services/UserServices';
import AccountServices from '../../services/AccountServices';

// Mockear UserService
jest.mock('../../services/UserServices', () => ({
  create: jest.fn(() => Promise.resolve()),
}));

jest.mock('../../services/AccountServices', () => ({
  create: jest.fn(() => Promise.resolve())
}));

describe('signupEdit.vue', () => {
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

    //NAME VALIDATIONS
    it('sets valid name and displays correct icon', async () => {
      wrapper.setData({ name: 'John' });
      wrapper.vm.validateName();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.nameValid).toBe(true);
      const errorIcon = wrapper.find('img[alt="Valid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    it('sets invalid name for name containing a number and displays incorrect icon', async () => {
      wrapper.setData({ name: 'John1' });
      wrapper.vm.validateName();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.nameValid).toBe(false);
      const errorIcon = wrapper.find('img[alt="Invalid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    it('sets invalid name for name containing a symbol and displays incorrect icon', async () => {
      wrapper.setData({ name: 'John&' });
      wrapper.vm.validateName();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.nameValid).toBe(false);
      const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
      expect(errorIcon.exists()).toBe(true);
    });
    
    it('sets valid name for name containing a space and displays correct icon', async () => {
      wrapper.setData({ name: 'John Pork' });
      wrapper.vm.validateName();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.nameValid).toBe(true);
      const errorIcon = wrapper.find('img[alt="Valid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    it('sets invalid name for name being only a space and displays incorrect icon', async () => {
      wrapper.setData({name: ' '});
      wrapper.vm.validateName();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.nameValid).toBe(false);
      const errorIcon = wrapper.find('img[title="Only letters are allowed."]');
      expect(errorIcon.exists()).toBe(true);
     });

     //CIF VALIDATIONS
     it('sets valid cif and displays correct icon', async () => {
      wrapper.setData({ cif: 'g56565656' });
      wrapper.vm.validateCIF();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.cifValid).toBe(true);
      const errorIcon = wrapper.find('img[alt="Valid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    it('sets invalid cif for cif not containing a letter and displays incorrect icon', async () => {
      wrapper.setData({ cif: '88888888' });
      wrapper.vm.validateCIF();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.cifValid).toBe(false);
      const errorIcon = wrapper.find('img[alt="Invalid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    it('sets invalid cif for cif being larger than 8 digits and displays incorrect icon', async () => {
      wrapper.setData({ cif: 'H234567890' });
      wrapper.vm.validateCIF();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.cifValid).toBe(false);
      const errorIcon = wrapper.find('img[alt="Invalid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    it('sets invalid cif for cif being shorter than 8 digits and displays incorrect icon', async () => {
      wrapper.setData({ cif: 'H23' });
      wrapper.vm.validateCIF();
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.cifValid).toBe(false);
      const errorIcon = wrapper.find('img[alt="Invalid"]');
      expect(errorIcon.exists()).toBe(true);
    });

    //MAIL COMPROVATIONS´
  it('sets valid email and displays correct icon', async () => {
    wrapper.setData({ email: 'example@gmail.com' });
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(true);
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid email without @ and displays incorrect icon', async () => {
    wrapper.setData({ email: 'asdasdasd.com' });
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid email without . and displays incorrect icon', async () => {
    wrapper.setData({ email: 'asdasdasd@com' });
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid email without domain part and displays incorrect icon', async () => {
    wrapper.setData({ email: 'asdasdasd@.com' });
    wrapper.vm.validateEmail();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.emailValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

  //PASSWORD VALIDATION
  it('sets correct password and displays correct icon', async () => {
    wrapper.setData({ password: 'Testing#' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(true);
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid password for a password with less than 8 chars and displays incorrect icon', async () => {
    wrapper.setData({ password: 'Test#' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid password for a password with more than 40 chars but with all the character requisites and displays incorrect icon', async () => {
    wrapper.setData({ password: 'Testing#Testing#Testing#Testing#Testing#1' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid password for a password without a capital letter but with the correct length and a symbol and displays incorrect icon', async () => {
    wrapper.setData({ password: 'testing#' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid password for a password without a symbol but with the correct length and a capital letter and displays incorrect icon', async () => {
    wrapper.setData({ password: 'Testingg' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets invalid password for a password without a symbol or a capital letter but with the correct length and displays incorrect icon', async () => {
    wrapper.setData({ password: 'testingg' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.passwordValid).toBe(false);
    const errorIcon = wrapper.find('img[alt="Invalid"]');
    expect(errorIcon.exists()).toBe(true);
});

  //CONFIRM PASSWORD COMPROVATIONS
  it('sets correct confirm password for valid password and displays correct icon', async () => {
    wrapper.setData({ password: 'Testing#' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({ confirmPassword: 'Testing#' });
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(true);
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets correct confirm password for invalid password and displays correct icon', async () => {
    wrapper.setData({ password: 'Testing' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({ confirmPassword: 'Testing' });
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(true);
    const errorIcon = wrapper.find('img[alt="Valid"]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets incorrect confirm password when they are not the same but password is valid and displays incorrect icon', async () => {
    wrapper.setData({ password: 'Testing#' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({ confirmPassword: 'Testing1#' });
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(false);
    const errorIcon = wrapper.find('img[title="Passwords do not match."]');
    expect(errorIcon.exists()).toBe(true);
});

it('sets incorrect confirm password when they were the same but password is changed and displays incorrect icon', async () => {
    wrapper.setData({ password: 'Testing#' });
    wrapper.vm.validatePassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({ confirmPassword: 'Testing#' });
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    wrapper.setData({ password: 'Testing1#' });
    wrapper.vm.validateConfirmPassword();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.confirmPasswordValid).toBe(false);
    const errorIcon = wrapper.find('img[title="Passwords do not match."]');
    expect(errorIcon.exists()).toBe(true);
});
//LOGIN LINK 
it('navigates to login page when login link is clicked', async () => {
  const loginLink = wrapper.find(".login-link-text");
  expect(loginLink.exists()).toBe(true);
  expect(loginLink.attributes('to')).toBe('/login');
});

//BUTTON SIGNUP
it('should return true for canRegister when all validations pass and terms are agreed to', async() =>{
  wrapper.setData({nameValid: true});
  wrapper.setData({cifValid : true});
  wrapper.setData({emailValid : true});
  wrapper.setData({passwordValid : true});
  wrapper.setData({confirmPasswordValid : true});
  wrapper.setData({agreedToTerms: true});
  expect(wrapper.vm.canRegister).toBe(true);
});

it('should return false for canRegister when not all validations pass and terms are agreed to', async() =>{
  wrapper.setData({nameValid: true});
  wrapper.setData({cifValid : false});
  wrapper.setData({emailValid : true});
  wrapper.setData({passwordValid : true});
  wrapper.setData({confirmPasswordValid : true});
  wrapper.setData({agreedToTerms: true});
  expect(wrapper.vm.canRegister).toBe(false);
});


it('should return false for canRegister when all validations pass and terms are not agreed to', async() =>{
  wrapper.setData({nameValid: true});
  wrapper.setData({cifValid : true});
  wrapper.setData({emailValid : true});
  wrapper.setData({passwordValid : true});
  wrapper.setData({confirmPasswordValid : true});
  wrapper.setData({agreedToTerms: false});
  expect(wrapper.vm.canRegister).toBe(false);
});

it('calls UserService.create when form is valid and button is clicked', async () => {

  wrapper.setData({
    name: 'John',
    cif: '1234567890123',
    email: 'john.doe@example.com',
    password: 'Password@123',
    confirmPassword: 'Password@123',
    nameValid: true,
    cifValid: true,
    emailValid: true,
    passwordValid: true,
    confirmPasswordValid: true,
    agreedToTerms: true
  });
  UserService.create.mockResolvedValue({ id: 123 });
  AccountServices.create.mockResolvedValue({});;
  window.alert = jest.fn();
  await wrapper.find('form').trigger('submit');
  expect(UserService.create).toHaveBeenCalledWith({
    name: 'John',
    cif: '1234567890123',
    is_editor: true,
    email: 'john.doe@example.com',
    password: 'Password@123'
  });
  expect(AccountServices.create).toHaveBeenCalledWith(123);
  expect(window.alert).toHaveBeenCalledWith('La cuenta se ha creado correctamente. Por favor inicie sesión.');
  expect(wrapper.vm.$router.push).toHaveBeenCalledWith({ path: '/login' });
});

it('handles error when creating a user', async () => {
  wrapper.setData({
    name: 'John',
    cif: '1234567890123',
    email: 'john.doe@example.com',
    password: 'Password@123',
    confirmPassword: 'Password@123',
    nameValid: true,
    cifValid: true,
    emailValid: true,
    passwordValid: true,
    confirmPasswordValid: true,
    agreedToTerms: true
  });
  const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  window.alert = jest.fn();
  UserService.create.mockRejectedValue(new Error('Error de creación'));
  await wrapper.find('form').trigger('submit');
  await wrapper.vm.$nextTick();
  expect(UserService.create).toHaveBeenCalledWith({
    name: 'John',
    cif: '1234567890123',
    is_editor: true,
    email: 'john.doe@example.com',
    password: 'Password@123'
  });
  expect(consoleErrorSpy).toHaveBeenCalledWith(expect.any(Error));
  expect(window.alert).toHaveBeenCalledWith('Hubo un error al crear la cuenta.');
});

it('shows alert if canRegister is false', async() => {
  wrapper.setData({ nameValid: false });
  window.alert = jest.fn();
  await wrapper.find('form').trigger('submit');
  expect(window.alert).toHaveBeenCalledWith('Please correct the errors in the form.');
});

});

