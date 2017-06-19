from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from cms.models import Book, Impression
from cms.forms import BookForm, ImpressionForm

from django.views.generic.list import ListView


def book_list(request):
    """書籍一覧"""
    # return HttpResponse('書籍の一覧')
    books = Book.objects.all().order_by('id')
    return render(request,
                  'cms/book_list.html',  # 使用するテンプレート
                  {'books': books})      # テンプレートに渡すデータ


def book_edit(request, book_id=None):
    # return HttpResponse('書籍の編集')
    if book_id:                 # 書籍の修正
        book = get_object_or_404(Book, pk=book_id)
    else:                       # 書籍の追加
        book = Book()

        # POSTでもGETでもformを作る
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # POSTされたデータからform作成
        if form.is_valid():            # エラーがなければ保存 -> 一覧へ
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')
    else:                       # GETの時
        form = BookForm(instance=book)

    return render(request, 'cms/book_edit.html', dict(form=form, book_id=book_id))


def book_del(request, book_id):
    """書籍の削除"""
    # return HttpResponse('書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('cms:book_list')


class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name = 'impressions'
    template_name = 'cms/impression_list.html'
    paginate_by = 2             # 1ページは最大2件でページング

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])  # 親書籍
        impressions = book.impressions.all().order_by('id')   # 書籍の感想
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)


def impression_edit(request, book_id=None, impression_id=None):
    """感想の編集・追加"""
    # return HttpResponse('書籍の編集・追加')
    book = get_object_or_404(Book, pk=book_id)  # 親のBook
    if impression_id:                           # 編集
        impression = get_object_or_404(Impression, pk=impression_id)
    else:                                       # 追加
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)
        if form.is_valid():
            impression = form.save(commit=False)
            impression.book = book
            impression.save()
            return redirect('cms:impression_list', book_id=book_id)
    else:
        form = ImpressionForm(instance=impression)

    return render(request,
                  'cms/impression_edit.html',
                  dict(form=form, book_id=book_id, impression_id=impression_id))


def impression_del(request, book_id=None, impression_id=None):
    """感想削除"""
    # return HttpResponse('書籍の削除')
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('cms:impression_list', book_id=book_id)
