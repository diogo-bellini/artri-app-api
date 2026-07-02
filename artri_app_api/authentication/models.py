from django.db import models
from django.contrib.auth.models import AbstractUser

# define the days of the week 
DAYS_OF_WEEK = [
        ('Monday', 'Segunda-feira'),
        ('Tuesday', 'Terça-feira'),
        ('Wednesday', 'Quarta-feira'),
        ('Thursday', 'Quinta-feira'),
        ('Friday', 'Sexta-feira'),
        ('Saturday', 'Sábado'),
        ('Sunday', 'Domingo')
    ]

DIFFICULTY = [
        ('Easy', 'Fácil'),
        ('Medium', 'Médio'),
        ('Hard', 'Difícil')
    ]

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)

    def __str__(self):
        return self.username
    
class Remedy(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField()
    days_of_week = models.CharField(choices=DAYS_OF_WEEK, max_length=9, default='Monday')
    hour = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Exercise(models.Model):
    name = models.CharField(max_length=100) 
    
    description = models.TextField() 
    
    sets_reps = models.CharField(max_length=50, null=True, blank=True)
    rest_time = models.CharField(max_length=50, null=True, blank=True)
    
    tutorial_link = models.URLField()
    difficulty = models.CharField(choices=DIFFICULTY, default='Easy')

    def __str__(self):
        return self.name
    
class TrainingExercise(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0) # Controla a ordem (0, 1, 2...)

    class Meta:
        ordering = ['order'] # O Django sempre vai devolver os exercícios ordenados por este campo

class Training(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # Adicionamos o 'through' para avisar o Django que a relação agora tem uma ordem
    exercises = models.ManyToManyField(Exercise, through=TrainingExercise)
    difficulty = models.CharField(choices=DIFFICULTY, default='Easy')

    def __str__(self):
        return self.name
    
class TrainingReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.training.name} - {self.date}'
    
class DailyPainReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    pain_level = models.IntegerField()# 0-10
    pain_location = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.date}'
    
class DailySleepReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    sleep_duration = models.IntegerField()  # in hours
    sleep_quality = models.CharField(max_length=50)  # e.g., 'Good', 'Fair', 'Poor'

    def __str__(self):
        return f'{self.user.username} - {self.date}'
    
class DailySwellingReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    swelling_level = models.IntegerField()  # 0-10
    swelling_location = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} - {self.date}'

class DailyFatigueReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    fatigue_level = models.IntegerField()  # 0-10
    fatigue_description = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.date}'