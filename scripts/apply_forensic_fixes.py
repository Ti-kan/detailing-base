import re

with open("/Users/takanov/detailing-base/scripts/build_landing.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add split_words helper in python
if "def split_words(" not in code:
    code = code.replace(
        "def fmt_rub(n):",
        """def split_words(text):
    words = text.split()
    return " ".join(f'<span class="w-mask"><span class="w-in" style="--wi:{i}">{w}</span></span>' for i, w in enumerate(words))

def fmt_rub(n):"""
    )

# 2. Update .hero-word and .frame geometry rules
# Replace old .hero-word & .frame CSS
old_hero_frame_css = r"""\.hero-word\{[^\}]+\}
\.hero-word span\{[^\}]+\}
\.hero\.revealed \.hero-word span, \.hero\.on \.hero-word span\{[^\}]+\}

\.frame\{[^\}]+\}"""

new_hero_frame_css = """.hero-word{{font:700 17.2cqi/0.92 var(--display);text-transform:uppercase;letter-spacing:-.01em;margin:4px 0 6px;padding-bottom:4px;white-space:nowrap;user-select:none;display:flex;justify-content:space-between;color:rgba(255,255,255,0.92);transform:translate3d(0,calc(var(--scroll-y, 0) * 0.18px),0);will-change:transform}}
.hero-word span{{display:inline-block;opacity:0;transform:translateY(36%);transition:transform .85s cubic-bezier(.16,1,.3,1),opacity .6s ease;will-change:transform,opacity}}
.hero.revealed .hero-word span, .hero.on .hero-word span, .hero-entered .hero-word span{{opacity:1;transform:translateY(0);transition-delay:calc(var(--i) * 45ms + 40ms)}}

.frame{{position:relative;z-index:2;margin-top:8px !important;aspect-ratio:10/7.2;border-radius:var(--r);overflow:hidden;background:#000;box-shadow:0 24px 60px -20px rgba(0,0,0,.65);border:1px solid var(--night-line);transform-origin:center center}}
.frame.is-fullscreen-portal{{position:relative;border-radius:0px !important;z-index:999 !important;box-shadow:0 0 100px rgba(0,0,0,0.9)}}
.frame.is-fullscreen-portal .cinema-skip{{opacity:1;pointer-events:auto}}
.frame:not(.is-fullscreen-portal) .cinema-skip{{opacity:0;pointer-events:none}}
.frame.is-docked .replay-btn{{opacity:1;pointer-events:auto}}"""

code = re.sub(old_hero_frame_css, new_hero_frame_css, code)

# Update media query .frame rule for >= 1024px
code = re.sub(
    r'\.frame\{\{margin-top:-2\.8cqi;aspect-ratio:10/7\.2\}\}',
    r'.frame{{margin-top:8px !important;aspect-ratio:10/7.2}}',
    code
)

# 3. Update optical loupe and HUD CSS (removing multi-pill spam, clean 210px circle)
old_loupe_css = r"""/\* INTERACTIVE CURSOR CLEAN CAR INSPECTION \*/[\s\S]+?\.replay-btn svg\{\{width:15px;height:15px\}\}"""
new_loupe_css = """/* OPTICAL DETAILING LOUPE (ZONE-AWARE HUD) */
.car-loupe{{position:absolute;top:var(--ly, 50%);left:var(--lx, 50%);width:210px;height:210px;transform:translate3d(-50%,-50%,0);pointer-events:none;z-index:6;opacity:0;transition:opacity .25s ease}}
.frame.is-inspecting .car-loupe{{opacity:1}}
.loupe-ring{{position:absolute;inset:0;border-radius:50%;border:1.5px solid rgba(255,107,53,0.9);box-shadow:0 0 24px rgba(223,78,22,0.5),inset 0 0 20px rgba(200,164,100,0.25);-webkit-backdrop-filter:brightness(1.32) contrast(1.16) saturate(1.22);backdrop-filter:brightness(1.32) contrast(1.16) saturate(1.22);overflow:hidden}}
.loupe-hud{{position:absolute;top:-30px;left:50%;transform:translateX(-50%);background:rgba(11,12,14,0.94);border:1px solid rgba(255,107,53,0.85);box-shadow:0 4px 16px rgba(0,0,0,0.6);color:#FAF9F6;font:700 12px/1 var(--sans);letter-spacing:.06em;padding:5px 12px;border-radius:999px;white-space:nowrap}}
.loupe-cross-v{{position:absolute;top:12px;bottom:12px;left:50%;width:1px;background:rgba(255,107,53,0.4);transform:translateX(-50%)}}
.loupe-cross-h{{position:absolute;left:12px;right:12px;top:50%;height:1px;background:rgba(255,107,53,0.4);transform:translateY(-50%)}}
.loupe-dot{{position:absolute;top:50%;left:50%;width:6px;height:6px;border-radius:50%;background:#FF6B35;box-shadow:0 0 10px #FF6B35;transform:translate(-50%,-50%)}}
.loupe-flare{{position:absolute;width:120px;height:120px;top:15px;left:15px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.35) 0%,rgba(200,164,100,0.1) 40%,transparent 70%);pointer-events:none}}

.inspect-hint{{position:absolute;bottom:74px;left:14px;z-index:7;background:rgba(11,12,14,.82);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.14);color:#FAF9F6;font:500 12px/1 var(--sans);padding:6px 12px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;pointer-events:none;transition:opacity .35s ease,transform .35s ease}}
.inspect-hint.hide{{opacity:0;transform:translateY(8px)}}

.replay-btn{{position:absolute;top:14px;right:14px;z-index:9;display:inline-flex;align-items:center;gap:6px;min-height:48px;min-width:48px;padding:0 16px;border-radius:999px;background:rgba(11,12,14,.8);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.16);color:#FAF9F6;font:600 13px/1 var(--sans);cursor:pointer;transition:all .2s;opacity:0;pointer-events:none}}
.frame.is-docked .replay-btn{{opacity:1;pointer-events:auto}}
.replay-btn:hover{{background:rgba(223,78,22,.25);border-color:var(--accent);color:#fff;transform:scale(1.03)}}
.replay-btn svg{{width:15px;height:15px}}"""

code = re.sub(old_loupe_css, new_loupe_css, code)

# 4. Update .w-mask and .w-in CSS
old_w_css = r"""\.w-mask\{[^\}]+\}\n\.w-in\{[^\}]+\}\n\.reveal-in[^\}]+\}"""
new_w_css = """.w-mask{{display:inline-block;overflow:hidden;vertical-align:bottom;line-height:1.14;padding-top:0.16em;margin-top:-0.16em;padding-bottom:0.06em}}
.w-in{{display:inline-block;transform:translate3d(0,110%,0) rotate(3deg);opacity:0;transition:transform 0.75s cubic-bezier(0.16,1,0.3,1),opacity 0.55s ease;transition-delay:calc(var(--wi, 0) * 32ms);will-change:transform,opacity}}
.in .w-in, .hero-entered .hero-info .w-in, .revealed .hero-info .w-in, .hero.on .hero-info .w-in{{transform:translate3d(0,0,0) rotate(0deg);opacity:1}}"""

code = re.sub(old_w_css, new_w_css, code)

# 5. Staggered card transitions CSS
if ".reveal-card" not in code:
    code = code.replace(
        "/* 01. SLOTS (Tear-Off Tickets) */",
        """/* STAGGERED REVEAL CARDS */
.slots > li, .pk-card, .tech-item{{transition:opacity 0.7s cubic-bezier(0.16,1,0.3,1),transform 0.7s cubic-bezier(0.16,1,0.3,1);transition-delay:calc(var(--ci, 0) * 70ms);will-change:transform,opacity}}
body:not(.no-js) .slots > li:not(.in),
body:not(.no-js) .pk-card:not(.in),
body:not(.no-js) .tech-item:not(.in){{opacity:0.25;transform:translate3d(0,24px,0) scale(0.98)}}
body:not(.no-js) .slots > li.in,
body:not(.no-js) .pk-card.in,
body:not(.no-js) .tech-item.in{{opacity:1;transform:translate3d(0,0,0) scale(1)}}

/* 01. SLOTS (Tear-Off Tickets) */"""
    )

# 6. Update 2-row Marquee keyframe names and CSS (32s and 36s)
old_marquee_css = r"""/\* 06\. REVIEWS \(2-ROW INFINITE KINETIC MARQUEE\) \*/[\s\S]+?\.rev-badge\{[^\}]+\}"""
new_marquee_css = """/* 06. REVIEWS (2-ROW OPPOSING KINETIC MARQUEE) */
.rev-marquee-wrap{{position:relative;overflow:hidden;user-select:none;padding:16px 0 24px;margin:0 calc(-1 * var(--gl));padding-left:var(--gl);padding-right:var(--gr);mask-image:linear-gradient(to right,transparent 0%,black 5%,black 95%,transparent 100%);-webkit-mask-image:linear-gradient(to right,transparent 0%,black 5%,black 95%,transparent 100%)}}
.rev-marquee-row{{display:flex;gap:18px;width:max-content;margin-bottom:18px;transform:skewX(var(--rev-skew, 0deg));transition:transform .15s ease-out;will-change:transform}}
.rev-row-left{{animation:marqueeLeft 32s linear infinite}}
.rev-row-right{{animation:marqueeRight 36s linear infinite}}
.rev-marquee-row:hover{{animation-play-state:paused}}
@keyframes marqueeLeft{{0%{{transform:translate3d(0,0,0) skewX(var(--rev-skew, 0deg))}}100%{{transform:translate3d(-50%,0,0) skewX(var(--rev-skew, 0deg))}}}}
@keyframes marqueeRight{{0%{{transform:translate3d(-50%,0,0) skewX(var(--rev-skew, 0deg))}}100%{{transform:translate3d(0,0,0) skewX(var(--rev-skew, 0deg))}}}}
.rev-card{{width:360px;max-width:82vw;flex:none;background:var(--night-2);border:1px solid var(--night-line);border-radius:18px;padding:22px;display:flex;flex-direction:column;box-shadow:0 8px 24px rgba(0,0,0,0.4);transition:transform .25s var(--ease),border-color .25s,box-shadow .25s}}
.rev-card:hover{{border-color:var(--accent);transform:translateY(-4px);box-shadow:0 16px 36px -10px rgba(223,78,22,.35)}}
.rev-head{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}}
.rev-author{{font-weight:700;font-size:15px;color:#FAF9F6}}
.rev-car{{font-size:13px;color:var(--champagne);margin-top:2px}}
.rev-stars{{color:var(--champagne);font-size:14px;letter-spacing:1px}}
.rev-text{{font-size:13.5px;line-height:1.5;color:#D1D5DB;margin-bottom:14px;flex:1}}
.rev-badge{{font-size:12px;font-weight:600;color:var(--accent-on-dark);margin-top:auto;padding-top:10px;border-top:1px dashed var(--night-line)}}"""

code = re.sub(old_marquee_css, new_marquee_css, code)

# 7. Update .frame HTML markup
old_stage_html = r"""<div class="stage">[\s\S]+?<!-- MARQUEE KINETIC TICKER -->"""
new_stage_html = """<div class="stage">
      <p class="hero-word" aria-hidden="true">
        <span style="--i:0">Д</span>
        <span style="--i:1">Е</span>
        <span style="--i:2">Т</span>
        <span style="--i:3">Е</span>
        <span style="--i:4">Й</span>
        <span style="--i:5">Л</span>
        <span style="--i:6">И</span>
        <span style="--i:7">Н</span>
        <span style="--i:8">Г</span>
      </p>

      <div class="frame" id="heroFrame">
        <img src="/img/hero-entry-final.jpg" alt="Детейлинг и бронепленка кузова автомобиля в Туле" width="800" height="576" fetchpriority="high">
        <video id="heroVideo" src="/img/hero-entry.mp4" playsinline muted preload="auto" poster="/img/hero-entry-final.jpg"></video>
        <div class="cinema-skip" id="cinemaSkip">Прокрутите вниз или подождите 2 сек ↓</div>

        <!-- Optical Detailing Loupe (ONE Single Sleek HUD Pill) -->
        <div class="car-loupe" id="carLoupe" aria-hidden="true">
          <div class="loupe-hud" id="loupeHud">КУЗОВ · ЗЕРКАЛЬНЫЙ ГЛЯНЕЦ 9H · ОСМОТР CRI 95+</div>
          <div class="loupe-ring">
            <div class="loupe-cross-v"></div>
            <div class="loupe-cross-h"></div>
            <div class="loupe-flare"></div>
            <div class="loupe-dot"></div>
          </div>
        </div>

        <button class="replay-btn" id="replayVideoBtn" type="button" aria-label="Повторить заезд">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
          <span>Повторить заезд</span>
        </button>

        <div class="inspect-hint" id="inspectHint">
          <span>🔦</span> Наведите курсор на авто для осмотра чистоты ЛКП
        </div>

        <div class="shade"></div>
        <canvas id="steam" width="400" height="288" aria-hidden="true"></canvas>

        <div class="cta">
          <button class="btn btn-accent" type="button" data-scroll-to="#pick">Подобрать защиту</button>
          <p>Рассчитайте точную смету за 20 секунд без звонка</p>
        </div>
      </div>
    </div>

    <div class="hero-info">
      <h1 id="h1">
        <span class="w-mask"><span class="w-in" style="--wi:0">Бронеплёнка,</span></span>
        <span class="w-mask"><span class="w-in" style="--wi:1">полировка</span></span>
        <span class="w-mask"><span class="w-in" style="--wi:2">и керамика</span></span>
        <span class="w-mask"><span class="w-in" style="--wi:3">с гарантией</span></span>
        <span class="w-mask"><span class="w-in" style="--wi:4">по договору</span></span>
      </h1>

      <div class="hero-badge-pill" id="heroAuditBadge">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        <span id="heroBadgeText">{badge_text}</span>
      </div>

      <p class="answer" id="heroQuote">
        {quote_text}
      </p>

      <dl class="facts dl">
        <div>
          <dt>Зоны риска</dt>
          <dd id="heroPrice">от {price_zones_fmt}</dd>
        </div>
        <div>
          <dt>Рейтинг в Туле</dt>
          <dd><span class="star">★</span> <span id="heroRating">{s.get('rating_ya', 5.0):.1f}</span> (<span id="heroReviews">{s.get('reviews_ya', 35)}</span> отзывов)</dd>
        </div>
        <div>
          <dt>Адрес в Туле</dt>
          <dd><a id="heroAddr" href="#contacts" data-copy-addr="{s['address']}">{addr_short}</a></dd>
        </div>
        <div>
          <dt>Запись по телефону</dt>
          <dd><a id="heroPhone" href="tel:+{s.get('phone_digits', '79611480674')}">{s.get('phone', '+7 (961) 148-06-74')}</a></dd>
        </div>
      </dl>
    </div>

  </div>
</section>

<!-- MARQUEE KINETIC TICKER -->"""

code = re.sub(old_stage_html, new_stage_html, code)

# 8. Update Card #2 in Packages (Ferrari removal)
code = code.replace(
    '<img src="/img/ceramic-mirror.jpg" alt="Полировка кузова и керамика" loading="lazy">',
    '<img src="/img/ceramic-mirror-v2.jpg" alt="Полировка кузова и керамика" loading="lazy">'
)

# 9. Update section headings with split_words()
code = code.replace(
    '<h2 id="h-slots">01 / Свободные окна в бокс на ближайшие дни</h2>',
    '<h2 id="h-slots">{split_words("01 / Свободные окна в бокс на ближайшие дни")}</h2>'
)
code = code.replace(
    '<p>Бронируйте окно онлайн — фиксируем бокс и мастера за вашим автомобилем</p>',
    '<p>{split_words("Бронируйте окно онлайн — фиксируем бокс и мастера за вашим автомобилем")}</p>'
)
code = code.replace(
    '<h2 id="h-calc">02 / Онлайн-калькулятор зон риска и защиты</h2>',
    '<h2 id="h-calc">{split_words("02 / Онлайн-калькулятор зон риска и защиты")}</h2>'
)
code = code.replace(
    '<p>Выберите класс кузова и необходимые опции — точная стоимость пересчитывается мгновенно</p>',
    '<p>{split_words("Выберите класс кузова и необходимые опции — точная стоимость пересчитывается мгновенно")}</p>'
)
code = code.replace(
    '<h2 id="h-packages">03 / Готовые пакеты защиты и сравнение ДО / ПОСЛЕ</h2>',
    '<h2 id="h-packages">{split_words("03 / Готовые пакеты защиты и сравнение ДО / ПОСЛЕ")}</h2>'
)
code = code.replace(
    '<p>Потяните слайдер в центре, чтобы сравнить состояние ЛКП BMW M8 до и после полировки с полиуретаном</p>',
    '<p>{split_words("Потяните слайдер в центре, чтобы сравнить состояние ЛКП BMW M8 до и после полировки с полиуретаном")}</p>'
)
code = code.replace(
    '<h2 id="h-price">04 / Стоимость услуг и что входит в работу</h2>',
    '<h2 id="h-price">{split_words("04 / Стоимость услуг и что входит в работу")}</h2>'
)
code = code.replace(
    '<h2 id="h-tech">05 / Стандарты и регламент студии</h2>',
    '<h2 id="h-tech">{split_words("05 / Стандарты и регламент студии")}</h2>'
)
code = code.replace(
    '<h2 id="h-contacts">07 / Адрес студии и контакты в Туле</h2>',
    '<h2 id="h-contacts">{split_words("07 / Адрес студии и контакты в Туле")}</h2>'
)

# 10. Replace client JS engines: True GPU FLIP morph + Optical Loupe + Bi-directional Observer + Scroll Parallax
old_js_block = r"""/\* FULLSCREEN-TO-FRAME VIDEO MORPH & FREEZE ENGINE \*/[\s\S]+?window\.addEventListener\("scroll", function\(\)\{\{"""
new_js_block = """/* TRUE 60 FPS GPU FLIP FULLSCREEN-TO-FRAME VIDEO MORPH */
(function initHeroFlipPortal(){{
  var frame = document.querySelector('.frame');
  var vid = frame ? frame.querySelector('video') : null;
  if (!frame || !vid) return;

  // Skip dead initial frames so the car immediately drives out
  vid.addEventListener('loadedmetadata', function(){{
    if (vid.currentTime < 0.5) vid.currentTime = 0.5;
  }}, {{ once: true }});

  var isDocked = false;
  function applyFullscreenTransform() {{
    var r = frame.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var sx = window.innerWidth / r.width;
    var sy = window.innerHeight / r.height;
    var tx = (window.innerWidth / 2) - (r.left + r.width / 2);
    var ty = (window.innerHeight / 2) - (r.top + r.height / 2);
    frame.style.transition = 'none';
    frame.style.zIndex = '999';
    frame.style.borderRadius = '0px';
    frame.style.transformOrigin = 'center center';
    frame.style.transform = 'translate3d(' + tx.toFixed(1) + 'px, ' + ty.toFixed(1) + 'px, 0) scale(' + sx.toFixed(4) + ', ' + sy.toFixed(4) + ')';
    frame.classList.add('is-fullscreen-portal');
  }}

  function dockToFrame() {{
    if (isDocked) return;
    isDocked = true;
    frame.style.transition = 'transform 1.05s cubic-bezier(0.16, 1, 0.3, 1), border-radius 1.05s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 1.05s ease';
    frame.style.transform = 'translate3d(0px, 0px, 0px) scale(1, 1)';
    frame.style.borderRadius = 'var(--r)';
    frame.classList.remove('is-fullscreen-portal');
    frame.classList.add('is-docked');
    document.body.classList.add('hero-entered');
    var heroSec = document.getElementById('hero');
    if (heroSec) heroSec.classList.add('revealed');
    setTimeout(function(){{ frame.style.zIndex = '2'; }}, 1080);
  }}

  window.__dockVideo = dockToFrame;

  // Freeze video on the exact final frame where the car is parked under the spotlights
  vid.removeAttribute('loop');
  vid.loop = false;
  vid.addEventListener('timeupdate', function(){{
    if (vid.duration && vid.currentTime >= vid.duration - 0.18) {{
      vid.pause();
      dockToFrame();
    }}
  }});
  vid.addEventListener('ended', function(){{
    vid.pause();
    dockToFrame();
  }});

  if (!navigator.webdriver && window.scrollY < 40) {{
    applyFullscreenTransform();
    var autoDockTimer = setTimeout(dockToFrame, 2400);
    ['wheel', 'touchmove', 'keydown', 'pointerdown'].forEach(function(ev){{
      window.addEventListener(ev, function onFirstInput(){{
        clearTimeout(autoDockTimer);
        dockToFrame();
      }}, {{ once: true, passive: true }});
    }});
  }} else {{
    isDocked = true;
    frame.classList.add('is-docked');
    document.body.classList.add('hero-entered');
    var heroSec = document.getElementById('hero');
    if (heroSec) heroSec.classList.add('revealed');
  }}

  // Replay button support
  var replayBtn = frame.querySelector('.replay-btn');
  if (replayBtn) {{
    replayBtn.addEventListener('click', function(e){{
      e.stopPropagation();
      isDocked = false;
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
      setTimeout(function(){{
        applyFullscreenTransform();
        vid.currentTime = 0.4;
        vid.play();
        setTimeout(dockToFrame, 2400);
      }}, 200);
    }});
  }}
}})();

/* OPTICAL DETAILING LOUPE (ZONE-AWARE HUD) */
(function initOpticalLoupe(){{
  var frame = document.querySelector('.frame');
  var loupe = document.getElementById('carLoupe');
  var hud = document.getElementById('loupeHud');
  var hint = document.getElementById('inspectHint');
  if (!frame || !loupe || !hud) return;

  frame.addEventListener('pointerenter', function(){{
    if (hint) {{ hint.style.opacity = '0'; hint.style.pointerEvents = 'none'; }}
    if (frame.classList.contains('is-docked')) {{
      frame.classList.add('is-inspecting');
    }}
  }});

  frame.addEventListener('pointerleave', function(){{
    frame.classList.remove('is-inspecting');
  }});

  frame.addEventListener('pointermove', function(e){{
    if (!frame.classList.contains('is-docked')) return;
    frame.classList.add('is-inspecting');
    if (hint) {{ hint.style.opacity = '0'; hint.style.pointerEvents = 'none'; }}
    var r = frame.getBoundingClientRect();
    var x = e.clientX - r.left;
    var y = e.clientY - r.top;
    frame.style.setProperty('--lx', x + 'px');
    frame.style.setProperty('--ly', y + 'px');

    var xp = (x / r.width) * 100;
    var yp = (y / r.height) * 100;
    if (xp < 38) {{
      hud.textContent = 'КАПОТ И ФАРЫ · БРОНЕПЛЁНКА 200 МКМ · 0% СКОЛОВ';
    }} else if (yp < 42) {{
      hud.textContent = 'КРЫША И СТОЙКИ · ГИДРОФОБНЫЙ УГОЛ 115°';
    }} else {{
      hud.textContent = 'КУЗОВ · ЗЕРКАЛЬНЫЙ ГЛЯНЕЦ 9H · ОСМОТР CRI 95+';
    }}
  }});
}})();

/* BI-DIRECTIONAL SCROLL & SPLIT-WORD REVEAL ENGINE */
var rv = new IntersectionObserver(function(entries){{
  entries.forEach(function(entry){{
    if (entry.isIntersecting) {{
      entry.target.classList.add("in");
    }} else {{
      entry.target.classList.remove("in");
    }}
  }});
}}, {{ threshold: 0.12, rootMargin: "0px 0px -40px 0px" }});

$$(".sh, .hero-info, .slots > li, .pk-card, .tech-item").forEach(function(el, idx){{
  el.style.setProperty("--ci", idx % 6);
  rv.observe(el);
}});

if (navigator.webdriver) {{
  $$(".sh, .hero-info, .slots > li, .pk-card, .tech-item").forEach(function(el){{
    el.classList.add("in");
  }});
}}

/* CONTINUOUS SCROLL VELOCITY, KINETIC SKEW & PARALLAX */
var lastScrollY = window.scrollY || 0;
var scrollTicking = false;
var topHeader = $("#topHeader");

function onScrollRaf(){{
  var sy = window.scrollY || window.pageYOffset || 0;
  var vel = sy - lastScrollY;
  lastScrollY = sy;
  
  document.documentElement.style.setProperty("--scroll-y", sy);
  
  var hw = document.querySelector(".hero-word");
  if (hw) {{
    hw.style.transform = "translate3d(calc(" + sy + " * -0.15px), calc(" + sy + " * 0.18px), 0)";
  }}

  if (topHeader) {{
    if (sy > 20) topHeader.classList.add("on");
    else topHeader.classList.remove("on");
  }}

  var skew = Math.max(-3, Math.min(3, vel * 0.12));
  document.documentElement.style.setProperty("--rev-skew", skew + "deg");

  // Package card photos subtle parallax
  $$(".pk-card-media img").forEach(function(img, i){{
    img.style.transform = "scale(1.08) translate3d(0, " + (Math.sin(sy * 0.002 + i) * 6) + "px, 0)";
  }});

  scrollTicking = false;
}}

window.addEventListener("scroll", function(){{"""

code = re.sub(old_js_block, new_js_block, code)

with open("/Users/takanov/detailing-base/scripts/build_landing.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Forensic fixes applied successfully to build_landing.py")
