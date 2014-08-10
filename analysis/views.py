from io import StringIO, BytesIO
import zipfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from analysis.models import MusicData, Composition
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
    total_duration = request.POST['select-duration']
    time_signature = request.POST['select-time-signature']

    select_filter('title__iexact', title, kwargs, template='%s')
    select_filter('key', key, kwargs)
    select_filter('total_duration', total_duration, kwargs)
    select_filter('time_signature', time_signature, kwargs)

    compositions = Composition.objects.filter(**kwargs)

    args = {
        'input_size': len(compositions),
        'filter_collection': title,
        'filter_key': key,
        'filter_total_duration': total_duration,
        'filter_time_signature': time_signature,
        }

    return compositions, args


def make_filter_args(composition_model):
    args = {'compositions': uniq_items_in_model('title', composition_model),
            'keys': uniq_items_in_model('key'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
    }
    return args


def show_ambitus(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(ambitus.analysis(compositions))
        return render(request, 'ambitus_result.html', args)

    args = make_filter_args(Composition)
    return render(request, 'ambitus.html', args)


def show_intervals(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(intervals.analysis(compositions))
        return render(request, 'intervals_result.html', args)

    args = make_filter_args(Composition)
    return render(request, 'intervals.html', args)


def list_compositions(request):
    compositions = Composition.objects.all()

    args = {
        "compositions": compositions
    }
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

    args = make_filter_args(Composition)
    return render(request, 'durations.html', args)


def show_contour(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(contour.analysis(compositions))
        return render(request, 'contour_result.html', args)

    args = make_filter_args(Composition)
    return render(request, 'contour.html', args)


def show_pure_data(request):
    if request.method == 'POST':
        markov_order = request.POST['select-markov-order']

        compositions, args = filter_compositions(request)
        pure_data_args = pure_data.analysis(compositions, order=int(markov_order))
        args.update(pure_data_args)

        buff = BytesIO()
        zip_archive = zipfile.ZipFile(buff, mode='w')

        for key, value in pure_data_args.items():
            zip_archive.writestr(key + '.coll', "".join(value))

        zip_archive.close()

        response = HttpResponse(buff.getvalue(), mimetype="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % "markov-chains.zip"
        return response

    args = make_filter_args(Composition)
    args['order_numbers'] = range(1, 11)

    return render(request, 'pure_data.html', args)


def show_cluster_duration_ambitus(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(cluster_duration_ambitus.analysis(compositions))
        return render(request, 'cluster_duration_ambitus_result.html', args)

    args = make_filter_args(Composition)
    return render(request, 'cluster_duration_ambitus.html', args)


def show_cluster_intervals_frequency(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(cluster_intervals_frequency.analysis(compositions))
        return render(request, 'cluster_intervals_frequency_result.html', args)

    args = make_filter_args(Composition)
    return render(request, 'cluster_intervals_frequency.html', args)


def show_cluster_durations_frequency(request):
    if request.method == 'POST':
        compositions, args = filter_compositions(request)
        args.update(cluster_durations_frequency.analysis(compositions))
        return render(request, 'cluster_durations_frequency_result.html', args)

    args = make_filter_args(Composition)
    return render(request, 'cluster_durations_frequency.html', args)


def show_cluster_contour(request):
    if request.method == 'POST':
        contour_size = request.POST['select-contour-size']
        compositions, args = filter_compositions(request)
        args.update(cluster_contour.analysis(compositions, int(contour_size)))
        return render(request, 'cluster_contour_result.html', args)

    args = make_filter_args(Composition)
    args['size_numbers'] = range(2, 5)
    return render(request, 'cluster_contour.html', args)    


def show_cluster_all(request):
    if request.method == 'POST':
        contour_size = request.POST['select-contour-size']
        compositions, args = filter_compositions(request)
        args.update(cluster_all.analysis(compositions, int(contour_size)))
        return render(request, 'cluster_all_result.html', args)

    args = make_filter_args(Composition)
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
