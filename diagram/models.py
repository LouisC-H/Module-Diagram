from django.db import models
import datetime
import numpy as np
import math

class Map():

    def __init__(self):

        super().__init__()
        self.init_map()

    def init_map(self):

        self.Y1_credits = 120
        self.Y2_credits = 120
        self.Y3_credits = 120
        self.Y4_credits = 120
        self.chosen_departments = ['Phy','NatSci','Bio']
        self.relevant_modules_ids = []
        self.module_names = []
        self.module_departments = []
        self.module_categories = []
        self.module_sub_categories = []
        self.module_position_col = []
        self.module_year = []
        self.module_term = []
        self.columns_dict = {}
        self.table_data = []
        self.num_columns = 0

        self.find_relevant_modules()
        self.generate_table_matrix()
        for row in self.table_data:
            print(row)
            for column in row:
                print(column)

    def find_relevant_modules(self):
        for department in self.chosen_departments:
            for module in Module.objects.filter(department = department):

                if module.department not in self.columns_dict:
                    self.columns_dict[module.department] = {}
                if module.category not in self.columns_dict[module.department]:
                    self.columns_dict[module.department][module.category] = {}
                if module.sub_category not in self.columns_dict[module.department][module.category]:
                    self.columns_dict[module.department][module.category][module.sub_category] = self.num_columns
                    self.num_columns +=1
                self.populate_module_detail_lists(module)

    def populate_module_detail_lists(self, module):
        self.relevant_modules_ids.append(module.id)
        self.module_names.append(module.name)
        self.module_departments.append(module.department)
        self.module_categories.append(module.category)
        self.module_sub_categories.append(module.sub_category)
        self.module_position_col.append(self.determine_module_col(module))
        self.determine_module_row(module)

    def determine_module_row(self, module):

        year_mod = 'na'
        term_mod = 'na'

        if module.year == '1':
            year_mod = 0
        elif module.year == '2':
            year_mod = 1
        elif module.year == '3':
            year_mod = 2
        elif module.year == '4':
            year_mod = 3
        else:
            year_mod = 'na'

        if module.term == '1':
            term_mod = 0
        elif module.term == '2':
            term_mod = 1
        elif module.term == '3':
            term_mod = 2
        elif module.term == '12':
            term_mod = 0.5
        else:
            term_mod = 'na'

        self.module_year.append(year_mod)
        self.module_term.append(term_mod)

    def determine_module_col(self, module):
        column = 'na'
        for department in self.columns_dict.items():
            if module.department == department[0]:
                for category in department[1].items():
                    if module.category == category[0]:
                        for sub in category[1].items():
                            if module.sub_category == sub[0]:
                                column = sub[1]

        return column

    def generate_table_matrix(self):
        #Add one list per row
        for row in range(4):
            self.table_data.append([])
            #Add one sub-list per column
            for column in range(self.num_columns):
                self.table_data[row].append([])

        for module_index in range(len(self.relevant_modules_ids)):
            self.add_module_data(module_index)

    def add_module_data(self, index):
        double_term = 0
        col = self.module_position_col[index]
        row = self.module_year[index]

        self.table_data[row][col].append([self.module_names[index],self.module_term[index]])


class Module(models.Model):

    def __str__(self):
        return self.code

    uni_years = [('1','1'),('2','2'),('3','3'),('4','4'),('na','N/A')]
    uni_terms = [('1','1'),('2','2'),('3','3'),('12','1 and 2'),('Other','Other')]
    departments = [('CSM', 'Camborne School of Mines'), ('Comp', 'Computing'), ('Eng', 'Engineering'), ('Maths', 'Mathematics'), ('NatSci', 'Natural Sciences'), ('Phy', 'Physics and Astronomy'), ('Bio', 'Biosciences'), ('Geo', 'Geography'), ('Other','Other')]
    name = models.CharField(max_length = 200)
    code = models.CharField(max_length = 20)
    year = models.CharField(max_length = 20, choices = uni_years)
    term = models.CharField(max_length = 20, choices = uni_terms)
    credits = models.IntegerField(default = 15)
    department = models.CharField(max_length = 200, choices = departments)
    category = models.CharField(max_length = 200, blank = True, default= 'na')
    sub_category = models.CharField(max_length = 200, blank = True, default= 'na')
    website = models.URLField(max_length = 200, blank = True)

class Links(models.Model):

    link_types = [('pre','Pre-requisites'),('co','Co-requisites')]
    parent_module = models.ForeignKey(Module, related_name = 'parent_module', on_delete = models.CASCADE)
    linked_module = models.ForeignKey(Module, related_name = 'linked_module', on_delete = models.CASCADE)
    year_in_school = models.CharField(max_length=3,choices=link_types,
                                        default= 'pre',)

class Lecturer(models.Model):

    def __str__(self):
        return '{self.first_name} {self.last_name}'.format(self=self)

    module = models.ForeignKey(Module, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    email_address = models.EmailField()
