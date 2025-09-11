// static/js/script.js

window.addEventListener('DOMContentLoaded', () => {
  console.log('アクセスOK');
  const h1 = document.querySelector('h1');
  if (h1) {
    h1.classList.add('red-text');
  }
});