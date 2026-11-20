#!/usr/bin/env python3
"""Builds the f1devbin.github.io landing page in 7 languages (static HTML, committed to the repo).

    python3 build.py

Writes index.html (English, x-default), <lang>/index.html, assets/site.css, sitemap.xml, robots.txt and
404.html. Images come from tools/images.py. robots.txt sits at the host root, so it governs every project
site under f1devbin.github.io and lists their sitemaps. Search-engine verification codes come from
verification.json.

The page loads nothing from other hosts: the fonts are self-hosted (IBM Plex Sans, OFL) and a Content
Security Policy allows only same-origin styles, fonts and images, and no scripts at all.
"""
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://f1devbin.github.io/"
GH = "https://github.com/f1devbin"
YEAR = 2026
LANGS = {"en": ("English", "en", "en_US"), "ru": ("Русский", "ru", "ru_RU"), "es": ("Español", "es", "es_ES"),
         "pt": ("Português", "pt-BR", "pt_BR"), "tr": ("Türkçe", "tr", "tr_TR"), "vi": ("Tiếng Việt", "vi", "vi_VN"),
         "zh": ("中文", "zh-Hans", "zh_CN")}
PROJECT_SITEMAPS = ["Crypto-Research-Labs/sitemap.xml", "telegram-bot-manager/sitemap.xml", "c6-zigbee-stick/sitemap.xml",
                    "grbl-wifi-bridge/sitemap.xml"]
TALL = {"myip"}  # portrait screenshots, shown narrower
TBM_LANGS = ("ru", "es", "pt", "zh")  # Telegram Bot Manager has these besides English
# connect-src only lets audit tools (Lighthouse) read robots.txt; the page itself has no scripts
CSP = ("default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self'; connect-src 'self'; "
       "base-uri 'none'; form-action 'none'")

# image sizes, written by tools/images.py (width and height attributes keep the layout from jumping)
SIZES_FILE = ROOT / "assets" / "sizes.json"
SIZES = json.loads(SIZES_FILE.read_text()) if SIZES_FILE.exists() else {}
CAT_SIZES = "(max-width: 380px) 106px, (max-width: 760px) 124px, 216px"  # .cat width in the CSS below

