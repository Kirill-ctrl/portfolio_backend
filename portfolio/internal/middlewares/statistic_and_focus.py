from datetime import datetime, timedelta
from flask import request


def get_sort_statistic(func):
    def wrapper(*args, **kwargs):
        data = datetime.date(datetime.now())
        delta = timedelta(weeks=1)  # default
        if request.args.get('sort_statistic'):
            sort_statistic = request.args.get('sort_statistic')
            if sort_statistic == 'month':
                delta = timedelta(days=30)
            elif sort_statistic == 'year':
                delta = timedelta(days=365)
            elif sort_statistic == 'all_time':
                delta = timedelta(days=999999999)
        result_sort_statistic = data - delta
        response = func(*args, result_sort_statistic=result_sort_statistic, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper


def get_sort_focus(func):
    def wrapper(*args, **kwargs):
        data = datetime.date(datetime.now())
        delta = timedelta(weeks=1)  # default
        if request.args.get('sort_focus'):
            sort_focus = request.args.get('sort_focus')
            if sort_focus == 'month':
                delta = timedelta(days=30)
            elif sort_focus == 'year':
                delta = timedelta(days=365)
            elif sort_focus == 'all_time':
                delta = timedelta(days=999999999)
        result_sort_focus = data - delta
        response = func(*args, result_sort_focus=result_sort_focus, **kwargs)
        return response
    wrapper.__name__ = func.__name__
    return wrapper
