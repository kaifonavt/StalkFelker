Установите необходимые библиотеки:
pip install -r requirements.txt

Запустить Венв
venv\scripts\activate
Получите api_id и api_hash на сайте https://my.telegram.org/
Настройте переменные окружения:
export TELEGRAM_API_ID="ваш_api_id"
export TELEGRAM_API_HASH="ваш_api_hash"
export TELEGRAM_PHONE_NUMBER="ваш_номер_телефона"
export SUPABASE_URL="ваш_url_supabase"
export SUPABASE_KEY="ваш_ключ_supabase"
export SUPABASE_URL="ваш_url"
export SUPABASE_KEY="ваш_ключ"

Запустите скрипт:
python telegram.py