# Text. [label](key) becomes a link to links(lang)[key]; the label is escaped like the rest.
T = {
"en": {
 "title": "Max (f1devbin): programmer and electronics engineer",
 "desc": "I’m Max, a programmer and electronics engineer. Open source: a crypto research lab, Telegram tools, a KDE Plasma 6 widget and a Zigbee coordinator for Home Assistant.",
 "og_line": "Programmer and electronics engineer", "job": "Electronics engineer",
 "skip": "Skip to content", "lang_label": "Language",
 "h1": "Hi, I’m Max",
 "intro": [
  "I trained as a programmer and have worked as an electronics engineer for many years. Most of the software "
  "I write is for myself, for problems I actually run into.",
  "When a tool turns out to be useful to other people too, I tidy it up, write tests and documentation and "
  "publish it.",
  "Oh, and I love cats. This one in the penguin costume lives in the icon of my KDE widget."],
 "cat_alt": "A cartoon cat in a penguin costume pointing at the greeting",
 "projects_h": "My projects", "source": "Source code",
 "crl_what": "An open lab where I test crypto trading ideas and publish every result, failures included.",
 "crl_story": "It started with my own trading bot. When I replayed its 7,649 signals on real prices, it called the "
              "direction worse than a coin toss. Luckily, it only ever traded on a test exchange. Instead of tuning "
              "it until the backtest looked good, I built a lab where that trick doesn’t work: each idea is written "
              "down and sealed with a hash before it is tested, fees are always included, and GitHub Actions "
              "re-test everything on new data on a schedule. Most ideas fail, and the failures are written up as "
              "carefully as the passes.",
 "crl_proof": "The [methodology](crl_method) explains how a test works, the [research page](crl_findings) lists "
              "every result, and there’s a [beginners’ course](crl_course) in seven languages.",
 "crl_cap": "The dashboard on 28 October 2026.",
 "crl_alt": "Crypto Research Labs dashboard: 30 trading ideas tested, 2 passed",
 "crl_cta": "Open the dashboard",
 "tbm_what": "A free page for setting up a Telegram bot right in the browser: webhooks, commands, name and "
             "description, avatar, menu button and admin rights.",
 "tbm_story": "I run several bots of my own, and every webhook change used to mean another curl command with the "
              "bot token typed into a terminal. Now it takes a few clicks. There is no server behind the page. "
              "Requests go from your browser straight to Telegram, the token stays in the open tab unless you ask "
              "the browser to remember it, and a strict Content Security Policy keeps outside scripts off the "
              "page. No analytics, no counters. It works in five languages and on a phone.",
 "tbm_proof": "There are step-by-step guides on how to [set a webhook](tbm_set), [check it with getWebhookInfo](tbm_info) "
              "and [delete it](tbm_del), and on the [bot commands editor](tbm_cmd). How the token is protected is "
              "described in the README under [Privacy and security](tbm_privacy).",
 "tbm_cap": "A demo bot. Everything in the screenshot is example data.",
 "tbm_alt": "Telegram Bot Manager: webhook status of a demo bot with its last delivery error",
 "tbm_cta": "Open Bot Manager",
 "myip_what": "A KDE Plasma\u00a06 widget: your public IP and country, local interfaces, a network scanner with "
              "port scan, diagnostics, a speed test, traffic per app and a device monitor.",
 "myip_story": "I wanted to see at a glance which country I go online from and whether the VPN is really on. Over "
               "time the tools I used to run in a terminal moved in as well. When the internet drops, the "
               "diagnostics tell you in plain words where the chain broke: the connection, the router, DNS or "
               "somewhere further. On Kubuntu it needs no root rights and nothing extra to install, and there is "
               "no telemetry.",
 "myip_proof": "Every outside service it talks to, and why, is listed in the [README](myip_privacy).",
 "myip_cap": "The address in the screenshot belongs to a VPN server.",
 "myip_alt": "My IP & Geo widget: public IP, location, provider, system load and traffic",
 "myip_cta": "Download the widget",
 "c6_what": "Turns an inexpensive ESP32-C6 board into a Zigbee coordinator for Home Assistant: flash it from the browser, plug it in, press “Add”.",
 "c6_story": "Home Assistant recognises store-bought Zigbee sticks by their USB name, but every ESP32-C6 reports the same generic one, so a home-made coordinator meant editing configs by hand. My integration asks the board over the ZBOSS protocol whether it really is a coordinator, then installs and sets up Zigbee2MQTT on its own and restarts it if the stick is unplugged and plugged back in. The firmware is Espressif’s, flashed straight from the page; nothing to install on your computer.",
 "c6_proof": "The [firmware page](c6_live) has a FAQ, and the README explains [how it works](c6_how).",
 "c6_cap": "The firmware page: one button flashes the board.",
 "c6_alt": "C6 Zigbee Stick firmware page with the Install firmware button",
 "c6_cta": "Flash the firmware",
 "grbl_what": "Runs a GRBL laser engraver or CNC router over Wi-Fi: an ESP32-S3 plugs into the machine’s USB port and LightBurn connects to it over the network.",
 "grbl_story": "Hobby laser engravers and 3018 routers want a laptop on a USB cable right next to them. The bridge takes the laptop’s place: the ESP32-S3 works as a USB host for the machine’s own serial chip and passes GRBL to a TCP port unchanged, so LightBurn and Universal Gcode Sender work as before. If the connection drops in the middle of a job, it stops the machine and switches the laser off. The machine itself needs no changes, and the web panel has a big STOP button and a GRBL console.",
 "grbl_proof": "The [firmware page](grbl_live) flashes the board and sets up Wi-Fi in one go and answers common questions; the README lists the [safety rules](grbl_safety).",
 "grbl_cap": "The bridge’s web panel. Everything in the screenshot is example data.",
 "grbl_alt": "GRBL Wi-Fi Bridge web panel: machine status, STOP button and GRBL console",
 "grbl_cta": "Flash the firmware",
 "how_h": "How I work",
 "how": [
  "I don’t write anything in a README that I haven’t checked myself. In the lab the checking is part of the "
  "method, and the other projects are checked automatically on GitHub Actions.",
  "My projects don’t collect anything about you. There are no analytics, cookies or ads, and this page doesn’t "
  "load anything from other sites either; its source code shows it.",
  "All the code is open under the MIT license. I keep the documentation up to date and answer questions and "
  "bug reports."],
 "stack_h": "What I work with",
 "stack": ["Languages", "Databases", "Servers and CI"],
 "contact_h": "Get in touch",
 "contact": "Questions, bug reports and ideas are welcome in the issues of the project: [Crypto Research "
            "Labs](crl_issues), [Telegram Bot Manager](tbm_issues), [My IP & Geo](myip_issues), [C6 Zigbee Stick](c6_issues), [GRBL Wi-Fi Bridge](grbl_issues). Russian is my native "
            "language and English is fine too. You can also write in your own language; I’ll use a translator.",
 "foot_privacy": "This page uses no cookies or analytics and loads nothing from other sites.",
 "foot_src": "Page source",
 "nf_title": "Page not found", "nf_text": "There’s no such page here. It may have moved.",
 "home": "Go to the home page", "me": "Max"},

"ru": {
 "title": "Макс (f1devbin): программист и инженер-электроник",
 "desc": "Макс, программист и инженер-электроник. Открытые проекты: проверка торговых идей, инструменты для Telegram, виджет KDE Plasma 6, Zigbee-координатор для Home Assistant.",
 "og_line": "Программист и инженер-электроник", "job": "Инженер-электроник",
 "skip": "Перейти к содержимому", "lang_label": "Язык",
 "h1": "Привет, я Макс",
 "intro": [
  "По образованию я программист, а уже много лет работаю инженером-электроником. Программы пишу в основном "
  "для себя, под задачи, которые у меня действительно возникают.",
  "Когда инструмент оказывается полезен не только мне, я привожу его в порядок, пишу тесты и документацию "
  "и выкладываю в открытый доступ.",
  "А ещё я люблю котиков. Вот этот, в костюме пингвина, живёт в иконке моего виджета для KDE."],
 "cat_alt": "Нарисованный кот в костюме пингвина показывает лапой на приветствие",
 "projects_h": "Мои проекты", "source": "Исходный код",
 "crl_what": "Открытая лаборатория, где я проверяю торговые идеи для криптовалют и публикую все результаты, "
             "включая провалы.",
 "crl_story": "Началось всё с моего торгового бота. Я прогнал его 7\u00a0649 сигналов на реальных ценах, и оказалось, "
              "что направление он угадывал хуже подброшенной монетки. Хорошо, что торговал он только на тестовой "
              "бирже. Подкручивать его, пока бэктест не станет красивым, я не стал, а сделал лабораторию, где "
              "такой фокус не пройдёт: каждая идея записывается и запечатывается хешем до проверки, комиссии "
              "учитываются всегда, а GitHub Actions по расписанию перепроверяют всё на новых данных. Большинство "
              "идей проверку не проходят, и провалы описаны так же подробно, как удачи.",
 "crl_proof": "Как устроена проверка, объяснено в [методике](crl_method), все результаты собраны на [странице "
              "исследований](crl_findings), а для тех, кто только начинает, есть [курс для новичков](crl_course) "
              "на семи языках.",
 "crl_cap": "Дашборд 28 октября 2026 года.",
 "crl_alt": "Дашборд Crypto Research Labs: проверено 30 торговых идей, прошли 2",
 "crl_cta": "Открыть дашборд",
 "tbm_what": "Бесплатная страница, чтобы настроить Telegram-бота прямо в браузере: вебхуки, команды, имя "
             "и описание, аватар, кнопку меню и права администратора.",
 "tbm_story": "У меня несколько своих ботов, и раньше каждая смена вебхука означала очередную команду curl "
              "с токеном бота в терминале. Теперь это пара кликов. Сервера у страницы нет. Запросы идут из вашего "
              "браузера прямо в Telegram, токен хранится только в открытой вкладке, если вы сами не попросите "
              "браузер его запомнить, а строгая политика CSP не пускает на страницу чужие скрипты. Ни аналитики, "
              "ни счётчиков. Работает на пяти языках и на телефоне.",
 "tbm_proof": "Есть пошаговые инструкции: как [установить вебхук](tbm_set), [проверить его через "
              "getWebhookInfo](tbm_info) и [удалить](tbm_del), а также про [редактор команд бота](tbm_cmd). Как "
              "защищён токен, описано в разделе [«Безопасность»](tbm_privacy) в README.",
 "tbm_cap": "Демо-бот, все данные на снимке вымышленные.",
 "tbm_alt": "Telegram Bot Manager: состояние вебхука демо-бота и последняя ошибка доставки",
 "tbm_cta": "Открыть Bot Manager",
 "myip_what": "Виджет для KDE Plasma\u00a06: внешний IP и страна, локальные интерфейсы, сканер сети с проверкой "
              "портов, диагностика, тест скорости, трафик по приложениям и монитор устройств.",
 "myip_story": "Мне хотелось одним взглядом видеть, из какой страны я выхожу в интернет и правда ли включён VPN. "
               "Со временем туда переехали и утилиты, которые я раньше запускал в терминале. Когда пропадает "
               "интернет, диагностика простыми словами говорит, где оборвалась цепочка: в подключении, на роутере, "
               "в DNS или дальше. В Kubuntu ему не нужны права root и не нужно ничего доустанавливать, "
               "телеметрии нет.",
 "myip_proof": "Все внешние сервисы, к которым он обращается, и зачем, перечислены в [README](myip_privacy) "
               "(на английском).",
 "myip_cap": "IP-адрес на снимке принадлежит VPN-серверу.",
 "myip_alt": "Виджет My IP & Geo: внешний IP, местоположение, провайдер, загрузка системы и трафик",
 "myip_cta": "Скачать виджет",
 "c6_what": "Превращает недорогую плату ESP32-C6 в Zigbee-координатор для Home Assistant: прошить из браузера, вставить в USB, нажать «Добавить».",
 "c6_story": "Покупные Zigbee-стики Home Assistant узнаёт по имени USB-устройства, а все ESP32-C6 называются одинаково, поэтому самодельный координатор приходилось настраивать руками в конфигах. Моя интеграция спрашивает плату по протоколу ZBOSS, действительно ли это координатор, потом сама ставит и настраивает Zigbee2MQTT и перезапускает его, если стик вынули и вставили обратно. Прошивка от Espressif, заливается прямо со страницы, на компьютер ничего ставить не нужно.",
 "c6_proof": "На [странице прошивки](c6_live) есть ответы на частые вопросы, а в README описано, [как всё устроено](c6_how).",
 "c6_cap": "Страница прошивки: плата прошивается одной кнопкой.",
 "c6_alt": "Страница прошивки C6 Zigbee Stick с кнопкой установки",
 "c6_cta": "Прошить плату",
 "grbl_what": "Управление GRBL-гравером или фрезером по Wi-Fi: ESP32-S3 подключается к USB-порту станка, а LightBurn работает с ней по сети.",
 "grbl_story": "Любительским лазерным граверам и фрезерам 3018 нужен ноутбук на USB-кабеле прямо рядом со станком. Мост занимает место ноутбука: ESP32-S3 работает как USB host для собственного USB-чипа станка и без изменений передаёт GRBL на TCP-порт, поэтому LightBurn и Universal Gcode Sender работают как раньше. Если связь оборвётся посреди задания, мост остановит станок и выключит лазер. Сам станок переделывать не нужно, а в веб-панели есть большая кнопка СТОП и консоль GRBL.",
 "grbl_proof": "[Страница прошивки](grbl_live) за один раз прошивает плату и настраивает Wi-Fi и отвечает на частые вопросы, а в README описаны [правила безопасности](grbl_safety).",
 "grbl_cap": "Веб-панель моста. Всё на снимке — пример данных.",
 "grbl_alt": "Веб-панель GRBL Wi-Fi Bridge: состояние станка, кнопка СТОП и консоль GRBL",
 "grbl_cta": "Прошить плату",
 "how_h": "Как я работаю",
 "how": [
  "Я не пишу в README того, что не проверил сам. В лаборатории проверка заложена в сам метод, а остальные "
  "проекты проверяются автоматически на GitHub Actions.",
  "Мои проекты ничего о вас не собирают, в них нет ни аналитики, ни cookies, ни рекламы. Эта страница тоже "
  "ничего не загружает с чужих сайтов, и это видно по её исходному коду.",
  "Весь код открыт под лицензией MIT. Документацию я держу в актуальном состоянии, на вопросы и сообщения "
  "об ошибках отвечаю."],
 "stack_h": "С чем я работаю",
 "stack": ["Языки", "Базы данных", "Серверы и CI"],
 "contact_h": "Как со мной связаться",
 "contact": "Вопросы, ошибки и идеи пишите в issues нужного проекта: [Crypto Research Labs](crl_issues), "
            "[Telegram Bot Manager](tbm_issues), [My IP & Geo](myip_issues), [C6 Zigbee Stick](c6_issues), [GRBL Wi-Fi Bridge](grbl_issues). Отвечаю по-русски и по-английски.",
 "foot_privacy": "Эта страница не использует cookies и аналитику и ничего не загружает с других сайтов.",
 "foot_src": "Исходный код страницы",
 "nf_title": "Страница не найдена", "nf_text": "Такой страницы здесь нет. Возможно, она переехала.",
 "home": "На главную", "me": "Макс"},

"es": {
 "title": "Max (f1devbin): programador e ingeniero electrónico",
 "desc": "Max, programador e ingeniero electrónico. Código abierto: laboratorio de trading cripto, herramientas de Telegram, widget de KDE Plasma 6 y coordinador Zigbee para Home Assistant.",
 "og_line": "Programador e ingeniero electrónico", "job": "Ingeniero electrónico",
 "skip": "Saltar al contenido", "lang_label": "Idioma",
 "h1": "Hola, soy Max",
 "intro": [
  "Estudié programación y llevo muchos años trabajando como ingeniero electrónico. La mayor parte del software "
  "que escribo es para mí, para problemas con los que de verdad me encuentro.",
  "Cuando una herramienta resulta útil también para otras personas, la pulo, le escribo tests y documentación y "
  "la publico.",
  "Ah, y me encantan los gatos. Este, disfrazado de pingüino, vive en el icono de mi widget para KDE."],
 "cat_alt": "Un gato de dibujos animados disfrazado de pingüino señala el saludo",
 "projects_h": "Mis proyectos", "source": "Código fuente",
 "crl_what": "Un laboratorio abierto donde pruebo ideas de trading con criptomonedas y publico todos los "
             "resultados, también los fracasos.",
 "crl_story": "Todo empezó con mi propio bot de trading. Al reproducir sus 7649 señales con precios reales, "
              "resultó que acertaba la dirección peor que una moneda lanzada al aire. Por suerte, solo operaba en "
              "un exchange de pruebas. En vez de ajustarlo hasta que el backtest quedara bonito, monté un "
              "laboratorio donde ese truco no funciona: cada idea se escribe y se sella con un hash antes de "
              "probarla, las comisiones siempre se incluyen y GitHub Actions vuelve a comprobarlo todo con datos "
              "nuevos de forma periódica. La mayoría de las ideas fracasan, y los fracasos se documentan con el "
              "mismo cuidado que los aciertos.",
 "crl_proof": "La [metodología](crl_method) explica cómo se hace cada prueba, la [página de "
              "investigación](crl_findings) reúne todos los resultados y hay un [curso para "
              "principiantes](crl_course) en siete idiomas.",
 "crl_cap": "El panel el 28 de octubre de 2026.",
 "crl_alt": "Panel de Crypto Research Labs: 30 ideas de trading probadas, 2 aprobadas",
 "crl_cta": "Abrir el panel",
 "tbm_what": "Una página gratuita para configurar un bot de Telegram directamente en el navegador: webhooks, "
             "comandos, nombre y descripción, avatar, botón de menú y permisos de administrador.",
 "tbm_story": "Tengo varios bots propios, y cada cambio de webhook suponía otro comando curl con el token del bot "
              "escrito en la terminal. Ahora son un par de clics. La página no tiene servidor detrás: las "
              "peticiones van de tu navegador directamente a Telegram, el token se queda en la pestaña abierta "
              "salvo que le pidas al navegador que lo recuerde, y una política CSP estricta impide que se carguen "
              "scripts ajenos. Sin analítica ni contadores. Funciona en cinco idiomas y también en el móvil.",
 "tbm_proof": "Hay guías paso a paso para [configurar un webhook](tbm_set), [revisarlo con "
              "getWebhookInfo](tbm_info) y [eliminarlo](tbm_del), y sobre el [editor de comandos](tbm_cmd). Cómo se "
              "protege el token se explica en la sección de [privacidad y seguridad](tbm_privacy) del README, "
              "en inglés.",
 "tbm_cap": "Un bot de demostración: todos los datos de la captura son de ejemplo.",
 "tbm_alt": "Telegram Bot Manager: estado del webhook de un bot de demostración con su último error de entrega",
 "tbm_cta": "Abrir Bot Manager",
 "myip_what": "Un widget para KDE Plasma\u00a06: tu IP pública y país, interfaces locales, un escáner de red con "
              "escaneo de puertos, diagnóstico, test de velocidad, tráfico por aplicación y un monitor de "
              "dispositivos.",
 "myip_story": "Quería ver de un vistazo desde qué país salgo a internet y si la VPN está realmente activa. Con el "
               "tiempo, las herramientas que antes usaba en la terminal también se mudaron ahí. Cuando se cae la "
               "conexión, el diagnóstico te dice con palabras sencillas dónde se rompió la cadena: en la conexión, "
               "en el router, en el DNS o más allá. En Kubuntu no necesita permisos de root ni instalar nada "
               "extra, y no tiene telemetría.",
 "myip_proof": "Todos los servicios externos que consulta, y para qué, están en el [README](myip_privacy), "
               "en inglés.",
 "myip_cap": "La dirección de la captura pertenece a un servidor VPN.",
 "myip_alt": "Widget My IP & Geo: IP pública, ubicación, proveedor, carga del sistema y tráfico",
 "myip_cta": "Descargar el widget",
 "c6_what": "Convierte una placa ESP32-C6 económica en un coordinador Zigbee para Home Assistant: se flashea desde el navegador, se conecta y se pulsa «Añadir».",
 "c6_story": "Home Assistant reconoce los adaptadores Zigbee comerciales por su nombre USB, pero todas las ESP32-C6 muestran el mismo nombre genérico, así que un coordinador casero obligaba a editar la configuración a mano. Mi integración pregunta a la placa por el protocolo ZBOSS si de verdad es un coordinador, luego instala y configura Zigbee2MQTT por su cuenta y lo reinicia si el adaptador se desconecta y se vuelve a conectar. El firmware es de Espressif y se flashea desde la propia página, sin instalar nada en el ordenador.",
 "c6_proof": "La [página del firmware](c6_live) tiene preguntas frecuentes, y el README explica [cómo funciona](c6_how), en inglés.",
 "c6_cap": "La página del firmware: la placa se flashea con un botón.",
 "c6_alt": "Página del firmware de C6 Zigbee Stick con el botón de instalación",
 "c6_cta": "Flashear el firmware",
 "grbl_what": "Controla por Wi-Fi un grabador láser o una fresadora CNC con GRBL: un ESP32-S3 se conecta al puerto USB de la máquina y LightBurn se conecta a él por la red.",
 "grbl_story": "Los grabadores láser y las fresadoras 3018 domésticas piden un portátil con cable USB justo al lado. El puente ocupa el lugar del portátil: el ESP32-S3 actúa como host USB para el chip serie de la propia máquina y pasa GRBL a un puerto TCP sin cambios, así que LightBurn y Universal Gcode Sender funcionan como antes. Si la conexión se corta en mitad de un trabajo, detiene la máquina y apaga el láser. La máquina no necesita cambios, y el panel web tiene un gran botón STOP y una consola GRBL.",
 "grbl_proof": "La [página del firmware](grbl_live) graba la placa y configura el Wi-Fi de una vez y responde a las preguntas frecuentes; el README recoge las [reglas de seguridad](grbl_safety).",
 "grbl_cap": "El panel web del puente. Todo en la captura son datos de ejemplo.",
 "grbl_alt": "Panel web de GRBL Wi-Fi Bridge: estado de la máquina, botón STOP y consola GRBL",
 "grbl_cta": "Grabar el firmware",
 "how_h": "Cómo trabajo",
 "how": [
  "No escribo en un README nada que no haya comprobado yo mismo. En el laboratorio, la comprobación forma parte "
  "del método, y los demás proyectos se comprueban automáticamente en GitHub Actions.",
  "Mis proyectos no recopilan nada sobre ti: ni analítica, ni cookies, ni publicidad. Esta página tampoco carga "
  "nada de otros sitios, y su código fuente lo demuestra.",
  "Todo el código es abierto, con licencia MIT. Mantengo la documentación al día y respondo a preguntas "
  "e informes de errores."],
 "stack_h": "Con qué trabajo",
 "stack": ["Lenguajes", "Bases de datos", "Servidores y CI"],
 "contact_h": "Contacto",
 "contact": "Las preguntas, los errores y las ideas van a los issues de cada proyecto: [Crypto Research "
            "Labs](crl_issues), [Telegram Bot Manager](tbm_issues), [My IP & Geo](myip_issues), [C6 Zigbee Stick](c6_issues), [GRBL Wi-Fi Bridge](grbl_issues). Mi lengua materna es "
            "el ruso y el inglés también me va bien, pero puedes escribirme en español: usaré un traductor.",
 "foot_privacy": "Esta página no usa cookies ni analítica y no carga nada de otros sitios.",
 "foot_src": "Código fuente de la página",
 "nf_title": "Página no encontrada",
 "nf_text": "Aquí no hay ninguna página con esta dirección. Puede que se haya movido.",
 "home": "Ir a la página principal", "me": "Max"},

"pt": {
 "title": "Max (f1devbin): programador e engenheiro eletrônico",
 "desc": "Max, programador e engenheiro eletrônico. Código aberto: laboratório de trading cripto, ferramentas para Telegram, widget para KDE Plasma 6 e coordenador Zigbee para Home Assistant.",
 "og_line": "Programador e engenheiro eletrônico", "job": "Engenheiro eletrônico",
 "skip": "Pular para o conteúdo", "lang_label": "Idioma",
 "h1": "Oi, eu sou o Max",
 "intro": [
  "Sou formado em programação e trabalho há muitos anos como engenheiro eletrônico. A maior parte do software "
  "que escrevo é para mim mesmo, para problemas que eu realmente enfrento.",
  "Quando uma ferramenta se mostra útil para outras pessoas também, eu dou um acabamento, escrevo testes e "
  "documentação e publico.",
  "Ah, e eu adoro gatos. Este aqui, fantasiado de pinguim, mora no ícone do meu widget para KDE."],
 "cat_alt": "Um gato de desenho animado fantasiado de pinguim apontando para a saudação",
 "projects_h": "Meus projetos", "source": "Código-fonte",
 "crl_what": "Um laboratório aberto onde testo ideias de trading com criptomoedas e publico todos os "
             "resultados, inclusive os fracassos.",
 "crl_story": "Tudo começou com o meu próprio bot de trading. Quando reproduzi seus 7.649 sinais com preços reais, "
              "descobri que ele acertava a direção pior do que cara ou coroa. Ainda bem que ele só operava numa "
              "corretora de testes. Em vez de ajustá-lo até o backtest ficar bonito, montei um laboratório onde "
              "esse truque não funciona: cada ideia é escrita e selada com um hash antes do teste, as taxas sempre "
              "entram na conta e o GitHub Actions retesta tudo com dados novos periodicamente. A maioria das "
              "ideias fracassa, e os fracassos são descritos com o mesmo cuidado que os acertos.",
 "crl_proof": "A [metodologia](crl_method) explica como cada teste é feito, a [página de pesquisa](crl_findings) "
              "reúne todos os resultados e há um [curso para iniciantes](crl_course) em sete idiomas.",
 "crl_cap": "O painel em 28 de outubro de 2026.",
 "crl_alt": "Painel do Crypto Research Labs: 30 ideias de trading testadas, 2 aprovadas",
 "crl_cta": "Abrir o painel",
 "tbm_what": "Uma página gratuita para configurar um bot do Telegram direto no navegador: webhooks, comandos, "
             "nome e descrição, avatar, botão de menu e permissões de administrador.",
 "tbm_story": "Tenho vários bots próprios, e cada mudança de webhook significava mais um comando curl com o token "
              "do bot digitado no terminal. Agora são poucos cliques. Não há servidor por trás da página: as "
              "requisições vão do seu navegador direto para o Telegram, o token fica só na aba aberta, a menos que "
              "você peça ao navegador para lembrá-lo, e uma política CSP rígida impede scripts de fora. Sem "
              "analytics, sem contadores. Funciona em cinco idiomas e no celular.",
 "tbm_proof": "Há guias passo a passo para [configurar um webhook](tbm_set), [verificá-lo com "
              "getWebhookInfo](tbm_info) e [excluí-lo](tbm_del), além do [editor de comandos](tbm_cmd). Como o token "
              "é protegido está na seção de [privacidade e segurança](tbm_privacy) do README, em inglês.",
 "tbm_cap": "Um bot de demonstração: todos os dados da captura são fictícios.",
 "tbm_alt": "Telegram Bot Manager: status do webhook de um bot de demonstração com o último erro de entrega",
 "tbm_cta": "Abrir o Bot Manager",
 "myip_what": "Um widget para KDE Plasma\u00a06: seu IP público e país, interfaces locais, um scanner de rede com "
              "varredura de portas, diagnóstico, teste de velocidade, tráfego por aplicativo e um monitor de "
              "dispositivos.",
 "myip_story": "Eu queria ver de relance de que país estou saindo para a internet e se a VPN está mesmo ligada. Com "
               "o tempo, as ferramentas que eu rodava no terminal também foram parar lá. Quando a internet cai, o "
               "diagnóstico diz em palavras simples onde a corrente se rompeu: na conexão, no roteador, no DNS ou "
               "mais adiante. No Kubuntu ele não precisa de root nem de pacotes extras, e não tem telemetria.",
 "myip_proof": "Todos os serviços externos que ele consulta, e para quê, estão listados no [README](myip_privacy), "
               "em inglês.",
 "myip_cap": "O endereço na captura pertence a um servidor VPN.",
 "myip_alt": "Widget My IP & Geo: IP público, localização, provedor, carga do sistema e tráfego",
 "myip_cta": "Baixar o widget",
 "c6_what": "Transforma uma placa ESP32-C6 barata em um coordenador Zigbee para o Home Assistant: grave pelo navegador, conecte e toque em “Adicionar”.",
 "c6_story": "O Home Assistant reconhece os adaptadores Zigbee comprados prontos pelo nome USB, mas toda ESP32-C6 mostra o mesmo nome genérico, então um coordenador caseiro exigia editar configurações à mão. Minha integração pergunta à placa, pelo protocolo ZBOSS, se ela é mesmo um coordenador, depois instala e configura o Zigbee2MQTT sozinha e o reinicia se o adaptador for desconectado e conectado de novo. O firmware é da Espressif e é gravado direto da página, sem instalar nada no computador.",
 "c6_proof": "A [página do firmware](c6_live) tem perguntas frequentes, e o README explica [como funciona](c6_how), em inglês.",
 "c6_cap": "A página do firmware: a placa é gravada com um botão.",
 "c6_alt": "Página do firmware do C6 Zigbee Stick com o botão de instalação",
 "c6_cta": "Gravar o firmware",
 "grbl_what": "Controle pelo Wi-Fi uma gravadora a laser ou uma fresadora CNC com GRBL: um ESP32-S3 se conecta à porta USB da máquina e o LightBurn se conecta a ele pela rede.",
 "grbl_story": "Gravadoras a laser e fresadoras 3018 caseiras pedem um notebook com cabo USB bem ao lado. A ponte ocupa o lugar do notebook: o ESP32-S3 atua como host USB para o chip serial da própria máquina e repassa o GRBL para uma porta TCP sem alterações, então o LightBurn e o Universal Gcode Sender funcionam como antes. Se a conexão cair no meio de um trabalho, ela para a máquina e desliga o laser. A máquina não precisa de mudanças, e o painel web tem um grande botão STOP e um console GRBL.",
 "grbl_proof": "A [página do firmware](grbl_live) grava a placa e configura o Wi-Fi de uma vez e responde às perguntas frequentes; o README traz as [regras de segurança](grbl_safety).",
 "grbl_cap": "O painel web da ponte. Tudo na captura são dados de exemplo.",
 "grbl_alt": "Painel web do GRBL Wi-Fi Bridge: estado da máquina, botão STOP e console GRBL",
 "grbl_cta": "Gravar o firmware",
 "how_h": "Como eu trabalho",
 "how": [
  "Não escrevo num README nada que eu mesmo não tenha verificado. No laboratório, a verificação faz parte do "
  "método, e os outros projetos são verificados automaticamente no GitHub Actions.",
  "Meus projetos não coletam nada sobre você: nada de analytics, cookies ou anúncios. Esta página também não "
  "carrega nada de outros sites, e o código-fonte dela mostra isso.",
  "Todo o código é aberto, sob a licença MIT. Mantenho a documentação atualizada e respondo a dúvidas e relatos "
  "de bugs."],
 "stack_h": "Com o que eu trabalho",
 "stack": ["Linguagens", "Bancos de dados", "Servidores e CI"],
 "contact_h": "Contato",
 "contact": "Dúvidas, bugs e ideias vão para as issues de cada projeto: [Crypto Research Labs](crl_issues), "
            "[Telegram Bot Manager](tbm_issues), [My IP & Geo](myip_issues), [C6 Zigbee Stick](c6_issues), [GRBL Wi-Fi Bridge](grbl_issues). Minha língua materna é o russo, e inglês "
            "também serve, mas pode escrever em português: eu uso um tradutor.",
 "foot_privacy": "Esta página não usa cookies nem analytics e não carrega nada de outros sites.",
 "foot_src": "Código-fonte da página",
 "nf_title": "Página não encontrada",
 "nf_text": "Não existe nenhuma página neste endereço. Talvez ela tenha mudado de lugar.",
 "home": "Ir para a página inicial", "me": "Max"},

"tr": {
 "title": "Max (f1devbin): programcı ve elektronik mühendisi",
 "desc": "Max, programcı ve elektronik mühendisi. Açık kaynak: kripto araştırma laboratuvarı, Telegram araçları, KDE Plasma 6 bileşeni ve Home Assistant için Zigbee koordinatörü.",
 "og_line": "Programcı ve elektronik mühendisi", "job": "Elektronik mühendisi",
 "skip": "İçeriğe geç", "lang_label": "Dil",
 "h1": "Merhaba, ben Max",
 "intro": [
  "Programcılık eğitimi aldım ve uzun yıllardır elektronik mühendisi olarak çalışıyorum. Yazdığım yazılımların "
  "çoğu kendim için; gerçekten karşılaştığım sorunlara çözüm olarak doğuyor.",
  "Bir araç başkalarının da işine yarayacak gibi olursa onu toparlıyor, testlerini ve belgelerini yazıp "
  "yayımlıyorum.",
  "Bir de kedileri çok severim. Penguen kostümlü bu kedi, KDE bileşenimin simgesinde yaşıyor."],
 "cat_alt": "Penguen kostümlü, selamlamayı gösteren çizgi film kedisi",
 "projects_h": "Projelerim", "source": "Kaynak kod",
 "crl_what": "Kripto para işlem fikirlerini test ettiğim ve başarısız olanlar dahil tüm sonuçları yayımladığım "
             "açık bir laboratuvar.",
 "crl_story": "Her şey kendi işlem botumla başladı. 7.649 sinyalini gerçek fiyatlarla yeniden oynattığımda, yönü "
              "yazı turadan daha kötü tahmin ettiği ortaya çıktı. Neyse ki yalnızca test borsasında işlem "
              "yapıyordu. Backtest güzel görünene kadar ayarlarıyla oynamak yerine, bu numaranın işlemediği bir "
              "laboratuvar kurdum: her fikir test edilmeden önce yazılıp bir hash ile mühürleniyor, komisyonlar "
              "her zaman hesaba katılıyor ve GitHub Actions her şeyi düzenli aralıklarla yeni verilerle yeniden "
              "test ediyor. Fikirlerin çoğu testi geçemiyor ve başarısızlıklar da başarılar kadar özenle yazılıyor.",
 "crl_proof": "Testlerin nasıl yapıldığı [yöntem](crl_method) bölümünde anlatılıyor, tüm sonuçlar [araştırma "
              "sayfasında](crl_findings) toplanıyor, yeni başlayanlar için de yedi dilde bir [kurs](crl_course) var.",
 "crl_cap": "Panel, 28 Ekim 2026.",
 "crl_alt": "Crypto Research Labs paneli: 30 işlem fikri test edildi, 2'si geçti",
 "crl_cta": "Paneli aç",
 "tbm_what": "Bir Telegram botunu doğrudan tarayıcıdan ayarlamak için ücretsiz bir sayfa: webhook'lar, komutlar, "
             "ad ve açıklama, avatar, menü düğmesi ve yönetici hakları.",
 "tbm_story": "Birkaç botum var ve her webhook değişikliği, botun token'ını terminale yazdığım bir curl komutu daha "
              "demekti. Artık birkaç tıklama yetiyor. Sayfanın arkasında sunucu yok: istekler tarayıcınızdan "
              "doğrudan Telegram'a gidiyor, siz tarayıcıdan hatırlamasını istemedikçe token yalnızca açık sekmede "
              "kalıyor ve sıkı bir CSP politikası dışarıdan betiklerin sayfaya girmesine izin vermiyor. Analitik "
              "yok, sayaç yok. Beş dilde ve telefonda çalışıyor.",
 "tbm_proof": "İngilizce adım adım kılavuzlar var: [webhook ayarlama](tbm_set), [getWebhookInfo ile "
              "kontrol](tbm_info), [webhook silme](tbm_del) ve [komut düzenleyici](tbm_cmd). Token'ın nasıl "
              "korunduğu README'nin [gizlilik ve güvenlik](tbm_privacy) bölümünde anlatılıyor.",
 "tbm_cap": "Demo bot: ekran görüntüsündeki tüm veriler örnek.",
 "tbm_alt": "Telegram Bot Manager: bir demo botun webhook durumu ve son teslim hatası",
 "tbm_cta": "Bot Manager'ı aç",
 "myip_what": "KDE Plasma\u00a06 için bir bileşen: genel IP adresiniz ve ülkeniz, yerel ağ arayüzleri, port taramalı "
              "ağ tarayıcı, tanılama, hız testi, uygulama başına trafik ve cihaz izleyici.",
 "myip_story": "İnternete hangi ülkeden çıktığımı ve VPN'in gerçekten açık olup olmadığını tek bakışta görmek "
               "istiyordum. Zamanla terminalde çalıştırdığım araçlar da oraya taşındı. İnternet kesildiğinde "
               "tanılama, zincirin nerede koptuğunu sade bir dille söylüyor: bağlantıda mı, yönlendiricide mi, "
               "DNS'te mi, yoksa daha ileride mi. Kubuntu'da root yetkisi ya da ek paket gerektirmiyor, telemetri "
               "de yok.",
 "myip_proof": "Bağlandığı tüm dış servisler ve nedenleri [README](myip_privacy) dosyasında listeleniyor "
               "(İngilizce).",
 "myip_cap": "Ekran görüntüsündeki adres bir VPN sunucusuna ait.",
 "myip_alt": "My IP & Geo bileşeni: genel IP, konum, sağlayıcı, sistem yükü ve trafik",
 "myip_cta": "Bileşeni indir",
 "c6_what": "Ucuz bir ESP32-C6 kartını Home Assistant için Zigbee koordinatörüne çevirir: tarayıcıdan yazılımı yükleyin, takın, “Ekle”ye basın.",
 "c6_story": "Home Assistant hazır Zigbee çubuklarını USB adlarından tanır, ama her ESP32-C6 aynı genel adı gösterir; bu yüzden ev yapımı bir koordinatör için yapılandırmayı elle düzenlemek gerekiyordu. Entegrasyonum karta ZBOSS protokolüyle gerçekten koordinatör olup olmadığını sorar, ardından Zigbee2MQTT’yi kendisi kurup ayarlar ve çubuk çıkarılıp yeniden takılırsa onu yeniden başlatır. Yazılım Espressif’in; doğrudan sayfadan yüklenir, bilgisayara bir şey kurmak gerekmez.",
 "c6_proof": "[Yazılım sayfasında](c6_live) sık sorulan sorular var, README de [nasıl çalıştığını](c6_how) İngilizce anlatıyor.",
 "c6_cap": "Yazılım sayfası: kart tek düğmeyle programlanır.",
 "c6_alt": "C6 Zigbee Stick yazılım sayfası ve yükleme düğmesi",
 "c6_cta": "Yazılımı yükle",
 "grbl_what": "GRBL lazer kazıma makinesini veya CNC frezeyi Wi-Fi üzerinden kullanın: ESP32-S3 makinenin USB portuna takılır, LightBurn ona ağ üzerinden bağlanır.",
 "grbl_story": "Hobi lazer kazıma makineleri ve 3018 frezeler yanı başlarında USB kablolu bir dizüstü bilgisayar ister. Köprü bu bilgisayarın yerini alır: ESP32-S3, makinenin kendi seri çipi için USB host olarak çalışır ve GRBL’i değiştirmeden bir TCP portuna aktarır; böylece LightBurn ve Universal Gcode Sender eskisi gibi çalışır. Bağlantı bir işin ortasında koparsa makineyi durdurur ve lazeri kapatır. Makinede değişiklik gerekmez; web panelinde büyük bir STOP düğmesi ve GRBL konsolu vardır.",
 "grbl_proof": "[Yazılım sayfası](grbl_live) kartı yazar ve Wi-Fi’yi tek seferde kurar, sık sorulan soruları yanıtlar; README’de [güvenlik kuralları](grbl_safety) yer alır.",
 "grbl_cap": "Köprünün web paneli. Ekran görüntüsündeki her şey örnek veridir.",
 "grbl_alt": "GRBL Wi-Fi Bridge web paneli: makine durumu, STOP düğmesi ve GRBL konsolu",
 "grbl_cta": "Yazılımı yükle",
 "how_h": "Nasıl çalışıyorum",
 "how": [
  "Kendim kontrol etmediğim hiçbir şeyi README'ye yazmam. Laboratuvarda kontrol yöntemin bir parçası; diğer "
  "projeler ise GitHub Actions üzerinde otomatik olarak kontrol ediliyor.",
  "Projelerim sizin hakkınızda hiçbir şey toplamaz: analitik, çerez ya da reklam yok. Bu sayfa da başka "
  "sitelerden hiçbir şey yüklemiyor, kaynak kodu da bunu gösteriyor.",
  "Kodun tamamı MIT lisansıyla açık. Belgeleri güncel tutuyor, sorulara ve hata bildirimlerine yanıt veriyorum."],
 "stack_h": "Neyle çalışıyorum",
 "stack": ["Diller", "Veritabanları", "Sunucular ve CI"],
 "contact_h": "İletişim",
 "contact": "Sorular, hata bildirimleri ve fikirler için ilgili projenin issue bölümünü kullanın: [Crypto Research "
            "Labs](crl_issues), [Telegram Bot Manager](tbm_issues), [My IP & Geo](myip_issues), [C6 Zigbee Stick](c6_issues), [GRBL Wi-Fi Bridge](grbl_issues). Ana dilim Rusça, "
            "İngilizce de olur; Türkçe de yazabilirsiniz, çeviri aracı kullanırım.",
 "foot_privacy": "Bu sayfa çerez ya da analitik kullanmaz ve başka sitelerden hiçbir şey yüklemez.",
 "foot_src": "Sayfanın kaynak kodu",
 "nf_title": "Sayfa bulunamadı", "nf_text": "Burada böyle bir sayfa yok. Taşınmış olabilir.",
 "home": "Ana sayfaya git", "me": "Max"},

"vi": {
 "title": "Max (f1devbin): lập trình viên và kỹ sư điện tử",
 "desc": "Max, lập trình viên và kỹ sư điện tử. Mã nguồn mở: phòng thí nghiệm giao dịch crypto, công cụ Telegram, tiện ích KDE Plasma 6 và bộ điều phối Zigbee cho Home Assistant.",
 "og_line": "Lập trình viên và kỹ sư điện tử", "job": "Kỹ sư điện tử",
 "skip": "Chuyển đến nội dung", "lang_label": "Ngôn ngữ",
 "h1": "Xin chào, tôi là Max",
 "intro": [
  "Tôi học ngành lập trình và đã làm kỹ sư điện tử nhiều năm. Phần lớn phần mềm tôi viết là cho chính mình, để "
  "giải quyết những vấn đề tôi thật sự gặp phải.",
  "Khi một công cụ hóa ra cũng có ích cho người khác, tôi chỉn chu lại nó, viết kiểm thử và tài liệu rồi công "
  "khai.",
  "À, tôi còn rất mê mèo. Chú mèo mặc đồ chim cánh cụt này sống trong biểu tượng của tiện ích KDE mà tôi làm."],
 "cat_alt": "Chú mèo hoạt hình mặc đồ chim cánh cụt đang chỉ vào lời chào",
 "projects_h": "Dự án của tôi", "source": "Mã nguồn",
 "crl_what": "Một phòng thí nghiệm mở, nơi tôi kiểm tra các ý tưởng giao dịch tiền mã hóa và công bố mọi kết quả, "
             "kể cả thất bại.",
 "crl_story": "Mọi chuyện bắt đầu từ con bot giao dịch của chính tôi. Khi chạy lại 7.649 tín hiệu của nó trên giá "
              "thật, hóa ra nó đoán hướng giá còn tệ hơn tung đồng xu. May mà nó chỉ giao dịch trên sàn thử "
              "nghiệm. Thay vì chỉnh nó cho đến khi backtest trông đẹp, tôi dựng một phòng thí nghiệm mà ở đó mẹo "
              "này không còn tác dụng: mỗi ý tưởng được viết ra và niêm phong bằng hash trước khi kiểm tra, phí "
              "giao dịch luôn được tính, và GitHub Actions định kỳ kiểm tra lại mọi thứ trên dữ liệu mới. Phần lớn "
              "ý tưởng không vượt qua, và những thất bại được ghi lại cẩn thận chẳng kém gì thành công.",
 "crl_proof": "Cách thực hiện mỗi phép kiểm tra được giải thích trong phần [phương pháp](crl_method), mọi kết quả "
              "nằm ở [trang nghiên cứu](crl_findings), và còn có [khóa học cho người mới](crl_course) bằng bảy "
              "ngôn ngữ.",
 "crl_cap": "Bảng điều khiển ngày 28/10/2026.",
 "crl_alt": "Bảng điều khiển Crypto Research Labs: đã kiểm tra 30 ý tưởng giao dịch, 2 ý tưởng đạt",
 "crl_cta": "Mở bảng điều khiển",
 "tbm_what": "Một trang miễn phí để thiết lập bot Telegram ngay trên trình duyệt: webhook, lệnh, tên và mô tả, "
             "ảnh đại diện, nút menu và quyền quản trị.",
 "tbm_story": "Tôi có vài con bot riêng, và trước đây mỗi lần đổi webhook lại phải gõ thêm một lệnh curl kèm token "
              "của bot vào terminal. Giờ chỉ cần vài cú nhấp. Trang này không có máy chủ phía sau: yêu cầu đi thẳng "
              "từ trình duyệt của bạn đến Telegram, token chỉ nằm trong tab đang mở trừ khi bạn bảo trình duyệt "
              "ghi nhớ, và chính sách CSP nghiêm ngặt không cho script bên ngoài chạy trên trang. Không có công "
              "cụ phân tích, không có bộ đếm. Trang có năm ngôn ngữ và dùng tốt trên điện thoại.",
 "tbm_proof": "Có hướng dẫn từng bước (tiếng Anh): [thiết lập webhook](tbm_set), [kiểm tra bằng "
              "getWebhookInfo](tbm_info), [xóa webhook](tbm_del) và [trình sửa lệnh bot](tbm_cmd). Cách token được "
              "bảo vệ có trong phần [quyền riêng tư và bảo mật](tbm_privacy) của README.",
 "tbm_cap": "Bot minh họa: mọi dữ liệu trong ảnh đều là ví dụ.",
 "tbm_alt": "Telegram Bot Manager: trạng thái webhook của một bot minh họa và lỗi gửi gần nhất",
 "tbm_cta": "Mở Bot Manager",
 "myip_what": "Tiện ích cho KDE Plasma\u00a06: IP công khai và quốc gia của bạn, các giao diện mạng cục bộ, trình "
              "quét mạng kèm quét cổng, chẩn đoán, đo tốc độ, lưu lượng theo ứng dụng và giám sát thiết bị.",
 "myip_story": "Tôi muốn liếc qua là biết mình đang ra internet từ nước nào và VPN có thật sự bật hay không. Dần "
               "dần, các công cụ tôi từng chạy trong terminal cũng chuyển hết vào đó. Khi mất mạng, phần chẩn đoán "
               "cho bạn biết bằng lời dễ hiểu chuỗi kết nối bị đứt ở đâu: ở kết nối, ở router, ở DNS hay xa hơn "
               "nữa. Trên Kubuntu, nó không cần quyền root, không cần cài thêm gì và không có telemetry.",
 "myip_proof": "Mọi dịch vụ bên ngoài mà nó kết nối, cùng lý do, đều được liệt kê trong [README](myip_privacy) "
               "(tiếng Anh).",
 "myip_cap": "Địa chỉ trong ảnh thuộc về một máy chủ VPN.",
 "myip_alt": "Tiện ích My IP & Geo: IP công khai, vị trí, nhà cung cấp, tải hệ thống và lưu lượng",
 "myip_cta": "Tải tiện ích",
 "c6_what": "Biến một bo mạch ESP32-C6 giá rẻ thành bộ điều phối Zigbee cho Home Assistant: nạp firmware từ trình duyệt, cắm vào, bấm “Thêm”.",
 "c6_story": "Home Assistant nhận ra các USB Zigbee mua sẵn qua tên USB của chúng, nhưng mọi ESP32-C6 đều báo cùng một tên chung, nên trước đây bộ điều phối tự làm phải sửa cấu hình bằng tay. Tích hợp của tôi hỏi bo mạch qua giao thức ZBOSS xem nó có thật là bộ điều phối không, rồi tự cài và cấu hình Zigbee2MQTT, và khởi động lại nó nếu USB bị rút ra rồi cắm lại. Firmware là của Espressif, được nạp ngay từ trang web, không cần cài gì lên máy tính.",
 "c6_proof": "[Trang firmware](c6_live) có phần hỏi đáp, còn README giải thích [cách hoạt động](c6_how) bằng tiếng Anh.",
 "c6_cap": "Trang firmware: chỉ một nút là nạp xong bo mạch.",
 "c6_alt": "Trang firmware của C6 Zigbee Stick với nút cài đặt",
 "c6_cta": "Nạp firmware",
 "grbl_what": "Điều khiển máy khắc laser hoặc máy phay CNC chạy GRBL qua Wi-Fi: ESP32-S3 cắm vào cổng USB của máy, còn LightBurn kết nối với nó qua mạng.",
 "grbl_story": "Máy khắc laser và máy phay 3018 dân dụng cần một chiếc laptop nối cáp USB ngay bên cạnh. Cầu nối thay chỗ chiếc laptop đó: ESP32-S3 làm USB host cho chip serial của chính máy và chuyển GRBL sang một cổng TCP nguyên vẹn, nên LightBurn và Universal Gcode Sender vẫn hoạt động như trước. Nếu kết nối bị ngắt giữa chừng, nó dừng máy và tắt laser. Máy không cần sửa đổi gì, và bảng điều khiển web có nút STOP lớn cùng console GRBL.",
 "grbl_proof": "[Trang firmware](grbl_live) nạp firmware và cài Wi-Fi trong một lần, kèm phần hỏi đáp; README nêu [các quy tắc an toàn](grbl_safety).",
 "grbl_cap": "Bảng điều khiển web của cầu nối. Mọi thứ trong ảnh là dữ liệu mẫu.",
 "grbl_alt": "Bảng điều khiển web GRBL Wi-Fi Bridge: trạng thái máy, nút STOP và console GRBL",
 "grbl_cta": "Nạp firmware",
 "how_h": "Cách tôi làm việc",
 "how": [
  "Tôi không ghi vào README điều gì mà mình chưa tự kiểm tra. Ở phòng thí nghiệm, việc kiểm tra là một phần của "
  "phương pháp; các dự án khác được kiểm tra tự động trên GitHub Actions.",
  "Các dự án của tôi không thu thập gì về bạn: không công cụ phân tích, không cookie, không quảng cáo. Trang này "
  "cũng không tải gì từ trang web khác, và mã nguồn của nó cho thấy điều đó.",
  "Toàn bộ mã nguồn mở theo giấy phép MIT. Tôi luôn cập nhật tài liệu và trả lời câu hỏi cũng như báo lỗi."],
 "stack_h": "Công cụ tôi dùng",
 "stack": ["Ngôn ngữ", "Cơ sở dữ liệu", "Máy chủ và CI"],
 "contact_h": "Liên hệ",
 "contact": "Câu hỏi, báo lỗi và ý tưởng xin gửi vào mục issues của từng dự án: [Crypto Research Labs](crl_issues), "
            "[Telegram Bot Manager](tbm_issues), [My IP & Geo](myip_issues), [C6 Zigbee Stick](c6_issues), [GRBL Wi-Fi Bridge](grbl_issues). Tiếng mẹ đẻ của tôi là tiếng Nga, tiếng "
            "Anh cũng được, và bạn cứ viết bằng tiếng Việt, tôi sẽ dùng công cụ dịch.",
 "foot_privacy": "Trang này không dùng cookie hay công cụ phân tích và không tải gì từ trang web khác.",
 "foot_src": "Mã nguồn của trang",
 "nf_title": "Không tìm thấy trang", "nf_text": "Ở đây không có trang này. Có thể nó đã được chuyển đi.",
 "home": "Về trang chủ", "me": "Max"},

"zh": {
 "title": "Max（f1devbin）：程序员、电子工程师",
 "desc": "我是 Max，程序员、电子工程师。开源项目：加密货币交易研究实验室、Telegram 工具、KDE Plasma 6 小部件，以及 Home Assistant 用的 Zigbee 协调器。",
 "og_line": "程序员、电子工程师", "job": "电子工程师",
 "skip": "跳到正文", "lang_label": "语言",
 "h1": "你好，我是 Max",
 "intro": [
  "我学的是编程，做电子工程师已经很多年了。我写的软件大多是给自己用的，为了解决自己真正遇到的问题。",
  "如果某个工具对别人也有用，我就把它整理好，写上测试和文档，公开发布。",
  "对了，我很喜欢猫。这只穿企鹅服的猫，就住在我那个 KDE 小部件的图标里。"],
 "cat_alt": "一只穿着企鹅服的卡通猫，正用爪子指向问候语",
 "projects_h": "我的项目", "source": "源代码",
 "crl_what": "一个开放的实验室：我在这里检验加密货币交易想法，并公开所有结果，包括失败的。",
 "crl_story": "一切始于我自己的交易机器人。我用真实价格回放了它的 7649 个信号，结果发现它判断方向还不如抛硬币。"
              "好在它只在测试交易所里交易过。我没有去调参数直到回测曲线变好看，而是搭了一个让这种把戏行不通的实验室："
              "每个想法在检验之前先写下来，并用哈希值封存；手续费一律计入；GitHub Actions 定期用新数据把所有想法"
              "重新检验一遍。大多数想法没能通过，失败的结果和成功的一样被认真记录。",
 "crl_proof": "检验怎么做写在[方法说明](crl_method)里，全部结果汇总在[研究页面](crl_findings)上，另外还有一门"
              "七种语言的[新手课程](crl_course)。",
 "crl_cap": "2026 年 10 月 28 日的仪表盘。",
 "crl_alt": "Crypto Research Labs 仪表盘：已检验 30 个交易想法，2 个通过",
 "crl_cta": "打开仪表盘",
 "tbm_what": "一个免费网页，直接在浏览器里设置 Telegram 机器人：webhook、命令、名称和简介、头像、菜单按钮和"
             "管理员权限。",
 "tbm_story": "我自己有好几个机器人，以前每改一次 webhook，就得在终端里再敲一条带着机器人 token 的 curl 命令。"
              "现在点几下就行。这个页面背后没有服务器：请求从你的浏览器直接发往 Telegram；除非你让浏览器记住，"
              "token 只保存在当前标签页里；严格的 CSP 策略不让外部脚本进入页面。没有统计分析，也没有计数器。"
              "支持五种语言，手机上也能用。",
 "tbm_proof": "还有分步指南：[设置 Webhook](tbm_set)、[用 getWebhookInfo 检查](tbm_info)、[删除 Webhook](tbm_del)，"
              "以及[机器人命令编辑器](tbm_cmd)。token 如何受到保护，见 README 的[隐私与安全](tbm_privacy)一节（英文）。",
 "tbm_cap": "演示机器人：截图中的数据都是示例。",
 "tbm_alt": "Telegram Bot Manager：演示机器人的 webhook 状态和最近一次投递错误",
 "tbm_cta": "打开 Bot Manager",
 "myip_what": "一个 KDE Plasma\u00a06 小部件：显示你的公网 IP 和所在国家、本地网络接口，还有带端口扫描的网络扫描器、"
              "诊断、测速、按应用统计流量和设备监控。",
 "myip_story": "我想一眼就看到自己是从哪个国家连上互联网的，以及 VPN 是不是真的开着。后来，我以前在终端里运行的"
               "那些工具也陆续搬了进来。断网时，诊断功能会用大白话告诉你链路断在哪里：本机连接、路由器、DNS，"
               "还是更远的地方。在 Kubuntu 上它不需要 root 权限，不用额外安装任何东西，也没有遥测。",
 "myip_proof": "它会连接哪些外部服务、为什么连接，都列在 [README](myip_privacy) 里（英文）。",
 "myip_cap": "截图中的地址属于一台 VPN 服务器。",
 "myip_alt": "My IP & Geo 小部件：公网 IP、位置、运营商、系统负载和流量",
 "myip_cta": "下载小部件",
 "c6_what": "把一块便宜的 ESP32-C6 开发板变成 Home Assistant 的 Zigbee 协调器：在浏览器里刷固件，插上 USB，点“添加”。",
 "c6_story": "Home Assistant 靠 USB 名称识别现成的 Zigbee 适配器，但所有 ESP32-C6 报出的都是同一个通用名称，所以自制协调器以前只能手动改配置。我的集成会通过 ZBOSS 协议询问开发板是否真的是协调器，然后自动安装并配置 Zigbee2MQTT，适配器拔下再插上时还会自动重启它。固件来自 Espressif，直接在网页上刷写，电脑上什么都不用装。",
 "c6_proof": "[固件页面](c6_live)有常见问题解答，README 用英文说明了[工作原理](c6_how)。",
 "c6_cap": "固件页面：一个按钮就能刷好开发板。",
 "c6_alt": "C6 Zigbee Stick 固件页面和安装按钮",
 "c6_cta": "刷写固件",
 "grbl_what": "通过 Wi-Fi 控制 GRBL 激光雕刻机或 CNC 雕铣机：把 ESP32-S3 插到机器的 USB 口上，LightBurn 通过网络连接它。",
 "grbl_story": "家用激光雕刻机和 3018 雕铣机都需要旁边放一台插着 USB 线的笔记本。这个桥接器取代了那台笔记本：ESP32-S3 作为 USB 主机连接机器自带的串口芯片，把 GRBL 原样转发到 TCP 端口，所以 LightBurn 和 Universal Gcode Sender 照常可用。如果任务进行中连接断开，它会停下机器并关闭激光。机器本身无需改动，网页面板上有一个大大的 STOP 按钮和 GRBL 控制台。",
 "grbl_proof": "[固件页面](grbl_live)一次完成烧录和 Wi-Fi 设置，并解答常见问题；README 里写明了[安全规则](grbl_safety)。",
 "grbl_cap": "桥接器的网页面板。截图中的内容都是示例数据。",
 "grbl_alt": "GRBL Wi-Fi Bridge 网页面板：机器状态、STOP 按钮和 GRBL 控制台",
 "grbl_cta": "烧录固件",
 "how_h": "我怎么做事",
 "how": [
  "我不会在 README 里写任何自己没验证过的东西。在实验室里，验证本身就是方法的一部分；其他项目都在 "
  "GitHub Actions 上自动检查。",
  "我的项目不收集你的任何信息：没有统计分析，没有 cookie，没有广告。这个页面也不从其他网站加载任何内容，"
  "看源代码就知道。",
  "所有代码都以 MIT 许可证开源。我会及时更新文档，也会回复提问和错误报告。"],
 "stack_h": "我用的技术",
 "stack": ["语言", "数据库", "服务器与 CI"],
 "contact_h": "联系我",
 "contact": "问题、错误报告和想法，请提交到对应项目的 issues：[Crypto Research Labs](crl_issues)、"
            "[Telegram Bot Manager](tbm_issues)、[My IP & Geo](myip_issues)、[C6 Zigbee Stick](c6_issues)、[GRBL Wi-Fi Bridge](grbl_issues)。我的母语是俄语，英语也可以；"
            "用中文写也没问题，我会用翻译工具。",
 "foot_privacy": "本页面不使用 cookie 和统计分析，也不从其他网站加载任何内容。",
 "foot_src": "本页面的源代码",
 "nf_title": "页面不存在", "nf_text": "这里没有这个页面，它可能已经搬走了。", "home": "返回首页", "me": "Max"},
}

