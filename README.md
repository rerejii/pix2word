# pixWord

オープンキャンパスの出し物用に (学会前に一晩徹夜で) 作成した、深層学習による絵しりとりです。

## 使用したもの

- Django
- clarifai (公開モデル)
- ひらがな化API : gooラボ

## 使い方

どなたかが使うことを前提に設計してませんが...

1.  python manage.py runserver で開発者用サーバ稼働
2.   http://127.0.0.1:8000/plays/  にアクセス
3.  画面上部のフォームから繋がりそうな画像を[投稿]すると稼働します

## 精度

右下から左上です

![sample](C:\Users\hayak\work\git\pixWord\sample.png)

