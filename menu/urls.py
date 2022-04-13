

from django.conf.urls import url
from django.urls import path

from menu.views import (DayListView, DayView, ScheduleView, SuccessView,
                        export_data_to_file, recalculation_of_dishes)

from . import views

app_name = 'menu'

urlpatterns = [
    path('', DayView.as_view(), name='index'),
    path("schedule/", ScheduleView.as_view(), name="schedule"),
    path("api/schedule/", DayListView.as_view(), name="api-schedule"),
    path('export/', export_data_to_file, name="export"),
    path('recalculation/', recalculation_of_dishes, name="recalculation"),
    path('success/', SuccessView.as_view(), name="success")

]
