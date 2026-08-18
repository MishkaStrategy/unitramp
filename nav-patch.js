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

  if(!document.querySelector('script[data-unitramp-schema]')){
    const organization={
      '@type':'Organization',
      '@id':'https://unitramp.ru/#organization',
      name:'UnitRamp',
      legalName:'ООО «ЮНИТРАМП»',
      url:'https://unitramp.ru/',
      email:'info@unitramp.ru',
      telephone:'+78007007809',
      taxID:'5404505599',
      address:{'@type':'PostalAddress',addressLocality:'Новосибирск',streetAddress:'ул. Фабричная, 4, офис 411',addressCountry:'RU'}
    };
    const graph=[organization];
    if(document.body.dataset.page==='home') graph.push({'@type':'WebSite','@id':'https://unitramp.ru/#website',url:'https://unitramp.ru/',name:'UnitRamp',publisher:{'@id':'https://unitramp.ru/#organization'}});
    if(document.body.dataset.page==='turnkey'){
      const name=document.querySelector('h1')?.textContent?.trim();
      if(name) graph.push({'@type':'Service',name,provider:{'@id':'https://unitramp.ru/#organization'},areaServed:'RU',url:document.querySelector('link[rel="canonical"]')?.href||'https://unitramp.ru/'});
    }
    const script=document.createElement('script');
    script.type='application/ld+json';
    script.dataset.unitrampSchema='1';
    script.textContent=JSON.stringify({'@context':'https://schema.org','@graph':graph});
    document.head.appendChild(script);
  }
});
