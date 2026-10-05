# plugin.video.rutracker.vd — приватний даунпорт під Kodi 18 Leia

Приватна копія аддона **RuTracker** (`plugin.video.rutracker.vd`) для Kodi з даунпортом під **Kodi 18 Leia (Python 2)**.

## Походження (важливо)

- **Оригінальний проєкт:** [vadyur/plugin.video.rutracker.vd](https://github.com/vadyur/plugin.video.rutracker.vd) — RuTracker Kodi Addon, автор HAL9000 / -=Vd=- (vadyur), ліцензія MIT, розповсюдження також через vd-plugins.info.
- **База цього дерева:** upstream версія `0.30.5+matrix`, коміт `6fa3ae7` від 2026-01-24 (перша історія репо — імпорт саме цього стану).
- **Що зроблено:** даунпорт з Python 3 (Kodi 19+ Matrix) на Python 2 (Kodi 18 Leia). Див. другий коміт історії — він містить усі зміни над базовим станом.

## Суть даунпорту

- `addon.xml`: версія `+matrix`→`+leia`, `xbmc.python` 3.0.0→2.26.0, `script.module.requests` зроблено опційним.
- **Новий файл `xbmcup/compat.py`** — шім Python 2/3: `HTTPConnection`, `parse_qs`, `quote_plus`, `urlencode`, `translate_path`, `Cookie`, `MozillaCookieJar`, сімейство `urlparse`.
- Переписані під сумісність: `xbmcup/{app,net,errors,etor,cache,ctor,html,t2hxplayer}.py`, `default.py`, `drivers/{rutracker,kinopoisk,tmdb,tvdb,history,torrserveradd}.py` — зняті type-анотації, `urllib.parse/urllib.request` → шім, f-strings → `%`, `xbmcvfs.translatePath` → `translate_path` тощо.
- Хронологія правок: 2026-05-28 — масовий даунпорт; 2026-06-06/07 — дебаг `xbmcup/{app,errors,etor,net}`; 2026-06-07 — три збірки в `dist/` (фінальна `..._v4.zip`).

## ⚠️ Категорія «багатоканальний звук» у цьому дереві ВІДСУТНЯ

Приймалось, що до цього форку було додано категорію багатоканального звуку, але в коді її **немає** (перевірено: `CONTENT`-мапа forum-ID у `default.py` байт-в-байт ідентична upstream, жодних згадок multichannel/багатоканал/DTS/Dolby у дереві). Ймовірно, правка робилась на встановленій копії на TV-box і не повернулась у це дерево, або втрачена.

Якщо треба додати категорію заново, механізм такий:
1. Новий ключ у словнику `CONTENT{}` у `default.py` (~рядки 79–231): `"music": index=(список forum-ID розділів rutracker)`.
2. Пункт меню в `MenuRutracker` (~рядки 2140–2250): `self.item(Link("rutracker-folder", {"content": "..."}))`.

## Стан щодо upstream

Upstream пішов далеко вперед (0.30.6 → 0.35.2+matrix, жовтень 2026: роботи з FlareSolverr/Cloudflare) — це заморожений порт 0.30.5, цих виправлень він не має. Для дифів: `git remote add upstream https://github.com/vadyur/plugin.video.rutracker.vd.git`.

## Збірки

`dist/*.zip` — три збірки 2026-06-07; `..._v4.zip` байт-в-байт відповідає робочій папці для `default.py`/`addon.xml`.

Ліцензія: MIT (успадкована від upstream, див. LICENSE) — приватна похідна допустима, атрибуцію збережено.
