Установите необходимые библиотеки:
Copypip install selenium supabase-py qrcode pillow

Убедитесь, что у вас установлен ChromeDriver и он доступен в системном PATH.
Установите переменные окружения для URL и ключа Supabase:
Copyexport SUPABASE_URL="ваш_url"
export SUPABASE_KEY="ваш_ключ"

Запустите скрипт:
Copypython main.py

Отсканируйте сгенерированный QR-код с помощью WhatsApp на вашем телефоне для входа.