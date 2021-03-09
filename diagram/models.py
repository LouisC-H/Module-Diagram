from django.db import models
import datetime
#import numpy as np
#import math

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

        #Find a way to let users set this themselves
        # self.chosen_departments = ['Bio']
        self.chosen_departments = ['NatSci', 'Phy', 'Bio','Maths']

        #Find dimensions of data matrix
        self.columns_dict = {}
        self.num_depts = 0
        self.num_columns = 0

        #Store disordered module data
        self.relevant_modules_ids = []
        self.module_names = []
        self.module_codes = []
        self.module_year = []
        self.module_term = []
        self.module_website = []

        #Position disordered modules within data matrix
        self.module_position_dept = []
        self.module_position_col = []
        self.starting_column_index = []

        #Store data within matrix
        self.table_data = []

        #Beautify each department's columns with a background colour
        self.potential_departments = ['CSM', 'Comp', 'Eng', 'Maths', 'NatSci', 'Phy', 'Bio', 'Geo', 'Other']
        self.dept_colours = ['#b39559', '#ffb380', '#e67373', '#73e6e6', '#cf8cde', '#99bbff', '#95e67c', '#e6e673', '#ffffff']
        self.chosen_colours = []

        #Store data on inter-module links to be imported into the JS
        self.module_links_codes = []
        self.module_links_indices = []

        self.find_relevant_modules()
        self.generate_table_matrix()
        self.concentrate_modules()


    def find_relevant_modules(self):
        '''
        For all of the modules in the databse, find whether their department is in the
        self.chosen_departments list. If so, save the module details (by calling a new function).
        '''
        for department in self.chosen_departments:
            for module in Module.objects.filter(department = department):
                if module.department not in self.columns_dict:
                    self.columns_dict[module.department] = [{}, self.num_depts]
                    self.num_depts +=1
                if module.category not in self.columns_dict[module.department][0]:
                    self.columns_dict[module.department][0][module.category] = {}
                if module.sub_category not in self.columns_dict[module.department][0][module.category]:
                    self.columns_dict[module.department][0][module.category][module.sub_category] = self.num_columns
                    self.num_columns +=1
                self.populate_module_detail_lists(module)

    def populate_module_detail_lists(self, module):
        '''
        Save the details of relevant modules, and calculate their position in the diagram
        '''
        self.relevant_modules_ids.append(module.id)
        self.module_names.append(module.name)
        self.module_codes.append(module.code)
        self.module_website.append(module.website)

        link_list = []
        link_list.append(module.pre_req.split(", "))
        link_list.append(module.co_req.split(", "))
        self.module_links_codes.append(link_list)

        self.determine_module_col(module)
        self.determine_module_row(module)

    def determine_module_row(self, module):
        '''
        Determine the module's vertical position in the diagram, from its year and term
        '''
        year_mod = 'na'
        term_mod = 'na'

        if module.year == '1':
            year_mod = 1
        elif module.year == '2':
            year_mod = 2
        elif module.year == '3':
            year_mod = 3
        elif module.year == '4':
            year_mod = 4
        else:
            year_mod = 'na'

        if module.term == '1':
            term_mod = 1
        elif module.term == '2':
            term_mod = 2
        elif module.term == '3':
            term_mod = 3
        elif module.term == '12':
            term_mod = 12
        elif module.term == '123':
            term_mod = 123
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
        department = 'na'

        for department in self.columns_dict.items():
            if module.department == department[0]:
                department_index = department[1][1]
                for category in department[1][0].items():
                    if module.category == category[0]:
                        for sub_category in category[1].items():
                            if module.sub_category == sub_category[0]:
                                column = sub_category[1]


        self.module_position_dept.append(department_index)
        self.module_position_col.append(column)
        return column

    def generate_table_matrix(self):
        '''
        Create a matrix to order the modules within the diagram, then add the
        modules to this matrix
        '''

        row_num = 4
        total_column_number = 0

        #For each department
        for department in self.columns_dict:
            self.starting_column_index.append(total_column_number)
            dept_matrix = []
            dept_col_number = 0
            #... find the number of columns...
            for category in self.columns_dict[department][0]:
                for sub_category in self.columns_dict[department][0][category]:
                    dept_matrix.append([])
                    for row in range(row_num):
                        dept_matrix[dept_col_number].append([])
                    dept_col_number += 1
            total_column_number += dept_col_number

            #...then append to larger list
            dept_colour = self.dept_colour(department)
            self.table_data.append([dept_matrix, f'background-color: {dept_colour}'])

        #Once the matrix of nested tables has been initialised, populate it with data
        for module_index in range(len(self.relevant_modules_ids)):
            self.add_module_data(module_index)

        self.code_to_indices()

    def dept_colour(self, department):
        '''
        returns the department's columns' background colour
        '''
        return self.dept_colours[self.potential_departments.index(department)]

    def add_module_data(self, index):
        '''
        Add each module to the self.table_data matrix, according to their
        row and column position
        '''
        dept = self.module_position_dept[index]
        column_index_offset = self.starting_column_index[dept]
        col = self.module_position_col[index] - column_index_offset
        row = self.module_year[index] - 1

        self.table_data[dept][0][col][row].append([self.module_names[index], self.module_term[index], self.module_website[index]])

    def code_to_indices(self):
        '''
        For each module involved in a link, use their code to find the module's
        index in the disordered lists
        '''

        for module_links in self.module_links_codes:
            linked_module_indices = []
            for list in module_links:
                for link in list:
                    if link != "N/A":
                        if link in self.module_codes:
                            index = self.module_codes.index(str(link))
                            linked_module_indices.append(index)
                        else:
                            print(f"Link is not in the module list: _{link}_")

            self.module_links_indices.append(linked_module_indices)

    def concentrate_modules(self):
        '''
        Group the modules that could vertically coexist onto a single column, adding
        spacer elements if necessary
        '''

        for department in range(self.num_depts):
            max_num_columns = len(self.table_data[department][0])
            for column in range(self.num_columns):
                column_index_offset = self.starting_column_index[department]
                col_index = column - column_index_offset
                if 0 <= col_index < max_num_columns:
                    for row in range(4):
                        cell_module_names = []
                        cell_module_terms = []
                        cell_module_websites = []
                        for module in self.table_data[department][0][col_index][row]:
                            if len(module) == 0:
                                continue
                            cell_module_names.append(module[0])
                            cell_module_terms.append(module[1])
                            cell_module_websites.append(module[2])

                        self.table_data[department][0][col_index][row] = self.group_modules([], cell_module_names, cell_module_terms, cell_module_websites)

    def group_modules(self, data_grouped, names, terms, websites):
        '''
        In order to group modules, first determine the term of the first module
        in the list, then call the relevant function
        '''
        if len(names) == 0:
            return data_grouped

        if terms[0] == 1:
            self.group_start_T1(data_grouped, names, terms, websites)

        elif terms[0] == 12:
            self.group_start_T1_and_2(data_grouped, names, terms, websites)

        elif terms[0] == 123:
            self.group_start_T1_2_3(data_grouped, names, terms, websites)

        elif terms[0] == 2:
            self.group_start_T2(data_grouped, names, terms, websites)

        elif terms[0] == 3:
            self.group_start_T3(data_grouped, names, terms, websites)

        return data_grouped

    def group_start_T1(self, data_grouped, names, terms, websites):
        '''
        Group a T1 module with a T2 and/or a T3, then remove the grouped modules
        from the list of modules to be grouped
        '''

        #If there's a T2 module
        if 2 in terms:
            T2_index = terms.index(2)
            #If there's a T3 module
            if 3 in terms:
                T3_index = terms.index(3)
                data_grouped.append([[names[0],terms[0], websites[0]],[names[T2_index],terms[T2_index], websites[T2_index]],[names[T3_index],terms[T3_index], websites[T3_index]]])
                del names[T2_index], terms[T2_index], websites[T2_index], names[terms.index(3)], websites[terms.index(3)], terms[terms.index(3)], names[0], terms[0]
            else:
                data_grouped.append([[names[0],terms[0], websites[0]],[names[T2_index],terms[T2_index], websites[T2_index]]])
                del names[T2_index], terms[T2_index], websites[T2_index], names[0], terms[0], websites[0],

        #Elif there's a T3 module
        elif 3 in terms:
            T3_index = terms.index(3)
            data_grouped.append([[names[0],terms[0], websites[0]], ["Spacer", -1], [names[T3_index],terms[T3_index], websites[T3_index]]])
            del names[T3_index], terms[T3_index], websites[T3_index], names[0], terms[0], websites[0],

        else:
            data_grouped.append([[names[0],terms[0], websites[0]]])
            del names[0], terms[0], websites[0]

        self.group_modules(data_grouped, names, terms, websites)

    def group_start_T1_and_2(self, data_grouped, names, terms, websites):
        '''
        Group a T(1 and 2) module with a T3, then remove the grouped modules
        from the list of modules to be grouped
        '''
        #If there's a T3 module
        if 3 in terms:
            T3_index = terms.index(3)
            data_grouped.append([[names[0],terms[0]], websites[0],[names[T3_index],terms[T3_index], websites[T3_index]]])
            del names[T3_index], terms[T3_index], websites[T3_index], names[0], terms[0], websites[0]

        else:
            data_grouped.append([[names[0],terms[0], websites[0]]])
            del names[0], terms[0], websites[0]

        self.group_modules(data_grouped, names, terms, websites)

    def group_start_T1_2_3(self, data_grouped, names, terms, websites):
        '''
        Group a T(1 + 2 + 3) module on its own, then remove it from the list
        of modules to be grouped
        '''
        #If there's a T3 module

        data_grouped.append([[names[0],terms[0], websites[0]]])
        del names[0], terms[0], websites[0]

        self.group_modules(data_grouped, names, terms, websites)

    def group_start_T2(self, data_grouped, names, terms, websites):
        '''
        Group a T2 module with a T1 and/or a T3, then remove the grouped modules
        from the list of modules to be grouped
        '''

        #If there's a T1 module
        if 1 in terms:
            T1_index = terms.index(1)
            #If there's a T3 module
            if 3 in terms:
                T3_index = terms.index(3)
                data_grouped.append([[names[T1_index],terms[T1_index]], websites[T1_index], [names[0],terms[0], websites[0]], [names[T3_index],terms[T3_index], websites[T3_index]]])
                del names[T1_index], terms[T1_index], websites[T1_index], names[terms.index(3)], websites[terms.index(3)], terms[terms.index(3)], names[0], terms[0], websites[0]
            else:
                data_grouped.append([[names[T1_index],terms[T1_index], websites[T1_index]], [names[0],terms[0], websites[0]]])
                del names[T1_index], terms[T1_index], websites[T1_index], names[0], terms[0], websites[0],

        #Elif there's a T3 module
        elif 3 in terms:
            T3_index = terms.index(3)
            data_grouped.append([["Spacer", -1], [names[0], terms[0], websites[0]], [names[T3_index], terms[T3_index], websites[T3_index]]])
            del names[T3_index], terms[T3_index], websites[T3_index], names[0], terms[0], websites[0],

        else:
            data_grouped.append([ ["Spacer", -1], [names[0], terms[0], websites[0]]])
            del names[0], terms[0], websites[0]

        self.group_modules(data_grouped, names, terms, websites)

    def group_start_T3(self, data_grouped, names, terms, websites):
        '''
        Group a T3 module with a T1 and/or a T3 and/or a T(1 and 2), then
        remove the grouped modules from the list of modules to be grouped
        '''
        #If there's a T1 module
        if 1 in terms:
            T1_index = terms.index(1)
            #If there's a T2 module
            if 2 in terms:
                T2_index = terms.index(2)
                data_grouped.append([[names[T1_index],terms[T1_index], websites[T1_index]],[names[T2_index],terms[T2_index]], [names[0],terms[0], websites[0]]])
                del names[T1_index], terms[T1_index], websites[T1_index], names[terms.index(2)], websites[terms.index(2)], terms[terms.index(2)], names[0], terms[0], websites[0],
            else:
                data_grouped.append([[names[T1_index],terms[T1_index], websites[T1_index]], ["Spacer", -1], [names[0],terms[0], websites[0]]])
                del names[T1_index], terms[T1_index], websites[T1_index], names[0], terms[0], websites[0]

        #Elf there's a T2 module
        elif 2 in terms:
            T2_index = terms.index(2)
            data_grouped.append([ ["Spacer", -1], [names[T2_index],terms[T2_index], websites[T2_index]], [names[0],terms[0], websites[0]]])
            del  names[T2_index], terms[T2_index], websites[T2_index], names[0], terms[0], websites[0]

        #Elf there's a T(1 and 2) module
        elif 12 in terms:
            T1_2_index = terms.index(12)
            data_grouped.append([[names[T1_2_index],terms[T1_2_index]], websites[T1_2_index], [names[0],terms[0], websites[0]]])
            del  names[T1_2_index], terms[T1_2_index], websites[T1_2_index], names[0], terms[0], websites[0],

        else:
            data_grouped.append([ ["Spacer", -1],  ["Spacer", -1], [names[0],terms[0], websites[0]]])
            del names[0], terms[0], websites[0]

        self.group_modules(data_grouped, names, terms, websites)


