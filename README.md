Установите необходимые библиотеки:
pip install selenium supabase-py qrcode pillow

Убедитесь, что у вас установлен ChromeDriver и он доступен в системном PATH.
Установите переменные окружения для URL и ключа Supabase:
export SUPABASE_URL="ваш_url"
export SUPABASE_KEY="ваш_ключ"

Запустите скрипт:
python main.py

Отсканируйте сгенерированный QR-код с помощью WhatsApp на вашем телефоне для входа.

становите необходимые библиотеки:
pip install telethon supabase

Получите api_id и api_hash на сайте https://my.telegram.org/
Настройте переменные окружения:
export TELEGRAM_API_ID="ваш_api_id"
export TELEGRAM_API_HASH="ваш_api_hash"
export TELEGRAM_PHONE_NUMBER="ваш_номер_телефона"
export SUPABASE_URL="ваш_url_supabase"
export SUPABASE_KEY="ваш_ключ_supabase"

