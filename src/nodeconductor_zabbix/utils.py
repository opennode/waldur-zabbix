import datetime

from django.contrib.contenttypes.models import ContentType


def get_period(request):
    period = request.query_params.get('period')
    return period or format_period(datetime.date.today())


def format_period(date):
    return '%d-%02d' % (date.year, date.month)


def filter_for_qs(model, instance):
    if not isinstance(instance, list):
        instance = [instance]

    content_type = ContentType.objects.get_for_model(instance[0])
    object_ids = [obj.id for obj in instance]
    return model.objects.filter(content_type=content_type, object_id__in=object_ids)