class Module(models.Model):
    '''
    This class is used to store information about the modules in the database
    '''

    def __str__(self):
        return self.code

    uni_years = [('1','1'),('2','2'),('3','3'),('4','4'),('na','N/A')]
    uni_terms = [('1','1'),('2','2'),('3','3'),('12','1 and 2'),('Other','Other')]
    departments = [('CSM', 'Camborne School of Mines'), ('Comp', 'Computing'),
                    ('Eng', 'Engineering'), ('Maths', 'Mathematics'),
                    ('NatSci', 'Natural Sciences'), ('Phy', 'Physics and Astronomy'),
                    ('Bio', 'Biosciences'), ('Geo', 'Geography'), ('Other','Other')]
    name = models.CharField(max_length = 200)
    code = models.CharField(max_length = 20)
    year = models.CharField(max_length = 20, choices = uni_years)
    term = models.CharField(max_length = 20, choices = uni_terms)
    credits = models.IntegerField(default = 15)
    department = models.CharField(max_length = 200, choices = departments)
    category = models.CharField(max_length = 200, blank = True, default= 'na')
    sub_category = models.CharField(max_length = 200, blank = True, default= 'na')
    website = models.URLField(max_length = 200, blank = True)
    co_req = models.CharField(max_length = 200, blank = True, default = "N/A")
    pre_req = models.CharField(max_length = 200, blank = True, default = "N/A")

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
