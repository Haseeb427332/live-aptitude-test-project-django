from django.db import models
from django.contrib.auth.models import User

class registertion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def __str__(self):
        return f'id: {self.id} -  User: {self.user}'

class Createquestions(models.Model):
    question = models.CharField(max_length=900)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correctanswer = models.CharField(max_length=100)
    subjects = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.question}'

class TestResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Createquestions,on_delete=models.CASCADE)
    answer = models.CharField(max_length=900)
    count = models.CharField(max_length=100 , default=0)
    subjects = models.CharField(max_length=900)
    total = models.CharField(max_length=100,default=0)

    def __str__(self):
        return f'user:{self.user} - subjects:{self.subjects} - count:{self.count}'

class Queries(models.Model):
    email = models.CharField(max_length=100)
    comments = models.CharField(max_length=900)

    def __str__(self):
        return f'email:{self.email}'


