from django.core.management.base import BaseCommand, CommandError
from progressbar import ProgressBar
from analysis.models import Composition, Composer, CompositionType
import os
import configparser
import base64
import urllib.request, urllib.parse, urllib.error
import json


# auxiliary functions
def get_cfg_info(section, item, cfg_file='.musiAnalysis.cfg'):
    basename = os.path.expanduser('~')
    path = os.path.join(basename, cfg_file)
    config = configparser.ConfigParser()
    config.read(path)

    return config.get(section, item)


def dic_add_attrib(output_dic, input_dic, pair):
    if pair[1] in input_dic:
        output_dic[pair[0]] = input_dic[pair[1]]


# imslp id class and functions
def filename_to_id_code(filename):
    base = os.path.basename(filename).rstrip('.xml')
    first_char = base[0]
    if first_char == 'I':
        return base[2:].split('_')[0]
    elif first_char == 'E':
        print(("There is no IMSLP code for {0}.".format(base)))
    else:
        print(("Wrong file. {0}.".format(base)))


# imslp data functions
def get_imslp_data(id_number, i_type='3', retformat='json'):

    def make_api_info(id_number, i_type, retformat):

        api_info = {}
        api_info['account'] = get_cfg_info('Imslp', 'user')
        api_info['type'] = i_type

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


def get_imslp_source_data(id_number):

    imslp_source = {}
    imslp_data = get_imslp_data(id_number, '3')['0']

    extvals = imslp_data['extvals']
    intvals = imslp_data['intvals']

    ext_seq = (
        ('editor', 'Editor'),
        ('publisherInformation', 'Publisher Information'),
        ('miscNotes', 'Misc. Notes')
        )

    score_info_seq = (
        ('description', 'description'),
        ('uploader', 'uploader'),
        ('id', 'index'),
        ('timestamp', 'timestamp'),
        ('pagecount', 'pagecount'),
        ('rawpagecount', 'rawpagecount'),
        ('rating', 'rating')
        )

    parent = imslp_data['parent']
    # extract composer from parent
    parent_composer = parent[parent.find("(")+1:parent.find(")")]

    imslp_source['parent'] = parent
    imslp_source['parent_composer'] = parent_composer

    for ext_pair in ext_seq:
        if ext_pair[1] in extvals:
            dic_add_attrib(imslp_source, extvals, ext_pair)

    for k in list(intvals.keys()):
        if k.isdigit:
            if 'index' in intvals[k]:
                if intvals[k]['index'] == id_number:
                    score_info = intvals[k]
                    for score_info_pair in score_info_seq:
                        dic_add_attrib(imslp_source, score_info, score_info_pair)

    imslp_source['title'] = parent.split(' (')[0]

    return imslp_source


def get_imslp_composer_data(parent_composer):
    """Return an object of ImslpComposer class."""

    imslp_composer = {}
    dic = get_imslp_data(str(parent_composer).encode('utf-8'), '1')['0']

    parent = dic['parent']
    extvals = dic['extvals']
    intvals = dic['intvals']

    ext_seq = (('birthDate', 'Birth Date'),
              ('bornDay', 'Born Day'),
              ('bornMonth', 'Born Month'),
              ('bornYear', 'Born Year'),
              ('deathDate', 'Death Date'),
              ('diedDay', 'Died Day'),
              ('diedMonth', 'Died Month'),
              ('diedYear', 'Died Year'),
              ('pictureCaption', 'Picture Caption'),
              ('timePeriod', 'Time Period'),
              ('nationality', 'Nationality'))

    intSeq = (('firstName', 'firstname'),
              ('lastName', 'lastname'),
              ('normal_name', 'normalname'),
              ('pictureLinkRaw', 'picturelinkraw'),
              ('rawCats', 'rawcats'),
              ('totalDate', 'totaldate'))

    imslp_composer['parent'] = parent

    for ext_pair in ext_seq:
        dic_add_attrib(imslp_composer, extvals, ext_pair)

    for int_pair in intSeq:
        dic_add_attrib(imslp_composer, intvals, int_pair)

    return imslp_composer


def import_imslp_data(filename, options=None):
    id_code = filename_to_id_code(filename)
    source_data = get_imslp_source_data(id_code)
    composer = source_data['parent_composer']
    composer_data = get_imslp_composer_data(composer)

    pass


class Command(BaseCommand):
    args = '<file1 [file2 ...]>'
    help = 'Import metadata from IMSLP'

    def handle(self, *args, **options):
        progress = ProgressBar()

        for filename in progress(args):
            import_imslp_data(filename, options)
