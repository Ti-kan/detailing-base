#!/usr/bin/env python3
"""
Builds ~/detailing-base/tula-50.html - Master Outreach Cockpit
and ~/detailing-base/TUESDAY_50_TULA_OUTREACH.md for 50 Tula Detailing Studios.
Zero slop, zero hallucination, psychologically sound B2B templates.
"""

import json
import os
import re

DATA_PATH = "/Users/takanov/detailing-base/studios-tula.json"
HTML_OUT_PATH = "/Users/takanov/detailing-base/tula-50.html"
MD_OUT_PATH = "/Users/takanov/detailing-base/TUESDAY_50_TULA_OUTREACH.md"

NAME_OVERRIDES = {
    'Tonertut_71': 'Tonertut 71',
    'Body_Repair71': 'Body Repair 71',
    'ThePerfectCar71': 'The Perfect Car',
    'Zatoner71': 'Zatoner 71',
    'Avtostudio 71': 'Avtostudio 71',
    'Dотошный Тульский Dетейлинг': 'Дотошный Детейлинг',
    'Я. Помыл': 'Я.Помыл',
    '3 Семёрки': 'Три Семёрки',
    'Коро центр Антикор': 'КороЦентр Антикор',
    'ThreeA group': 'ThreeA Group',
    'Мир Фар 71': 'Мир Фар',
    'Пленка 71': 'Плёнка 71',
    'Detailing Datalava': 'Detailing Datalava',
    'Помыли — и Точка': 'Помыли — и Точка',
    'ТинСкин - КарСкин': 'ТинСкин - КарСкин',
    'Корс Сервис': 'Корс Сервис',
    'Автоблеск детейлинг': 'Автоблеск',
    'Гараж детейлинг': 'Гараж',
    'Никмен Детейлинг': 'Никмен',
    'БезСколов Детейлинг': 'БезСколов',
    'Black Shine Detailing': 'Black Shine',
    'Gp Detailing': 'GP Detailing',
    'V Garage': 'V Garage',
}

def clean_detailing_name(s):
    slug = s.get('slug', '')
    raw_name = s.get('name', '').strip()
    if slug == 'studio-83':
        return 'Автоювелир на Рязанской'
    if slug == 'avtoyuvelir71':
        return 'Автоювелир'
    if raw_name in NAME_OVERRIDES:
        return NAME_OVERRIDES[raw_name]
    name = raw_name.replace('_', ' ')
    name = re.sub(r'\[.*?\]', '', name).strip()
    return name

