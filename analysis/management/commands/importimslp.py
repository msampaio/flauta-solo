from django.core.management.base import BaseCommand, CommandError
from progressbar import ProgressBar
from analysis.models import Composition, Composer, CompositionType
import os
import configparser
import base64
import urllib
import json
import datetime
import logging


def get_cfg_info(section, item, cfg_file='.musiAnalysis.cfg'):
    basename = os.path.expanduser('~')
    path = os.path.join(basename, cfg_file)
    config = configparser.ConfigParser()
    config.read(path)

    return config.get(section, item)


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

    if birth != None:
        birth = datetime.date(*birth)

    death = []
    for k in ['Died Year', 'Died Month','Died Day']:
        if k.isalnum():
            death.append(int(data_dict[k]))
        else:
            death = None
            break

    if death != None:
        death = datetime.date(*death)

    return birth, death


def filename_to_id_code(filename):
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    first_char = base_filename[0]
    if first_char == 'I':
        return base_filename[2:].split('_')[0]
    elif first_char == 'E':
        print(("There is no IMSLP code for {0}.".format(base_filename)))
    else:
        print(("Wrong file. {0}.".format(base_filename)))


def split_title_composer(parent):
    title, composer = parent.split('(')
    return title.rstrip(' '), composer.rstrip(')')


def get_imslp_data(id_number, i_type='3', retformat='json'):

    def make_api_info(id_number, i_type, retformat):
        api_info = {}
        api_info['account'] = get_cfg_info('Imslp', 'user')
        api_info['type'] = i_type

        id_number = str(id_number)
        if i_type == '1':
            id_number = 'Category:' + id_number

        bytes_id = bytes(id_number.lstrip('0'), 'utf-8')
        id_number = base64.b64encode(bytes_id).decode('utf-8')

        api_info['id'] = id_number
        api_info['disclaimer'] = 'accepted'
        api_info['retformat'] = retformat

        return api_info

    def make_url(api_info, initURL):
        data = []
        for k, v in list(api_info.items()):
            data.append('{0}={1}'.format(k, v))
        data = '/'.join(data)

        return initURL + data

    def get_url(url):
        response = urllib.request.urlopen(url)
        return response.read()

    initURL='http://imslp.org/imslpscripts/API.ISCR.php?'
    api_info = make_api_info(id_number, i_type, retformat)
    url = make_url(api_info, initURL)
    html = get_url(url).decode('utf-8')

    return json.loads(html)

def make_composer(composer_id, composer=None):
    composer = Composer()

    imslp_data = get_imslp_data(composer_id, '1')['0']
    extvals = imslp_data['extvals']
    intvals = imslp_data['intvals']

    composer.first_name = intvals['firstname']
    composer.last_name = intvals['lastname']
    composer.date_birth, composer.date_death = get_date(extvals)
    if 'Nationality' in extvals:
        composer.nationality = extvals['Nationality']
    else:
        composer.nationality = None
    composer.time_period = extvals['Time Period']


def make_composition(imslp_data, id_code, composition):

    extvals = imslp_data['extvals']

    # TODO: confirm intvals key = '0'
    intvals = imslp_data['intvals']['0']

    # TODO: how to handle the composer id in imslp?
    title, composer_name = split_title_composer(imslp_data['parent'])

    composer = Composer()
    make_composer(composer_name)
    composer.save()

    composition.title = title
    composition.composer = composer
    composition.publisher_information = extvals['Publisher Information']
    composition.editor = extvals['Editor']
    composition.misc_notes = extvals['Misc. Notes']

    composition.uploader = intvals['uploader']
    composition.raw_pagecount = intvals['rawpagecount']
    composition.pagecount = intvals['pagecount']
    composition.imslp_filename = intvals['filename']
    composition.rating = intvals['rating']
    composition.description= intvals['description']
    composition.uploader = intvals['uploader']

    # TODO: define how to define composition_type
    # composition.composition_type = None


def import_imslp_data(filename, options):
    # criar compositor primeiro, composicao e finalmente colecao

    base_filename = os.path.basename(filename)

    # composition
    composition = Composition()
    try:
        id_code = filename_to_id_code(filename)
        make_composition(get_imslp_data(id_code)['0'], id_code, composition)
        composition.save()
        return 0
    except Exception as error:
        logging.error("Couldn't parse music file: %s, %s" % (error, base_filename))
        return 1


class Command(BaseCommand):
    args = '<file1 [file2 ...]>'
    help = 'Import metadata from IMSLP'

    def handle(self, *args, **options):
        progress = ProgressBar()

        for filename in progress(args):
            import_imslp_data(filename, options)
