from datetime import date, timedelta

from rooms.models import RoomsApplicationModel, Reservation

def get_reservs_date(kwargs):
    room = RoomsApplicationModel.objects.get(pk=kwargs['pk'])
    # Извлечение броней связанных с данным жильем
    reservs = Reservation.objects.filter(apartment_id=room.pk).filter(status=True)
    reserv_days_in = []      # Список занятых дат прибытия
    reserv_days_out = []     # Список занятых дат выезда
    # Извлечение списка зарезервированных дат для передачи в календарь
    for reserv in reservs:
        if reserv.end_date >= date.today():
            start_day = reserv.start_date
            end_day = reserv.end_date
            delta_days = int((end_day - start_day).days)
            day = 0
            for day in range(delta_days):
                reserv_days_in.append(start_day.strftime("%d-%m-%Y"))
                reserv_days_out.append(end_day.strftime("%d-%m-%Y"))
                start_day += timedelta(days=1)
                end_day -= timedelta(days=1)
    reserv_days_in.sort()   # Сортировка дат по возрастанию
    reserv_days_out.sort()  # Сортировка дат по возрастанию
    room.views += 1
    room.save()
    return(reserv_days_in, reserv_days_out)