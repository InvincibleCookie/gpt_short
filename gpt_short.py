import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

# Установка API-ключа OpenAI
openai.api_key = "token"
# https://platform.openai.com/account/api-keys вот тут ключ бери (не забудь vpn включить)
# Создание объектов бота и диспетчера
bot = Bot(token="token")
dp = Dispatcher(bot)


# Функция для создания выдержки из длинного текста
def generate_excerpt(text, length):
    # Задаем параметры для вызова GPT-3 API
    completions = openai.Completion.create(
        engine="text-davinci-003",  # выбираем модель
        prompt=f"Сделай краткую выдержку из главного по тексту:\n{text}",
        # передаем длинный текст и желаемую длину выдержки
        max_tokens=length,  # ограничиваем количество токенов в выдержке
        n=1,  # ограничиваем количество вариантов выдержки
        stop=None,  # останавливаем генерацию текста без дополнительных условий
        temperature=0.5,  # задаем температуру для случайного выбора токенов
    )

    # Извлекаем выдержку из ответа от ChatGPT
    excerpt = completions.choices[0].text.strip()
    return excerpt


@dp.message_handler(Text)
async def generate_excerpt_handler(message: types.Message):
    # Получаем текст от пользователя
    text = message.text.strip()
    length = 600  # Длина выдержки в символах
    #Генерируем выдержку и отправляем пользователю
    excerpt = generate_excerpt(text, length)
    await message.answer(excerpt)




# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
