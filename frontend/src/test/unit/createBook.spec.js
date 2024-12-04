import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import WelcomePage from '../../components/welcomePage.vue';
import MainPagePublisher from '../../components/mainPagePublisher.vue';
import CreatePublication from '../../components/createPublication.vue';
import Login from '../../components/login.vue';

global.URL.createObjectURL = jest.fn(() => 'mockedObjectURL');

describe('Create publication tests', () => {
    let router;
    let wrapper;
    const localVue = createLocalVue();
    localVue.use(VueRouter);
  
    beforeEach(() => {
      // Mock del estado de autenticación. Aquí asumimos que el usuario no está autenticado.
      const routes = [
        { path: '/login', component: Login },
        { path: '/create_publication', component: CreatePublication, meta: { requiresAuth: true } },
        { path: '/', component: WelcomePage },
      ];
  
      router = new VueRouter({
        mode: 'history',
        routes,
      });

       wrapper = mount(CreatePublication, {
        localVue,
        router,
      });
    });

    it('should go to create publication', async () => {

        router.push('/create_publication');



          expect(wrapper.vm.$route.path).toBe('/create_publication');4

          expect(wrapper.find('input[placeholder="Title"]').exists()).toBe(true)
          expect(wrapper.find('input[placeholder="Author"]').exists()).toBe(true)
          expect(wrapper.find('input[placeholder="Editorial"]').exists()).toBe(true)
          expect(wrapper.find('input[placeholder="Year of Publication"]').exists()).toBe(true)
          expect(wrapper.find('input[placeholder="ISBN"]').exists()).toBe(true)
          expect(wrapper.find('input[placeholder="Price"]').exists()).toBe(true)
          expect(wrapper.find('textarea[placeholder="Synopsis"]').exists()).toBe(true)
          expect(wrapper.find('.genre-selection').exists()).toBe(true)
          expect(wrapper.findAll('input[type="checkbox"]').length).toBe(5)
          expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
        });

        it('sets invalid title for an empty title and displays incorrect icon', async () => {
            wrapper.setData({ title: '' });
            wrapper.vm.validateTitle();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.titleValid).toBe(false);
          });
          
          
          it('sets valid title for a title with 1 or more characters and displays correct icon', async () => {
            wrapper.setData({ title: 'Valid Title' });
            wrapper.vm.validateTitle();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.titleValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });

          it('sets invalid author for an empty author and displays incorrect icon', async () => {
            wrapper.setData({ author: '' });
            wrapper.vm.validateAuthor();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.authorValid).toBe(false);
          });
          
          it('sets valid author for an author with 1 or more characters and displays correct icon', async () => {
            wrapper.setData({ author: 'John Doe' });
            wrapper.vm.validateAuthor();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.authorValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });
          
          it('sets invalid author for an author with non-alphabetical characters and displays incorrect icon', async () => {
            wrapper.setData({ author: 'John123' });
            wrapper.vm.validateAuthor();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.authorValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets valid author for an author with spaces and alphabetical characters and displays correct icon', async () => {
            wrapper.setData({ author: 'John Doe' });
            wrapper.vm.validateAuthor();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.authorValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });

          it('sets invalid editorial for an editorial with non-alphabetical characters and displays incorrect icon', async () => {
            wrapper.setData({ editorial: 'Editorial123' });
            wrapper.vm.validateEditorial();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.editorialValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets valid editorial for an editorial with only alphabetic characters and displays correct icon', async () => {
            wrapper.setData({ editorial: 'Editorial' });
            wrapper.vm.validateEditorial();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.editorialValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });

          it('sets invalid year for a year before 1000 and displays incorrect icon', async () => {
            wrapper.setData({ year: 999 });
            wrapper.vm.validateYear();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.yearValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets invalid year for a year after the current year and displays incorrect icon', async () => {
            const futureYear = new Date().getFullYear() + 1;
            wrapper.setData({ year: futureYear });
            wrapper.vm.validateYear();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.yearValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets valid year for a valid year between 1000 and the current year and displays correct icon', async () => {
            const validYear = 2020;
            wrapper.setData({ year: validYear });
            wrapper.vm.validateYear();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.yearValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });
          
          it('sets invalid ISBN for an ISBN with less than 10 digits and displays incorrect icon', async () => {
            wrapper.setData({ isbn: '123456789' });
            wrapper.vm.validateISBN();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.isbnValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets invalid ISBN for an ISBN with more than 13 digits and displays incorrect icon', async () => {
            wrapper.setData({ isbn: '123456789012345' });
            wrapper.vm.validateISBN();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.isbnValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets valid ISBN for an ISBN with 10 digits and displays correct icon', async () => {
            wrapper.setData({ isbn: '1234567890' });
            wrapper.vm.validateISBN();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.isbnValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });
          
          it('sets valid ISBN for an ISBN with 13 digits and displays correct icon', async () => {
            wrapper.setData({ isbn: '1234567890123' });
            wrapper.vm.validateISBN();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.isbnValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });

          it('sets invalid price for a negative price and displays incorrect icon', async () => {
            wrapper.setData({ price: -10 });
            wrapper.vm.validatePrice();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.priceValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets invalid price for a non-numeric price and displays incorrect icon', async () => {
            wrapper.setData({ price: 'abc' });
            wrapper.vm.validatePrice();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.priceValid).toBe(false);
            const errorIcon = wrapper.find('img[alt="Invalid"]');
            expect(errorIcon.exists()).toBe(true);
          });
          
          it('sets valid price for a valid positive numeric price and displays correct icon', async () => {
            wrapper.setData({ price: 20 });
            wrapper.vm.validatePrice();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.priceValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });

          it('sets invalid genre selection when no genres are selected and displays an error message', async () => {
            wrapper.setData({ selectedGenres: [] });
            wrapper.vm.validateGenreSelection();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.errorGenre).toBe('Please select at least one genre.');
          });
          
          it('sets invalid genre selection when more than 2 genres are selected and displays an error message', async () => {
            wrapper.setData({ selectedGenres: ['Fiction', 'Non-fiction', 'Science'] });
            wrapper.vm.validateGenreSelection();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.errorGenre).toBe('You can select up to two genres.');
          });
          
          it('sets valid genre selection when 1 or 2 genres are selected and clears the error message', async () => {
            wrapper.setData({ selectedGenres: ['Fiction', 'Non-fiction'] });
            wrapper.vm.validateGenreSelection();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.errorGenre).toBe('');
          });

          it('sets invalid synopsis when the synopsis is empty and displays incorrect icon', async () => {
            wrapper.setData({ synopsis: '' });
            wrapper.vm.validateSynopsis();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.synopsisValid).toBe(false);
          });
          
          it('sets valid synopsis when the synopsis has content and displays correct icon', async () => {
            wrapper.setData({ synopsis: 'A compelling story about a hero.' });
            wrapper.vm.validateSynopsis();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.synopsisValid).toBe(true);
            const successIcon = wrapper.find('img[alt="Valid"]');
            expect(successIcon.exists()).toBe(true);
          });

          it('should add a new link when there are less than 3 links', async () => {
            wrapper.setData({ publisherLinks: ['http://link1.com'] });
            wrapper.vm.addLink();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.publisherLinks.length).toBe(2);
          });
          
          it('should not add a new link when there are 3 or more links', async () => {
            wrapper.setData({ publisherLinks: ['http://link1.com', 'http://link2.com', 'http://link3.com'] });
            wrapper.vm.addLink();
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.publisherLinks.length).toBe(3);
          });

          it('should remove a link when there are more than one link', async () => {
            wrapper.setData({ publisherLinks: ['http://link1.com', 'http://link2.com'] });
            wrapper.vm.removeLink(0);
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.publisherLinks.length).toBe(1);
            expect(wrapper.vm.publisherLinks).not.toContain('http://link1.com');
          });
          
          it('should not remove the last link and clear the list when only one link remains', async () => {
            wrapper.setData({ publisherLinks: ['http://link1.com'] });
            wrapper.vm.removeLink(0);
            await wrapper.vm.$nextTick();
            expect(wrapper.vm.publisherLinks.length).toBe(0);
          });

          it('should display an error message if no links are added', async () => {
            wrapper.setData({ publisherLinks: [] });
            await wrapper.vm.$nextTick();
            const errorMessage = wrapper.find('.error-message');
            expect(errorMessage.exists()).toBe(true);
            expect(errorMessage.text()).toBe('You can add up to 3 links.');
          });
          
          
          it('should set image and preview for valid JPEG file', async () => {
          
            const mockFile = new File(['dummy content'], 'test.jpg', { type: 'image/jpeg' });
            
            const event = { target: { files: [mockFile] } };
            await wrapper.vm.handleImageUpload(event);
            
            expect(global.URL.createObjectURL).toHaveBeenCalledWith(mockFile);

            expect(wrapper.vm.image).toBe(mockFile);
            expect(wrapper.vm.imageError).toBe('');
            expect(wrapper.vm.imagePreview).toBe(URL.createObjectURL(mockFile));
          });


          it('should set an error for invalid file type', async () => {
            const mockFile = new File(['dummy content'], 'test.png', { type: 'image/png' });
            
            const event = { target: { files: [mockFile] } };
            await wrapper.vm.handleImageUpload(event);
        
            expect(wrapper.vm.image).toBeNull();
            expect(wrapper.vm.imagePreview).toBeNull();
            expect(wrapper.vm.imageError).toBe('Only JPEG images are allowed.');
          });

          it('should convert an image to Base64', async () => {
            const mockFile = new File(['dummy content'], 'test.jpg', { type: 'image/jpeg' });
        
            const result = await wrapper.vm.convertImageToBase64(mockFile);
        
            expect(result).toContain('data:image/jpeg;base64');
          });


          it('canSubmit should be true if all fields are filled', async () => {
            
            wrapper.setData({titleValid: true});
            wrapper.setData({authorValid : true});
            wrapper.setData({editorialValid : true});
            wrapper.setData({yearValid : true});
            wrapper.setData({isbnValid : true});
            wrapper.setData({priceValid: true});
            wrapper.setData({synopsisValid: true});
            wrapper.setData({ selectedGenres: ['Fiction', 'Non-fiction'] });
            wrapper.setData({ image: new File(['dummy content'], 'test.jpg', { type: 'image/jpeg' }) });
            expect(wrapper.vm.canSubmit).toBe(true);
          });


          it('canSubmit is false when a field is missing', async () => {
            // Completamos todos los campos requeridos
            wrapper.setData({titleValid: true});
            wrapper.setData({authorValid : true});
            wrapper.setData({editorialValid : true});
            wrapper.setData({yearValid : false});
            wrapper.setData({isbnValid : true});
            wrapper.setData({priceValid: true});
            wrapper.setData({synopsisValid: true});
            wrapper.setData({ selectedGenres: ['Fiction', 'Non-fiction'] });
            wrapper.setData({ image: new File(['dummy content'], 'test.jpg', { type: 'image/jpeg' }) });
            expect(wrapper.vm.canSubmit).toBe(false);
          });
});
