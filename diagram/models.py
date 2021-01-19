from django.db import models
import datetime
import numpy as np
import math

class Map():
    '''
    This class sits in the background and organises all of the (relevant)
    modules from the database into a diagram.
    '''

    def __init__(self):

        super().__init__()
        self.init_map()

    def init_map(self):
        '''
        Initialise variables and call functions
        '''
        self.Y1_credits = 120
        self.Y2_credits = 120
        self.Y3_credits = 120
        self.Y4_credits = 120
        self.chosen_departments = ['Phy','NatSci','Bio']
        self.relevant_modules_ids = []
        self.module_names = []
        self.module_position_col = []
        self.module_year = []
        self.module_term = []
        self.columns_dict = {}
        self.table_data = []
        self.num_columns = 0

        self.find_relevant_modules()
        self.generate_table_matrix()
        self.concentrate_modules()

    def find_relevant_modules(self):
        '''
        For all of the modules in the databse, find whether their department is in the
        self.chosen_departments list. If so, save the module details.
        '''
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
        '''
        Save the details of relevant modules, and calculate their position in the diagram
        '''
        self.relevant_modules_ids.append(module.id)
        self.module_names.append(module.name)
        self.module_position_col.append(self.determine_module_col(module))
        self.determine_module_row(module)

    def determine_module_row(self, module):
        '''
        Determine the module's vertical position in the diagram, from its year and term
        '''
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
        '''
        Determine the module's horizontal position in the diagram, from its
        department, category and sub-category
        '''
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
        '''
        Create a matrix to order the modules within the diagram, then add the
        modules to this matrix
        '''
        #Add one list per row
        for colummn in range(self.num_columns):
            self.table_data.append([])
            #Add one sub-list per column
            for row in range(4):
                self.table_data[colummn].append([])

        for module_index in range(len(self.relevant_modules_ids)):
            self.add_module_data(module_index)

    def add_module_data(self, index):
        '''
        Add each module to the self.table_data matrix, according to their
        row and column position
        '''
        col = self.module_position_col[index]
        row = self.module_year[index]

        self.table_data[col][row].append([self.module_names[index],self.module_term[index]])

    def concentrate_modules(self):
        '''
        Group the modules that could vertically coexist onto a single column, adding
        spacer elements if necessary
        '''

        for colummn in range(self.num_columns):
            for row in range(4):
                cell_module_names = []
                call_module_terms = []
                for module in self.table_data[colummn][row]:
                    if len(module) == 0:
                        continue
                    cell_module_names.append(module[0])
                    call_module_terms.append(module[1])

                self.table_data[colummn][row] = self.group_modules([], cell_module_names, call_module_terms)

    def group_modules(self, data_grouped, names, terms):
        '''
        In order to group modules, first determine the term of the first module
        in the list, then call the relevant function
        '''
        if len(names) == 0:
            return data_grouped

        if terms[0] == 0:
            self.group_start_T1(data_grouped, names, terms)

        elif terms[0] == 0.5:
            self.group_start_T1_and_2(data_grouped, names, terms)

        elif terms[0] == 1:
            self.group_start_T2(data_grouped, names, terms)

        elif terms[0] == 2:
            self.group_start_T3(data_grouped, names, terms)

        return data_grouped

    def group_start_T1(self, data_grouped, names, terms):
        '''
        Group a T1 module with a T2 and/or a T3, then remove the grouped modules
        from the list of modules to be grouped
        '''
        #If there's a T2 module
        if 1 in terms:
            T2_index = terms.index(1)
            #If there's a T3 module
            if 2 in terms:
                T3_index = terms.index(2)
                data_grouped.append([[names[0],terms[0]],[names[T2_index],terms[T2_index]],[names[T3_index],terms[T3_index]]])
                del names[T2_index], terms[T2_index], names[terms.index(2)], terms[terms.index(2)], names[0], terms[0]
            else:
                data_grouped.append([[names[0],terms[0]],[names[T2_index],terms[T2_index]]])
                del names[T2_index], terms[T2_index], names[0], terms[0],

        #Elif there's a T3 module
        elif 2 in terms:
            T3_index = terms.index(2)
            data_grouped.append([[names[0],terms[0]], ["Spacer", -1], [names[T3_index],terms[T3_index]]])
            del names[T3_index], terms[T3_index], names[0], terms[0],

        else:
            data_grouped.append([[names[0],terms[0]]])
            del names[0], terms[0]

        self.group_modules(data_grouped, names, terms)

    def group_start_T1_and_2(self, data_grouped, names, terms):
        '''
        Group a T(1 and 2) module with a T3, then remove the grouped modules
        from the list of modules to be grouped
        '''
        #If there's a T3 module
        if 2 in terms:
            T3_index = terms.index(2)
            data_grouped.append([[names[0],terms[0]],[names[T3_index],terms[T3_index]]])
            del names[T3_index], terms[T3_index], names[0], terms[0]

        else:
            data_grouped.append([[names[0],terms[0]]])
            del names[0], terms[0]

        self.group_modules(data_grouped, names, terms)

    def group_start_T2(self, data_grouped, names, terms):
        '''
        Group a T2 module with a T1 and/or a T3, then remove the grouped modules
        from the list of modules to be grouped
        '''
        #If there's a T1 module
        if 0 in terms:
            T1_index = terms.index(0)
            #If there's a T3 module
            if 2 in terms:
                T3_index = terms.index(2)
                data_grouped.append([[names[T1_index],terms[T1_index]], [names[0],terms[0]], [names[T3_index],terms[T3_index]]])
                del names[T1_index], terms[T1_index], names[terms.index(2)], terms[terms.index(2)], names[0], terms[0],
            else:
                data_grouped.append([[names[T1_index],terms[T1_index]], [names[0],terms[0]]])
                del names[T1_index], terms[T1_index], names[0], terms[0],

        #Elif there's a T3 module
        elif 2 in terms:
            T3_index = terms.index(2)
            data_grouped.append([["Spacer", -1], [names[0],terms[0]], [names[T3_index],terms[T3_index]]])
            del names[T3_index], terms[T3_index], names[0], terms[0],

        else:
            data_grouped.append([ ["Spacer", -1], [names[0],terms[0]]])
            del names[0], terms[0]

        self.group_modules(data_grouped, names, terms)

    def group_start_T3(self, data_grouped, names, terms):
        '''
        Group a T3 module with a T1 and/or a T3 and/or a T(1 and 2), then
        remove the grouped modules from the list of modules to be grouped
        '''
        #If there's a T1 module
        if 0 in terms:
            T1_index = terms.index(0)
            #If there's a T2 module
            if 1 in terms:
                T2_index = terms.index(1)
                data_grouped.append([[names[T1_index],terms[T1_index]],[names[T2_index],terms[T2_index]], [names[0],terms[0]]])
                del names[T1_index], terms[T1_index], names[terms.index(1)], terms[terms.index(1)], names[0], terms[0],
            else:
                data_grouped.append([[names[T1_index],terms[T1_index]], ["Spacer", -1], [names[0],terms[0]]])
                del names[T1_index], terms[T1_index], names[0], terms[0],

        #Elf there's a T2 module
        elif 1 in terms:
            T2_index = terms.index(1)
            data_grouped.append([ ["Spacer", -1], [names[T2_index],terms[T2_index]], [names[0],terms[0]]])
            del  names[T2_index], terms[T2_index], names[0], terms[0],

        #Elf there's a T(1 and 2) module
        elif 0.5 in terms:
            T1_2_index = terms.index(0.5)
            data_grouped.append([[names[T1_2_index],terms[T1_2_index]], [names[0],terms[0]]])
            del  names[T1_2_index], terms[T1_2_index], names[0], terms[0],

        else:
            data_grouped.append([ ["Spacer", -1],  ["Spacer", -1], [names[0],terms[0]]])
            del names[0], terms[0]

        self.group_modules(data_grouped, names, terms)

class Module(models.Model):
    '''
    This class is used to store information about the modules in the database
    '''

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
    '''
    This class is used to store information about the links between modules in the database
    '''

    link_types = [('pre','Pre-requisites'),('co','Co-requisites')]
    parent_module = models.ForeignKey(Module, related_name = 'parent_module', on_delete = models.CASCADE)
    linked_module = models.ForeignKey(Module, related_name = 'linked_module', on_delete = models.CASCADE)
    year_in_school = models.CharField(max_length=3,choices=link_types,
                                        default= 'pre',)

class Lecturer(models.Model):
    '''
    This class is used to store information about a module's lecturers
    '''

    def __str__(self):
        return '{self.first_name} {self.last_name}'.format(self=self)

    module = models.ForeignKey(Module, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    email_address = models.EmailField()
