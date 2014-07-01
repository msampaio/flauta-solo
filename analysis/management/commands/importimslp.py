from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from progressbar import ProgressBar
from analysis.models import Composition, Composer, Collection, CompositionType, MusicXMLScore, MusicData
import os
import configparser
import base64
import urllib.request
import json
import datetime
import re

IMSLP_USERNAME = None


def dic_add_attrib(output_dic, input_dic, pair):
    if pair[1] in input_dic:
        output_dic[pair[0]] = input_dic[pair[1]]


def get_date(data_dict):
    birth = []
    for k in ['Born Year', 'Born Month','Born Day']:
        if k.isalnum():
            birth.append(int(data_dict[k]))
        else:
            birth = None
            break

    if birth:
        birth = datetime.date(*birth)

    death = []
    for k in ['Died Year', 'Died Month','Died Day']:
        if k.isalnum():
            death.append(int(data_dict[k]))
        else:
            death = None
            break

    if death:
        death = datetime.date(*death)

    return birth, death


def split_title_composer(parent):
    title, composer = parent.split('(')
    return title.rstrip(' '), composer.rstrip(')')


def get_imslp_data(id_number, i_type='3', retformat='json'):

    def make_api_info(o_id_number):
        api_info = {
            'account': IMSLP_USERNAME,
            'type': i_type
        }

        id_number = str(o_id_number)
        if i_type == '1':
            id_number = 'Category:' + id_number

        bytes_id = bytes(id_number.lstrip('0'), 'utf-8')
        id_number = base64.b64encode(bytes_id).decode('utf-8')

        api_info['id'] = id_number
        api_info['disclaimer'] = 'accepted'
        api_info['retformat'] = retformat

        return api_info

    def make_url(api_info):
        api_base_url = 'http://imslp.org/imslpscripts/API.ISCR.php?'
        data = []
        for k, v in list(api_info.items()):
            data.append('{0}={1}'.format(k, v))
        data = '/'.join(data)

        return api_base_url + data

    api_information = make_api_info(id_number)
    url = make_url(api_information)
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    return json.loads(html)


def make_composer(composer_id, composer):
    imslp_data = get_imslp_data(composer_id, '1')['0']
    extvals = imslp_data['extvals']
    intvals = imslp_data['intvals']

    composer.imslp_id = composer_id
    composer.first_name = intvals['firstname']
    composer.last_name = intvals['lastname']
    composer.date_birth, composer.date_death = get_date(extvals)

    if 'Nationality' in extvals:
        composer.nationality = extvals['Nationality']
    else:
        composer.nationality = None
    composer.time_period = extvals['Time Period']


def make_composition(imslp_id_code):
    imslp_data = get_imslp_data(imslp_id_code)['0']

    # TODO: confirm intvals key = '0'
    intvals = imslp_data['intvals']['0']
    extvals = imslp_data['extvals']
    title, composer_id = split_title_composer(imslp_data['parent'])

    composition = Composition()

    try:
        composer = Composer.objects.get(imslp_id=composer_id)
    except Composer.DoesNotExist:
        composer = Composer()
        make_composer(composer_id, composer)
        composer.save()

    collection, created = Collection.objects.get_or_create(imslp_id=imslp_id_code, name=title)

    composition.composer = composer
    composition.collection = collection

    composition.title = title
    composition.publisher_information = extvals['Publisher Information']
    composition.editor = extvals['Editor']
    composition.misc_notes = extvals['Misc. Notes']

    composition.uploader = intvals['uploader']
    composition.raw_pagecount = intvals['rawpagecount']
    composition.pagecount = intvals['pagecount']
    composition.description = intvals['description']
    composition.imslp_filename = intvals['filename']
    composition.rating = intvals['rating']

    # TODO: define how to get composition_type and subtitle
    composition.composition_type = None
    composition.subtitle = None

    return composition


def import_imslp_data(base_filename, imslp_id_code):
    try:
        music_data = MusicData.objects.get(score__filename=base_filename)
    except MusicData.DoesNotExist:
        raise("Don't have MusicData for %s. Aborting" % base_filename)

    try:
        Composition.objects.get(music_data=music_data)
    except ObjectDoesNotExist:
        composition = make_composition(imslp_id_code)
        composition.music_data = music_data
        composition.save()


## main

def get_imslp_username():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.musiAnalysis.cfg'))
    return config.get('Imslp', 'user')


def get_code_from_filename(filename):
    base_filename = os.path.splitext(filename)[0]
    return base_filename[2:].split('_')[0]


class Command(BaseCommand):
    args = '<file1 [file2 ...]>'
    help = 'Import metadata from IMSLP'

    def handle(self, *args, **options):
        # FIXME: find the problem with IF322968 files
        def not_pattern(x):
            pattern = '^IF322968.*E.xml$'
            if re.match(pattern, x):
                return False
            else:
                return True

        global IMSLP_USERNAME

        progress = ProgressBar()
        # FIXME: find the problem with IF322968 files
        files = [x for x in args if os.path.basename(x)[0] == 'I' and not_pattern(x)]
        # files = [x for x in args if os.path.basename(x)[0] == 'I']

        try:
            IMSLP_USERNAME = get_imslp_username()
        except configparser.NoSectionError:
            raise CommandError("Can't read the ~/.musiAnalysis.cfg file")

        for filename in progress(files):
            base_filename = os.path.basename(filename)
            imslp_id_code = get_code_from_filename(base_filename)
            import_imslp_data(base_filename, imslp_id_code)
