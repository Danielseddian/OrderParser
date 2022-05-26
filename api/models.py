from datetime import datetime as dt
from django.db import models

from .tools import get_exchange


class Order(models.Model):
    own_id = models.PositiveSmallIntegerField(unique=True, verbose_name="№")
    order_id = models.PositiveIntegerField(verbose_name="заказ №")
    price = models.FloatField(verbose_name="стоимость,$")
    delivery_date = models.DateField(verbose_name="срок поставки")

    def __str__(self):
        usd = format(self.price, ".2f")
        rub = format(self.price * float(get_exchange()), ".2f")
        return f"Заказ: {self.order_id}, цена: {usd}$ / {rub}₽"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("own_id",)


def format_values(name, value):
    if name == "delivery_date":
        return dt.strptime(value, "%d.%m.%Y")
    return value


def sync_array_to_bd(model, matching_field: str, array: [[]] = None, fields_mapping: dict = None, formatter=None):
    """
    Sync Google sheet and existing model's objects
    :param model: DB Model for sync to array
    :param matching_field: A DB Model field's name to match with an array title
    :param array: An array for updates
    :param fields_mapping: Fields mapping between Google sheets titles and model fields
    :param formatter: Function receiving the model field name and an array value and returning value in expected format
    :return: None
    """
    if array:
        if not formatter:
            def formatter(n, v): return v
        try:
            queryset = model.objects.all()
        except AttributeError:
            raise TypeError("model должен быть классом модели базы данных, унаследованным от django.db.models.Model")
        fields = tuple(f.name for f in model._meta.fields)[1:]
        titles = array[0]

        if len(fields) != len(titles):
            raise IndexError('Количество полей модели базы данных (без "id") и столбцов массива должны соответствовать')

        if fields_mapping:
            if set(fields) != set(fields_mapping.values()):
                raise ValueError("Значения fields_mapping должны соответствовать полям модели базы данных без id.")
            try:
                fields = tuple(fields_mapping[t] for t in titles)
            except KeyError:
                raise KeyError("Ключи fields_mapping должны соответствовать заголовкам массива (в нулевом списке).")

        leaving_objects = []
        for values in array[1:]:
            data = {}
            for i, field in enumerate(fields):
                data[field] = (value := formatter(field, values[i]))
                if field == matching_field:
                    leaving_objects.append(value)
            if not (order := queryset.filter(**{matching_field: data[matching_field]})):
                Order(**data).save()
            else:
                order.update(**data)
        queryset.exclude(**{matching_field + "__in": leaving_objects}).delete()
