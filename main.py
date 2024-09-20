import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from supabase import create_client, Client
import time
import qrcode

# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def save_message_to_supabase(sender, receiver, content, message_type, chat_id):
    try:
        data, count = supabase.rpc(
            'insert_message', 
            {
                'p_sender': sender,
                'p_receiver': receiver,
                'p_content': content,
                'p_message_type': message_type,
                'p_chat_id': chat_id
            }
        ).execute()
        
        print(f"Message saved to Supabase: {content}")
        return data[0]['id']
    except Exception as e:
        print(f"Error saving to Supabase: {e}")
        return None

def get_chat_messages(chat_id):
    data, count = supabase.table("whatsapp_messages").select("*").eq("chat_id", chat_id).order("timestamp", desc=True).execute()
    return data

def get_latest_messages():
    data, count = supabase.table("latest_messages").select("*").execute()
    return data

def mark_as_read(message_id):
    data, count = supabase.table("whatsapp_messages").update({"is_read": True}).eq("id", message_id).execute()
    return count > 0

def main():
    driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver
    driver.get("https://web.whatsapp.com/")

    # Ожидание появления QR-кода
    qr_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
    )

    # Получение данных QR-кода
    qr_data = qr_element.get_attribute("data-ref")

    # Создание и сохранение QR-кода как изображения
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("whatsapp_qr.png")

    print("QR код сохранен как 'whatsapp_qr.png'. Отсканируйте его с помощью WhatsApp на вашем телефоне.")

    # Ожидание входа пользователя
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chatlist-header"]'))
    )

    print("Вход выполнен успешно. Начинаю мониторинг сообщений.")

    last_message = ""
    while True:
        try:
            messages = driver.find_elements(By.XPATH, '//div[@data-testid="msg-container"]')
            if messages:
                latest_message = messages[-1]
                sender = latest_message.find_element(By.XPATH, './/span[@data-testid="author"]').text
                content = latest_message.find_element(By.XPATH, './/div[@data-testid="msg-text"]').text

                if content != last_message:
                    print(f"Новое сообщение от {sender}: {content}")
                    message_id = save_message_to_supabase(sender, 'me', content, 'text', f"{sender}_me")
                    if message_id:
                        print(f"Сообщение сохранено с ID: {message_id}")
                    last_message = content

            # Пример получения и вывода последних сообщений
            latest_messages = get_latest_messages()
            print("Последние сообщения:")
            for message in latest_messages:
                print(f"Chat: {message['chat_id']}, Last message: {message['content']}")

        except Exception as e:
            print(f"Ошибка при чтении сообщений: {e}")

        time.sleep(5)  # Пауза между проверками новых сообщений

if __name__ == "__main__":
    main()