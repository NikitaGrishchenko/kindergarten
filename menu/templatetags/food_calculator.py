from django import template

from ..models import Day

register = template.Library()


@register.simple_tag
def food_calculator(norm, date):
    """ Метод считающий количество продукта на всех детей """
    day = Day.objects.filter(date=date)
    result = (norm * day[0].count_person) / 1000
    return result

