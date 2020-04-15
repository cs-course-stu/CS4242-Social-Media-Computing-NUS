import json
from json import JSONEncoder

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from classify.forms import MyForm
from classify.textclassifier import TextClassifier


def upload_file(file):
    if file is not None:
        import os
        dir_path = "./upload"
        (filename, extension) = os.path.splitext(file.name)
        filename += extension
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return file_path


class IndexView(View):
    """首页view"""
    def get(self, request):
        return render(request, 'index.html', {"tags": []})

    def post(self, request):
        my_form = MyForm(request.POST)
        print(my_form)
        if my_form.is_valid():
            user_text = request.POST.get("user_text","")
            print(user_text)
            textclassifier = TextClassifier(
                '/Users/wangyifan/Google Drive/multi-label-classification', 'dictionary.txt', 'hashtag.txt', 'input.train.text.csv')
            
            string = user_text
            # print(string)
            result = textclassifier.predict(string)
            print(result)
            content = {'tags': result}
            result = json.dumps(content, cls=JSONEncoder, ensure_ascii=False)
            return HttpResponse(result)

class FileView(View):
    def post(self, request):
        file = request.FILES.get('path')
        file_path = upload_file(file)
        print(file_path)
        content = {'tags': ["4多云", "5下雪", "6闪电"]}
        result = json.dumps(content, cls=JSONEncoder, ensure_ascii=False)
        return HttpResponse(result)
