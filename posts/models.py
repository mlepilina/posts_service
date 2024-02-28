from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):

    title = models.CharField(max_length=1000, verbose_name='заголовок')
    text = models.TextField(verbose_name='основной текст')
    image = models.ImageField(upload_to='posts/', verbose_name='изображение', **NULLABLE)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    change_date = models.DateTimeField(auto_now=True, verbose_name='дата и время редактирования', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор поста')

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return f'{self.author} {self.title}'


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор комментария')
    text = models.TextField(verbose_name='текст комментария')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    change_date = models.DateTimeField(auto_now=True, verbose_name='дата и время редактирования', **NULLABLE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.pk} {self.post} {self.text}'

