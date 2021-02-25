from django.db import models

class Module(models.Model):

    uni_years = [('1','1'),('2','2'),('3','3'),('4','4'),('1,2','1,2'),('na','N/A')]
    uni_terms = [('1','1'),('2','2'),('3','3'),('12','1 and 2'),('1,2,3','1,2,3'),('1 or 2','1 or 2'),('1 or 3','1 or 3'),('2 or 3', '2 or 3'),('Other','Other')]
    #departments = [('CSM', 'Camborne School of Mines'), ('Comp', 'Computing'), ('Eng', 'Engineering'), ('Maths', 'Mathematics'), ('NatSci', 'Natural Sciences'), ('Phy', 'Physics'), ('Bio', 'Biosciences'), ('Geo', 'Geography'), ('Other','Other')]

    name = models.CharField(max_length = 10000, blank = True)
    code = models.CharField(max_length = 7, blank = False)
    department = models.CharField(max_length = 200, blank = False)
    category = models.CharField(max_length = 200, blank = True, default= 'na')
    sub_category = models.CharField(max_length = 200, blank = True, default= 'na')
    year = models.CharField(max_length = 20, choices = uni_years)
    term = models.CharField(max_length = 20, choices = uni_terms)
    credits = models.IntegerField(default = 15)
    lecturer = models.CharField(max_length = 150, blank = True)
    core_Natural_Sciences = models.CharField(max_length = 1, blank=True)
    core_Mathematics = models.CharField(max_length = 1, blank=True)
    core_Physics_BPhys = models.CharField(max_length = 1, blank=True)
    core_Biological_Sciences = models.CharField(max_length = 1, blank=True)
    core_Biochemistry = models.CharField(max_length = 1, blank=True)
    core_Biological_and_Medicinal_Chemistry = models.CharField(max_length = 1, blank=True)
    core_Physics_MPhys = models.CharField(max_length = 1, blank = True)
    natural_Sciences_History = models.CharField(max_length = 1, blank = True)
    topic_pathway = models.CharField(max_length = 100, blank = True, default = 'N/A')
    module_descriptor = models.URLField(max_length = 500, blank = False)
    Pre_req = models.CharField(max_length = 100, blank = True, default = 'N/A')
    Co_req = models.CharField(max_length = 100, blank = True, default = 'N/A')

    #requisites = models.ManyToManyField('Requisites', blank = True)

#class Requisites(models.Model):
#    Pre_req = models.CharField(max_length = 100, blank = True, default = 'N/A')
#    Co_req = models.CharField(max_length = 100, blank = True, default = 'N/A')
