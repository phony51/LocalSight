import json

# """
# add new museums
# """
# with open("E:\DataTurism\museum_2gis.json", 'r', encoding='utf8') as json_museum:
#     museum = json.load(json_museum)


# for ms in museum:
#     adress = f'{ms["address"]["components"][0]["street"]}, {ms["address"]["components"][0]["number"]}'
#     name = f'{ms["org"]["name"]}'
#     try:
#         url = f'{ms["contact_groups"][0]["contacts"][2]["text"]}' 
#         main_photo = f'{ms["external_content"][0]["main_photo_url"]}' 
#         rating = f'{ms["reviews"]["org_rating"]}'
      
        
#     except Exception:
#         continue
#     print(f"\nИмя: {name}\nАдрес: {adress}\nРейтинг: {rating}\nСсылка: {url}\nФото: {main_photo}\n") # , ' : ', f"{mon}/n{tue}/n{wed}/n{thi}/n{fri}/n{sat}/n{sun}



# '''
# schedule museums
# ''' 
# for day in f'{ms["schedule"]}':
#     mon = f'с {day["Mon"]["working_hours"][0]["from"]} до {day["Mon"]["working_hours"][0]["to"]}'
#     tue = f'с {day["Tue"]["working_hours"][0]["from"]} до {day["Tue"]["working_hours"][0]["to"]}'
#     wed = f'с {day["Wed"]["working_hours"][0]["from"]} до {day["Wed"]["working_hours"][0]["to"]}'
#     thi = f'с {day["Thu"]["working_hours"][0]["from"]} до {day["Thu"]["working_hours"][0]["to"]}'
#     fri = f'с {day["Fri"]["working_hours"][0]["from"]} до {day["Fri"]["working_hours"][0]["to"]}'
#     sat = f'с {day["Sat"]["working_hours"][0]["from"]} до {day["Sat"]["working_hours"][0]["to"]}'
#     sun = f'с {day["Sun"]["working_hours"][0]["from"]} до {day["Sun"]["working_hours"][0]["to"]}'


"""
add new cinemas
"""
with open("E:\DataTurism\cinema_2gis.json", 'r', encoding='utf8') as json_museum:
    cinema = json.load(json_museum)

for cn in cinema:
    adress = f'{cn["address"]}'