STACK = ["PHP\u00a08, Python, JavaScript, QML", "MariaDB, SQLite", "Ubuntu, Armbian, Nginx, systemd, GitHub Actions"]

# fontsource subsets of IBM Plex Sans; the browser downloads only the ones a page uses
FONT_RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,"
             "U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latin-ext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
                 "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
    "cyrillic": "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116",
    "vietnamese": "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,"
                  "U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB",
}
PRELOAD = {"ru": "cyrillic", "vi": "vietnamese"}  # the first font each page needs; latin for the rest

CSS = """
:root{--bg:#0f1b2d;--rule:#33496b;--text:#fff;--text2:#dce6f3;--link:#8fd0ff;--accent:#ffb547;--btn:#8fd0ff;
--btn-text:#0b1626;--shadow:rgba(0,0,0,.5);color-scheme:dark}
@media (prefers-color-scheme:light){:root{--bg:#f7f9fc;--rule:#bccadb;--text:#0a1424;--text2:#1d2d43;
--link:#084a8e;--accent:#9a4a00;--btn:#084a8e;--btn-text:#fff;--shadow:rgba(16,32,64,.32);color-scheme:light}}
*,*::before,*::after{box-sizing:border-box}
html{font-size:112.5%;-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text2);
font:400 1rem/1.65 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif}
html[lang="zh-Hans"] body{font-family:"IBM Plex Sans","PingFang SC","Hiragino Sans GB","Microsoft YaHei",
"Noto Sans CJK SC","Source Han Sans SC",sans-serif;line-height:1.75}
html[lang="zh-Hans"] h1{word-break:keep-all}
h1,h2,h3{color:var(--text);font-weight:700;text-wrap:balance}
p{text-wrap:pretty}
a{color:var(--link);text-decoration-thickness:1px;text-underline-offset:.2em}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:2px}
.wrap{max-width:62rem;margin:0 auto;padding:0 1.25rem}
.skip{position:absolute;left:-100vw;top:.5rem}
.skip:focus{left:1rem;z-index:2;background:var(--bg);color:var(--text);padding:.5rem 1rem}
.top{border-bottom:1px solid var(--rule)}
.top .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0 1.5rem;
padding-top:.5rem;padding-bottom:.5rem}
.brand{padding:.4rem 0;font-size:1.05rem;font-weight:700;color:var(--text);text-decoration:none}
.brand:hover{text-decoration:underline}
.langs{display:flex;flex-wrap:wrap;gap:0 1rem;margin:0;padding:0;list-style:none;font-size:.9rem}
.langs a{display:inline-block;padding:.4rem 0;color:var(--text2);text-decoration:none}
.langs a:hover{text-decoration:underline}
.langs a[aria-current]{color:var(--text);font-weight:600;text-decoration:underline;text-decoration-thickness:2px;
text-underline-offset:.35em}
.hero{padding:3rem 0 0}
.hello{display:flex;align-items:center;gap:1.75rem;margin:0 0 2rem}
.cat{flex:none;width:12rem;height:auto;transform:rotate(-4deg);filter:drop-shadow(0 .5rem .7rem var(--shadow))}
h1{margin:2.4rem 0 0;font-size:3.6rem;line-height:1.05;letter-spacing:-.025em}
.intro,.prose{max-width:40rem}
.intro p,.prose p{margin:0 0 1.1rem}
.intro .lead{font-size:1.25rem;line-height:1.55;color:var(--text)}
h2{margin:4.25rem 0 1.25rem;font-size:1.85rem;line-height:1.2;letter-spacing:-.015em}
.project{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:1.25rem 2.75rem;padding:2.25rem 0}
.project:first-child{padding-top:.5rem}
.project+.project{border-top:1px solid var(--rule)}
.project h3{margin:0 0 .6rem;font-size:1.5rem;line-height:1.25;letter-spacing:-.01em}
.project p{margin:0 0 1rem}
.project .what{font-size:1.1rem;color:var(--text)}
.actions{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.5rem}
.btn{display:inline-flex;align-items:center;min-height:2.75rem;padding:.45rem 1.1rem;border:2px solid var(--btn);
border-radius:.5rem;color:var(--text);font-weight:600;text-decoration:none}
.btn:hover{text-decoration:underline;text-decoration-thickness:2px}
.btn.primary{background:var(--btn);color:var(--btn-text)}
.shot{margin:0}
.shot img{display:block;width:100%;height:auto;border:1px solid var(--rule);border-radius:.5rem}
.shot.tall img{width:auto;max-width:100%;max-height:26rem}
.shot figcaption{margin-top:.6rem;font-size:.875rem;line-height:1.5}
.stack{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:.55rem 2.25rem;max-width:46rem;margin:0}
.stack dt{font-weight:600;color:var(--text)}
.stack dd{margin:0}
footer{margin-top:5rem;border-top:1px solid var(--rule);padding:1.75rem 0 3rem;font-size:.9rem}
footer p{margin:0 0 .4rem}
@media (max-width:760px){
html{font-size:106.25%}
.hero{padding-top:2rem}
.hello{gap:1.1rem;margin-bottom:1.5rem}
.cat{width:7.25rem}
h1{margin-top:1.3rem;font-size:2.3rem}
.intro .lead{font-size:1.15rem}
h2{margin-top:3.25rem;font-size:1.55rem}
.project{grid-template-columns:minmax(0,1fr);padding:1.75rem 0}
.stack{grid-template-columns:minmax(0,1fr);gap:0}
.stack dd{margin-bottom:.8rem}
}
@media (max-width:380px){.cat{width:6.25rem}h1{font-size:2rem}}
"""