def clean_detailing_street(addr):
    raw = addr.strip()
    raw = re.sub(r'\s*·\s*Тула$', '', raw).strip()
    raw = re.sub(r'^Тула,\s*', '', raw).strip()
    raw = re.sub(r',\s*Тула$', '', raw).strip()
    
    if 'Щёкино' in raw:
        return 'в Щёкино (ул. Лукашина, 18А)'
    if 'Менделеевский' in raw:
        return 'в Менделеевском (пр. Энергетиков, 8А)'
    if 'Рождественский' in raw:
        return 'в Рождественском (ул. Фёдорова, 24)'
    if 'Плеханово' in raw:
        return 'в Плеханово (территория Тулаэлектропривод, 265)'
    if 'Гостиный двор' in raw:
        return 'в ТК «Гостиный двор» (Советская ул., 47/1)'
    if 'Мясново' in raw:
        m = re.search(r'^(.*?),\s*(микрорайон\s+Мясново|Мясново)', raw)
        street = m.group(1) if m else raw
        return f'в Мясново ({street})'
    if 'Городской пер.' in raw:
        return 'в Городском пер., 64Б'
    if 'Карла Маркса' in raw:
        return 'на ул. Карла Маркса, 5/1'
    if 'Шишкина' in raw:
        return 'на ул. Шишкина, 18'
    if 'Станиславского' in raw:
        return 'на ул. Станиславского, 51'
    if 'Оборонная' in raw:
        return 'на Оборонной, 93к3'
    if 'Епифанская' in raw:
        return 'на Епифанской, 68'
    if 'Демидовская' in raw:
        return 'на Демидовской, 179а'
    if 'Калужское ш.' in raw:
        num = re.search(r'(\d+[А-Яа-яA-Za-z]?)', raw)
        return f'на Калужском ш., {num.group(1)}' if num else 'на Калужском шоссе'
    if 'Рязанская' in raw:
        num = re.search(r'(\d+[А-Яа-яA-Za-z]?)', raw)
        return f'на Рязанской, {num.group(1)}' if num else 'на Рязанской'
    if 'Ложевая' in raw:
        return 'на Ложевой, 130А'
    if 'Октябрьская' in raw:
        num = re.search(r'(\d+(?:/\d+)?[А-Яа-яA-Za-z]?)', raw)
        return f'на Октябрьской, {num.group(1)}' if num else 'на Октябрьской'
    if 'Пролетарская' in raw:
        num = re.search(r'(\d+[А-Яа-яA-Za-z]?)', raw)
        return f'на Пролетарской, {num.group(1)}' if num else 'на Пролетарской'
    if 'Новомедвенский' in raw:
        return 'на Новомедвенском пр., 4А'
    if 'Филимоновская' in raw:
        return 'на Филимоновской'
    if 'Одоевское ш.' in raw:
        return 'на Одоевском ш., 61'
    if '1-я Хомутовка' in raw:
        return 'на ул. 1-я Хомутовка, 36'
    if 'Дементьева' in raw:
        return 'на ул. Дементьева, 56'
    if 'Кирова' in raw:
        return 'на ул. Кирова, 171А/1'
    if 'Пузакова' in raw:
        return 'на ул. Пузакова, 151'
    if 'Ленина' in raw:
        return 'на просп. Ленина, 38Б'
    if 'Тимирязева' in raw:
        return 'на пр. Тимирязева, 6/3'
    if 'Нестерова' in raw:
        return 'на ул. Нестерова, 95'
    if 'Будённого' in raw:
        return 'на ул. Будённого, 95'
    if 'Коминтерна' in raw:
        return 'на ул. Коминтерна, 24А'
    if 'Калинина' in raw:
        return 'на ул. Калинина, 14В'
    if 'Джамбула' in raw:
        return 'на ул. Джамбула, 22'
    if 'Демонстрации' in raw:
        num = re.search(r'(\d+[А-Яа-яA-Za-z]?)', raw)
        return f'на ул. Демонстрации, {num.group(1)}' if num else 'на ул. Демонстрации'
    if 'Горького' in raw:
        return 'на ул. Максима Горького, 37в'

    clean = raw
    if not (clean.startswith('на ') or clean.startswith('в ')):
        clean = 'на ' + clean
    return clean

def build_detailing_messages(s):
    name_clean = clean_detailing_name(s)
    street_short = clean_detailing_street(s['address'])
    slug = s['slug']
    price_min = s.get('price_zones', 35000)
    price_min_fmt = f"{price_min:,}".replace(",", " ")
    url = f"https://ti-kan.github.io/detailing-base/s/{slug}/"
    
    # Template 1: [ 💬 Шаг 1: Мягкий пробив (без ссылки) ]
    msg1 = (
        f"Здравствуйте! Меня зовут Кирилл, я разработчик. Подскажите, через этот чат можно связаться с руководителем студии «{name_clean}» ({street_short}) или вы передадите информацию?\n\n"
        f"Мы на выходных собрали специально под вашу студию готовый демонстрационный сайт с интерактивным осмотром авто и калькулятором по зонам риска (от {price_min_fmt} ₽). "
        f"Ничего вслепую не навязываю — можно скину ссылку сюда, покажете руководителю?"
    )
    
    # Template 2: [ 💰 Шаг 2 / Прямая продажа сайта: Эффект владения + Мягкий вывод на цену ]
    msg2 = (
        f"Приветствую! Меня зовут Кирилл. Мы в эти выходные отобрали сильные детейлинг-студии Тулы и вместо пустых коммерческих предложений сразу собрали конкретно под «{name_clean}» ({street_short}) готовый премиальный сайт:\n"
        f"👉 {url}\n\n"
        f"Откройте прямо с телефона (с мобильного смотрится эффектнее всего):\n"
        f"— При входе выезжает авто и пальцем стирается пыль до зеркального глянца;\n"
        f"— Встроен слайдер До/После и точный онлайн-калькулятор по классам кузова с вашими ценами (бронеплёнка от {price_min_fmt} ₽, полировка, керамика);\n"
        f"— Клиент за 20 секунд сам собирает нужные зоны и отправляет вам в Telegram или WhatsApp уже готовую сформированную заявку.\n\n"
        f"Поскольку сайт уже на 95% собран именно под вас, мы не просим за него студийные 70–100 тыс. ₽ — готовы отдать его полностью в вашу собственность на ваш домен по стоимости буквально одного стандартного заезда в ваш бокс, чтобы он окупился с первого же клиента с Яндекс.Карт или 2ГИС.\n\n"
        f"Посмотрите с телефона — как вам визуал и сам калькулятор?"
    )
    
    # Template 3: [ 🤝 Шаг 3: Выяснение комфортного чека и закрытие на сделку (после ответа/просмотра) ]
    msg3 = (
        f"Как вам сайт «{name_clean}» вживую с телефона? Если нужно подкорректировать какие-то позиции в прайсе или фото — сделаем за 15 минут.\n\n"
        f"По условиям передачи: мы сейчас отдаём готовые проекты только одной студии в каждом районе Тулы. Мы можем либо передать вам сайт разовым выкупом под ключ навсегда (с привязкой вашего домена и настройкой заявок в ваш личный Telegram/WhatsApp), либо запустить его в тест.\n\n"
        f"Скажите честно, если забирать его полностью себе под ключ — на какую комфортную сумму вы бы сами ориентировались, чтобы мы сразу пожали руки и сегодня перенесли его на ваш домен?"
    )
    
    return {
        'name_clean': name_clean,
        'street_short': street_short,
        'price_min_formatted': price_min_fmt,
        'url': url,
        'msg1': msg1,
        'msg2': msg2,
        'msg3': msg3
    }

