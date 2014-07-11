from us_ignite.sections.models import SectionPage


def get_section_page(**kwargs):
    data = {
        'title': 'Sample page',
        'section': 'about',
    }
    data.update(**kwargs)
    return SectionPage.objects.create(**data)
