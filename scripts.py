from random import choice

from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, \
    Lesson

COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def fix_marks(schoolkid: Schoolkid) -> None:
    bad_marks = [2, 3]
    good_mark = 5

    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=bad_marks
    ).update(
        points=good_mark
    )


def remove_chastisements(schoolkid: Schoolkid) -> None:
    student_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    student_chastisements.delete()


def create_commendation(
        schoolkid: Schoolkid,
        subject: str,
        commendations: list
) -> None:
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('-date').first()

    if not last_lesson:
        print(
            f'Предмет {subject} не найден.',
            'Проверьте правильность написания и повторите попытку.'
        )
        return

    Commendation.objects.create(
        text=choice(commendations),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )


def get_student(name: str) -> Schoolkid | None:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print(
            f'Ученик {name} не найден.',
            'Проверьте правильность написания и повторите попытку.'
        )
    except Schoolkid.MultipleObjectsReturned:
        print(
            f'По вашему запросу \'{name}\' найдено несколько учеников.',
            'Уточните запрос и повторите попытку.'
        )
    else:
        return schoolkid
