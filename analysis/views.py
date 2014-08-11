from io import StringIO, BytesIO
import zipfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from analysis.models import MusicData, Composition, Composer, CompositionType
from analysis.computation import ambitus
from analysis.computation import intervals
from analysis.computation import durations
from analysis.computation import contour
from analysis.computation import pure_data
from analysis.computation import cluster_duration_ambitus
from analysis.computation import cluster_intervals_frequency
from analysis.computation import cluster_durations_frequency
from analysis.computation import cluster_contour
from analysis.computation import cluster_all
from analysis.computation import composition_analysis


def home(request):
    return render(request, "index.html")


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login_user.html", {'error': True})
        else:
            return render(request, "login_user.html", {'error': True})

    else:
        return render(request, 'login_user.html')


def dashboard(request):
    music_data_count = MusicData.objects.count()
    composition_count = Composition.objects.count()
    args = {'music_data_count': music_data_count,
            'composition_count': composition_count}
    return render(request, "dashboard.html", args)


def uniq_items_in_model(item, model=MusicData):
    items = model.objects.values(item).distinct().order_by(item)
    return [x[item] for x in items]


def select_filter(name, item, arguments, template='music_data__%s'):
    if item != "all":
        arguments[template % name] = item


def filter_compositions(request):
    kwargs = {}

    title = request.POST['select-composition']
    key = request.POST['select-key']
    composer = request.POST['select-composer']
    composition_type = request.POST['select-composition-type']
    mode = request.POST['select-mode']
    total_duration = request.POST['select-duration']
    time_signature = request.POST['select-time-signature']

    select_filter('title__iexact', title, kwargs, template='%s')
    select_filter('composition__composer__last_name', composer, kwargs)
    select_filter('mode', mode, kwargs)
    select_filter('composition_type', composition_type, kwargs)
    select_filter('key', key, kwargs)
    select_filter('total_duration', total_duration, kwargs)
    select_filter('time_signature', time_signature, kwargs)

    compositions = Composition.objects.filter(**kwargs)

    args = {
        'input_size': len(compositions),
        'filter_collection': title,
        'filter_composer': composer,
        'filter_composition_type': composition_type,
        'filter_mode': mode,
        'filter_key': key,
        'filter_total_duration': total_duration,
        'filter_time_signature': time_signature,
        }

    return compositions, args


def make_filter_args():
    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'composers': uniq_items_in_model('last_name', Composer),
            'tcompositions': uniq_items_in_model('name', CompositionType),
            'modes': uniq_items_in_model('mode'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
    }
    return args


