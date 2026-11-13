from django.db import models

class Pokemon(models.Model):
    title_ru = models.CharField(verbose_name='Название', max_length=200)
    title_en = models.CharField(verbose_name='Название (анг.)', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название (яп.)', max_length=200, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    photo = models.ImageField(verbose_name='Изображение', upload_to="pokemons/", blank=True, null=True)
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционировал',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE,
        related_name='entities',
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появится в', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет в', blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Атака', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)

    def __str__(self):
        return f'{self.lat} {self.lon}'