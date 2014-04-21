from django.core.management.base import BaseCommand, CommandError
from progressbar import ProgressBar
from analysis.models import Composition, Composer, CompositionType


def import_imslp_data(filename, options):
    pass


class Command(BaseCommand):
    args = '<file1 [file2 ...]>'
    help = 'Import metadata from IMSLP'

    def handle(self, *args, **options):
        progress = ProgressBar()

        for filename in progress(args):
            import_imslp_data(filename, options)
