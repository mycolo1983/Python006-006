from django.db import models

# Create your models here.
class MovieTest(models.Model):
    name = models.CharField(max_length=50)
    stars = models.IntegerField()
    remark = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_test'

    def __str__(self):
        return self.name
