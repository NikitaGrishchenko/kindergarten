
from rest_framework import serializers

from .models import Day


class DayListSerializer(serializers.ModelSerializer):
    """ Сериализатор дней для отправки на фронт """

    class Meta:
        model = Day
        fields = ["pk", "type_group", "count_person", "date"]
