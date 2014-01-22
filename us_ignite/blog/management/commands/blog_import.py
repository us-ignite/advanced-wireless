from datetime import datetime

from django.core.management.base import BaseCommand

from us_ignite.blog import consumer


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print "Importing blogposts."
        post_list = consumer.consume(count=1000)
        print "Imported %s posts" % len(post_list)
        print "Done at %s." % datetime.now()