LINK = re.compile(r"\[([^\]]+)\]\((\w+)\)")


def e(x) -> str:
    return html.escape(str(x), quote=True)


def plain(text: str) -> str:
    return LINK.sub(r"\1", text)


def typo(text: str, lang: str) -> str:
    """Russian typesetting: a one-letter word never ends a line."""
    if lang == "ru":
        text = re.sub(r"(?<![\w-])([а-яА-ЯёЁ]) ", "\\1\u00a0", text)
    return text


def rich(text: str, links: dict, lang: str) -> str:
    """Escapes text and turns [label](key) into links."""
    out, pos = [], 0
    text = typo(text, lang)
    for m in LINK.finditer(text):
        out.append(e(text[pos:m.start()]))
        out.append(f'<a href="{e(links[m.group(2)])}">{e(m.group(1))}</a>')
        pos = m.end()
    out.append(e(text[pos:]))
    return "".join(out)


def url(lang: str) -> str:
    return BASE if lang == "en" else f"{BASE}{lang}/"


def links(lang: str) -> dict:
    crl = f"{BASE}Crypto-Research-Labs/" + ("" if lang == "en" else f"{lang}/")
    return {
        "crl_live": crl, "crl_method": crl + "about.html#methodology", "crl_findings": crl + "research.html#all",
        "crl_course": crl + "course.html", "crl_repo": f"{GH}/Crypto-Research-Labs",
        "tbm_live": f"{BASE}telegram-bot-manager/" + (f"{lang}/" if lang in TBM_LANGS else ""),
        "tbm_repo": f"{GH}/telegram-bot-manager",
        **{k: f"{BASE}telegram-bot-manager/" + (f"{lang}/" if lang in TBM_LANGS else "") + slug for k, slug in
           (("tbm_set", "set-webhook/"), ("tbm_info", "webhook-info/"), ("tbm_del", "delete-webhook/"),
            ("tbm_cmd", "bot-commands/"))},
        "tbm_privacy": (f"{GH}/telegram-bot-manager/blob/main/README.ru.md#безопасность" if lang == "ru"
                        else f"{GH}/telegram-bot-manager#privacy-and-security"),
        "myip_live": f"{GH}/my-ip-geo-plasma6/releases/latest", "myip_repo": f"{GH}/my-ip-geo-plasma6",
        "myip_privacy": f"{GH}/my-ip-geo-plasma6#network-access-and-privacy",
        "crl_issues": f"{GH}/Crypto-Research-Labs/issues", "tbm_issues": f"{GH}/telegram-bot-manager/issues",
        "myip_issues": f"{GH}/my-ip-geo-plasma6/issues",
        "c6_live": f"{BASE}c6-zigbee-stick/" + ("ru/" if lang == "ru" else ""), "c6_repo": f"{GH}/c6-zigbee-stick",
        "c6_how": (f"{GH}/c6-zigbee-stick/blob/main/README.ru.md#как-это-устроено" if lang == "ru"
                   else f"{GH}/c6-zigbee-stick#how-it-works"),
        "c6_issues": f"{GH}/c6-zigbee-stick/issues",
        "grbl_live": f"{BASE}grbl-wifi-bridge/" + ("ru/" if lang == "ru" else ""),
        "grbl_repo": f"{GH}/grbl-wifi-bridge", "grbl_issues": f"{GH}/grbl-wifi-bridge/issues",
        "grbl_safety": (f"{GH}/grbl-wifi-bridge/blob/main/README.ru.md#безопасность" if lang == "ru"
                        else f"{GH}/grbl-wifi-bridge#safety-notes"),
        "gh": GH, "src": f"{GH}/f1devbin.github.io",
    }


