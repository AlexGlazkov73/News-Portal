from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating_comment'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating_user = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    news = 'NW'
    article = 'AR'
    CONTENT = [
        (news, 'Новости'),
        (article, 'Статья')
    ]
    choice = models.CharField(max_length=2, choices=CONTENT, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=1)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating == 1:
            print('Comment have lowest rating')
        else:
            self.rating -= 1
            self.save()

    def preview(self):
        return self.text[:125] + '...'

    def get_comments(self):
        return self.post_comments.all()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='post_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=1)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        if self.rating_comment == 1:
            print('Comment have lowest rating')
        else:
            self.rating_comment -= 1
            self.save()
