from django.http import HttpResponse

from us_ignite.common import csv_unicode as csv


def export_users(profile_queryset):
    """Prepares the users to be exported."""
    user_list = []
    for profile in profile_queryset:
        user_list.append((profile.full_name, profile.user.email))
    return user_list


def csv_response(filename, row_list):
    """Returns a CSV response from the row list and the filename given."""
    response = HttpResponse(content_type='text/csv')
    writer = csv.UnicodeWriter(response)
    for row in row_list:
        writer.writerow(row)
    response['Content-Disposition'] = (
        'attachment; filename="%s.csv"' % filename)
    response['Content-Length'] = len(response.content)
    return response
