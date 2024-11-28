import { mount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import MainPageUser from '../../components/MainPageUser.vue'; // Asegúrate de importar el componente correcto
import Login from '../../components/login.vue';
import Swal from 'sweetalert2';

const localVue = createLocalVue();
localVue.use(VueRouter);

describe('MainPageUser redirection when no token', () => {
  let router;
  let wrapper;

  beforeEach(() => {
    const routes = [
      { path: '/login', component: Login },
      { path: '/mainPage_user', component: MainPageUser },
    ];

    router = new VueRouter({
      mode: 'history',
      routes,
    });

    wrapper = mount(MainPageUser, {
      localVue,
      router,
    });
  });

  it('should redirect to login if no token is found', async () => {
    localStorage.removeItem('access_token'); 

    await router.push('/mainPage_user');
    await wrapper.vm.$nextTick(); 

    expect(router.currentRoute.path).toBe('/login');
  });

  
});
