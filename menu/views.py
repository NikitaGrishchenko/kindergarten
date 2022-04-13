import xlwt
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from rest_framework import generics

from .models import Day, Dish, ProductInDish
from .serializers import DayListSerializer


class DayView(ListView):
    template_name = 'index.html'
    model = Day

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["day_for_young"] = Day.objects.filter(type_group="Y")
        context["day_for_old"] = Day.objects.filter(type_group="S")
        return context


class DayListView(generics.ListCreateAPIView):
    """  """

    serializer_class = DayListSerializer
    queryset = Day.objects.all()


class ScheduleView(TemplateView):
    template_name = "schedule.html"


class SuccessView(TemplateView):
    template_name = "success.html"

def recalculation_of_dishes(self):
    """
    Функция для пересчета БЖУ в продуктах
    """
    product_in_dishes = ProductInDish.objects.all()

    # БЖУ и калорийность продуктов в блюде
    for product_in_dish in product_in_dishes:
        # белки
        if product_in_dish.product.protein != None:
            product_in_dish.protein = round(product_in_dish.product.protein * product_in_dish.count / 100, 2)
            product_in_dish.save()
        # жиры
        if product_in_dish.product.fats != None:
            product_in_dish.fats = round(product_in_dish.product.fats * product_in_dish.count / 100, 2)
            product_in_dish.save()
        # углеводы
        if product_in_dish.product.carbohydrates != None:
            product_in_dish.carbohydrates = round(product_in_dish.product.carbohydrates * product_in_dish.count / 100, 2)
            product_in_dish.save()
        # калорийность продукта в блюде
        if product_in_dish.protein != None and product_in_dish.fats != None and product_in_dish.carbohydrates != None:
            product_in_dish.caloric = round((product_in_dish.protein*4)+(product_in_dish.fats*9)+(product_in_dish.carbohydrates*3.75),2)
            product_in_dish.save()

    # Калорийность блюда
    dishes = Dish.objects.all()

    for dish in dishes:
        product_in_dishes = ProductInDish.objects.filter(dish=dish)
        if product_in_dishes.count() > 0:
            caloric = 0
            count = 0
            for product_in_dish in product_in_dishes:
                if product_in_dish.caloric != None and product_in_dish.count != None:
                    caloric = caloric + product_in_dish.caloric
                    count = count + product_in_dish.count
                if caloric != 0 and count !=0:
                    dish.caloric = round(caloric/count*100, 2)
        dish.save()

    return redirect("/success")



def export_data_to_file(request):
    """ Функция, для экспорта данных из базы данных """

    # дефолтные настройки для экспорта данных в excel в библиотеке xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="menu.xls"'
    wb = xlwt.Workbook(encoding='utf-8')

    # ws = wb.add_sheet('Users')

    # настройка стилей
    style = xlwt.XFStyle()

    style_bold = xlwt.XFStyle()
    style_bold.font.bold = True
    # font_style = xlwt.XFStyle()
    #

    # columns = ['Username', 'First name', 'Last name', 'Email address', ]

    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num], font_style)




    # получение данных
    days = Day.objects.all()

    # запись данных в excel
    for day in days:
        # создание листа
        ws = wb.add_sheet(f'{day.get_type_group_display()} {day.date}')
        row_num = 0
        # запись основной информации о дне
        ws.write(row_num, 2, f"МЕНЮ-ТРЕБОВАНИЕ НА ВЫДАЧУ ПРОДУКТОВ ПИТАНИЯ В ВОЗРАСТНОЙ ГРУППЕ {day.get_type_group_display()} № ____________", style)
        row_num = row_num + 1
        ws.write(row_num, 2, f"НА {day.date}, {day.get_day_week_display()}, {day.get_parity_of_the_week_display()}", style)
        row_num = row_num + 1
        ws.write(row_num, 2, f"Учреждение _______________МБДОУ \"Детский сад № 28 \"Нэбзый\"_______________________", style)
        row_num = row_num + 1
        ws.write(row_num, 2, f"Структурное подразделение __________________________________________________________________________", style)
        row_num = row_num + 1
        ws.write(row_num, 2, f"Материально ответственное лицо _____________________________________________________________________", style)
        row_num = row_num + 3
        ws.write(row_num, 0, f"Приём пищи", style_bold)
        ws.write(row_num, 1, f"Блюдо", style_bold)
        ws.write(row_num, 2, f"Ингредиент", style_bold)
        ws.write(row_num, 3, f"Количество на 1 человека", style_bold)
        ws.write(row_num, 4, f"Общее количество для блюда", style_bold)
        ws.write(row_num, 5, f"Общее количество за день", style_bold)
        for eat in day.eating.all():
            row_num = row_num + 1
            ws.write(row_num, 0, f"{eat.get_type_eating_display()} ", style_bold)
            for one_dish in eat.dish.all():
                ws.write(row_num, 1, f"{one_dish.name}", style)
                row_num = row_num + 1
                for ingredient in one_dish.dish.all():
                    ws.write(row_num, 2, f"{ingredient.product}", style)
                    ws.write(row_num, 3, f"{ingredient.count} {ingredient.unit}", style)
                    ws.write(row_num, 4, f"{food_calculator(ingredient.count, day.date)} {ingredient.unit_after}", style)
                    ws.write(row_num, 5, f"{amount_ingredient_per_day(day.id, ingredient.product)} {ingredient.unit_after}", style)
                    row_num = row_num + 1
        row_num = row_num + 2
        ws.write(row_num, 0, f"Руководитель учреждения     __________Гиш С.Ш.",
        style_bold)
        row_num = row_num + 1
        ws.write(row_num, 0, f"Повар      _______________",
        style_bold)
        row_num = row_num + 1
        ws.write(row_num, 0, f"Врач (диетсестра)      ___________",
        style_bold)
        row_num = row_num + 1
        ws.write(row_num, 0, f"Кладовщик     __________Войтлева Н.М.",
        style_bold)
        row_num = row_num + 1
    wb.save(response)
    return response


def food_calculator(norm, date):
    """ Метод считающий количество продукта на всех детей """
    day = Day.objects.filter(date=date)
    result = (norm * day[0].count_person) / 1000
    return result

def amount_ingredient_per_day(day_id, ingredient):
    """ Сумма ингредиента за день """

    count = 0
    day = Day.objects.filter(pk=day_id)
    for item in day:
        for eat in item.eating.all():
            for dishes in eat.dish.all():
                for item_ingredient in dishes.dish.all():
                    if (item_ingredient.product == ingredient):
                        count = count + item_ingredient.count
    result = (count * day[0].count_person) / 1000
    return result
