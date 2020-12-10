from django.db import models
import datetime

class Map(models.Model):
    credits = 120

class Module(models.Model):
    uni_years = [('1','1'),('2','2'),('3','3'),('4','4'),('na','N/A')]
    uni_terms = [('1','1'),('2','2'),('3','3'),('12','1 and 2'),('na','N/A')]
    name = models.CharField(max_length = 200)
    code = models.CharField(max_length = 20)
    year = models.CharField(max_length = 20, choices = uni_years)
    term = models.CharField(max_length = 20, choices = uni_terms)
    credits = models.IntegerField(default = 15)
    department = models.CharField(max_length = 200)
    category = models.CharField(max_length = 200, blank = True)
    ELE = models.URLField(max_length = 200, blank = True)
    website = models.URLField(max_length = 200, blank = True)


class Links(models.Model):
    link_types = [('pre','Pre-requisites'),('co','Co-requisites')]
    parent_module = models.ForeignKey(Module, related_name = 'parent_module', on_delete = models.CASCADE)
    linked_module = models.ForeignKey(Module, related_name = 'linked_module', on_delete = models.CASCADE)
    year_in_school = models.CharField(max_length=3,choices=link_types,
                                        default= 'pre',)

class Lecturer(models.Model):
    module = models.ForeignKey(Module, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    email_address = models.EmailField()
