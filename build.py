#!/usr/bin/env python3
"""Builds the f1devbin.github.io landing page in 7 languages (static HTML, committed to the repo).

    python3 build.py

Writes index.html (English, x-default), <lang>/index.html, sitemap.xml, robots.txt, 404.html.
robots.txt sits at the host root, so it governs every project site under f1devbin.github.io and
lists their sitemaps. Search-engine verification codes come from verification.json.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://f1devbin.github.io/"
GH = "https://github.com/f1devbin"
LANGS = {"en": ("English", "en", "en_US"), "ru": ("Русский", "ru", "ru_RU"), "es": ("Español", "es", "es_ES"),
         "pt": ("Português", "pt-BR", "pt_BR"), "tr": ("Türkçe", "tr", "tr_TR"), "vi": ("Tiếng Việt", "vi", "vi_VN"),
         "zh": ("中文", "zh-Hans", "zh_CN")}
PROJECT_SITEMAPS = ["Crypto-Research-Labs/sitemap.xml", "telegram-bot-manager/sitemap.xml"]

PROJECTS = [
    {"id": "crl", "name": "Crypto Research Labs", "img": "assets/crl.webp", "w": 800, "h": 420,
     "live": BASE + "Crypto-Research-Labs/", "repo": GH + "/Crypto-Research-Labs", "tags": "Python · GitHub Actions · LLM",
     "live_lang": True},
    {"id": "tbm", "name": "Telegram Bot Manager", "img": "assets/tbm.webp", "w": 800, "h": 400,
     "live": BASE + "telegram-bot-manager/", "repo": GH + "/telegram-bot-manager", "tags": "JavaScript · Bot API",
     "live_lang": False},
    {"id": "myip", "name": "My IP & Geo", "img": "assets/myip.webp", "w": 416, "h": 607,
     "live": GH + "/my-ip-geo-plasma6/releases/latest", "repo": GH + "/my-ip-geo-plasma6", "tags": "QML · KDE Plasma 6",
     "live_lang": False},
]

T = {
"en": {
 "title": "Max (f1devbin): open-source tools and honest crypto research",
 "desc": "Projects by Max (f1devbin): Crypto Research Labs, an open lab that tests crypto trading ideas honestly; Telegram Bot Manager, a free browser tool for Telegram bots; My IP & Geo, a KDE Plasma 6 network widget.",
 "lead": "Programmer by education and an electronics engineer with many years of experience. I build tools that run on my own home servers: Telegram bots, monitoring dashboards, KDE Plasma widgets and an honest research lab for crypto trading ideas. Everything here is free and open source.",
 "projects": "Projects", "open": "Open", "download": "Download", "source": "Source code",
 "crl": "Every trading idea is written down and locked before it is tested, then re-tested automatically on new data. A live dashboard, a market diagnosis in plain words, a weekly digest and a beginners' course in 7 languages. Negative results are published too.",
 "tbm": "Manage a Telegram bot right in the browser: set, check and delete webhooks, edit commands, name, description, avatar, menu button and admin rights. No code, no install, no backend.",
 "myip": "A compact KDE Plasma 6 widget: public IP and location, local interfaces, a network scanner with TCP port scan, diagnostics, a speed test, per-app traffic and a device monitor. No root, no extra packages.",
 "how": "How I build", "principles": ["Real data over mocks, small tools over big frameworks.",
  "Prove it or drop it: tests are fixed in advance and negative results are published.",
  "Living documentation: every README is kept up to date."],
 "stack": "Tools I use", "contact": "Contact",
 "contact_text": "Questions and ideas are welcome in the Issues or Discussions of each project.",
 "lang": "Language", "nf_title": "Page not found", "nf_text": "This page does not exist.", "home": "Home"},
"ru": {
 "title": "Макс (f1devbin): открытые инструменты и честные исследования крипты",
 "desc": "Проекты Макса (f1devbin): Crypto Research Labs — открытая лаборатория честной проверки торговых идей для криптовалют; Telegram Bot Manager — бесплатный инструмент для Telegram-ботов в браузере; My IP & Geo — сетевой виджет для KDE Plasma 6.",
 "lead": "Программист по образованию, много лет работаю инженером-электроником. Делаю инструменты, которые работают на моих домашних серверах: Telegram-боты, дашборды мониторинга, виджеты KDE Plasma и лабораторию честной проверки торговых идей для криптовалют. Всё здесь бесплатно и с открытым кодом.",
 "projects": "Проекты", "open": "Открыть", "download": "Скачать", "source": "Исходный код",
 "crl": "Каждая торговая идея записывается и фиксируется до проверки, а потом автоматически перепроверяется на новых данных. Живой дашборд, диагноз рынка простыми словами, недельные сводки и курс для новичков на 7 языках. Отрицательные результаты тоже публикуются.",
 "tbm": "Управление Telegram-ботом прямо в браузере: установка, проверка и удаление вебхуков, команды, имя, описание, аватар, кнопка меню и права администратора. Без кода, без установки, без сервера.",
 "myip": "Компактный виджет для KDE Plasma 6: внешний IP и местоположение, локальные интерфейсы, сканер сети с проверкой TCP-портов, диагностика, тест скорости, трафик по приложениям и монитор устройств. Без root и лишних пакетов.",
 "how": "Как я работаю", "principles": ["Реальные данные вместо заглушек, небольшие инструменты вместо громоздких фреймворков.",
  "Докажи или откажись: проверки фиксируются заранее, отрицательные результаты публикуются.",
  "Живая документация: каждый README поддерживается в актуальном состоянии."],
 "stack": "Чем пользуюсь", "contact": "Связь",
 "contact_text": "Вопросы и идеи — в Issues или Discussions любого проекта.",
 "lang": "Язык", "nf_title": "Страница не найдена", "nf_text": "Такой страницы нет.", "home": "На главную"},
"es": {
 "title": "Max (f1devbin): herramientas de código abierto e investigación cripto honesta",
 "desc": "Proyectos de Max (f1devbin): Crypto Research Labs, un laboratorio abierto que prueba ideas de trading cripto con honestidad; Telegram Bot Manager, una herramienta gratuita para bots de Telegram en el navegador; My IP & Geo, un widget de red para KDE Plasma 6.",
 "lead": "Programador de formación e ingeniero electrónico con muchos años de experiencia. Creo herramientas que funcionan en mis propios servidores domésticos: bots de Telegram, paneles de monitorización, widgets de KDE Plasma y un laboratorio honesto de ideas de trading cripto. Todo es gratuito y de código abierto.",
 "projects": "Proyectos", "open": "Abrir", "download": "Descargar", "source": "Código fuente",
 "crl": "Cada idea de trading se escribe y se fija antes de probarla, y luego se vuelve a probar automáticamente con datos nuevos. Panel en vivo, diagnóstico del mercado en palabras sencillas, resumen semanal y curso para principiantes en 7 idiomas. También se publican los resultados negativos.",
 "tbm": "Gestiona un bot de Telegram en el navegador: configura, comprueba y elimina webhooks, edita comandos, nombre, descripción, avatar, botón de menú y permisos de administrador. Sin código, sin instalación, sin servidor.",
 "myip": "Un widget compacto para KDE Plasma 6: IP pública y ubicación, interfaces locales, escáner de red con escaneo de puertos TCP, diagnóstico, test de velocidad, tráfico por aplicación y monitor de dispositivos. Sin root ni paquetes extra.",
 "how": "Cómo trabajo", "principles": ["Datos reales en lugar de simulaciones, herramientas pequeñas en lugar de grandes frameworks.",
  "Demuéstralo o descártalo: las pruebas se fijan de antemano y se publican los resultados negativos.",
  "Documentación viva: cada README se mantiene al día."],
 "stack": "Herramientas", "contact": "Contacto",
 "contact_text": "Preguntas e ideas, en los Issues o Discussions de cada proyecto.",
 "lang": "Idioma", "nf_title": "Página no encontrada", "nf_text": "Esta página no existe.", "home": "Inicio"},
"pt": {
 "title": "Max (f1devbin): ferramentas de código aberto e pesquisa cripto honesta",
 "desc": "Projetos de Max (f1devbin): Crypto Research Labs, um laboratório aberto que testa ideias de trading cripto com honestidade; Telegram Bot Manager, uma ferramenta gratuita para bots do Telegram no navegador; My IP & Geo, um widget de rede para KDE Plasma 6.",
 "lead": "Programador por formação e engenheiro eletrônico há muitos anos. Crio ferramentas que rodam nos meus próprios servidores domésticos: bots do Telegram, painéis de monitoramento, widgets do KDE Plasma e um laboratório honesto de ideias de trading cripto. Tudo aqui é gratuito e de código aberto.",
 "projects": "Projetos", "open": "Abrir", "download": "Baixar", "source": "Código-fonte",
 "crl": "Cada ideia de trading é escrita e travada antes do teste e depois retestada automaticamente com dados novos. Painel ao vivo, diagnóstico do mercado em palavras simples, resumo semanal e curso para iniciantes em 7 idiomas. Resultados negativos também são publicados.",
 "tbm": "Gerencie um bot do Telegram no navegador: defina, verifique e apague webhooks, edite comandos, nome, descrição, avatar, botão de menu e permissões de administrador. Sem código, sem instalação, sem servidor.",
 "myip": "Um widget compacto para KDE Plasma 6: IP público e localização, interfaces locais, scanner de rede com varredura de portas TCP, diagnóstico, teste de velocidade, tráfego por aplicativo e monitor de dispositivos. Sem root e sem pacotes extras.",
 "how": "Como eu trabalho", "principles": ["Dados reais em vez de simulações, ferramentas pequenas em vez de grandes frameworks.",
  "Prove ou descarte: os testes são fixados antes e resultados negativos são publicados.",
  "Documentação viva: cada README é mantido atualizado."],
 "stack": "Ferramentas", "contact": "Contato",
 "contact_text": "Perguntas e ideias são bem-vindas nos Issues ou Discussions de cada projeto.",
 "lang": "Idioma", "nf_title": "Página não encontrada", "nf_text": "Esta página não existe.", "home": "Início"},
"tr": {
 "title": "Max (f1devbin): açık kaynak araçlar ve dürüst kripto araştırmaları",
 "desc": "Max'in (f1devbin) projeleri: kripto işlem fikirlerini dürüstçe test eden açık laboratuvar Crypto Research Labs; Telegram botları için ücretsiz tarayıcı aracı Telegram Bot Manager; KDE Plasma 6 için ağ bileşeni My IP & Geo.",
 "lead": "Eğitimim programcılık; uzun yıllardır elektronik mühendisi olarak çalışıyorum. Kendi ev sunucularımda çalışan araçlar yapıyorum: Telegram botları, izleme panelleri, KDE Plasma bileşenleri ve kripto işlem fikirleri için dürüst bir araştırma laboratuvarı. Buradaki her şey ücretsiz ve açık kaynaktır.",
 "projects": "Projeler", "open": "Aç", "download": "İndir", "source": "Kaynak kod",
 "crl": "Her işlem fikri test edilmeden önce yazılıp kilitlenir, ardından yeni verilerle otomatik olarak yeniden test edilir. Canlı panel, sade dille piyasa teşhisi, haftalık özet ve 7 dilde yeni başlayanlar kursu. Olumsuz sonuçlar da yayımlanır.",
 "tbm": "Bir Telegram botunu doğrudan tarayıcıda yönetin: webhook ayarlayın, kontrol edin ve silin; komutları, adı, açıklamayı, avatarı, menü düğmesini ve yönetici haklarını düzenleyin. Kod yok, kurulum yok, sunucu yok.",
 "myip": "KDE Plasma 6 için kompakt bir bileşen: genel IP ve konum, yerel arayüzler, TCP port taramalı ağ tarayıcı, tanılama, hız testi, uygulama başına trafik ve cihaz izleyici. Root ve ek paket gerekmez.",
 "how": "Nasıl çalışırım", "principles": ["Sahte veri yerine gerçek veri, büyük çerçeveler yerine küçük araçlar.",
  "Kanıtla ya da bırak: testler önceden sabitlenir, olumsuz sonuçlar yayımlanır.",
  "Yaşayan belgeler: her README güncel tutulur."],
 "stack": "Kullandığım araçlar", "contact": "İletişim",
 "contact_text": "Sorular ve fikirler her projenin Issues veya Discussions bölümüne.",
 "lang": "Dil", "nf_title": "Sayfa bulunamadı", "nf_text": "Böyle bir sayfa yok.", "home": "Ana sayfa"},
"vi": {
 "title": "Max (f1devbin): công cụ mã nguồn mở và nghiên cứu crypto trung thực",
 "desc": "Các dự án của Max (f1devbin): Crypto Research Labs, phòng thí nghiệm mở kiểm tra trung thực các ý tưởng giao dịch crypto; Telegram Bot Manager, công cụ miễn phí cho bot Telegram trên trình duyệt; My IP & Geo, tiện ích mạng cho KDE Plasma 6.",
 "lead": "Tốt nghiệp ngành lập trình, nhiều năm làm kỹ sư điện tử. Tôi làm các công cụ chạy trên máy chủ tại nhà: bot Telegram, bảng giám sát, tiện ích KDE Plasma và một phòng thí nghiệm trung thực cho các ý tưởng giao dịch crypto. Mọi thứ ở đây đều miễn phí và mã nguồn mở.",
 "projects": "Dự án", "open": "Mở", "download": "Tải về", "source": "Mã nguồn",
 "crl": "Mỗi ý tưởng giao dịch được ghi lại và khóa trước khi kiểm tra, sau đó tự động kiểm tra lại trên dữ liệu mới. Bảng điều khiển trực tiếp, chẩn đoán thị trường bằng lời đơn giản, tóm tắt hằng tuần và khóa học cho người mới bằng 7 ngôn ngữ. Kết quả tiêu cực cũng được công bố.",
 "tbm": "Quản lý bot Telegram ngay trên trình duyệt: đặt, kiểm tra và xóa webhook, sửa lệnh, tên, mô tả, ảnh đại diện, nút menu và quyền quản trị. Không cần code, không cài đặt, không máy chủ.",
 "myip": "Tiện ích gọn nhẹ cho KDE Plasma 6: IP công khai và vị trí, giao diện mạng cục bộ, quét mạng kèm quét cổng TCP, chẩn đoán, đo tốc độ, lưu lượng theo ứng dụng và giám sát thiết bị. Không cần root, không thêm gói.",
 "how": "Cách tôi làm việc", "principles": ["Dữ liệu thật thay vì dữ liệu giả, công cụ nhỏ thay vì framework lớn.",
  "Chứng minh hoặc bỏ: kiểm tra được cố định trước và kết quả tiêu cực được công bố.",
  "Tài liệu sống: mọi README đều được cập nhật."],
 "stack": "Công cụ", "contact": "Liên hệ",
 "contact_text": "Câu hỏi và ý tưởng xin gửi vào Issues hoặc Discussions của từng dự án.",
 "lang": "Ngôn ngữ", "nf_title": "Không tìm thấy trang", "nf_text": "Trang này không tồn tại.", "home": "Trang chủ"},
"zh": {
 "title": "Max（f1devbin）：开源工具与诚实的加密研究",
 "desc": "Max（f1devbin）的项目：Crypto Research Labs，诚实检验加密交易想法的开放实验室；Telegram Bot Manager，在浏览器中管理 Telegram 机器人的免费工具；My IP & Geo，KDE Plasma 6 网络小部件。",
 "lead": "程序员出身，多年从事电子工程师工作。我做的工具运行在自己的家庭服务器上：Telegram 机器人、监控仪表盘、KDE Plasma 小部件，以及一个诚实检验加密交易想法的研究实验室。这里的一切都免费且开源。",
 "projects": "项目", "open": "打开", "download": "下载", "source": "源代码",
 "crl": "每个交易想法都在检验前写下并锁定，之后用新数据自动复检。实时仪表盘、通俗的市场诊断、每周摘要和 7 种语言的新手课程。负面结果同样公开。",
 "tbm": "直接在浏览器中管理 Telegram 机器人：设置、检查和删除 webhook，编辑命令、名称、描述、头像、菜单按钮和管理员权限。无需代码、无需安装、无需服务器。",
 "myip": "紧凑的 KDE Plasma 6 小部件：公网 IP 与位置、本地网卡、带 TCP 端口扫描的网络扫描器、诊断、测速、按应用统计流量和设备监控。无需 root，无需额外软件包。",
 "how": "我的做法", "principles": ["用真实数据而非模拟数据，用小工具而非庞大框架。",
  "要么证明，要么放弃：检验事先固定，负面结果也会公开。",
  "活的文档：每个 README 都保持最新。"],
 "stack": "常用工具", "contact": "联系",
 "contact_text": "欢迎在各项目的 Issues 或 Discussions 中提问和提出想法。",
 "lang": "语言", "nf_title": "页面不存在", "nf_text": "该页面不存在。", "home": "首页"},
}

STACK = ["PHP 8", "Python", "JavaScript", "QML", "MariaDB", "SQLite", "Nginx", "systemd", "GitHub Actions",
         "Telegram Bot API", "Home Assistant", "LoRa · Meshtastic", "Ubuntu · Armbian"]

CSS = """
:root{--bg:#0f1b2d;--panel:#15243b;--raised:#1b2e4a;--line:#2f4568;--text:#fff;--text2:#e3eaf5;--link:#8ccbff;
--accent:#7cc4ff;--pass:#46c281;--ink:#0f1b2d}
@media (prefers-color-scheme:light){:root{--bg:#f5f8fc;--panel:#fff;--raised:#eaf0f8;--line:#c3cfdf;--text:#08111f;
--text2:#1c293b;--link:#0a58a8;--accent:#0a58a8;--pass:#127a43;--ink:#fff}}
*{box-sizing:border-box}html{font-size:18px}
body{margin:0;background:var(--bg);color:var(--text);font:1rem/1.6 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--link);text-underline-offset:.18em}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);background:var(--panel)}
header .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:8px 20px;padding-top:14px;padding-bottom:14px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--text);text-decoration:none}
.brand svg{width:30px;height:30px}
nav{margin-left:auto;display:flex;flex-wrap:wrap;gap:2px 14px;font-size:.88rem}
nav a{color:var(--text2);text-decoration:none}nav a[aria-current]{color:var(--text);font-weight:700;text-decoration:underline}
.hero{padding:56px 0 24px}
h1{font-size:2.6rem;line-height:1.1;letter-spacing:-.02em;margin:0 0 .35em}
h1 span{display:block;font-size:1.05rem;letter-spacing:0;font-weight:500;color:var(--text2);margin-top:.5em}
.lead{font-size:1.15rem;max-width:62ch;color:var(--text2)}
h2{font-size:1.45rem;letter-spacing:-.01em;margin:2.2em 0 .8em;padding-bottom:.35em;border-bottom:1px solid var(--line)}
.project{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:24px;align-items:center;background:var(--panel);
border:1px solid var(--line);border-radius:16px;padding:20px;margin:0 0 18px}
.project img{width:100%;height:auto;border-radius:10px;border:1px solid var(--line);display:block;background:var(--raised)}
.project.tall img{max-height:340px;width:auto;margin:0 auto}
.project h3{font-size:1.35rem;margin:0 0 .2em}
.tags{color:var(--text2);font-size:.88rem;margin:0 0 .6em}
.project p{color:var(--text2);margin:.2em 0 1em}
.actions{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-block;padding:8px 16px;border-radius:999px;font-weight:600;text-decoration:none;border:1px solid var(--line);color:var(--text)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--ink)}
.btn:hover{border-color:var(--accent)}
ul.principles{padding-left:1.2em}ul.principles li{margin:.35em 0;color:var(--text2)}
.chips{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}
.chips li{border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:.9rem;background:var(--panel)}
footer{margin-top:56px;border-top:1px solid var(--line);padding:20px 0 40px;font-size:.9rem;color:var(--text2)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
@media (max-width:760px){html{font-size:16px}.project{grid-template-columns:1fr}h1{font-size:2rem}.hero{padding-top:32px}
nav{margin-left:0}}
"""

LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#15243b"/>'
        '<path d="M10 46 L24 30 L34 38 L54 16" fill="none" stroke="#7cc4ff" stroke-width="6" stroke-linecap="round" '
        'stroke-linejoin="round"/><circle cx="54" cy="16" r="5.5" fill="#46c281"/></svg>')
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" '
           'fill="#0f1b2d"/><path d="M10 46 L24 30 L34 38 L54 16" fill="none" stroke="#7cc4ff" stroke-width="6" '
           'stroke-linecap="round" stroke-linejoin="round"/><circle cx="54" cy="16" r="5" fill="#46c281"/></svg>')


def e(x) -> str:
    return html.escape(str(x), quote=True)


def url(lang: str) -> str:
    return BASE if lang == "en" else f"{BASE}{lang}/"


def verification_meta() -> str:
    p = ROOT / "verification.json"
    v = json.loads(p.read_text()) if p.exists() else {}
    names = {"google": "google-site-verification", "yandex": "yandex-verification", "bing": "msvalidate.01"}
    return "".join(f'<meta name="{names[k]}" content="{e(c)}">' for k, c in v.items() if k in names and c)


def page(lang: str) -> str:
    s = T[lang]
    up = "" if lang == "en" else "../"
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[c][1]}" href="{url(c)}">' for c in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}">'
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{up}{"" if c == "en" else c + "/"}" hreflang="{LANGS[c][1]}" lang="{LANGS[c][1]}"'
                  f'{cur if c == lang else ""}>{e(LANGS[c][0])}</a>' for c in LANGS)
    cards = []
    for p in PROJECTS:
        live = p["live"] + (f"{lang}/" if p["live_lang"] and lang != "en" else "")
        label = s["download"] if p["id"] == "myip" else s["open"]
        cards.append(
            f'<article class="project{" tall" if p["h"] > p["w"] else ""}"><a href="{e(live)}">'
            f'<img src="{up}{p["img"]}" width="{p["w"]}" height="{p["h"]}" alt="{e(p["name"])}" loading="lazy"></a>'
            f'<div><h3>{e(p["name"])}</h3><p class="tags">{e(p["tags"])}</p><p>{e(s[p["id"]])}</p>'
            f'<div class="actions"><a class="btn primary" href="{e(live)}">{e(label)}</a>'
            f'<a class="btn" href="{e(p["repo"])}">{e(s["source"])}</a></div></div></article>')
    principles = "".join(f"<li>{e(x)}</li>" for x in s["principles"])
    stack = "".join(f"<li>{e(x)}</li>" for x in STACK)
    ld = [{"@context": "https://schema.org", "@type": "ProfilePage", "url": url(lang), "inLanguage": LANGS[lang][1],
           "mainEntity": {"@type": "Person", "name": "Max", "alternateName": "f1devbin", "url": BASE,
                          "sameAs": [GH], "description": s["lead"]}},
          {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": i, "item": {
                  "@type": "SoftwareApplication" if p["id"] != "crl" else "Dataset", "name": p["name"],
                  "url": p["live"], "description": T[lang][p["id"]],
                  **({"applicationCategory": "DeveloperApplication", "operatingSystem":
                      "Web browser" if p["id"] == "tbm" else "Linux (KDE Plasma 6)",
                      "offers": {"@type": "Offer", "price": 0, "priceCurrency": "USD"}} if p["id"] != "crl" else {})}}
              for i, p in enumerate(PROJECTS, 1)]}]
    return f"""<!doctype html>
<html lang="{LANGS[lang][1]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(s['title'])}</title>
<meta name="description" content="{e(s['desc'])}">
<link rel="canonical" href="{url(lang)}">
{alts}
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="color-scheme" content="dark light">
{verification_meta()}
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(s['title'])}">
<meta property="og:description" content="{e(s['desc'])}">
<meta property="og:url" content="{url(lang)}">
<meta property="og:locale" content="{LANGS[lang][2]}">
<meta property="og:image" content="{BASE}Crypto-Research-Labs/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><div class="wrap"><a class="brand" href="{up or './'}">{LOGO}<span>f1devbin</span></a>
<nav aria-label="{e(s['lang'])}">{nav}</nav></div></header>
<main class="wrap">
<section class="hero"><h1>Max<span>f1devbin · github.com/f1devbin</span></h1><p class="lead">{e(s['lead'])}</p></section>
<h2 id="projects">{e(s['projects'])}</h2>
{''.join(cards)}
<h2>{e(s['how'])}</h2><ul class="principles">{principles}</ul>
<h2>{e(s['stack'])}</h2><ul class="chips">{stack}</ul>
<h2>{e(s['contact'])}</h2><p>{e(s['contact_text'])} <a href="{GH}">github.com/f1devbin</a></p>
</main>
<footer><div class="wrap">© f1devbin · MIT-licensed open source · <a href="{GH}">GitHub</a></div></footer>
</body>
</html>
"""


def sitemap() -> str:
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[c][1]}" href="{url(c)}"/>' for c in LANGS)
    alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    urls = "".join(f"<url><loc>{url(c)}</loc>{alts}</url>" for c in LANGS)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n')


def not_found() -> str:
    s = T["en"]
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width, initial-scale=1"><title>{s["nf_title"]} | f1devbin</title>'
            f'<meta name="robots" content="noindex"><style>{CSS}</style></head><body><main class="wrap">'
            f'<section class="hero"><h1>404</h1><p class="lead">{s["nf_text"]} {T["ru"]["nf_text"]}</p>'
            f'<p><a class="btn primary" href="/">{s["home"]}</a></p></section></main></body></html>\n')


def main() -> None:
    for lang in LANGS:
        out = ROOT / ("index.html" if lang == "en" else f"{lang}/index.html")
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(lang), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\n" + "".join(
        f"Sitemap: {BASE}{p}\n" for p in ["sitemap.xml"] + PROJECT_SITEMAPS), encoding="utf-8")
    (ROOT / "404.html").write_text(not_found(), encoding="utf-8")
    (ROOT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("built", len(LANGS), "languages")


if __name__ == "__main__":
    main()
