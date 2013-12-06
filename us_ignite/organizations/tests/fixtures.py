from us_ignite.organizations.models import Organization


def get_organization(**kwargs):
    data = {
        'name': 'US Ignite',
        'slug': 'us-ignite',
    }
    data.update(kwargs)
    return Organization.objects.create(**data)
