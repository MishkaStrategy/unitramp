(() => {
  const qs = (s, ctx=document) => ctx.querySelector(s);
  const qsa = (s, ctx=document) => [...ctx.querySelectorAll(s)];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const progress = qs('#scrollProgress');
  const header = qs('.site-header');
  const onScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (progress) progress.style.width = `${max > 0 ? (scrollY/max)*100 : 0}%`;
    header?.classList.toggle('is-compact', scrollY > 80);
  };
  addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  const revealItems = qsa('.reveal');
  if (reduced) revealItems.forEach(el => el.classList.add('is-visible'));
  else revealItems.forEach((el, i) => setTimeout(() => el.classList.add('is-visible'), 120 + i*120));

  const menuBtn = qs('.menu-button');
  const mobileNav = qs('.mobile-nav');
  const toggleMenu = (force) => {
    const open = force ?? !mobileNav.classList.contains('is-open');
    mobileNav.classList.toggle('is-open', open);
    header.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    mobileNav.setAttribute('aria-hidden', String(!open));
    document.body.style.overflow = open ? 'hidden' : '';
  };
  menuBtn?.addEventListener('click', () => toggleMenu());
  qsa('a', mobileNav).forEach(a => a.addEventListener('click', () => toggleMenu(false)));

  const stage = qs('.transform-stage');
  qsa('.stage-step').forEach(btn => btn.addEventListener('click', () => {
    const n = btn.dataset.stageStep;
    stage.dataset.stage = n;
    qsa('.stage-step').forEach(b => b.classList.toggle('is-active', b === btn));
  }));

  const solutionData = {
    activity: {no:'01',title:'ACTIVITY\nPARK',eyebrow:'FORMAT / 01',name:'Семейный активити-парк',copy:'Комбинирует несколько игровых и спортивных сценариев в одном объекте: батутные зоны, ниндзя, лабиринты, интерактив и дополнительные активности.',scenario:'семейный досуг / ТРЦ / отдельное помещение',components:'подбираются под площадь и концепцию',project:'3D → производство → монтаж',href:'https://unitramp.ru/aktiviti-park-pod-klyuch'},
    trampoline: {no:'02',title:'TRAMPOLINE\nCENTER',eyebrow:'FORMAT / 02',name:'Батутный центр',copy:'Батутная зона как самостоятельный центр или часть более крупного развлекательного пространства — с проектированием под конкретную геометрию помещения.',scenario:'спорт / семейный досуг / активити-центр',components:'батутные поля, спортивные и игровые зоны',project:'проект → производство → монтаж',href:'https://unitramp.ru/batutnyj-centr-pod-klyuch'},
    ninja: {no:'03',title:'NINJA\nPARK',eyebrow:'FORMAT / 03',name:'Ниндзя-парк',copy:'Полоса препятствий с заданиями разной сложности — от самостоятельной зоны до большого OCR-пространства для тренировок и развлечений.',scenario:'OCR / спорт / семейный активити',components:'каркасы, препятствия, соревновательные элементы',project:'3D → инженерия → производство',href:'https://unitramp.ru/nindzya-park-pod-klyuch'},
    kids: {no:'04',title:'KIDS\nPLAY',eyebrow:'FORMAT / 04',name:'Игровой комплекс',copy:'Многоуровневые игровые комплексы и лабиринты для детских центров, семейных пространств, ТРЦ и других коммерческих объектов.',scenario:'детский центр / семейная зона / ТРЦ',components:'лабиринты, горки, сухие бассейны, тематические элементы',project:'индивидуальная компоновка под помещение',href:'https://unitramp.ru/katalog/igrovye-kompleksy/'},
    touch: {no:'05',title:'TOUCH\nARENA',eyebrow:'FORMAT / 05',name:'Touch Arena',copy:'Интерактивный формат, который можно интегрировать в развлекательное пространство как самостоятельную цифровую активность или часть общей концепции.',scenario:'интерактив / спорт / game-based activity',components:'цифровые игровые сценарии и физическая активность',project:'интеграция в общую концепцию объекта',href:'https://unitramp.ru/touch-arena-pod-klyuch'},
    climb: {no:'06',title:'CLIMBING\nWALL',eyebrow:'FORMAT / 06',name:'Скалодром',copy:'Скалодромы для детской, семейной и спортивной аудитории — с подбором конструкции, страховочных решений и компоновки под помещение.',scenario:'детский / спортивный / комбинированный формат',components:'скалодром, страховка, игровые и тренировочные трассы',project:'проектирование → производство → монтаж',href:'https://unitramp.ru/skalodromy-pod-klyuch'}
  };
  qsa('.solution-tab').forEach(btn => btn.addEventListener('click', () => {
    const d = solutionData[btn.dataset.solution];
    qsa('.solution-tab').forEach(b => b.classList.toggle('is-active', b === btn));
    const visual = qs('.explorer-visual');
    qs('.visual-number', visual).textContent = d.no;
    qs('.visual-title', visual).innerHTML = d.title.replace('\n','<br>');
    const copy = qs('.explorer-copy');
    qs('.eyebrow', copy).textContent = d.eyebrow;
    qs('h3', copy).textContent = d.name;
    qs('p', copy).textContent = d.copy;
    const dd = qsa('dd', copy); dd[0].textContent=d.scenario; dd[1].textContent=d.components; dd[2].textContent=d.project;
    qs('.text-link', copy).href=d.href;
  }));

  const selection = {space:'ТРЦ',area:'200–500 м²'};
  qsa('[data-builder]').forEach(group => qsa('.chip', group).forEach(btn => btn.addEventListener('click', () => {
    qsa('.chip', group).forEach(b => b.classList.toggle('is-active', b===btn));
    selection[group.dataset.builder] = btn.dataset.value;
    qs('#builderSummary').textContent = `${selection.space} / ${selection.area}`;
    const briefArea = qs('[name="area"]'); if (briefArea) briefArea.value = selection.area;
  })));

  const compare = qs('#compareRange');
  const built = qs('.compare-built');
  const handle = qs('.compare-handle');
  const setCompare = () => {
    if (!compare || !built || !handle) return;
    const v = compare.value;
    built.style.clipPath = `inset(0 0 0 ${v}%)`;
    handle.style.left = `${v}%`;
  };
  compare?.addEventListener('input', setCompare); setCompare();

  qsa('.filter').forEach(btn => btn.addEventListener('click', () => {
    const f = btn.dataset.filter;
    qsa('.filter').forEach(b => b.classList.toggle('is-active', b===btn));
    qsa('.case').forEach(card => {
      const categories = card.dataset.category.split(' ');
      card.classList.toggle('is-hidden', f !== 'all' && !categories.includes(f));
    });
  }));

  const counters = qsa('.count');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target; const target = Number(el.dataset.target); const start=performance.now(); const dur=1100;
      const tick = now => { const p=Math.min(1,(now-start)/dur); el.textContent=Math.round(target*(1-Math.pow(1-p,3))).toLocaleString('ru-RU'); if(p<1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick); io.unobserve(el);
    }), {threshold:.5}); counters.forEach(el=>io.observe(el));
  } else counters.forEach(el=>el.textContent=Number(el.dataset.target).toLocaleString('ru-RU'));

  const processTrack = qs('.process-track');
  if (processTrack && !reduced) {
    const scrollProcess = () => {
      const section = qs('.process');
      if (!section) return;
      const rect = section.getBoundingClientRect();
      const total = rect.height + innerHeight;
      const p = Math.max(0, Math.min(1, (innerHeight - rect.top) / total));
      const overflow = Math.max(0, processTrack.scrollWidth - innerWidth + 80);
      processTrack.style.transform = `translateX(${-overflow*p}px)`;
    };
    addEventListener('scroll', scrollProcess, {passive:true}); scrollProcess();
  }

  const form = qs('#leadForm');
  form?.addEventListener('submit', e => {
    e.preventDefault();
    const status=qs('#formStatus');
    if (!form.checkValidity()) { form.reportValidity(); status.textContent='Проверьте обязательные поля.'; return; }
    const data = Object.fromEntries(new FormData(form).entries());
    status.textContent='Запрос подготовлен. Открываю почтовое приложение…';
    const subject = encodeURIComponent(`Запрос проекта UnitRamp — ${data.city}, ${data.area}`);
    const body = encodeURIComponent([
      'Здравствуйте! Хочу обсудить проект развлекательного пространства.', '',
      `Город: ${data.city}`, `Площадь: ${data.area}`, `Тип объекта: ${data.type}`,
      `Задача: ${data.comment || '—'}`, '', `Имя: ${data.name}`, `Контакт: ${data.contact}`,
      '', 'Запрос сформирован через web-коммерческое предложение UnitRamp.'
    ].join('\n'));
    window.location.href=`mailto:info@unitramp.ru?subject=${subject}&body=${body}`;
    window.dispatchEvent(new CustomEvent('unitramp:lead_form_submit',{detail:data}));
  });

  qsa('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{
    if (a.getAttribute('href')==='#') return;
    window.dispatchEvent(new CustomEvent('unitramp:anchor_click',{detail:{href:a.getAttribute('href')}}));
  }));
})();