def fonts_css() -> str:
    return "".join(
        f'@font-face{{font-family:"IBM Plex Sans";font-style:normal;font-weight:{w};font-display:swap;'
        f'src:url(fonts/ibm-plex-sans-{sub}-{w}-normal.woff2) format("woff2");unicode-range:{rng}}}\n'
        for sub, rng in FONT_RANGES.items() for w in (400, 600, 700))


def stylesheet() -> str:
    return fonts_css() + CSS.lstrip()


def verification_meta() -> str:
    p = ROOT / "verification.json"
    v = json.loads(p.read_text()) if p.exists() else {}
    names = {"google": "google-site-verification", "yandex": "yandex-verification", "bing": "msvalidate.01"}
    return "".join(f'<meta name="{names[k]}" content="{e(c)}">\n' for k, c in v.items() if k in names and c)


def head(lang: str, title: str, desc: str, up: str, css_ver: str, canonical: str | None, extra: str = "") -> str:
    hl, loc = LANGS[lang][1], LANGS[lang][2]
    font = PRELOAD.get(lang, "latin")
    parts = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<meta http-equiv="Content-Security-Policy" content="{CSP}">',
        f"<title>{e(title)}</title>",
        f'<meta name="description" content="{e(desc)}">',
    ]
    if canonical:
        parts.append(f'<link rel="canonical" href="{canonical}">')
        parts += [f'<link rel="alternate" hreflang="{LANGS[c][1]}" href="{url(c)}">' for c in LANGS]
        parts.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}">')
    parts += [
        '<meta name="color-scheme" content="dark light">',
        '<meta name="theme-color" content="#0f1b2d" media="(prefers-color-scheme: dark)">',
        '<meta name="theme-color" content="#f7f9fc" media="(prefers-color-scheme: light)">',
        f'<link rel="icon" href="{up}favicon.ico" sizes="16x16 32x32 48x48">',
        f'<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">',
        f'<link rel="preload" href="{up}assets/fonts/ibm-plex-sans-{font}-400-normal.woff2" as="font" '
        'type="font/woff2" crossorigin>',
        f'<link rel="stylesheet" href="{up}assets/site.css?v={css_ver}">',
    ]
    return "\n".join(parts) + "\n" + extra


