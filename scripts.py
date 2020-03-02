import random
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Subject
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

child_name = 'Фролов Иван'
try:
    child = Schoolkid.objects.get(full_name__contains=child_name)
except ObjectDoesNotExist:
    print("Ученик не найден")
except MultipleObjectsReturned:
    print("Найдено несколько учеников. Конкретизируйте запрос.")

def fix_marks(schoolkid):
    bad_points=[2,3]
    child_points=Mark.objects.filter(schoolkid=schoolkid, points__in=bad_points)
    for point in child_points:
        mark = Mark.objects.get(id=point.id)
        mark.points = 5
        mark.save()

def remove_chastisements(schoolkid):
    chastisements=Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()

Commendations=['Молодец!','Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!']

def create_commendation(schoolkid, subject_title):
    try:
        subject=Subject.objects.get(title__contains=subject_title, year_of_study=schoolkid.year_of_study)
        lesson=Lesson.objects.filter(subject__title=subject.title, year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter).order_by('-date')[0]
        Commendation.objects.create(text=random.choice(Commendations), created=lesson.date, schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
    except ObjectDoesNotExist:
        print("Не найден предмет")
    except MultipleObjectsReturned:
        print("Найдено несколько предметов. Конкретизируйте запрос.")