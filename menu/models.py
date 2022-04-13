from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver


class Product(models.Model):
    """
    Продукт
    """
    id = id
    name = models.CharField(
        max_length=255,
        verbose_name=("Наименование"),
    )
    protein = models.FloatField(verbose_name=("Белки"), blank=True, null=True)
    fats = models.FloatField(verbose_name=("Жиры"), blank=True, null=True)
    carbohydrates = models.FloatField(verbose_name=("Углеводы"), blank=True, null=True)


    class Meta:
        verbose_name = ("Продукт")
        verbose_name_plural = ("Продукты")

    def __str__(self):
        return f"{self.name}"



class Dish(models.Model):
    """
    Блюдо
    """

    name = models.CharField(
        max_length=255,
        verbose_name=("Наименование"),
    )
    caloric = models.FloatField(verbose_name=("Калорийность"), blank=True, null=True)

    class Meta:
        verbose_name = ("Блюдо")
        verbose_name_plural = ("Блюда")

    def __str__(self):
        return f"{self.name}"



class ProductInDish(models.Model):
    """
    Продукты в блюде
    """
    dish = models.ForeignKey(
        Dish,
        models.CASCADE,
        null=True,
        blank=True,
        related_name="dish",
        verbose_name=("Блюдо"),
    )
    product = models.ForeignKey(
        Product,
        models.CASCADE,
        null=True,
        blank=True,
        related_name="product",
        verbose_name=("Продукт"),
    )

    count = models.FloatField(
        verbose_name=("Норма на чел."),
    )
    protein = models.FloatField(verbose_name=("Белки"), blank=True, null=True)
    fats = models.FloatField(verbose_name=("Жиры"), blank=True, null=True)
    carbohydrates = models.FloatField(verbose_name=("Углеводы"), blank=True, null=True)
    caloric = models.FloatField(verbose_name=("Калорийность"), blank=True, null=True)
    unit = models.CharField(
        max_length=255,
        verbose_name=("Единица измерения"),
    )
    unit_after = models.CharField(
        max_length=255,
        verbose_name=("Единица измерения после перевода"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = ("Продукт в блюде")
        verbose_name_plural = ("Продукты в блюде")

    def __str__(self):
        return f"{self.product}"

    def get_count(self):
        return f"{self.count}"



class Day(models.Model):
    """
    День приема пищи

    """
    TYPE_GROUP = (
        ('Y', 'Ясли'),
        ('S', 'Старшая группа'),
    )
    DAY_WEEK = (
        ('MON', 'Понедельник'),
        ('TUE', 'Вторник'),
        ('SAT', 'Среда'),
        ('THU', 'Четверг'),
        ('FRI', 'Пятница'),
    )
    PARITY_OF_THE_WEEK = (
        ('EVEN', 'Четная неделя'),
        ('ODD', 'Нечетная неделя'),
    )

    date = models.DateField(null=True, blank=True, verbose_name=("Дата"))

    type_group = models.CharField(max_length=300, choices = TYPE_GROUP, verbose_name=("Тип группы"))

    count_person = models.IntegerField(default=20,verbose_name=("Количество детей"))

    day_week = models.CharField(max_length=300, choices = DAY_WEEK,verbose_name=("День недели"))

    parity_of_the_week = models.CharField(max_length=300, choices = PARITY_OF_THE_WEEK, verbose_name=("Четность недели"))

    class Meta:
        verbose_name = ("День приема пищи")
        verbose_name_plural = ("Дни приема пищи")


    def get_type_group(self):
        return f"{self.type_group}"

    def __str__(self):
        return f"{self.date} {self.type_group}"

class Eating(models.Model):
    """
    Прием пищи

    """
    TYPE_EATING = (
        ('Z', 'Завтрак'),
        ('SZ', 'Второй завтрак'),
        ('O', 'Обед'),
        ('P', 'Полдник'),
    )
    eating = models.ForeignKey(
        Day,
        models.CASCADE,
        null=True,
        blank=True,
        related_name="eating",
        verbose_name=("Прием пищи"),
    )
    type_eating = models.CharField(max_length=300, choices = TYPE_EATING, verbose_name=("Какой приём пищи?"))
    dish = models.ManyToManyField(Dish, verbose_name=("Блюда"))

    class Meta:
        verbose_name = ("Прием пищи")
        verbose_name_plural = ("Приемы пищи")

    def __str__(self):
        return f"{self.eating} {self.type_eating}"


