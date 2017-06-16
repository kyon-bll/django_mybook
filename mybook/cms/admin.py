from django.contrib import admin
from cms.models import Book, Impression


# 最低限表示
# admin.site.register(Book)
# admin.site.register(Impression)

# たくさん表示、リンクも生成
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'page')  # 一覧に出す項目
    list_display_links = ('id', 'name')  # リンクでとべるやつ


admin.site.register(Book, BookAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment')
    list_display_links = ('id', 'comment')


admin.site.register(Impression, ImpressionAdmin)
