import datetime

datatime = datetime.datetime.now()

def is_date(s):
        day, month, year = datatime.strftime("%d"), datatime.strftime("%m"), datatime.strftime("%Y")   
        date = s.split('.')

        # Если есть только день (месяц м год - актуальный)
        if len(date) == 1 and 1 <= int(date[0]) <= 31:
            day = int(date[0])
            return f"{str(day).zfill(2)}.{str(month).zfill(2)}.{year}"

        # Если есть день, месяц (год актуальный)
        elif len(date) == 2 and 1 <= int(date[0]) <= 31 and 1 <= int(date[1]) <= 12:
            day, month = int(date[0]), int(date[1])
            return f"{str(day).zfill(2)}.{str(month).zfill(2)}.{year}"

        # Если есть день, месяц, год (проверка с 22 и 2022)
        elif len(date) == 3 and 1 <= int(date[0]) <= 31 and 1 <= int(date[1]) <= 12:
            day, month, year = int(date[0]), int(date[1]), int(date[2])
            if len(date[2]) == 4:   
                pass
            elif len(date[2]) == 2:  
                year = f'20{date[2]}'
        
            return f"{str(day).zfill(2)}.{str(month).zfill(2)}.{year}"

        else:
            return f"{str(day).zfill(2)}.{str(month).zfill(2)}.{year}"