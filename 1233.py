import telebot
from telebot import types

# Замените на ваш API-ключ и ID-чата администраторов
API_TOKEN = '8041888206:AAGPDnHLJywXotSq0eegHWwPQ20J3jstriM'
ADMIN_CHAT_ID = '-1002217794018'

# Создаем объект бота
bot = telebot.TeleBot(API_TOKEN)

# Хранение состояния пользователя и их сообщений для отслеживания
user_state = {}
user_message_map = {}  # Сопоставление сообщений пользователя и ID администратора

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с 5 кнопками
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    # Назначаем текст для каждой кнопки
    button_texts = [
        "Жалобы на участников", 
        "Получение приписки", 
        "Апелляция наказаний", 
        "Предложения и пожелания для чата", 
        "Связь с администрацией"
    ]
    
    # Создаем кнопки на основе текста
    buttons = [types.KeyboardButton(text=text) for text in button_texts]
    
    markup.add(*buttons)
    bot.send_message(
        message.chat.id, 
        "Здравствуйте, добро пожаловать в чат-бот администрации чата HUB_Anime! Выберите тему нашей беседы:", 
        reply_markup=markup
    )

# Обработчик нажатий на кнопки и отправка определенного текста
@bot.message_handler(func=lambda message: message.text in [
    "Жалобы на участников", 
    "Получение приписки", 
    "Апелляция наказаний", 
    "Предложения и пожелания для чата", 
    "Связь с администрацией"
])
def handle_button_click(message):
    if message.text == "Жалобы на участников":
        response = ("Укажите, какие правила были нарушены, и прикрепите доказательства. "
                    "Чтобы прикрепить скриншот или видео, опубликуйте его (например, на Imgur) "
                    "и пригласите свидетелей нарушения (если они есть).")
    elif message.text == "Получение приписки":
        response = ("Для того чтобы получить приписку, укажите свой никнейм, установленный в чате, "
                    "прикрепите доказательство, что вы достигли Топ-15 месяца (скриншот на Imgur), "
                    "и укажите желаемую приписку.")
    elif message.text == "Апелляция наказаний":
        response = ("Кто выдал вам наказание? (Если неизвестно, не указывайте этот пункт.) "
                    "Какое наказание вам выдали и по какой причине? "
                    "Прикрепите доказательства вашей невиновности (скриншоты на Imgur).")
    elif message.text == "Предложения и пожелания для чата":
        response = "Какие у вас есть пожелания для чата?"
    elif message.text == "Связь с администрацией":
        response = "Напишите тему разговора, и свободный администратор ответит вам в ближайшее время."
    
    # Отправляем ответ пользователю
    bot.send_message(message.chat.id, response)
    
    # Сохраняем состояние пользователя
    user_state[message.chat.id] = message.text
    
    # Уведомляем администраторов
    bot.send_message(ADMIN_CHAT_ID, f"Пользователь выбрал: {message.text} и готов отправить сообщение.")

# Обработчик сообщений пользователей (после выбора темы)
@bot.message_handler(func=lambda message: message.chat.id in user_state)
def forward_message_to_admin(message):
    # Пересылаем сообщение пользователя администратору
    user_id = message.chat.id
    selected_topic = user_state.get(user_id)
    
    # Отправляем уведомление администратору и пересылаем сообщение
    forwarded_message = bot.forward_message(ADMIN_CHAT_ID, user_id, message.message_id)

    # Сохраняем сопоставление сообщения администратора и пользователя
    user_message_map[forwarded_message.message_id] = user_id

# Обработчик сообщений от администратора (ответ пользователю)
@bot.message_handler(func=lambda message: message.chat.id == int(ADMIN_CHAT_ID) and message.reply_to_message)
def reply_to_user(message):
    # Получаем ID пользователя по пересланному сообщению
    original_message_id = message.reply_to_message.message_id
    user_id = user_message_map.get(original_message_id)

    if user_id:
        # Отправляем сообщение пользователю
        bot.send_message(user_id, f"Сообщение от администратора: {message.text}")
        bot.send_message(ADMIN_CHAT_ID, "Сообщение успешно отправлено пользователю.")
    else:
        bot.send_message(ADMIN_CHAT_ID, "Не удалось найти пользователя для ответа.")

# Запуск бота
bot.polling()
