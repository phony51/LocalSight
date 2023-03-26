from telebot import TeleBot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from pathlib import Path
from keyboards import *
from date_validator import *
from word_validator import *
from answers import *

# https://qna.habr.com/q/619516

''' will
1. Уникальный ключ записи
2. Find поправить (даты, теги)
3. Добавить в desrptn и feedback сразу требования к тексту (русский и тд)
'''

# main("CREATE TABLE Sights (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `area` TEXT, `year` INTEGER, `season` TEXT, `month` TEXT, `description` TEXT, `feedback` TEXT, `mark` INTEGER, `tags` TEXT, `date` TEXT, `userid` INTEGER, `src` TEXT);")
# main("CREATE TABLE Moders (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `moder_id` INTEGER, UNIQUE(moder_id));")
# main("CREATE TABLE Reactions (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `userid` INTEGER, `messageid` INTEGER, `flag` INTEGER);")
# main("DROP TABLE Reactions;")
# main("DELETE FROM Reactions;")
# main(f"INSERT INTO Moders (`moder_id`) VALUES ('806902493')")


def main(sql):
    try:
        connection = sqlite3.connect("localsight_db.db")
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result 
    except Exception as e:
        print(f'{e}')

TOKEN_BOT = '5729656929:AAHSxglQG-DeuNCWOlENB91H8usjvoAzkps'
bot = TeleBot(TOKEN_BOT)
MODER_IDS = main(f"SELECT moder_id FROM Moders;")

