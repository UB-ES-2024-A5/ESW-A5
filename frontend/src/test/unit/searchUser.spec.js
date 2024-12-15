import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import searchUserProfile from '../../components/searchUserProfile.vue';
import searchPublisherProfile from '../../components/searchPublisherProfile.vue'
import Swal from 'sweetalert2';
import accountServices from '../../services/AccountServices';
import UserServices from '../../services/UserServices';
import wishlistServices from '../../services/WishlistServices';

  const flushPromises = () => new Promise(resolve => setImmediate(resolve));


  jest.mock('../../services/AccountServices', () => ({
    getAccountById: jest.fn(),
    getFollowingAccounts: jest.fn(),
    followAccount : jest.fn(),
    unfollowAccount: jest.fn(),
  }));
  jest.mock('../../services/UserServices', () => ({
    getUserById: jest.fn(),
  }));
  
  jest.mock('../../services/WishlistServices', () => ({
    getWishlistByUserId : jest.fn(),
    readBooksOfWishlist: jest.fn(),
  }));

  describe('UserProfile.vue - Follow functionality', () => {
    let wrapper
  
    beforeEach(() => {
     
      wrapper = mount(searchUserProfile, {
        mocks: {
          $route: { query: { userID: '123' } }
        }
      })
    })
  
    it('should toggle follow state to true when following a user', async () => {
      accountServices.followAccount.mockResolvedValue();
      UserServices.getUserById.mockResolvedValue({
        id: '123',
        name: 'Test User',
        surname: 'Test Surname',
        email: 'testuser@example.com',
      });
      accountServices.getAccountById.mockResolvedValue({
        id: '123',
        num_followers: '10',
        num_following: '5',
        bio: 'Test bio',
        photo: null,
      });
      accountServices.getFollowingAccounts.mockResolvedValue({ data: [] } );

      wrapper.setData({ isFollowing: false });

      await wrapper.vm.fetchUserProfile();
      await wrapper.vm.checkIfFollowing();
      
      

      await wrapper.vm.toggleFollow();

      expect(accountServices.followAccount).toHaveBeenCalledWith('123');

      accountServices.getFollowingAccounts.mockResolvedValue({ data: [{following_id : '123'}] } );
      await wrapper.vm.fetchUserProfile();
      expect(wrapper.vm.isFollowing).toBe(true);
    });
  
    it('should toggle follow state to false when unfollowing a user', async () => {
      accountServices.unfollowAccount.mockResolvedValue();
      UserServices.getUserById.mockResolvedValue({
        id: '123',
        name: 'Test User',
        surname: 'Test Surname',
        email: 'testuser@example.com',
      });
      accountServices.getAccountById.mockResolvedValue({
        id: '123',
        num_followers: '10',
        num_following: '5',
        bio: 'Test bio',
        photo: null,
      });
      accountServices.getFollowingAccounts.mockResolvedValue({ data: [{following_id : '123'}] } );

      await wrapper.vm.fetchUserProfile();
      await wrapper.vm.checkIfFollowing();


      wrapper.setData({ isFollowing: true });

      await wrapper.vm.toggleFollow();
      await wrapper.vm.fetchUserProfile();

      expect(accountServices.unfollowAccount).toHaveBeenCalledWith('123')
      accountServices.getFollowingAccounts.mockResolvedValue({ data: [] } );
      await wrapper.vm.fetchUserProfile();
      expect(wrapper.vm.isFollowing).toBe(false)
    });

    it('should display "Unfollow" when following', async () => {
      await wrapper.setData({ isFollowing: true });
      const button = wrapper.find('.follow-button');
      expect(button.text()).toBe('Unfollow');
    });

    it('should display "Follow" when not following', async () => {
      await wrapper.setData({ isFollowing: false });
      const button = wrapper.find('.follow-button');
      expect(button.text()).toBe('Follow');
    });
  });
