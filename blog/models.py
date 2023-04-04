from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

class Author(models.Model):
    author_first_name = models.CharField(max_length=50)
    author_last_name = models.CharField(max_length=50)
    author_email = models.EmailField()

    def __str__(self):
        return self.author_first_name+' '+self.author_last_name

class Blog(models.Model):
    slug  = models.SlugField(max_length=100, unique=True, db_index=True)
    author = models.ForeignKey(Author, on_delete= models.SET_NULL, null=True, related_name='posts' )
    date = models.DateField(auto_now=True)
    title = models.CharField(max_length= 100)
    excerpt = models.CharField(max_length=200)
    content = models.TextField(validators= [MinLengthValidator(10)] )
    image_name = models.ImageField(upload_to='uploads/images' , default='blank.jpg')
    caption = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments" )


    

