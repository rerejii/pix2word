from django.conf import settings
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import PhotoForm
from .models import Photo
from clarifai.rest import ClarifaiApp
from goolabs import GoolabsAPI
import random
from tqdm import tqdm

api_key='99fd740f4ee0432cb45863eeebfa0ce4'
goo_api_key = '33c79ec819c57a6d021899ae4a122c803e24e312497308b68eed781950ea290f' # rerejii アカウント
# goo_api_key = '68b3b5c067f235222b7da12ddd56fa624879aec24f13fcdfc6550ed5024ba37a'
max_concepts=200
min_value=0.0

def dakuten(s):
    if s == 'が':
        s = 'か'
    elif s == 'ぎ':
        s = 'き'
    elif s == 'ぐ':
        s = 'く'
    elif s == 'げ':
        s = 'け'
    elif s == 'ご':
        s = 'こ'
    elif s == 'ざ':
        s = 'さ'
    elif s == 'じ':
        s = 'し'
    elif s == 'ず':
        s = 'す'
    elif s == 'ぜ':
        s = 'せ'
    elif s == 'ぞ':
        s = 'そ'
    elif s == 'だ':
        s = 'た'
    elif s == 'ぢ':
        s = 'ち'
    elif s == 'づ':
        s = 'つ'
    elif s == 'で':
        s = 'て'
    elif s == 'ど':
        s = 'と'
    elif s == 'ば':
        s = 'は'
    elif s == 'び':
        s = 'ひ'
    elif s == 'ぶ':
        s = 'ふ'
    elif s == 'べ':
        s = 'へ'
    elif s == 'ぼ':
        s = 'ほ'
    elif s == 'ぱ':
        s = 'は'
    elif s == 'ぴ':
        s = 'ひ'
    elif s == 'ぷ':
        s = 'ふ'
    elif s == 'ぺ':
        s = 'へ'
    elif s == 'ぽ':
        s = 'ほ'
    elif s == 'ぁ':
        s = 'あ'
    elif s == 'ぃ':
        s = 'い'
    elif s == 'ぅ':
        s = 'う'
    elif s == 'ぇ':
        s = 'え'
    elif s == 'ぉ':
        s = 'お'
    elif s == 'ゃ':
        s = 'や'
    elif s == 'ゅ':
        s = 'ゆ'
    elif s == 'ょ':
        s = 'よ'
    return s

# def index(req, check):
#     if req.method == 'GET':
#         if check == 0:
#             return render(req, 'plays/index.html', {
#                 'form': PhotoForm(),
#                 'photos': Photo.objects.all().order_by('created_at').reverse(), # ここを追加
#                 'messages': '合致する単語が見つかりませんでした...',
#             })
#         else:
#             return render(req, 'plays/index.html', {
#                 'form': PhotoForm(),
#                 'photos': Photo.objects.all().order_by('created_at').reverse(), # ここを追加
#                 'messages': '',
#             })

def index_f(req):
    if req.method == 'GET':
        return render(req, 'plays/index.html', {
            'form': PhotoForm(),
            'photos': Photo.objects.all().order_by('created_at').reverse(), # ここを追加
            'messages': '合致する単語が見つかりませんでした',
        })


    elif req.method == 'POST':
        form = PhotoForm(req.POST, req.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')

        photo = Photo()
        photo.image = form.cleaned_data['image']
        print(photo.image.url)
        # print(form.cleaned_data['image'])
        photo.created_at = datetime.now()
        img_path = settings.BASE_DIR + settings.MEDIA_URL + 'plays/' + str(form.cleaned_data['image'])

        lastObject = Photo.objects.order_by('created_at').reverse().first()
        photo.save()

        clarifai_app = ClarifaiApp(api_key=api_key)
        goo_api = GoolabsAPI(goo_api_key)
        clarifai_model = clarifai_app.models.get('aaa03c23b3724a16a56b629203edc62c')
        response = clarifai_model.predict_by_filename(img_path, max_concepts=max_concepts)
        rList = response['outputs'][0]['data']['concepts']
        oklist = []
        oklist_ruby = []

        bottom_word = str(lastObject.tag_ruby)[-1]
        bottom_word = dakuten(bottom_word)
        pbar = tqdm(total=len(rList), desc='check now!')  # プロセスバーの設定
        c = 0
        for i in range(len(rList)):
            concept_name = str(rList[i]['name'])
            ret = goo_api.hiragana(sentence=concept_name, output_type="hiragana")
            ret = ret['converted']
            # print(ret)
            print('===========')
            print(ret)
            print(dakuten(ret[0]))
            print(bottom_word)
            print('===========')
            if (dakuten(ret[0]) == bottom_word) and (ret[-1] != 'ん'):
                photo.tag_name = concept_name
                photo.tag_ruby = ret
                c = 1
                photo.save()
                break
            if i+1 == len(rList):
                # 解答がなかった
                Photo.objects.order_by('created_at').reverse().first().delete()
                c = 0
            pbar.update(1)  # プロセスバーを進行
        pbar.close()  # プロセスバーの終了

        if c == 1:
            return redirect('/plays')
        return redirect('/plays/false')


def index(req):
    if req.method == 'GET':
        return render(req, 'plays/index.html', {
            'form': PhotoForm(),
            'photos': Photo.objects.all().order_by('created_at').reverse(), # ここを追加
            'messages': '',
        })


    elif req.method == 'POST':
        form = PhotoForm(req.POST, req.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')

        photo = Photo()
        photo.image = form.cleaned_data['image']
        print(photo.image.url)
        # print(form.cleaned_data['image'])
        photo.created_at = datetime.now()
        img_path = settings.BASE_DIR + settings.MEDIA_URL + 'plays/' + str(form.cleaned_data['image'])

        lastObject = Photo.objects.order_by('created_at').reverse().first()
        photo.save()

        clarifai_app = ClarifaiApp(api_key=api_key)
        goo_api = GoolabsAPI(goo_api_key)
        clarifai_model = clarifai_app.models.get('aaa03c23b3724a16a56b629203edc62c')
        response = clarifai_model.predict_by_filename(img_path, max_concepts=max_concepts)
        rList = response['outputs'][0]['data']['concepts']
        oklist = []
        oklist_ruby = []

        bottom_word = str(lastObject.tag_ruby)[-1]
        bottom_word = dakuten(bottom_word)
        pbar = tqdm(total=len(rList), desc='check now!')  # プロセスバーの設定
        c = 0
        for i in range(len(rList)):
            concept_name = str(rList[i]['name'])
            ret = goo_api.hiragana(sentence=concept_name, output_type="hiragana")
            ret = ret['converted']
            # print(ret)
            print('===========')
            print(ret)
            print(dakuten(ret[0]))
            print(bottom_word)
            print('===========')
            if (dakuten(ret[0]) == bottom_word) and (ret[-1] != 'ん') or bottom_word == 'e':
                photo.tag_name = concept_name
                if (ret[-1] == 'ー'):
                    photo.tag_ruby = ret[:-1]
                else:
                    photo.tag_ruby = ret
                c = 1
                photo.save()
                break
            if i+1 == len(rList):
                # 解答がなかった
                Photo.objects.order_by('created_at').reverse().first().delete()
                c = 0
            pbar.update(1)  # プロセスバーを進行
        pbar.close()  # プロセスバーの終了

        if c == 1:
            return redirect('/plays')
        return redirect('/plays/false')
