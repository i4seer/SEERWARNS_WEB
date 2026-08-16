const menuButton=document.querySelector('.menu-btn');
const nav=document.querySelector('.site-nav');
if(menuButton&&nav){menuButton.addEventListener('click',()=>{const open=nav.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));});document.addEventListener('click',e=>{if(!nav.contains(e.target)&&e.target!==menuButton&&nav.classList.contains('open')){nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');}})}
