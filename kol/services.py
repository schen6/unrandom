import sys
sys.path.append('/home/panther/vagabond/')
from crawlers.tencent import get_tencent_translate
from django.db import models
from groups.models import GroupKOLAssociation
from kol.models import Post

from django.utils.timezone import make_aware
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncDay, TruncWeek, TruncMonth, TruncYear


def translate(text):
    return get_tencent_translate(text)


def get_group_post_analytics(group_id, aggregation='Day', range_days=90):
    shanghai_tz = pytz.timezone(settings.TIME_ZONE)
    start_date = datetime.now(shanghai_tz) - timedelta(days=range_days)

    uids = GroupKOLAssociation.objects.filter(group_id=group_id).values_list('uid', flat=True)

    # Select the appropriate truncation function based on the aggregation
    if aggregation == 'Day':
        trunc_func = TruncDate('created_at_timestamp')
    elif aggregation == 'Week':
        trunc_func = TruncWeek('created_at_timestamp')
    elif aggregation == 'Month':
        trunc_func = TruncMonth('created_at_timestamp')
    elif aggregation == 'Year':
        trunc_func = TruncYear('created_at_timestamp')
    else:
        raise ValueError("Invalid aggregation type")

    analytics = (Post.objects.filter(uid__in=uids, created_at_timestamp__gte=start_date)
                 .annotate(date=trunc_func)
                 .values('date')
                 .annotate(
        total_shares=Sum('share_count'),
        total_likes=Sum('like_count'),
        total_comments=Sum('comment_count'),
        total_plays=Sum('play_count')
    )
                 .order_by('date'))

    result = [
        {
            'date': entry['date'].strftime('%Y-%m-%d' if aggregation == 'Day' else
                                '%Y-%m-%d' if aggregation == 'Week' else
                                '%Y-%m' if aggregation == 'Month' else
                                '%Y'),
            'total_shares': entry['total_shares'],
            'total_likes': entry['total_likes'],
            'total_comments': entry['total_comments'],
            'total_plays': entry['total_plays']
        }
        for entry in analytics
    ]

    return result