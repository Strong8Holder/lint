# lint

Purpose
- Єдині стилі і перевірки для всіх репозиторіїв PPKrypto.

How to use in іншому репо
1. Скопіюй `tools/text_lint.py` та `.github/workflows/text-lint.yml` у свій репозиторій.
2. Закоміть і створи PR − GitHub Actions автоматично проганяє перевірки.
3. У `PULL_REQUEST_TEMPLATE.md` додай наш чек-лист.

What we check
- Довгі тире → заборонені.
- UTM та інші трекінг-параметри у лінках → заборонені.
- Таб-символи та трейлінг-пробіли → заборонені.

Notes
- Розширюй `INCLUDE_EXT` і `TRACKING_KEYS` у `tools/text_lint.py` під свої потреби.
