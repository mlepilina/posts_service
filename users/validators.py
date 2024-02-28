from rest_framework.validators import ValidationError


class EmailValidator:
    """Валидация почты."""
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = value.get(field, None)
            if field_value:
                self.find_email_domaine(field_value)

    def find_email_domaine(self, value):
        """Проверяет, содержит ли почта разрешенные домены."""
        if 'mail.ru' not in value and 'yandex.ru' not in value:
            raise ValidationError("Разрешены только домены: mail.ru, yandex.ru. Проверьте правильность написания почты.")


class PasswordValidator:
    """Валидация пароля."""
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = value.get(field, None)
            if field_value:
                self.validate_password(field_value)

    def validate_password(self, value):
        """Проверяет, соответствует ли значение паттерну пароля."""
        if len(value) < 8:
            raise ValidationError("Длина пароля должна быть более 8 символов.")
        elif not any(ch.isdigit() for ch in value):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


class PhoneValidator:
    """Валидация номера телефона."""
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = value.get(field, None)
            if field_value:
                self.validate_phone(field_value)

    def validate_phone(self, value):
        """Проверяет, соответствует ли значение паттерну номера телефона."""
        if len(str(value)) < 9:
            raise ValidationError("Длина номера телефона должна быть более 8 символов.")
