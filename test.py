'''
add_sights.py
schedule museums
''' 
# if f'с {ms["schedule"]["Tue"]["working_hours"][0]["from"]}':
#     tue = f'с {ms["schedule"]["Tue"]["working_hours"][0]["from"]} до {ms["schedule"]["Tue"]["working_hours"][0]["to"]}'
# if f'с {ms["schedule"]["Wed"]["working_hours"][0]["from"]}':
#     wed = f'с {ms["schedule"]["Wed"]["working_hours"][0]["from"]} до {ms["schedule"]["Wed"]["working_hours"][0]["to"]}'
# if f'с {ms["schedule"]["Thu"]["working_hours"][0]["from"]}':
#     thi = f'с {ms["schedule"]["Thu"]["working_hours"][0]["from"]} до {ms["schedule"]["Thu"]["working_hours"][0]["to"]}'
# if f'с {ms["schedule"]["Fri"]["working_hours"][0]["from"]}':
#     fri = f'с {ms["schedule"]["Fri"]["working_hours"][0]["from"]} до {ms["schedule"]["Fri"]["working_hours"][0]["to"]}'
# if f'с {ms["schedule"]["Sat"]["working_hours"][0]["from"]}':
#     sat = f'с {ms["schedule"]["Sat"]["working_hours"][0]["from"]} до {ms["schedule"]["Sat"]["working_hours"][0]["to"]}'
# if f'с {ms["schedule"]["Sun"]["working_hours"][0]["from"]}':
#     sun = f'с {ms["schedule"]["Sun"]["working_hours"][0]["from"]} до {ms["schedule"]["Sun"]["working_hours"][0]["to"]}'
# if f'с {ms["schedule"]["Mon"]["working_hours"][0]["from"]}':
#     mon = f'с {ms["schedule"]["Mon"]["working_hours"][0]["from"]} до {ms["schedule"]["Mon"]["working_hours"][0]["to"]}'
# \nРасписание: \n{mon}\n{tue}\n{wed}\n{thi}\n{fri}\n{sat}\n{sun}


'''
add_sights.py
save main photos
'''
# r = requests.get(main_photo) 
# with open(f"ul_mus_img\\{name}.jpg", 'wb') as fd:  # f"ul_mus_img\\{name}.jpg" путь к фотке
#             for photo in r.iter_content():
#                 fd.write(photo)


'''
bot.py
send posts
'''
# elif post[1] != "None" and post[2] != "None" and post[3] != "None" and post[4] != "None" and post[5] != "None" and post[6] != "None" and post[7] != "None":
#     bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}\n\n<b>📅Месяц: </b> {post[4]}\n\n<b>📝Описание: </b> {post[5]}\n\n<b>📈Отзыв: </b> {post[6]}\n\n<b>🌟Субъективная оценка пользователя: </b> {post[7]}", reply_markup = reaction_markup(post[0]), parse_mode="html")
# elif post[1] != "None" and post[2] != "None" and post[3] != "None" and post[4] != "None" and post[5] != "None" and post[6] != "None":
#     bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}\n\n<b>📅Месяц: </b> {post[4]}\n\n<b>📝Описание: </b> {post[5]}\n\n<b>📈Отзыв: </b> {post[6]}", reply_markup = reaction_markup(post[0]), parse_mode="html")
# elif post[1] != "None" and post[2] != "None" and post[3] != "None" and post[4] != "None" and post[5] != "None":
#     bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}\n\n<b>📅Месяц: </b> {post[4]}\n\n<b>📝Описание: </b> {post[5]}", reply_markup = reaction_markup(post[0]), parse_mode="html")
# elif post[1] != "None" and post[2] != "None" and post[3] != "None" and post[4] != "None":
#     bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}\n\n<b>📅Месяц: </b> {post[4]}", reply_markup = reaction_markup(post[0]), parse_mode="html")
# elif post[1] != "None" and post[2] != "None" and post[3] != "None":
#     bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}", reply_markup = reaction_markup(post[0]), parse_mode="html")
# elif post[1] != "None" and post[2] != "None":
#     bot.send_message(message.chat.id, f"<b>🏢Район: </b> {post[1]}\n\n<b>⏳Год: </b> {post[2]}\n\n<b>🏝️Сезон: </b> {post[3]}\n\n<b>📅Месяц: </b> {post[4]}\n\n<b>📝Описание: </b> {post[5]}", reply_markup = reaction_markup(post[0]), parse_mode="html")


'''
bot.py
def processing_criterion
'''
# elif message.text.lower() == "год посещения":
#     bot.send_message(message.chat.id , '⏳<b>Выберите год</b>', reply_markup=kb_year, parse_mode="html")
#     bot.register_next_step_handler(message, for_year)

# def for_year(message):
#     if message.content_type == 'text':
#         if message.text.lower() in ("2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"):
#             posts = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights WHERE year LIKE "{message.text}"')
#             send_posts(message, posts)
#         elif message.text.lower() == "назад":
#             processing_criterion(message)
#         else:
#             bot.send_message(message.chat.id, '🙁<b>Следует выбрать год из списка. Попробуйте снова</b>', parse_mode="html")
#             menu(message)
#     else:
#         bot.send_message(message.chat.id, '📄<b>Следует отправлять текст. Попробуйте снова</b>', reply_markup=ReplyKeyboardRemove(), parse_mode="html")
#         menu(message)


'''
bot.py
def get_location
'''
# @bot.message_handler(content_types=["location"])
# def location(message, coord):
    # r = requests.get('https://enterprise.api-maps.yandex.ru/2.1?apikey=cd0b5a9e-e507-4169-9779-dcba427a8812&lang=ru&format=json&geocode=' + coord)
    # print(r)
    
    # if len(r.json()['response']['GeoObjectCollection']['featureMember']) > 0:
    #     address = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
    #         'GeocoderMetaData']['text']
    #     bot.send_message(message.chat.id, 'Ваш адрес\n{}'.format(address))
    # else:
    #     bot.send_message(message.chat.id, 'Не удалось получить Ваш адрес')