def page(lang: str, css_ver: str, now: str) -> str:
    s, L = T[lang], links(lang)
    up = "" if lang == "en" else "../"
    hl = LANGS[lang][1]

    def r(text):
        return rich(text, L, lang)

    def t(text):
        return e(typo(text, lang))

    me = {"@type": "Person", "@id": BASE + "#max", "name": "Max", "alternateName": "f1devbin", "url": BASE,
          "jobTitle": s["job"], "description": plain(" ".join(s["intro"][:2])), "knowsLanguage": ["ru", "en"],
          "knowsAbout": ["Electronics", "PHP", "Python", "Telegram Bot API", "KDE Plasma", "Linux servers",
                         "Backtesting"], "sameAs": [GH]}
    who = {"@id": BASE + "#max"}
    ld = [{"@context": "https://schema.org", "@type": "ProfilePage", "url": url(lang), "name": s["title"],
           "inLanguage": hl, "dateModified": now, "mainEntity": me},
          {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "item": {
                  # Google's Dataset rich results want creator and license
                  "@type": "Dataset", "name": "Crypto Research Labs", "url": L["crl_live"],
                  "description": plain(s["crl_what"] + " " + s["crl_story"]), "creator": who,
                  "license": "https://opensource.org/licenses/MIT", "isAccessibleForFree": True,
                  "sameAs": L["crl_repo"]}},
              {"@type": "ListItem", "position": 2, "item": {
                  "@type": "SoftwareSourceCode", "name": "Telegram Bot Manager", "url": L["tbm_live"],
                  "description": plain(s["tbm_what"]), "codeRepository": L["tbm_repo"],
                  "programmingLanguage": "JavaScript", "license": "https://opensource.org/licenses/MIT",
                  "author": who}},
              {"@type": "ListItem", "position": 3, "item": {
                  "@type": "SoftwareSourceCode", "name": "My IP & Geo", "url": L["myip_repo"],
                  "description": plain(s["myip_what"]), "codeRepository": L["myip_repo"],
                  "programmingLanguage": ["QML", "JavaScript"], "runtimePlatform": "KDE Plasma 6",
                  "license": "https://opensource.org/licenses/MIT", "author": who}},
              {"@type": "ListItem", "position": 4, "item": {
                  "@type": "SoftwareSourceCode", "name": "C6 Zigbee Stick", "url": L["c6_live"],
                  "description": plain(s["c6_what"]), "codeRepository": L["c6_repo"],
                  "programmingLanguage": "Python", "runtimePlatform": "Home Assistant",
                  "license": "https://opensource.org/licenses/MIT", "author": who}},
              {"@type": "ListItem", "position": 5, "item": {
                  "@type": "SoftwareSourceCode", "name": "GRBL Wi-Fi Bridge", "url": L["grbl_live"],
                  "description": plain(s["grbl_what"]), "codeRepository": L["grbl_repo"],
                  "programmingLanguage": ["C", "JavaScript"], "runtimePlatform": "ESP32-S3",
                  "license": "https://opensource.org/licenses/MIT", "author": who}}]}]
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")

    og = "\n".join([
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        verification_meta().rstrip("\n"),
        '<meta property="og:type" content="profile">',
        '<meta property="og:site_name" content="f1devbin">',
        f'<meta property="og:title" content="{e(s["title"])}">',
        f'<meta property="og:description" content="{e(s["desc"])}">',
        f'<meta property="og:url" content="{url(lang)}">',
        f'<meta property="og:locale" content="{LANGS[lang][2]}">',
        *[f'<meta property="og:locale:alternate" content="{LANGS[c][2]}">' for c in LANGS if c != lang],
        f'<meta property="og:image" content="{BASE}assets/og/{lang}.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{e(s["h1"] + ". " + s["og_line"] + ".")}">',
        '<meta property="profile:username" content="f1devbin">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<script type="application/ld+json">{ld_json}</script>',
    ]).replace("\n\n", "\n")

    current = ' aria-current="page"'
    langs = "".join(
        f'<li><a href="{up}{"" if c == "en" else c + "/"}" hreflang="{LANGS[c][1]}" lang="{LANGS[c][1]}"'
        f'{current if c == lang else ""}>{e(LANGS[c][0])}</a></li>' for c in LANGS)

    def project(pid: str, name: str) -> str:
        w, h = SIZES[pid]
        if pid in TALL:
            img = (f'<img src="{up}assets/{pid}.webp" width="{w}" height="{h}" alt="{e(s[pid + "_alt"])}" '
                   'loading="lazy" decoding="async">')
        else:
            srcset = ", ".join(f"{up}assets/{pid}-{x}.webp {x}w" for x in (640, 960, 1280))
            img = (f'<img src="{up}assets/{pid}-1280.webp" srcset="{srcset}" '
                   f'sizes="(max-width: 760px) calc(100vw - 40px), 400px" width="{w}" height="{h}" '
                   f'alt="{e(s[pid + "_alt"])}" loading="lazy" decoding="async">')
        return (f'<article class="project" id="{pid}" aria-labelledby="{pid}-h">\n<div>\n'
                f'<h3 id="{pid}-h">{e(name)}</h3>\n'
                f'<p class="what">{r(s[pid + "_what"])}</p>\n<p>{r(s[pid + "_story"])}</p>\n'
                f'<p>{r(s[pid + "_proof"])}</p>\n'
                f'<p class="actions"><a class="btn primary" href="{e(L[pid + "_live"])}">{e(s[pid + "_cta"])}</a> '
                f'<a class="btn" href="{e(L[pid + "_repo"])}">{e(s["source"])}</a></p>\n</div>\n'
                f'<figure class="shot{" tall" if pid in TALL else ""}">{img}'
                f'<figcaption>{e(s[pid + "_cap"])}</figcaption></figure>\n</article>')

    lead = ' class="lead"'
    intro = "\n".join(f'<p{lead if i == 0 else ""}>{r(p)}</p>' for i, p in enumerate(s["intro"]))
    cat_w, cat_h = SIZES["cat"]
    how = "\n".join(f"<p>{r(p)}</p>" for p in s["how"])
    stack = "\n".join(f"<dt>{t(term)}</dt><dd>{e(v)}</dd>" for term, v in zip(s["stack"], STACK))
    return f"""<!doctype html>
<html lang="{hl}">
<head>
{head(lang, s["title"], s["desc"], up, css_ver, url(lang), og)}
</head>
<body>
<a class="skip" href="#main">{e(s["skip"])}</a>
<header class="top"><div class="wrap">
<a class="brand" href="./">f1devbin</a>
<nav aria-label="{e(s["lang_label"])}"><ul class="langs">{langs}</ul></nav>
</div></header>
<main id="main" class="wrap">
<section class="hero" aria-labelledby="hi">
<div class="hello"><img class="cat" src="{up}assets/cat.webp" srcset="{up}assets/cat-240.webp 240w, {up}assets/cat.webp {cat_w}w" sizes="{CAT_SIZES}" width="{cat_w}" height="{cat_h}" alt="{e(s["cat_alt"])}" fetchpriority="high"><h1 id="hi">{e(typo(s["h1"], lang))}</h1></div>
<div class="intro">
{intro}
</div>
</section>
<section aria-labelledby="projects">
<h2 id="projects">{t(s["projects_h"])}</h2>
<div class="projects">
{project("crl", "Crypto Research Labs")}
{project("tbm", "Telegram Bot Manager")}
{project("myip", "My IP & Geo")}
{project("c6", "C6 Zigbee Stick")}
{project("grbl", "GRBL Wi-Fi Bridge")}
</div>
</section>
<section aria-labelledby="how">
<h2 id="how">{t(s["how_h"])}</h2>
<div class="prose">
{how}
</div>
</section>
<section aria-labelledby="stack">
<h2 id="stack">{t(s["stack_h"])}</h2>
<dl class="stack">
{stack}
</dl>
</section>
<section aria-labelledby="contact">
<h2 id="contact">{t(s["contact_h"])}</h2>
<div class="prose">
<p>{r(s["contact"])}</p>
</div>
</section>
</main>
<footer><div class="wrap">
<p>{t(s["foot_privacy"])}</p>
<p><a href="{GH}">github.com/f1devbin</a></p>
<p><a href="{L["src"]}">{e(s["foot_src"])}</a></p>
<p>© {YEAR} {e(s["me"])} (f1devbin)</p>
</div></footer>
</body>
</html>
"""


