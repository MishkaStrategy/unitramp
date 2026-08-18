document.addEventListener('DOMContentLoaded',()=>{
  if(!document.querySelector('style[data-unitramp-responsive-fix]')){
    const style=document.createElement('style');
    style.dataset.unitrampResponsiveFix='1';
    style.textContent='@media(max-width:1180px){.mega{display:none!important}}@media(max-width:820px){.hero-bottom>*,.section-head>*,.cta-grid>*,.contact-grid>*,.park-builder>*,.footer-grid>*,.toolbar>*,.project-index-grid>*,.solution-grid>*,.article-grid>*{min-width:0}.project-index-card,.solution-card,.article-card,.product-card{min-width:0;max-width:100%}.section-head h2,.page-hero h1,.turnkey-copy h1,.project-index-card h2,.solution-card h3,.article-card h2,.cta-grid h2{hyphens:auto;overflow-wrap:anywhere}.project-meta>*{min-width:0;overflow-wrap:anywhere}.product-actions{flex-wrap:wrap}.filter-chip{max-width:calc(100vw - 48px);white-space:normal;overflow-wrap:anywhere}}@media(max-width:520px){.hero h1{font-size:clamp(35px,11vw,50px)}.toolbar>*{max-width:100%;min-width:0}.btn{max-width:100%;white-space:normal;text-align:center}}';
    document.head.appendChild(style);
  }

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
