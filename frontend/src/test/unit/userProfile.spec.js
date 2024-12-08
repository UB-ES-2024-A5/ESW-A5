import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import UserProfile from '../../components/userProfile.vue'
import accountServices from '../../services/AccountServices.js'
import wishlistServices from '../../services/WishlistServices.js'
import userServices from '../../services/UserServices';
import Swal from 'sweetalert2'

jest.mock('../../services/UserServices', () => ({
  getActualUser: jest.fn(),
}))

jest.mock('../../services/AccountServices.js', () => ({
  getActualAccount: jest.fn(),
  updateAccount: jest.fn(),
}))

jest.mock('../../services/WishlistServices.js', () => ({
  getMyWishlists: jest.fn(),
  readBooksOfWishlist: jest.fn(),
}))

describe('UserProfile.vue', () => {
    let wrapper;
    let router;
    const localVue = createLocalVue();
    localVue.use(VueRouter);

  beforeEach(() => {
    const routes = [
        { path: '/user_profile', component: UserProfile },
      ];
  
      router = new VueRouter({
        mode: 'history',
        routes,
      });

      wrapper = mount(UserProfile, {
        localVue,
        router,
      });
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('fetchUserProfile obtiene los datos del usuario correctamente', async () => {

    const userData = {
      name: 'John',
      surname: 'Doe',
      email: 'john.doe@example.com',
    }
    const accountData = {
      num_followers: 10,
      num_following: 5,
      bio: 'Hello, I am John!',
      photo: 'photo-url.jpg',
    }

    userServices.getActualUser.mockResolvedValue(userData)
    accountServices.getActualAccount.mockResolvedValue(accountData)

    await wrapper.vm.fetchUserProfile()

    expect(wrapper.vm.user.name).toBe('John')
    expect(wrapper.vm.user.surname).toBe('Doe')
    expect(wrapper.vm.user.email).toBe('john.doe@example.com')
    expect(wrapper.vm.account.num_followers).toBe(10)
    expect(wrapper.vm.account.num_following).toBe(5)
    expect(wrapper.vm.account.bio).toBe('Hello, I am John!')
    expect(wrapper.vm.userProfileImage).toBe('photo-url.jpg')
  })

  test('fetchWishlistsInformation obtiene correctamente la wishlist', async () => {
    const wishlistData = {
      data: [{ id: 'wishlist1' }],
    };
    const booksData = {
      data: [
        { id: 1, title: 'Book 1', author: 'Author 1' },
        { id: 2, title: 'Book 2', author: 'Author 2' },
      ],
    };
  
    wishlistServices.getMyWishlists.mockResolvedValue(wishlistData);
    wishlistServices.readBooksOfWishlist.mockResolvedValue(booksData);
  
    await wrapper.vm.fetchWishlistsInformation();
          
    await expect(wishlistServices.getMyWishlists).toHaveBeenCalled();
  
    await expect(wishlistServices.readBooksOfWishlist).toHaveBeenCalledWith('wishlist1');
  
    expect(wrapper.vm.user.wishlist).toEqual(booksData.data);
  });
  
})

describe('UserProfile.vue - Edición de biografía y foto de perfil', () => {
    let wrapper;
    let router;
    const localVue = createLocalVue();
    localVue.use(VueRouter);

  beforeEach(() => {
    const routes = [
        { path: '/user_profile', component: UserProfile },
      ];
  
      router = new VueRouter({
        mode: 'history',
        routes,
      });

      wrapper = mount(UserProfile, {
        localVue,
        router,
      });

    })
    it('toggleEditBio - Guarda una biografía válida', async () => {
        const validBio = 'This is a valid biography.';
        wrapper.setData({
          isEditingBio: true,
          editedBiography: validBio,
        });
    
        accountServices.updateAccount = jest.fn().mockResolvedValue({});
        wrapper.vm.fetchUserProfile = jest.fn();
    
        await wrapper.vm.toggleEditBio();
    
        expect(accountServices.updateAccount).toHaveBeenCalledWith({ bio: validBio });
        expect(wrapper.vm.fetchUserProfile).toHaveBeenCalled();
        expect(wrapper.vm.isEditingBio).toBe(false);
      });

      it('toggleEditBio - Rechaza una biografía que supera los 200 caracteres', async () => {
        const longBio = 'a'.repeat(201);
        wrapper.setData({
          isEditingBio: true,
          editedBiography: longBio,
        });
    
        Swal.fire = jest.fn();
    
        await wrapper.vm.toggleEditBio();
    
        expect(Swal.fire).toHaveBeenCalledWith({
          icon: 'error',
          title: 'Error',
          text: 'The biography cannot exceed 200 characters.',
          timer: 2000,
          showConfirmButton: false,
        });
      });

      it('should update the image correctly and handle valid JPEG file', async () => {

        const SwalMockSuccess = jest.spyOn(Swal, 'fire').mockResolvedValue();


        const mockFile = new File(['dummy content'], 'test.jpg', { type: 'image/jpeg' });
        
        const event = { target: { files: [mockFile] } };
    
        wrapper.vm.convertImageToBase64 = jest.fn().mockResolvedValue('data:image/jpeg;base64,dummyBase64String');
        
        await wrapper.vm.handleFileChange(event);

        expect(SwalMockSuccess).toHaveBeenCalledWith({
            icon: 'success',
            title: 'Photo updated',
            text: 'Your profile photo has been updated successfully.',
            timer: 2000,
            showConfirmButton: false
          });
    


          
    });

      it('handleFileChange - Rechaza archivos no JPEG', async () => {
        const file = new File(['dummy content'], 'photo.png', { type: 'image/png' });
        const event = { target: { files: [file] } };
    
        const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();
    
        await wrapper.vm.handleFileChange(event);
    
        expect(SwalMock).toHaveBeenCalledWith({
          icon: 'error',
          title: 'Invalid format',
          text: 'Por favor selecciona un archivo JPEG.',
          timer: 2000,
          showConfirmButton: false,
        });
    
        SwalMock.mockRestore();
      });
    
      it('handleFileChange - Maneja errores al convertir o guardar la foto', async () => {
        const file = new File(['dummy content'], 'photo.jpg', { type: 'image/jpeg' });
        const event = { target: { files: [file] } };
    
        wrapper.vm.convertImageToBase64 = jest.fn().mockRejectedValue(new Error('Conversion error'));
    
        const SwalMock = jest.spyOn(Swal, 'fire').mockResolvedValue();
    
        await wrapper.vm.handleFileChange(event);
    
        expect(wrapper.vm.convertImageToBase64).toHaveBeenCalledWith(file);
        expect(SwalMock).toHaveBeenCalledWith({
          icon: 'error',
          title: 'Error',
          text: 'The profile picture could not be updated.',
          timer: 2000,
          showConfirmButton: false,
        });
    
        SwalMock.mockRestore();
      });


});