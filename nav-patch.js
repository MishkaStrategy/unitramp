document.addEventListener('DOMContentLoaded',()=>{
  const routeFrom=(anchor,segment)=>{
    if(!anchor)return segment;
    return anchor.href.replace(/contacts\/?(?:#.*)?$/,'')+segment.replace(/^\//,'');
  };
  const desktop=document.querySelector('.desktop-nav');
  const contacts=desktop?.querySelector('a[href*="contacts"]');
  if(desktop&&contacts&&!desktop.querySelector('[data-nav-extra="services"]')){
    const items=[['services/','Услуги','services'],['franchises/','Франшизы','franchises'],['reviews/','Отзывы','reviews']];
    items.forEach(([path,label,key])=>{const a=document.createElement('a');a.className='nav-link';a.dataset.navExtra=key;a.href=routeFrom(contacts,path);a.textContent=label;desktop.insertBefore(a,contacts);});
  }
  const mobile=document.querySelector('.mobile-menu');
  const mobileContacts=mobile?.querySelector('a[href*="contacts"]');
  if(mobile&&mobileContacts&&!mobile.querySelector('[data-nav-extra="services"]')){
    [['services/','Услуги','services'],['franchises/','Франшизы','franchises'],['reviews/','Отзывы','reviews']].forEach(([path,label,key])=>{const a=document.createElement('a');a.dataset.navExtra=key;a.href=routeFrom(mobileContacts,path);a.textContent=label;mobile.insertBefore(a,mobileContacts);});
  }
  document.querySelectorAll('a[href="https://unitramp.ru/privacy-policy/"]').forEach(a=>a.href='https://unitramp.ru/privacy-policy');
});