def not_found(css_ver: str) -> str:
    en, ru = T["en"], T["ru"]
    return f"""<!doctype html>
<html lang="en">
<head>
{head("en", en["nf_title"] + " | f1devbin", en["nf_text"], "/", css_ver, None,
      '<meta name="robots" content="noindex">')}
</head>
<body>
<main id="main" class="wrap">
<section class="hero" aria-labelledby="hi">
<div class="hello"><img class="cat" src="/assets/cat.webp" width="{SIZES["cat"][0]}" height="{SIZES["cat"][1]}" alt=""><h1 id="hi">404</h1></div>
<div class="intro">
<p class="lead">{e(en["nf_text"])}</p>
<p lang="ru">{e(ru["nf_text"])}</p>
<p class="actions"><a class="btn primary" href="/">{e(en["home"])}</a> <a class="btn" href="/ru/" lang="ru">{e(ru["home"])}</a></p>
</div>
</section>
</main>
</body>
</html>
"""


def sitemap(today: str) -> str:
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[c][1]}" href="{url(c)}"/>' for c in LANGS)
    alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    urls = "".join(f"<url><loc>{url(c)}</loc><lastmod>{today}</lastmod>{alts}</url>" for c in LANGS)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n')


def main() -> None:
    missing = [k for lang in T for k in T["en"] if k not in T[lang]]
    if missing:
        raise SystemExit(f"untranslated keys: {missing}")
    css = stylesheet()
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets/site.css").write_text(css, encoding="utf-8")
    ver = hashlib.sha256(css.encode()).hexdigest()[:8]
    stamp = datetime.now(timezone.utc).replace(microsecond=0)
    today = stamp.date().isoformat()
    now = stamp.isoformat()  # Google wants a full date-time with a time zone in dateModified
    for lang in LANGS:
        out = ROOT / ("index.html" if lang == "en" else f"{lang}/index.html")
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(lang, ver, now), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(today), encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\n" + "".join(
        f"Sitemap: {BASE}{p}\n" for p in ["sitemap.xml"] + PROJECT_SITEMAPS), encoding="utf-8")
    (ROOT / "404.html").write_text(not_found(ver), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("built", len(LANGS), "languages")


if __name__ == "__main__":
    main()
