from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")
MARK = "<!-- UI_ENHANCE_V3 -->"
if MARK in s:
    raise SystemExit(0)

css = r'''

		/* UI_ENHANCE_V3 */
		:root{--mx:50vw;--my:20vh}
		body::before,body::after{content:"";position:fixed;z-index:-2;width:38vw;height:38vw;border-radius:50%;filter:blur(90px);opacity:.16;pointer-events:none;will-change:transform}
		body::before{left:-13vw;top:8vh;background:radial-gradient(circle,rgba(98,113,255,.9),transparent 68%);animation:ambientA 14s ease-in-out infinite alternate}
		body::after{right:-12vw;top:38vh;background:radial-gradient(circle,rgba(56,214,173,.72),transparent 68%);animation:ambientB 18s ease-in-out infinite alternate}
		.pointer-glow{position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(520px circle at var(--mx) var(--my),rgba(113,126,255,.075),transparent 65%)}
		.page-progress{position:fixed;left:0;top:0;z-index:1000;height:2px;width:100%;transform:scaleX(0);transform-origin:0 50%;background:linear-gradient(90deg,#8793ff,#8ce9cd);box-shadow:0 0 18px rgba(124,140,255,.55)}
		.nav{box-shadow:0 12px 42px rgba(0,0,0,.12)}
		.nav-links a{position:relative;display:inline-flex;align-items:center;gap:6px}
		.nav-links a::after{content:"";position:absolute;left:50%;bottom:-7px;width:0;height:1px;background:linear-gradient(90deg,#8390ff,#8ce9cd);transform:translateX(-50%);transition:width .24s ease}
		.nav-links a:hover::after{width:100%}
		.svg-icon{width:1.05em;height:1.05em;flex:0 0 auto;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;fill:none}
		.svg-icon.fill{fill:currentColor;stroke:none}
		.hero-logo-wrap{animation:logoFloat 5s ease-in-out infinite}
		.hero-logo-wrap::before{animation:logoPulse 4.8s ease-in-out infinite}
		.gradient-text{background-size:180% 180%;animation:gradientFlow 8s ease-in-out infinite}
		.btn{position:relative;overflow:hidden}
		.btn::before{content:"";position:absolute;inset:-2px;background:linear-gradient(110deg,transparent 20%,rgba(255,255,255,.18) 45%,transparent 70%);transform:translateX(-130%);transition:transform .55s ease;pointer-events:none}
		.btn:hover::before{transform:translateX(130%)}
		.feature,.arch-card,.latest-item,.notice-card,.community-group,.download-item,.gallery-item{transition:transform .28s cubic-bezier(.2,.8,.2,1),border-color .28s ease,background .28s ease,box-shadow .28s ease;will-change:transform}
		.feature:hover,.arch-card:hover,.latest-item:hover,.notice-card:hover,.community-group:hover{transform:translateY(-5px);border-color:rgba(132,146,255,.22);box-shadow:0 18px 52px rgba(0,0,0,.22),0 0 0 1px rgba(132,146,255,.035) inset}
		.download-item:hover{transform:translateY(-4px) scale(1.004);box-shadow:0 16px 42px rgba(0,0,0,.22)}
		.feature-icon,.download-icon,.community-logo{overflow:hidden}
		.feature-icon .svg-icon,.download-icon .svg-icon,.community-logo .svg-icon{width:22px;height:22px;transition:transform .26s ease}
		.feature:hover .feature-icon .svg-icon,.download-item:hover .download-icon .svg-icon,.community-group:hover .community-logo .svg-icon{transform:scale(1.13) rotate(-4deg)}
		.reveal-on-scroll{opacity:0;transform:translateY(24px) scale(.99);filter:blur(8px);transition:opacity .7s cubic-bezier(.2,.8,.2,1),transform .7s cubic-bezier(.2,.8,.2,1),filter .7s ease}
		.reveal-on-scroll.is-visible{opacity:1;transform:none;filter:blur(0)}
		.tilt-card{transform-style:preserve-3d;transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(var(--ty,0px))}
		.gallery-item::after{content:"";position:absolute;inset:0;background:radial-gradient(500px circle at var(--gx,50%) var(--gy,50%),rgba(255,255,255,.10),transparent 45%);opacity:0;transition:opacity .3s ease;pointer-events:none}
		.gallery-item:hover::after{opacity:1}
		.section-label{display:inline-flex;align-items:center;gap:7px}
		.section-label::before{content:"";width:18px;height:1px;background:linear-gradient(90deg,transparent,#8692ff)}
		@keyframes ambientA{from{transform:translate3d(0,0,0) scale(1)}to{transform:translate3d(10vw,8vh,0) scale(1.14)}}
		@keyframes ambientB{from{transform:translate3d(0,0,0) scale(1.08)}to{transform:translate3d(-8vw,-8vh,0) scale(.92)}}
		@keyframes logoFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
		@keyframes logoPulse{0%,100%{transform:scale(.94);opacity:.72}50%{transform:scale(1.08);opacity:1}}
		@keyframes gradientFlow{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
		@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}.reveal-on-scroll{opacity:1;transform:none;filter:none}.pointer-glow{display:none}}
'''