HTML_TEMPLATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>50 Студий детейлинга Тулы — Outreach Cockpit & Вторник-Рассылка</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230B0C0E'/%3E%3Cpath d='M6 22l10-14 10 14H6z' fill='none' stroke='%23DF4E16' stroke-width='2.6' stroke-linejoin='round'/%3E%3Ccircle cx='16' cy='18' r='3' fill='%23FF6B35'/%3E%3C/svg%3E">
<style>
@font-face{font-family:"Oswald";src:url("fonts/oswald.woff2") format("woff2");font-weight:600 700;font-display:swap}
@font-face{font-family:"Onest";src:url("fonts/onest.woff2") format("woff2");font-weight:400 500 600 700;font-display:swap}
:root{
  --night:#0B0C0E;
  --night-2:#13151A;
  --night-3:#1A1D24;
  --night-line:rgba(255,255,255,0.09);
  --night-muted:#8E94A3;

  --accent:#DF4E16;
  --accent-hover:#C4410F;
  --accent-on-dark:#FF6B35;
  --accent-glow:rgba(223,78,22,0.28);

  --champagne:#C8A464;
  --champagne-soft:rgba(200,164,100,0.14);

  --green:#10b981;
  --tg:#229ed9;
  --wa:#25d366;

  --display:"Oswald","Arial Narrow","Roboto Condensed",sans-serif;
  --sans:"Onest",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --r:18px;
}
*{box-sizing:border-box}
body{margin:0;background:var(--night);color:#FAF9F6;font:15px/1.5 var(--sans);-webkit-font-smoothing:antialiased;padding:28px 16px 80px}
.wrap{max-width:1320px;margin:0 auto}
a{color:inherit;text-decoration:none}

.hero-box{background:linear-gradient(135deg,rgba(223,78,22,.14) 0%,rgba(200,164,100,.05) 100%),var(--night-2);border:1px solid var(--night-line);border-radius:var(--r);padding:28px 32px;margin-bottom:28px}
h1{font:700 clamp(26px,3.5vw,40px)/1.15 var(--display);text-transform:uppercase;letter-spacing:-.01em;margin:0 0 10px;color:#fff}
.lead{font-size:15px;color:var(--night-muted);max-width:80ch;line-height:1.55;margin-bottom:20px}

/* Live Outreach Counters */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:22px}
.stat{background:rgba(255,255,255,.03);border:1px solid var(--night-line);border-radius:14px;padding:14px 16px;transition:border-color .2s}
.stat:hover{border-color:rgba(255,255,255,.2)}
.stat-val{font:700 28px/1 var(--display);color:#fff}
.stat-val.accent{color:var(--accent-on-dark)}
.stat-val.green{color:var(--green)}
.stat-val.champagne{color:var(--champagne)}
.stat-lbl{font-size:12px;color:var(--night-muted);margin-top:6px;text-transform:uppercase;letter-spacing:.04em;font-weight:600}

/* Base URL Configuration */
.base-url-bar{background:rgba(0,0,0,.5);border:1px solid var(--night-line);border-radius:12px;padding:12px 16px;margin-bottom:22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.base-url-bar label{font-size:12px;font-weight:700;color:var(--accent-on-dark);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.base-url-input{flex:1;min-width:280px;height:38px;border-radius:8px;border:1px solid var(--night-line);background:var(--night-3);color:#fff;padding:0 12px;font:600 13px var(--sans);outline:0}
.base-url-input:focus{border-color:var(--accent)}

/* Filter tabs & Search */
.controls{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px;align-items:center;justify-content:space-between}
.filter-tabs{display:flex;flex-wrap:wrap;gap:8px}
.tab{min-height:38px;padding:0 15px;border-radius:999px;border:1px solid var(--night-line);background:var(--night-2);color:var(--night-muted);font:600 13px/1 var(--sans);cursor:pointer;transition:all .15s}
.tab:hover{color:#fff;border-color:var(--accent)}
.tab.on{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 4px 16px var(--accent-glow)}

.search-wrap{position:relative;flex:1;max-width:360px;min-width:240px}
.search-input{width:100%;height:38px;border-radius:999px;border:1px solid var(--night-line);background:var(--night-2);color:#fff;padding:0 16px 0 38px;font:500 13px var(--sans);outline:0}
.search-input:focus{border-color:var(--accent)}
.search-icon{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:#6b7280;pointer-events:none}

/* Grid of Cards */
.grid{display:grid;grid-template-columns:1fr;gap:20px}
@media (min-width:768px){.grid{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1200px){.grid{grid-template-columns:repeat(3,1fr)}}

.card{background:var(--night-2);border:1px solid var(--night-line);border-radius:var(--r);padding:20px;display:flex;flex-direction:column;transition:all .2s;position:relative}
.card:hover{border-color:rgba(223,78,22,.4);box-shadow:0 12px 32px rgba(0,0,0,.4)}
.card.status-step1{border-color:rgba(200,164,100,.5)}
.card.status-site{border-color:rgba(223,78,22,.65)}
.card.status-replied{border-color:rgba(16,185,129,.7);box-shadow:0 8px 24px rgba(16,185,129,.12)}

.card-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.rank{font:700 13px/1 var(--display);color:var(--night-muted);letter-spacing:.02em}
.badge{font-size:11px;font-weight:700;padding:4px 9px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em}
.badge-ans{background:rgba(223,78,22,.16);color:var(--accent-on-dark);border:1px solid rgba(223,78,22,.4)}
.badge-top{background:rgba(200,164,100,.14);color:#eab308;border:1px solid rgba(200,164,100,.35)}

.name{font:700 20px/1.2 var(--display);text-transform:uppercase;color:#fff;margin-bottom:4px}
.addr{font-size:13px;color:#d1d5db;margin-bottom:6px;line-height:1.4}
.phone{font-size:13px;font-weight:600;color:var(--accent-on-dark);margin-bottom:12px;display:inline-flex;align-items:center;gap:6px}

.meta-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-top:1px solid var(--night-line);border-bottom:1px solid var(--night-line);margin-bottom:12px;font-size:12px}
.rating{color:#eab308;font-weight:600}
.price{color:#fff;font-weight:700}

/* Actions Row: Site Link & Copy URL */
.site-actions{display:grid;grid-template-columns:1fr auto;gap:8px;margin-bottom:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:38px;padding:0 12px;border-radius:8px;font:600 12px/1 var(--sans);cursor:pointer;transition:all .15s;border:0;text-align:center}
.btn-open{background:rgba(255,255,255,.07);color:#FAF9F6;border:1px solid rgba(255,255,255,.14)}
.btn-open:hover{background:rgba(255,255,255,.14);color:#fff}
.btn-copy-url{background:rgba(255,255,255,.04);color:var(--night-muted);border:1px solid var(--night-line);padding:0 10px}
.btn-copy-url:hover{color:#fff;border-color:rgba(255,255,255,.25)}

/* Outreach Box & Editable Textarea */
.outreach-box{background:rgba(0,0,0,.35);border:1px solid var(--night-line);border-radius:12px;padding:12px;margin-top:auto}
.tpl-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-bottom:10px}
.tpl-tab{background:var(--night-3);color:var(--night-muted);border:1px solid var(--night-line);border-radius:6px;padding:6px 4px;font:600 11px/1.2 var(--sans);cursor:pointer;text-align:center;transition:all .15s}
.tpl-tab:hover{color:#fff;border-color:var(--accent)}
.tpl-tab.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 2px 8px var(--accent-glow)}

.msg-textarea{width:100%;height:130px;background:var(--night-3);border:1px solid var(--night-line);border-radius:8px;color:#f3f4f6;font:12px/1.45 var(--sans);padding:8px 10px;resize:vertical;outline:0;box-sizing:border-box;margin-bottom:10px;transition:border-color .15s}
.msg-textarea:focus{border-color:var(--accent)}

.send-actions{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-bottom:12px}
.btn-copy-msg{background:rgba(255,255,255,.08);color:#FAF9F6;border:1px solid rgba(255,255,255,.15);font-size:11px;padding:0 6px}
.btn-copy-msg:hover{background:rgba(255,255,255,.16);color:#fff}
.btn-wa{background:rgba(37,211,102,.14);color:#25d366;border:1px solid rgba(37,211,102,.35);font-size:11px;padding:0 6px}
.btn-wa:hover{background:#25d366;color:#000}
.btn-tg{background:rgba(34,158,217,.14);color:#229ed9;border:1px solid rgba(34,158,217,.35);font-size:11px;padding:0 6px}
.btn-tg:hover{background:#229ed9;color:#fff}

/* Persistent CRM Checkboxes */
.crm-row{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding-top:10px;border-top:1px solid var(--night-line)}
.crm-label{display:flex;align-items:center;gap:6px;cursor:pointer;font-size:11px;color:var(--night-muted);font-weight:600;user-select:none}
.crm-label input{accent-color:var(--accent);cursor:pointer;width:14px;height:14px;margin:0}
.crm-label:hover{color:#fff}

.toast{position:fixed;bottom:24px;right:24px;background:#fff;color:var(--night);padding:12px 20px;border-radius:999px;font:700 13px/1 var(--sans);z-index:99;box-shadow:0 12px 30px rgba(0,0,0,.5);opacity:0;transform:translateY(20px);pointer-events:none;transition:all .25s}
.toast.show{opacity:1;transform:translateY(0)}
</style>
</head>
<body>
<div class="wrap">
  
  <div class="hero-box">
    <h1>50 Студий детейлинга Тулы — Outreach Cockpit</h1>
    <p class="lead">
      Персонализированная рассылка на вторник: психологические B2B-шаблоны без спам-блокировок.
      В карточке каждой студии доступен предпросмотр любого из 3 вариантов, редактируемый текст перед отправкой и сохранение статуса в <code>localStorage</code>.
    </p>

    <!-- Outreach Progress Stats -->
    <div class="stats">
      <div class="stat">
        <div class="stat-val" id="statTotal">50</div>
        <div class="stat-lbl">Всего студий</div>
      </div>
      <div class="stat">
        <div class="stat-val champagne" id="statStep1">0 / 50</div>
        <div class="stat-lbl">Шаг 1: Контакт</div>
      </div>
      <div class="stat">
        <div class="stat-val accent" id="statSite">0 / 50</div>
        <div class="stat-lbl">Шаг 2: Отправлен сайт</div>
      </div>
      <div class="stat">
        <div class="stat-val green" id="statReplied">0 / 50</div>
        <div class="stat-lbl">Ответили на диалог</div>
      </div>
    </div>

    <div class="base-url-bar">
      <label for="baseUrlInput">🌐 Live Base URL:</label>
      <input class="base-url-input" id="baseUrlInput" type="text" value="https://ti-kan.github.io/detailing-base">
      <span style="font-size:11px;color:var(--night-muted)">Ссылки в сообщениях синхронизируются автоматически</span>
    </div>

    <div class="controls">
      <div class="filter-tabs" id="filterTabs">
        <button class="tab on" type="button" data-filter="all">Все 50</button>
        <button class="tab" type="button" data-filter="unprocessed">⏳ Не начато</button>
        <button class="tab" type="button" data-filter="step1">💬 Шаг 1 отправлен</button>
        <button class="tab" type="button" data-filter="site">🚀 Сайт отправлен</button>
        <button class="tab" type="button" data-filter="replied">✅ Ответили</button>
      </div>

      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" id="searchInput" type="search" placeholder="Поиск по студии, улице, телефону...">
      </div>
    </div>
  </div>

  <div class="grid" id="studiosGrid">
    <!-- Rendered dynamically -->
  </div>
</div>

<div class="toast" id="toast">📋 Скопировано в буфер обмена!</div>

<script>
window.STUDIOS_DATA = __DATA_PLACEHOLDER__;

(function(){
  var grid = document.getElementById("studiosGrid");
  var toast = document.getElementById("toast");
  var baseInput = document.getElementById("baseUrlInput");
  var allData = window.STUDIOS_DATA || [];
  var activeFilter = "all";

  function showToast(text){
    if(text) toast.textContent = text;
    toast.classList.add("show");
    setTimeout(function(){ toast.classList.remove("show"); }, 2200);
  }

  function copyToClipboard(val, msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(val).then(function(){ showToast(msg || "📋 Скопировано!"); });
    } else {
      var t = document.createElement("textarea"); t.value = val; document.body.appendChild(t); t.select();
      try{ document.execCommand("copy"); showToast(msg || "📋 Скопировано!"); }catch(e){}
      document.body.removeChild(t);
    }
  }

  function getCrm(slug){
    try {
      var raw = localStorage.getItem("detailing_crm_" + slug);
      return raw ? JSON.parse(raw) : { step1: false, site: false, replied: false };
    } catch(e) {
      return { step1: false, site: false, replied: false };
    }
  }

  function saveCrm(slug, data){
    try {
      localStorage.setItem("detailing_crm_" + slug, JSON.stringify(data));
    } catch(e){}
    updateStats();
  }

  function updateStats(){
    var step1Count = 0;
    var siteCount = 0;
    var repliedCount = 0;

    allData.forEach(function(s){
      var crm = getCrm(s.slug);
      if(crm.step1) step1Count++;
      if(crm.site) siteCount++;
      if(crm.replied) repliedCount++;
    });

    document.getElementById("statTotal").textContent = allData.length;
    document.getElementById("statStep1").textContent = step1Count + " / " + allData.length;
    document.getElementById("statSite").textContent = siteCount + " / " + allData.length;
    document.getElementById("statReplied").textContent = repliedCount + " / " + allData.length;
  }

  function render(list){
    var base = (baseInput.value || "https://ti-kan.github.io/detailing-base").trim().replace(/\\/+$/, "");

    grid.innerHTML = list.map(function(s){
      var staticUrl = base + "/s/" + s.slug + "/";
      var badgeClass = s.audit_answered ? "badge-ans" : "badge-top";
      var badgeLabel = s.audit_answered ? ("⚡️ " + s.audit_response_time) : ("★ " + s.rating_ya.toFixed(1));

      var crm = getCrm(s.slug);
      var cardStatusClass = crm.replied ? "status-replied" : (crm.site ? "status-site" : (crm.step1 ? "status-step1" : ""));

      var waPhone = (s.phone_digits || "").replace(/\\D/g, "");
      var tgTarget = waPhone ? ("+" + waPhone) : "";

      return '<div class="card ' + cardStatusClass + '" id="card-' + s.slug + '" data-slug="' + s.slug + '">' +
        '<div class="card-top">' +
          '<span class="rank">#' + s.id + ' · ' + s.slug + '</span>' +
          '<span class="badge ' + badgeClass + '">' + badgeLabel + '</span>' +
        '</div>' +
        '<div class="name">' + s.name_clean + '</div>' +
        '<div class="addr">📍 ' + s.street_short + '</div>' +
        '<a class="phone" href="tel:' + s.phone_digits + '">📞 ' + s.phone + '</a>' +
        '<div class="meta-row">' +
          '<span class="rating">★ ' + s.rating_ya.toFixed(1) + ' (' + s.reviews_ya + ' отз.)</span>' +
          '<span class="price">Зоны: от ' + s.price_min_formatted + ' ₽</span>' +
        '</div>' +
        '<div class="site-actions">' +
          '<a class="btn btn-open" href="' + staticUrl + '" target="_blank">↗ Открыть сайт</a>' +
          '<button class="btn btn-copy-url" type="button" data-url="' + staticUrl + '">🔗 Ссылка</button>' +
        '</div>' +
        '<div class="outreach-box">' +
          '<div class="tpl-tabs" data-slug="' + s.slug + '">' +
            '<button class="tpl-tab active" type="button" data-tpl="1">💬 Шаг 1: Пробив</button>' +
            '<button class="tpl-tab" type="button" data-tpl="2">💰 Шаг 2: Продажа</button>' +
            '<button class="tpl-tab" type="button" data-tpl="3">🤝 Шаг 3: Чек и сделка</button>' +
          '</div>' +
          '<textarea class="msg-textarea" id="txt-' + s.slug + '" rows="7">' + s.msg1 + '</textarea>' +
          '<div class="send-actions">' +
            '<button class="btn btn-copy-msg" type="button" data-copy-for="' + s.slug + '">📋 Копировать</button>' +
            '<button class="btn btn-wa" type="button" data-wa-for="' + s.slug + '" data-wa-phone="' + waPhone + '">💬 WhatsApp</button>' +
            '<button class="btn btn-tg" type="button" data-tg-for="' + s.slug + '" data-tg-target="' + tgTarget + '">✈️ Telegram</button>' +
          '</div>' +
          '<div class="crm-row">' +
            '<label class="crm-label"><input type="checkbox" data-crm-type="step1" data-slug="' + s.slug + '" ' + (crm.step1 ? "checked" : "") + '> Шаг 1</label>' +
            '<label class="crm-label"><input type="checkbox" data-crm-type="site" data-slug="' + s.slug + '" ' + (crm.site ? "checked" : "") + '> Сайт</label>' +
            '<label class="crm-label"><input type="checkbox" data-crm-type="replied" data-slug="' + s.slug + '" ' + (crm.replied ? "checked" : "") + '> Ответили</label>' +
          '</div>' +
        '</div>' +
      '</div>';
    }).join("");

    attachCardHandlers();
    updateStats();
  }

  function attachCardHandlers(){
    // Copy URL
    grid.querySelectorAll("[data-url]").forEach(function(btn){
      btn.addEventListener("click", function(){
        copyToClipboard(btn.getAttribute("data-url"), "🔗 Ссылка на сайт скопирована!");
      });
    });

    // Template Switcher Tabs
    grid.querySelectorAll(".tpl-tab").forEach(function(tab){
      tab.addEventListener("click", function(){
        var tplNum = tab.getAttribute("data-tpl");
        var slug = tab.parentElement.getAttribute("data-slug");
        var item = allData.find(function(x){ return x.slug === slug; });
        if(!item) return;

        tab.parentElement.querySelectorAll(".tpl-tab").forEach(function(t){ t.classList.remove("active"); });
        tab.classList.add("active");

        var txtArea = document.getElementById("txt-" + slug);
        if(!txtArea) return;

        var base = (baseInput.value || "https://ti-kan.github.io/detailing-base").trim().replace(/\\/+$/, "");
        var currentUrl = base + "/s/" + slug + "/";

        var text = "";
        if(tplNum === "1") text = item.msg1;
        else if(tplNum === "2") text = item.msg2.replace(/https:\/\/ti-kan\.github\.io\/detailing-base\/s\/[^\/]+\//, currentUrl);
        else if(tplNum === "3") text = item.msg3.replace(/https:\/\/ti-kan\.github\.io\/detailing-base\/s\/[^\/]+\//, currentUrl);

        txtArea.value = text;
      });
    });

    // Copy Textarea Content
    grid.querySelectorAll("[data-copy-for]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var slug = btn.getAttribute("data-copy-for");
        var txtArea = document.getElementById("txt-" + slug);
        if(txtArea){
          copyToClipboard(txtArea.value, "💬 Текст сообщения скопирован!");
        }
      });
    });

    // Open WhatsApp
    grid.querySelectorAll("[data-wa-for]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var slug = btn.getAttribute("data-wa-for");
        var phone = btn.getAttribute("data-wa-phone");
        var txtArea = document.getElementById("txt-" + slug);
        var text = txtArea ? txtArea.value : "";
        var link = "https://wa.me/" + phone + "?text=" + encodeURIComponent(text);
        window.open(link, "_blank");
      });
    });

    // Open Telegram
    grid.querySelectorAll("[data-tg-for]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var slug = btn.getAttribute("data-tg-for");
        var target = btn.getAttribute("data-tg-target");
        var txtArea = document.getElementById("txt-" + slug);
        var text = txtArea ? txtArea.value : "";
        var link = "";
        if(target.match(/^\\+?\\d+$/)){
          var num = target.replace(/^\\+/, "");
          link = "https://t.me/+" + num + "?text=" + encodeURIComponent(text);
        } else {
          link = "https://t.me/" + target + "?text=" + encodeURIComponent(text);
        }
        window.open(link, "_blank");
      });
    });

    // CRM Checkboxes
    grid.querySelectorAll(".crm-label input").forEach(function(chk){
      chk.addEventListener("change", function(){
        var slug = chk.getAttribute("data-slug");
        var type = chk.getAttribute("data-crm-type");
        var crm = getCrm(slug);
        crm[type] = chk.checked;
        saveCrm(slug, crm);

        var card = document.getElementById("card-" + slug);
        if(card){
          card.classList.remove("status-step1", "status-site", "status-replied");
          if(crm.replied) card.classList.add("status-replied");
          else if(crm.site) card.classList.add("status-site");
          else if(crm.step1) card.classList.add("status-step1");
        }
      });
    });
  }

  function filterAndSearch(){
    var q = (document.getElementById("searchInput").value || "").toLowerCase().trim();
    var filtered = allData.filter(function(s){
      var crm = getCrm(s.slug);

      if(activeFilter === "unprocessed" && (crm.step1 || crm.site || crm.replied)) return false;
      if(activeFilter === "step1" && !crm.step1) return false;
      if(activeFilter === "site" && !crm.site) return false;
      if(activeFilter === "replied" && !crm.replied) return false;

      if(q){
        var match = s.name_clean.toLowerCase().includes(q) ||
                    s.street_short.toLowerCase().includes(q) ||
                    s.slug.toLowerCase().includes(q) ||
                    (s.phone && s.phone.includes(q));
        if(!match) return false;
      }
      return true;
    });
    render(filtered);
  }

  // Initial render
  render(allData);

  document.querySelectorAll("#filterTabs .tab").forEach(function(t){
    t.addEventListener("click", function(){
      document.querySelectorAll("#filterTabs .tab").forEach(function(x){ x.classList.remove("on"); });
      t.classList.add("on");
      activeFilter = t.getAttribute("data-filter");
      filterAndSearch();
    });
  });

  var sInput = document.getElementById("searchInput");
  if(sInput) sInput.addEventListener("input", filterAndSearch);

  if(baseInput){
    baseInput.addEventListener("input", function(){
      filterAndSearch();
    });
  }
})();
</script>
</body>
</html>
"""

def generate_markdown_cheat_sheet(studios):
    lines = [
        "# ВТОРНИК: 50 СТУДИЙ ДЕТЕЙЛИНГА ТУЛЫ — OUTREACH CHEAT-SHEET",
        "",
        "> **Инструкция по рассылке во вторник:**",
        "> 1. **Шаг 1 (Утро / Холодный контакт)**: отправляем короткий вход **без ссылок**, чтобы не ловить спам-блок от WhatsApp/Telegram.",
        "> 2. **Шаг 2 (После ответа / Владение)**: как только ответили или подтвердили контакт — отправляем ссылку на персональный сайт с калькулятором зон риска.",
        "> 3. **Вариант 3 (Короткий)**: для карточек в Яндекс.Картах, 2ГИС или в личных сообщениях сообществ ВК.",
        "",
        "## СВОДНАЯ ТАБЛИЦА (50 СТУДИЙ)",
        "",
        "| № | Название | Адрес | Телефон | WhatsApp | Готовый сайт |",
        "|---|---|---|---|---|---|"
    ]
    
    for s in studios:
        wa_phone = s.get('phone_digits', '')
        wa_link = f"https://wa.me/{wa_phone}" if wa_phone else "—"
        url = f"https://ti-kan.github.io/detailing-base/s/{s['slug']}/"
        lines.append(f"| {s['id']} | **{s['name_clean']}** | {s['street_short']} | `{s.get('phone', '')}` | [Написать]({wa_link}) | [{s['slug']}]({url}) |")
        
    lines.append("\n---\n")
    lines.append("## ПЕРСОНАЛЬНЫЕ СООБЩЕНИЯ ДЛЯ КАЖДОЙ СТУДИИ\n")
    
    for s in studios:
        lines.append(f"### #{s['id']} · {s['name_clean']} ({s['slug']})")
        lines.append(f"- **Локация:** {s['street_short']}")
        lines.append(f"- **Телефон:** `{s.get('phone', '')}`")
        lines.append(f"- **Сайт:** [{s['url']}]({s['url']})")
        
        wa_phone = s.get('phone_digits', '')
        if wa_phone:
            lines.append(f"- **WhatsApp:** https://wa.me/{wa_phone}")
            lines.append(f"- **Telegram:** https://t.me/+{wa_phone}")
            
        lines.append("\n**[ 💬 Шаг 1: Мягкий пробив (без ссылки) ]:**")
        lines.append("```text")
        lines.append(s['msg1'])
        lines.append("```")
        
        lines.append("\n**[ 💰 Шаг 2 / Прямая продажа сайта: Эффект владения + Мягкий вывод на цену ]:**")
        lines.append("```text")
        lines.append(s['msg2'])
        lines.append("```")
        
        lines.append("\n**[ 🤝 Шаг 3: Выяснение комфортного чека и закрытие на сделку (после ответа/просмотра) ]:**")
        lines.append("```text")
        lines.append(s['msg3'])
        lines.append("```")
        lines.append("\n---\n")
        
    return "\n".join(lines)

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        studios = json.load(f)
        
    print(f"Loaded {len(studios)} studios from {DATA_PATH}")
    
    for s in studios:
        info = build_detailing_messages(s)
        s.update(info)
        
    # Write enriched studios-tula.json
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(studios, f, ensure_ascii=False, indent=2)
    print(f"Saved enriched data back to {DATA_PATH}")
    
    # Generate HTML Cockpit
    html_content = HTML_TEMPLATE.replace("__DATA_PLACEHOLDER__", json.dumps(studios, ensure_ascii=False))
    with open(HTML_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved master cockpit to {HTML_OUT_PATH}")
    
    # Generate Markdown Cheat Sheet
    md_content = generate_markdown_cheat_sheet(studios)
    with open(MD_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved master cheat sheet to {MD_OUT_PATH}")

if __name__ == "__main__":
    main()
