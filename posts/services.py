from datetime import date


def validate_user_age(user) -> bool:
    """Проверяет, достиг ли пользователь возраста 18 лет."""

    birthday = user.birth_date
    today = date.today()
    user_age = (today.year - birthday.year)
    if birthday.month >= today.month and birthday.day > today.day:
        user_age -= 1

    if user_age >= 18:
        return True

    return False
