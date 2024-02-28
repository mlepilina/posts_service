from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='maria@mail.ru',
            phone='123456789',
            birth_date='2000-01-01',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('12345')
        user.save()