js = r'''
	<!-- UI_ENHANCE_V3 -->
	<script>
	(()=>{
	const I={
	download:'<path d="M12 3v12m0 0 4-4m-4 4-4-4"/><path d="M5 19h14"/>',play:'<circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z"/>',message:'<path d="M21 15a4 4 0 0 1-4 4H8l-5 3 1.6-4.8A7 7 0 0 1 3 12c0-4.4 4-8 9-8s9 3.6 9 8v3Z"/>',cloud:'<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.2 8.2 4.5 4.5 0 0 0 7 18Z"/><path d="M12 10v5m0 0 2-2m-2 2-2-2"/>',route:'<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h3a3 3 0 0 0 3-3V9a3 3 0 0 1 3-3"/>',spark:'<path d="m12 3 1.3 3.7L17 8l-3.7 1.3L12 13l-1.3-3.7L7 8l3.7-1.3L12 3Z"/>',image:'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8.5" cy="10" r="1.5"/><path d="m21 15-5-5L5 19"/>',rocket:'<path d="M14 4c3-2 6-1 6-1s1 3-1 6l-5 5-4-4 4-6Z"/><path d="m10 10-5 2-2 3 6-1M14 14l-2 5 3 2 1-6"/><circle cx="16" cy="7" r="1"/>',history:'<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/>',users:'<circle cx="9" cy="8" r="3"/><path d="M3 19c0-3.2 2.7-5 6-5s6 1.8 6 5"/><path d="M16 5.3a3 3 0 0 1 0 5.4M17 14c2.4.5 4 2 4 5"/>',browser:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 8h18M7 6h.01M10 6h.01"/>',check:'<circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/>',refresh:'<path d="M20 6v5h-5"/><path d="M19 11a7 7 0 1 0-1 5"/>',search:'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',bookmark:'<path d="M6 4h12v17l-6-4-6 4V4Z"/>',trash:'<path d="M4 7h16M9 7V4h6v3M7 7l1 14h8l1-14"/>',hash:'<path d="M10 3 8 21M16 3l-2 18M4 9h16M3 15h16"/>',shield:'<path d="M12 3 5 6v5c0 4.8 2.9 8.2 7 10 4.1-1.8 7-5.2 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',bolt:'<path d="m13 2-8 12h7l-1 8 8-12h-7l1-8Z"/>',github:'<path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.87c-2.78.6-3.37-1.18-3.37-1.18-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.64-1.34-2.22-.25-4.56-1.11-4.56-4.95 0-1.09.39-1.99 1.03-2.69-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.03A9.6 9.6 0 0 1 12 6.8a9.6 9.6 0 0 1 2.5.34c1.91-1.3 2.75-1.03 2.75-1.03.55 1.38.2 2.4.1 2.65.64.7 1.6 1.6 1.6 2.69 0 3.85-2.91 4.7-5.14 4.95.36.31.68.92.68 1.86v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/>',folder:'<path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z"/>',send:'<path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M22 2 11 13"/>',chat:'<path d="M4 5h16v11H9l-5 4V5Z"/><path d="M8 10h.01M12 10h.01M16 10h.01"/>'};
	const S=n=>`<svg class="svg-icon${n==='github'?' fill':''}" viewBox="0 0 24 24" aria-hidden="true">${I[n]||I.spark}</svg>`;
	const p=document.createElement('div');p.className='page-progress';document.body.prepend(p);const g=document.createElement('div');g.className='pointer-glow';document.body.prepend(g);
	const nav=[['#download','download'],['#video','play'],['bbs.gbtgame.me','message'],['pan.gbtgame.me','cloud'],['#architecture','route'],['#features','spark'],['#screenshots','image'],['#usage','rocket'],['#versions','history'],['#community','users']];
	document.querySelectorAll('.nav-links a').forEach(a=>{const h=a.getAttribute('href')||'',f=nav.find(x=>h.includes(x[0]));if(f&&!a.querySelector('svg'))a.insertAdjacentHTML('afterbegin',S(f[1]))});
	['download','spark','image','users','message','cloud'].forEach((n,i)=>{const b=document.querySelectorAll('.hero-actions .btn')[i];if(b&&!b.querySelector('svg'))b.insertAdjacentHTML('afterbegin',S(n))});
	['browser','check','refresh','search','bookmark','trash','hash','shield'].forEach((n,i)=>{const e=document.querySelectorAll('#features .feature-icon')[i];if(e)e.innerHTML=S(n)});
	document.querySelectorAll('#services .feature-icon').forEach((e,i)=>e.innerHTML=S(i?'folder':'message'));
	document.querySelectorAll('.download-icon').forEach(e=>{const t=e.textContent.trim().toLowerCase();e.innerHTML=S(t.includes('迅雷')?'bolt':t==='gh'?'github':'cloud')});
	document.querySelectorAll('.community-logo').forEach(e=>{const t=e.textContent.trim().toLowerCase();e.innerHTML=S(t==='tg'?'send':t==='qq'?'message':'chat')});
	document.querySelectorAll('.download-action').forEach(e=>{if(!e.querySelector('svg'))e.insertAdjacentHTML('beforeend',S('download'))});
	const rs=document.querySelectorAll('.section-head,.download-box,.arch-card,.feature,.latest-box,.latest-item,.gallery-item,.step,.release,.notice-card,.opensource,.community-group');rs.forEach((e,i)=>{e.classList.add('reveal-on-scroll');e.style.transitionDelay=`${Math.min(i%5*55,220)}ms`});
	if('IntersectionObserver'in window){const o=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('is-visible');o.unobserve(x.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});rs.forEach(e=>o.observe(e))}else rs.forEach(e=>e.classList.add('is-visible'));
	const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches,fine=matchMedia('(pointer:fine)').matches;if(!reduced&&fine){addEventListener('pointermove',e=>{document.documentElement.style.setProperty('--mx',e.clientX+'px');document.documentElement.style.setProperty('--my',e.clientY+'px')},{passive:true});document.querySelectorAll('.arch-card,.feature,.latest-item,.notice-card,.community-group').forEach(c=>{c.classList.add('tilt-card');c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',x*5+'deg');c.style.setProperty('--rx',-y*4+'deg');c.style.setProperty('--ty','-4px')});c.addEventListener('pointerleave',()=>{c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg');c.style.setProperty('--ty','0px')})});document.querySelectorAll('.gallery-item').forEach(x=>x.addEventListener('pointermove',e=>{const r=x.getBoundingClientRect();x.style.setProperty('--gx',e.clientX-r.left+'px');x.style.setProperty('--gy',e.clientY-r.top+'px')}))}
	const U=()=>{const m=document.documentElement.scrollHeight-innerHeight,v=m>0?Math.min(scrollY/m,1):0;p.style.transform=`scaleX(${v})`};U();addEventListener('scroll',U,{passive:true});addEventListener('resize',U,{passive:true});
	})();
	</script>
'''

s = s.replace("</style>", css + "\n\t</style>", 1)
s = s.replace("</body>", js + "\n</body>", 1)
p.write_text(s, encoding="utf-8")