def show_ambitus(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(ambitus.analysis(compositions))
        return render(request, 'ambitus_result.html', args)

    args = make_filter_args()
    return render(request, 'ambitus.html', args)


def show_intervals(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(intervals.analysis(compositions))
        return render(request, 'intervals_result.html', args)

    args = make_filter_args()
    return render(request, 'intervals.html', args)


def list_compositions(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update({'compositions': compositions})
        return render(request, 'compositions_result.html', args)

    args = make_filter_args()
    return render(request, 'compositions.html', args)


def list_composition(request, code):
    composition = Composition.objects.get(music_data__score__code=code)
    args = {'composition': composition}
    return render(request, 'composition.html', args)


def download_composition(request, code):
    data = MusicData.objects.get(score__code=code)

    buff = BytesIO()
    zip_archive = zipfile.ZipFile(buff, mode='w')

    zip_archive.writestr(code + '.xml', data.score.score)
    zip_archive.close()

    response = HttpResponse(buff.getvalue(), mimetype="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % code
    return response


def download_pure_data(request, code):
    data = MusicData.objects.get(score__code=code)

    buff = BytesIO()
    zip_archive = zipfile.ZipFile(buff, mode='w')

    # get pure_data
    for attrib, pd_map, pd_data in pure_data.get_all_attributes(data):
        zip_archive.writestr('{}-{}-data.coll'.format(code, attrib), pd_data)
        zip_archive.writestr('{}-{}-map.coll'.format(code, attrib), pd_map)
    zip_archive.close()

    response = HttpResponse(buff.getvalue(), mimetype="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=pure_data-%s.zip' % code
    return response


def composition_interval(request, code):
    composition = Composition.objects.get(music_data__score__code=code)
    args = intervals.analysis([composition])
    args.update({'composition_code': code})
    return render(request, 'intervals_result.html', args)


def composition_durations(request, code):
    composition = Composition.objects.get(music_data__score__code=code)
    args = durations.analysis([composition])
    args.update({'composition_code': code})
    return render(request, 'durations_result.html', args)


def composition_contour(request, code):
    composition = Composition.objects.get(music_data__score__code=code)
    args = contour.analysis([composition])
    args.update({'composition_code': code})
    return render(request, 'contour_result.html', args)


def composition_cluster(request, code):
    composition = Composition.objects.get(music_data__score__code=code)
    args = composition_analysis.analysis(composition)
    args.update({'composition_code': code})
    return render(request, 'composition_cluster.html', args)


def show_durations(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(durations.analysis(compositions))
        return render(request, 'durations_result.html', args)

    args = make_filter_args()
    return render(request, 'durations.html', args)


def show_contour(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(contour.analysis(compositions))
        return render(request, 'contour_result.html', args)

    args = make_filter_args()
    return render(request, 'contour.html', args)


def zip_pure_data(pure_data_args, attrib):
        buff = BytesIO()
        zip_archive = zipfile.ZipFile(buff, mode='w')

        for key, value in pure_data_args.items():
            zip_archive.writestr(key + '.coll', "".join(value))

        zip_archive.close()

        response = HttpResponse(buff.getvalue(), mimetype="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % "markov-chains-{}.zip".format(attrib)
        return response


def show_pure_data_contour(request):
    if request.method == 'POST':
        markov_order = request.POST['select-markov-order']

        compositions, args = filter_compositions(request)
        pure_data_args = pure_data.generate_contour_chain(compositions, order=int(markov_order))
        args.update(pure_data_args)

        return zip_pure_data(pure_data_args, 'contour')

    args = make_filter_args()
    args['order_numbers'] = range(1, 11)

    return render(request, 'pure_data_contour.html', args)


def show_pure_data_generic(request, attrib, html):
    if request.method == 'POST':
        markov_order = request.POST['select-markov-order']

        compositions, args = filter_compositions(request)
        pure_data_args = pure_data.make_general_chain(compositions, attrib, order=int(markov_order) + 1)
        args.update(pure_data_args)

        return zip_pure_data(pure_data_args, attrib)

    args = make_filter_args()
    args['order_numbers'] = range(1, 11)

    return render(request, 'pure_data_{}.html'.format(html), args)


def show_pure_data_durations(request):
    return show_pure_data_generic(request, 'durations', 'durations')


def show_pure_data_intervals(request):
    return show_pure_data_generic(request, 'intervals_midi', 'intervals')


def show_cluster_duration_ambitus(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(cluster_duration_ambitus.analysis(compositions))
        return render(request, 'cluster_duration_ambitus_result.html', args)

    args = make_filter_args()
    return render(request, 'cluster_duration_ambitus.html', args)


def show_cluster_intervals_frequency(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(cluster_intervals_frequency.analysis(compositions))
        return render(request, 'cluster_intervals_frequency_result.html', args)

    args = make_filter_args()
    return render(request, 'cluster_intervals_frequency.html', args)


def show_cluster_durations_frequency(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(cluster_durations_frequency.analysis(compositions))
        return render(request, 'cluster_durations_frequency_result.html', args)

    args = make_filter_args()
    return render(request, 'cluster_durations_frequency.html', args)


def show_cluster_contour(request):
    if request.method == 'POST':
        contour_size = request.POST['select-contour-size']
        compositions, args = filter_compositions(request)
        args.update(cluster_contour.analysis(compositions, int(contour_size)))
        return render(request, 'cluster_contour_result.html', args)

    args = make_filter_args()
    args['size_numbers'] = range(2, 5)
    return render(request, 'cluster_contour.html', args)    


def show_cluster_all(request):
    if request.method == 'POST':
        contour_size = request.POST['select-contour-size']
        compositions, args = filter_compositions(request)
        args.update(cluster_all.analysis(compositions, int(contour_size)))
        return render(request, 'cluster_all_result.html', args)

    args = make_filter_args()
    args['size_numbers'] = range(2, 5)
    return render(request, 'cluster_all.html', args)


def stats(request):
    args = {
        'number_music_data': MusicData.objects.count(),
        'number_compositions': Composition.objects.count(),
    }
    return render(request, 'stats.html', args)


def show_reports(request):
    return render(request, 'reports.html', {})


def show_pure_data(request):
    return render(request, 'pure_data.html', {})
