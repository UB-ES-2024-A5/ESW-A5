import { mount } from '@vue/test-utils';
import HelloWorld from '../components/HelloWorld.vue'; // ajusta el path si es necesario

describe('HelloWorld.vue', () => {
  it('muestra el mensaje de bienvenida', () => {
    const wrapper = mount(HelloWorld);
    const msg = wrapper.find('h1').text();
    expect(msg).toBe('Welcome to Your Vue.js App');
  });
});