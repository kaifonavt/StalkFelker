import os
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from supabase import create_client, Client

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Получение учетных данных из переменных окружения
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')

# Настройка Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Создание клиента Telegram
client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    try:
        # Попытка получить информацию о отправителе
        if event.sender:
            sender = event.sender.username or event.sender.first_name or "Unknown"
        else:
            # Если отправитель недоступен, попробуем получить информацию из чата
            sender = event.chat.title if event.chat else "Unknown"

        # Определение типа сообщения и получение контента
        if event.message.media:
            message_type = type(event.message.media).__name__
            content = f"Media: {message_type}"
        elif event.message.text:
            message_type = "text"
            content = event.message.text
        else:
            message_type = "unknown"
            content = "Unknown content"

        # Получение ID чата
        chat_id = str(event.chat_id) if event.chat_id else "Unknown"

        logger.info(f"Новое сообщение от {sender} в чате {chat_id}: {content}")

        # Сохранение сообщения в Supabase
        try:
            data, count = supabase.table("telegram_messages").insert({
                "sender": sender,
                "content": content,
                "chat_id": chat_id,
                "message_type": message_type
            }).execute()
            logger.info(f"Сообщение сохранено в Supabase")
        except Exception as e:
            logger.error(f"Ошибка при сохранении в Supabase: {e}")

        # Добавление небольшой задержки для избежания превышения лимитов API
        await asyncio.sleep(0.5)

    except Exception as e:
        logger.error(f"Произошла ошибка при обработке сообщения: {e}")

async def main():
    # Подключение к Telegram
    await client.start(phone=phone_number)
    logger.info("Клиент Telegram успешно запущен")

    # Получение информации о текущем пользователе
    me = await client.get_me()
    logger.info(f"Авторизован как {me.username}")

    # Запуск клиента
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())