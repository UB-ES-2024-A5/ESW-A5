import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import WelcomePage from '../../components/WelcomePage.vue';
import MainPageGuest from '../../components/MainPageGuest.vue';

describe('Navigation from Welcome Page to MainPageGuest', () => {
  let router;
  const localVue = createLocalVue();
  localVue.use(VueRouter);

  beforeEach(() => {
    // Configuración de las rutas para Vue 2
    const routes = [
      { path: '/', component: WelcomePage },
      { path: '/guest', component: MainPageGuest },
    ];

    router = new VueRouter({
      mode: 'history',
      routes,
    });
  });

  it('should navigate from Welcome Page to MainPageGuest on Guest Access click', async () => {
    const wrapper = mount(WelcomePage, {
      localVue,
      router,
    });

    await wrapper.vm.$nextTick();

    const button = wrapper.find('.sign-up-btn[href="/mainpage_guest"]');
    expect(button.exists()).toBe(true);


    await button.trigger('click');
    await wrapper.vm.$nextTick();

    expect(router.currentRoute.path).toBe('/mainpage_guest');
  });
});
