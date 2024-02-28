from rest_framework.validators import ValidationError


class TitleValidator:
    """Валидация заголовка поста."""
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = value.get(field, None)
            if field_value:
                self.find_forbidden_words(field_value)

    def find_forbidden_words(self, value):
        """Проверка на присутствие в заголовке запрещенных слов"""
        value = value.lower()
        forbidden_words = ['ерунда', 'глупость', 'чепуха']
        for word in forbidden_words:
            if word in value:
                raise ValidationError("Запрещено использовать слова: ерунда, глупость, чепуха.")

