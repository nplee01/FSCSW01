import os, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from btengine.stocks import download_all_stocks

class Command(BaseCommand):
    help = 'Download latest stock prices'

    def handle(self, *args, **options):
        download_all_stocks()