def menu(message):  
    bot.send_message(message.chat.id, '⬇️<b>Выберите, что вы хотите сделать:\n</b>/new - Создать новую запись о месте\n\n/find - Подобрать подходящие вам места по фильтрам\n\n/feedback - Отзывы/предложения/Нашли баг', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
    bot.register_next_step_handler(message, get_menu_mess)


def get_menu_mess(message):
    if message.content_type == 'text':
        if message.text == '/start':
                start(message)

        elif message.text == '/new':
            get_area(message)
        
        elif message.text == '/find':
            get_find_criterion(message)

        elif message.text == '/feedback':
            start_support(message)

        elif len(set(message.text.lower().split()) & set(["как", "дела"])) == 2:
            bot.send_message(message.chat.id, f'<b>{howareyou[random.randint(0, 3)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        elif len(set(message.text.lower().split()) & set(["что", "делаешь"])) == 2:
            bot.send_message(message.chat.id, f'<b>{whatareudo[random.randint(0, 3)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        elif len(set(message.text.lower().split()) & set(["как", "тебя", "зовут"])) == 3:
            bot.send_message(message.chat.id, f'<b>{botname[random.randint(0, 2)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        elif len(set(message.text.lower().split()) & set(["кто", "ты"])) == 2: 
            bot.send_message(message.chat.id, f'<b>{whoareu[random.randint(0, 1)]}</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Здравствуй, хочешь предложить свою достопримечательность/место в Ульяновске? Вперёд!\n\nУльяновск</b> — прекрасный город, который привлекает туристов историческими и архитектурными памятниками, а также природными достопримечательностями. Он известен не только как родина отца Октябрьской революции В. И. Ленина, но и как место, где появились на свет выдающиеся русские писатели Н. М. Карамзин и И. А. Гончаров.', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
    menu(message)


@bot.message_handler(commands=['new'])
def get_area(message):
    bot.send_message(message.chat.id, '1️⃣ <b>В каком районе находится достопримечательность/место?</b>', reply_markup=kb_area, parse_mode="html")
    bot.register_next_step_handler(message, get_year)


def get_year(message):
    if message.content_type == 'text':
        if message.text.lower() in ("засвияжский", "заволжский", "железнодорожный", "ленинский", "засвияжском", "заволжском", "железнодорожном", "ленинском"):
            bot.send_message(message.chat.id, '2️⃣ <b>В каком году Вы посещали достопримечательность/место?</b>', reply_markup=kb_year, parse_mode="html")
            bot.register_next_step_handler(message, get_season, message.text)
        elif message.text.lower() == "🔙 назад":
            menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_season(message, ms_area):
    if message.content_type == 'text':
        if message.text in ("2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"):
            bot.send_message(message.chat.id, '3️⃣ <b>В каком сезоне Вы посещали её/его?</b>', reply_markup=kb_season, parse_mode="html")
            bot.register_next_step_handler(message, get_month, ms_area, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '1️⃣ <b>В каком районе находится достопримечательность/место?</b>', reply_markup=kb_area, parse_mode="html")
            bot.register_next_step_handler(message, get_year)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_month(message, ms_area, ms_year):
    if message.content_type == 'text':
        if message.text.lower() in ("зима", "весна", "лето", "осень"):
            if message.text.lower() == "зима":
                for btn_winter in btns_winter:     
                    kb_mnh.add(btn_winter)
            elif message.text.lower() == "весна":
                for btn_spring in btns_spring:     
                    kb_mnh.add(btn_spring)
            elif message.text.lower() == "лето":
                for btn_summer in btns_summer:     
                    kb_mnh.add(btn_summer)
            elif message.text.lower() == "осень":
                for btn_autumn in btns_autumn:     
                    kb_mnh.add(btn_autumn)

            bot.send_message(message.chat.id, '4️⃣ <b>В каком месяце Вы посещали достопримечательность/место?</b>', reply_markup=kb_mnh, parse_mode="html")
            bot.register_next_step_handler(message, get_description, ms_area, ms_year, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '2️⃣ <b>В каком году Вы посещали достопримечательность/место?</b>', reply_markup=kb_year, parse_mode="html")
            bot.register_next_step_handler(message, get_season, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_description(message, ms_area, ms_year, ms_sesson):
    if message.content_type == 'text':
        if message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '3️⃣ <b>В каком сезоне Вы посещали её/его?</b>', reply_markup=kb_season, parse_mode="html")
            bot.register_next_step_handler(message, get_month, ms_area, message.text)
        elif message.text.lower() in ("декабрь", "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь"):
            bot.send_message(message.chat.id, '5️⃣ <b>Опишите данную достопримечательность/место: </b>\n<em>Не менее 100 символов</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_feedback, ms_area, ms_year, ms_sesson, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_feedback(message, ms_area, ms_year, ms_sesson, ms_month):
    if message.content_type == 'text':
        if message.text.lower() == "🔙 назад":
                bot.send_message(message.chat.id, '4️⃣ <b>В каком месяце Вы посещали достопримечательность/место?</b>', reply_markup=kb_mnh, parse_mode="html")
                bot.register_next_step_handler(message, get_description, ms_area, ms_year, message.text)
        elif 100 <= len(message.text) <= 1000:
            if check_words(message.text.lower()):
                bot.send_message(message.chat.id, '6️⃣ <b>Напишите отзыв о ней/нём: </b>\n<em>Не менее 50 символов</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.register_next_step_handler(message, get_mark, ms_area, ms_year, ms_sesson, ms_month, message.text)
            elif check_words(message.text.lower()) == 'forbidden_words':
                bot.send_message(message.chat.id, '🙁<b>Текст содержит недопустимые слова. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
            else:
                bot.send_message(message.chat.id, '🙁<b>Текст может содержать только буквы русского алфавита, цифры и базовые знаки препинания. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, количество символов должно быть не менее 100 и не более 1000. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_mark(message, ms_area, ms_year, ms_sesson, ms_month, ms_description):
    if message.content_type == 'text':
        if message.text.lower() == "🔙 назад":
                bot.send_message(message.chat.id, '5️⃣ <b>Опишите данную достопримечательность/место: </b>\n<em>Не менее 100 символов</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.register_next_step_handler(message, get_feedback, ms_area, ms_year, ms_sesson, message.text)
        elif 50 <= len(message.text) <= 1000:
            if check_words(message.text.lower()):
                bot.send_message(message.chat.id, '7️⃣ <b>Ваша субъективная оценка </b>\n<em>От 1 до 10:</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.register_next_step_handler(message, get_tags, ms_area, ms_year, ms_sesson, ms_month, ms_description, message.text)
            elif check_words(message.text.lower()) == 'forbidden_words':
                bot.send_message(message.chat.id, '🙁<b>Текст содержит недопустимые слова. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message) 
            else:
                bot.send_message(message.chat.id, '🙁<b>Текст может содержать только буквы русского алфавита, цифры и базовые знаки препинания. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                menu(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, количество символов должно быть не менее 50 и не более 1000. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_tags(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback):
    if message.content_type == 'text':
        if message.text in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            bot.send_message(message.chat.id, '8️⃣ <b>Напишите тег/теги (Через #), относящиеся к данному месту</b>\n<em>Минимум 1; через пробел</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, choise_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '6️⃣ <b>Напишите отзыв о ней/нём: </b>\n<em>Не менее 50 символов</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_mark, ms_area, ms_year, ms_sesson, ms_month, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, число должно быть от 1 до 10. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def choise_photo(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark):
    if message.content_type == 'text':
        if '#' in message.text and len(message.text.replace('#', '')) >= 2 and check_words(message.text.replace('#', '').lower()):
            bot.send_message(message.chat.id,  '9️⃣ <b>У вас есть фотография этой достопримечательности/места?</b>', reply_markup=kb_y_n, parse_mode="html")
            bot.register_next_step_handler(message, choise_moder, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, message.text)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '7️⃣ <b>Ваша субъективная оценка </b>\n<em>От 1 до 10:</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_tags, ms_area, ms_year, ms_sesson, ms_month, ms_description, message.text)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует писать тег через "#" и длинною не меньше 2 знаков, используя русские символы</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def choise_moder(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags):
    if message.content_type == 'text':
        if message.text.lower() == "✅да":
            bot.send_message(message.chat.id, '📸<b>Отправьте фотографию: </b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, get_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags)
        elif message.text.lower() == "❌нет":     
            bot.send_message(message.chat.id, '📥<b>Данные получены, отправить на модерацию?</b>', reply_markup=kb_y_n, parse_mode="html")
            bot.register_next_step_handler(message, insert_and_send, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags)
        elif message.text.lower() == "🔙 назад":
            bot.send_message(message.chat.id, '8️⃣ <b>Напишите тег/теги (Через #), относящиеся к данному месту</b>\n<em>Минимум 1; через пробел</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, choise_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, message.text)
        else:
            bot.send_message(message.chat.id, '🫢<b>Выберите одно из предложенных ответов. Попробуйте снова</b>', reply_markup=kb_y_n, parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_photo(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags):
    try:
        Path(f'files/{message.chat.id}/').mkdir(parents = True, exist_ok = True) # Создание папки

        if message.content_type == 'photo':              
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id) 
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'files/{message.chat.id}/{datetime.datetime.now().strftime("%Y%m%d_%H%M")}{file_info.file_path.replace("photos/", "")}'
            bot.send_message(message.chat.id, '📥<b>Данные получены, отправить на модерацию?</b>', reply_markup=kb_y_n, parse_mode="html")
          
            with open(src, 'wb') as new_file:   # Сохраняем файла
                new_file.write(downloaded_file)
            bot.register_next_step_handler(message, insert_and_send, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags, src)

        else:
            bot.send_message(message.chat.id, '🫢<b>Нужно отправлять изображение, а не прочие типы данных. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)

    except Exception as e:
        bot.send_message(message.chat.id, '🫢<b>Произошла ошибка при сохранении фотографии. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)
        print(f'!!!{e}')


bot.message_handler(content_types=["text"])
def insert_and_send(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, ms_tags, src = False):
    if message.content_type == 'text':
        if message.text.lower() == "✅да":
            bot.send_message(message.chat.id, '🆗 <b>Спасибо за то, что внесли данные. Мы уведовим вас, если данные пройдут модерацию</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")  
            date = datatime.now().strftime("%d.%m.%Y") 
            for moder_id in MODER_IDS:
                if src:
                    main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{ms_area}', '{ms_year}', '{ms_sesson}', '{ms_month}', '{ms_description}', '{ms_feedback}', '{ms_mark}', '{ms_tags}', '{date}', '{message.from_user.id}', '{src}')")
                    dates_id = main(f"SELECT id FROM Sights WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND tags='{ms_tags}' AND userid='{message.from_user.id}' AND `src`='{src}';")
                    if dates_id:
                        bot.send_photo(moder_id[0], open(src,'rb'))
                        bot.send_message(moder_id[0], f"<b>Район:</b> {ms_area}\n\n<b>Год:</b> {ms_year}\n\n<b>Сезон:</b> {ms_sesson}\n\n<b>Месяц:</b> {ms_month}\n\n<b>Описание:</b> {ms_description}\n\n<b>Отзыв:</b> {ms_feedback}\n\n<b>Субъективная оценка пользователя:</b> {ms_mark}\n\n{ms_tags}", reply_markup = mod_markup(dates_id), parse_mode="html")
                    else:
                        bot.send_message(message.chat.id, '🫢<b>Произошла ошибка при сохранении фотографии. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                        menu(message)
                        print("dates_id не найдено")
                else:
                    main(f"INSERT INTO Sights (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `tags`, `date`, `userid`, `src`) VALUES ('{ms_area}', '{ms_year}', '{ms_sesson}', '{ms_month}', '{ms_description}', '{ms_feedback}', '{ms_mark}', '{ms_tags}', '{date}', '{message.from_user.id}', '0')")
                    dates_id = main(f"SELECT id FROM Sights WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND tags='{ms_tags}' AND userid='{message.from_user.id}' AND src='0';")
                    if dates_id:
                        bot.send_message(moder_id[0], f"<b>Район:</b> {ms_area}\n\n<b>Год:</b> {ms_year}\n\n<b>Сезон:</b> {ms_sesson}\n\n<b>Месяц:</b> {ms_month}\n\n<b>Описание:</b> {ms_description}\n\n<b>Отзыв:</b> {ms_feedback}\n\n<b>Субъективная оценка пользователя:</b> {ms_mark}\n\n{ms_tags}", reply_markup = mod_markup(dates_id), parse_mode="html")
                    else:
                        bot.send_message(message.chat.id, '🫢<b>Произошла ошибка при сохранении фотографии. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                        menu(message)
                        print("dates_id не найдено")

        elif message.text.lower() == "❌нет":
            bot.send_message(message.chat.id, '🔜<b>Будем ждать вас снова!</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            start(message)

        else:
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)



@bot.message_handler(commands=['feedback'])
def start_support(message):
    bot.send_message(message.chat.id , '↘️<b>Оставьте ваше сообщение:</b>\n<em>Я передам его модераторам бота</em>', parse_mode="html", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_support)


def get_support(message):
    bot.send_message(message.chat.id, '😇<b>Cпасибо за обратную связь, мы ценим это!</b>', parse_mode="html")
    for moder_id in MODER_IDS:
        bot.send_message(moder_id[0], f"<b>Сообщение пользователя</b> @{message.from_user.username}", parse_mode="html", reply_markup=ReplyKeyboardRemove())
        bot.forward_message(moder_id[0], message.chat.id, message.message_id)



# Кнопки для модератора
def mod_markup(dates_id):
    markup_y_n = InlineKeyboardMarkup()
    markup_y_n.row_width = 2
    markup_y_n.add(InlineKeyboardButton("✅Запостить", callback_data=f"1 {dates_id[0][0]} Yes"), InlineKeyboardButton("❌Проигноривовать", callback_data=f"1 {dates_id[0][0]} No"))
    return markup_y_n

def reaction_markup(postid):
    likes, dislikes = get_reactions_from_bd(postid)
    markup_reaction = InlineKeyboardMarkup()
    markup_reaction.row_width = 2
    markup_reaction.add(InlineKeyboardButton(f"🔥 {likes}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes}", callback_data=f"reaction {postid} 0"))
    return markup_reaction

def get_reactions_from_bd(postid):
    flags = main(f'SELECT flag FROM Reactions WHERE messageid = "{postid}"') # [(1,), (1,), (1,)]
    sum_or_likes = 0
    for flag in flags:
        sum_or_likes += flag[0]
    dislike = len(flags) - sum_or_likes
    return [sum_or_likes, dislike]

# Обработчик call_back
@bot.callback_query_handler(func=lambda call: True)
def get_call(call):
    call_data = call.data.split()
    if call_data[0] == '1':
        print(call_data)
        data = main(f"SELECT * FROM Sights WHERE `id`={call_data[1]}")
        area, year, season, month, description, feedback, mark, tags, src = data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][11]
        for moder_id in MODER_IDS:
            if call_data[2] == "Yes":
                if src != '0':
                    bot.send_photo(-1001701836271, open(src, 'rb'))
                bot.send_message(-1001701836271, f"<b>🏢Район: </b> {area}\n\n<b>⏳Год: </b> {year}\n\n<b>🏝️Сезон: </b> {season}\n\n<b>📅Месяц: </b> {month}\n\n<b>📝Описание: </b> {description}\n\n<b>📈Отзыв: </b> {feedback}\n\n<b>🌟Субъективная оценка пользователя: </b> {mark}\n\n{tags}", parse_mode="html")
                bot.send_message(moder_id[0], "✅<b>Пост опубликован</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.send_message(data[0][10], '✅<b>Спасибо, ваши данные успешно прошли модерацию и опубликованы на канал!</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                bot.answer_callback_query(call.id, "OK, POST PUBLISHED")

            elif call_data[2] == "No":
                bot.send_message(data[0][10], '❌<b>Простите, данные не прошли модерацию. Повторите попытку</b>', parse_mode="html")
                bot.send_message(moder_id[0], "❌<b>Пост проигнорирован</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="html")
                main(f"DELETE FROM Sights WHERE `id` = {call_data[1]};")
                bot.answer_callback_query(call.id, "OK, POST IGNORED")

    
    if call_data[0] == 'reaction':   #  ['reaction', '1', '1']     
        userid_to_check = main(f"SELECT userid, messageid, flag FROM Reactions WHERE messageid = '{call_data[1]}' AND userid = '{call.message.chat.id}'")
        if userid_to_check:
            if tuple([call.message.chat.id, int(call_data[1])]) == userid_to_check[0][:2]: # сравнивание пары userid - messageid
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Вы уже поставили реакцию!")
                 
        else:
            bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id=call.message.message_id, reply_markup = recreation_markup_plus(call_data[1], call_data[2]))
            main(f"INSERT INTO Reactions (`userid`, `messageid`, `flag`) VALUES ('{call.message.chat.id}', '{call_data[1]}', '{call_data[2]}')")      
            if call_data[2] == "1":  
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="LIKE")
            elif call_data[2] == "0":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="DISLIKE")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Произошла ошибка, попробуйте снова!")


def recreation_markup_plus(postid, flag):
    likes, dislikes = get_reactions_from_bd(postid)
    if likes >= 0 and dislikes >= 0:
        recreation_markup_reaction = InlineKeyboardMarkup()
        if flag == '1':
            recreation_markup_reaction.row(InlineKeyboardButton(f"🔥 {likes + 1}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes}", callback_data=f"reaction {postid} 0"))
        elif flag == '0':
            recreation_markup_reaction.row(InlineKeyboardButton(f"🔥 {likes}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes + 1}", callback_data=f"reaction {postid} 0"))
        else:
            print('Error recreation_markup_plus')
        return recreation_markup_reaction
    else:
        print('Кол-во лайков меньше 0')
        return recreation_markup_reaction.row(InlineKeyboardButton(f"🔥 {likes}", callback_data=f"reaction {postid} 1"), InlineKeyboardButton(f"❄ {dislikes}", callback_data=f"reaction {postid} 0"))
        


@bot.message_handler(commands=['find'])
def get_find_criterion(message): 
    bot.send_message(message.chat.id, '🔍<b>Выберите, по чему вы хотите найти место</b>', reply_markup=kb_criterion, parse_mode="html")
    bot.register_next_step_handler(message, processing_criterion)


def processing_criterion(message):
    if message.content_type == 'text':
        if message.text.lower() == "дата/промежуток дат":
            bot.send_message(message.chat.id , '📆<b>Введите дату в формате ДД.ММ.ГГГГ</b>\n<em>Или ДД.ММ.ГГГГ-ДД.ММ.ГГГГ</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, for_date)
        elif message.text.lower() == "район":
            bot.send_message(message.chat.id , '🏢<b>Выберите район</b>', reply_markup=kb_area, parse_mode="html")
            bot.register_next_step_handler(message, for_area)
        elif message.text.lower() == "год":
            bot.send_message(message.chat.id , '⏳<b>Выберите год</b>', reply_markup=kb_year, parse_mode="html")
            bot.register_next_step_handler(message, for_year)
        elif message.text.lower() == "оценка":
            bot.send_message(message.chat.id , '🔢<b>Напишите число или промежуток чисел</b>\n<em>Через "-"</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, for_mark)
        elif message.text.lower() == "тег":
            bot.send_message(message.chat.id , '💱<b>Напишите один или несколько тегов через "#"</b>\n<em>Через пробел</em>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            bot.register_next_step_handler(message, for_tag)
        elif message.text.lower() == "🔙 назад":
            menu(message)
        else:
            bot.send_message(message.chat.id , '🙁<b>Пожалуйста, выберите критерий из списка</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def send_posts(message, posts): # Добавить 10 мест (пока что по 1)
    if posts:
        for post in posts[:1]: # [:5]
            print("путь фотки:", post[9])
            if post[9] != '0':
                bot.send_photo(message.chat.id, open(post[9], 'rb'))
            bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}\n\n<b>📅Месяц: </b> {post[4]}\n\n<b>📝Описание: </b> {post[5]}\n\n<b>📈Отзыв: </b> {post[6]}\n\n<b>🌟Субъективная оценка пользователя: </b> {post[7]}\n\n{post[8]}", reply_markup = reaction_markup(post[0]), parse_mode="html")
            posts.remove(posts[0]) # [x:]
            bot.send_message(message.chat.id , '🔄<b>Загрузить еще?</b>', reply_markup=kb_y_n, parse_mode="html")
            bot.register_next_step_handler(message, get_answer_to_send, posts)
    else:
        bot.send_message(message.chat.id , '🔚<b>Записей по данной категории нет</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def get_answer_to_send(message, posts):
    if message.content_type == 'text':
        if message.text.lower() == "✅да":
            send_posts(message, posts)
        elif message.text.lower() == "❌нет":
            bot.send_message(message.chat.id , '😊<b>Надеюсь, вы нашли место по душе</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
        else: 
            bot.send_message(message.chat.id, '🙁<b>Извините, не понимаю Вас. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_tag(message):
    if message.content_type == 'text':
        if '#' in message.text and len(message.text.replace('#', '')) > 1 and check_words(message.text.replace('#', '')):
            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE year LIKE "{message.text}"')
            send_posts(message, posts)
        elif message.text.lower() == "назад":
            processing_criterion(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует писать тег через "#" и длинною не меньше 2 знаков, используя русские символы</b>', parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_mark(message):
    if message.content_type == 'text':
        if message.text.lower() == "назад":
            processing_criterion(message)
        elif "-" in message.text:
            if message.text.split('-')[0] in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                if message.text.split('-')[1] in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                    mark_first = message.text.split('-')[0]
                    mark_second = message.text.split('-')[1]
                    posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE mark >= "{mark_first}" AND date <= "{mark_second}"')
                    send_posts(message, posts)
                else:
                    bot.send_message(message.chat.id, '🙁<b>Следует вводить число или промежуток чисел через "-". Попробуйте снова</b>', parse_mode="html")
                    menu(message)
            else:
                bot.send_message(message.chat.id, '🙁<b>Следует вводить число или промежуток чисел через "-". Попробуйте снова</b>', parse_mode="html")
                menu(message)
        elif message.text in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE mark LIKE "{message.text}"')
            send_posts(message, posts)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует вводить число или промежуток чисел через "-". Попробуйте снова</b>', parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_year(message):
    if message.content_type == 'text':
        if message.text.lower() in ("2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"):
            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE year LIKE "{message.text}"')
            send_posts(message, posts)
        elif message.text.lower() == "назад":
            processing_criterion(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует выбрать год из списка. Попробуйте снова</b>', parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_area(message):
    if message.content_type == 'text':
        if message.text.lower() in ("засвияжский", "заволжский", "железнодорожный", "ленинский"):
            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE area LIKE "{message.text.title()}"')
            send_posts(message, posts)
        elif message.text.lower() == "назад":
            processing_criterion(message)
        else:
            bot.send_message(message.chat.id, '🙁<b>Следует выбрать район из списка. Попробуйте снова</b>', parse_mode="html")
            menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


def for_date(message):
    if message.content_type == 'text':
        if message.text.lower() == "назад":
            processing_criterion(message)
        else:
            for i in message.text.split():
                if '.' in i:               
                    dates = i.split('-') 
                    if len(dates) == 1:
                        ms_date_part = is_date(dates[0])
                        if ms_date_part:
                            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE date LIKE "%{ms_date_part}%"') # [(), (), ()]
                            send_posts(message, posts)
                        else:
                            bot.send_message(message.chat.id, '🙁<b>Извините, мне не удалось найти дату/даты в сообщении. Попробуйте снова</b>', parse_mode="html")
                            menu(message)
                    elif len(dates) == 2:
                        ms_date_part1 = is_date(dates[0])
                        ms_date_part2 = is_date(dates[1])
                        if ms_date_part1 and ms_date_part2:
                            posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE date >= "{ms_date_part1}" AND date <= "{ms_date_part2}"')
                            send_posts(message, posts)   
                        else:
                            bot.send_message(message.chat.id, '🙁<b>Извините, мне не удалось найти дату/даты в сообщении. Попробуйте снова</b>', parse_mode="html")
                            menu(message)
                else:
                    bot.send_message(message.chat.id, '🙁<b>Следует вводить дату в формате ДД.ММ.ГГГГ. Попробуйте снова</b>', parse_mode="html")
                    menu(message)
    else:
        bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
        menu(message)


while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception as e:
        print(datetime.datetime.now(), e)
        time.sleep(5)
        continue