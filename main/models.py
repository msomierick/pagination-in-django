from django.db import models


class Student(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()  # date of birth
    gender = models.CharField(max_length=6, choices=GENDER)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ('first_name', )

    def full_name(self):
        return str(self)
