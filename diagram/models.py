from django.db import models
import datetime
import json
import numpy as np

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
        self.chosen_departments = ['NatSci', 'Phy', 'Bio','Maths']
        # self.chosen_departments = ['NatSci']
        self.years = ['1', '2', '3', '4']
        self.chosen_years = [True, True, True, True]

        #Find dimensions of data matrix
        self.columns_dict = {}
        self.num_columns = 0

        #Store disordered module data
        self.DiagBox_list = []
        self.table_data = []

        #Beautify each department's columns with a background colour
        self.potential_departments = ['CSM', 'Comp', 'Eng', 'Maths', 'NatSci', 'Phy', 'Bio', 'Geo', 'Other']
        self.departments_in_full = ['CSM', 'Computing', 'Engineering', 'Mathematics', 'Natural Science', 'Physics', 'Biosciences', 'Geography', 'Other']
        self.dept_colours = ['#b39559', '#ffb380', '#e67373', '#73e6e6',
                            '#cf8cde', '#99bbff', '#95e67c', '#e6e673', '#ffffff']
        self.chosen_colours = []


        self.debug_iteration = False


        self.set_relevant_years()
        self.initialise_DiagBoxes()
        self.set_diagram_columns()
        self.create_data_table()



    def set_relevant_years(self):
        '''
        For any years set to "False", change that value in self.years to "False"
        '''

        for i in range(len(self.chosen_years)):
            if not self.chosen_years[i]:
                self.years[i] = "False"

    def initialise_DiagBoxes(self):
        '''
        From each module in the databse, create one DiagBox object (as long as
        the module belongs to a dept/year in scope of what the user wants)
        '''

        for department in self.chosen_departments:
            for module in Module.objects.filter(department = department):
                if module.year in self.years:
                    new_DiagBox = DiagBoxes(module)
                    self.DiagBox_list.append(new_DiagBox)

    def set_diagram_columns(self):
        '''
        From the list of modules (Diagox objects), assign to each one a number
        according to their department and category.
        '''
        for module in self.DiagBox_list:

            #Make a dictionary, with each item corresponding to a department
            if module.database.department not in self.columns_dict:
                # self.depts_list.append(module.database.department)
                self.columns_dict[module.database.department] = {}

            #Assign the dictionary index number to the module
            module.dept_number = list(self.columns_dict.keys()).index(module.database.department)

            #Within the department dictionary item, create a dictionary of
            # module categories (corresponding to columns in the final diagram)
            if module.database.category not in self.columns_dict[module.database.department]:
                self.columns_dict[module.database.department][module.database.category] = self.num_columns
                self.num_columns +=1

            module.category_num_unordered = self.columns_dict[module.database.department][module.database.category]

        # self.order_diagram_columns()

    def order_diagram_columns(self):
        '''
        From the list of modules (Diagox objects), assign to each one a number
        according to their department and category.
        '''
        new_index = 0
        #For each column in the diagram...
        for department in self.columns_dict:
            for category in self.columns_dict[department]:
                # find which unordered index corresponded to it...
                old_index = self.columns_dict[department][category]
                for module in self.DiagBox_list:
                    if module.category_num_unordered == old_index:
                        # and set any modules in that category to the new, ordered index number
                        module.column_index = new_index
                self.columns_dict[department][category] = new_index
                new_index += 1

    def create_data_table(self):
        '''
        Create the table of nested data passed to the Django template to construct the diagram
        '''
        dept_index = 0
        #Within each department ...
        for department in self.columns_dict:
            #append some information, then...
            dept_data_position = self.potential_departments.index(department)
            dept_colour = self.dept_colours[dept_data_position]
            dept_full = self.departments_in_full[dept_data_position]
            self.table_data.append([[], f'background-color: {dept_colour}', dept_full])
            category_index = 0
            #list the module categories. Within each category ...
            for category_number in self.columns_dict[department].values():
                self.table_data[dept_index][0].append([])
                # are the years that a module could be taken in. Within each year ...
                for year in range(4):
                    # are some modules, grouped together.
                    self.table_data[dept_index][0][category_index].append([
                            self.group_modules(dept_index, category_number, year), self.years[year]])

                category_index += 1
            dept_index += 1

    def group_modules(self, dept_index, category_number, year):
        '''
        Find the modules in the required department/category/year, then prepare
        to group them together so that they take less space on the diagram
        '''
        modules_ungrouped = [module for module in self.DiagBox_list if module.dept_number == dept_index and module.category_num_unordered == category_number and module.year_index == year]

        grouped_sublist = []

        #Keep grouping modules until all of them are grouped.
        while len(modules_ungrouped) > 0:
            modules_ungrouped, grouped_sublist = self.group_first_module(modules_ungrouped, grouped_sublist)

        return grouped_sublist

    def group_first_module(self, modules_ungrouped, grouped_sublist):
        '''
        For a list of modules, groups them into lists, with no terms overlapping.
        This could result in 1, 2 or 3 modules grouped together.
        '''

        sum_module_height = [0, 0, 0]
        compatible_modules = []

        #The grouping will definitely contain the first module
        first_module_height = modules_ungrouped[0].height
        sum_module_height = np.add(sum_module_height, first_module_height)
        compatible_modules.append(modules_ungrouped[0])
        modules_ungrouped.remove(modules_ungrouped[0])

        #For every other module on the list, try adding it to the grouping,
        # reject this if any two modules overlap across the same term(s).
        for module in modules_ungrouped:
            sum_module_height = np.add(sum_module_height, module.height)

            if 2 in sum_module_height :
                sum_module_height = np.subtract(sum_module_height, module.height)

            else:
                compatible_modules.append(module)
                modules_ungrouped.remove(module)

        grouped_sublist.append(self.order_modules(compatible_modules))

        return modules_ungrouped, grouped_sublist

    def order_modules(self, compatible_modules):
        '''
        When passing in a list of up to 3 modules, whose terms don't overlap,
        return the same list, with the modules ordered by term (adding spacer
        elements to bump modules down correctly if required)
        '''

        ordered_modules = []
        term_1 = False
        term_2 = False
        term_3 = False

        #Check for modules that run in term 1
        for module in compatible_modules:
            if module.height[0] == 1:
                ordered_modules.append(module.module_information())
                compatible_modules.remove(module)
                term_1 = True
                if module.height[1] == 1:
                    term_2 = True
        #If not, add a spacer
        if term_1 == False:
            ordered_modules.append(["spacer", -1])

        #Check for modules that run in term 2 only
        for module in compatible_modules:
            if module.height[1] == 1:
                ordered_modules.append(module.module_information())
                compatible_modules.remove(module)
                term_2 = True

        #Add a spacer if needed
        if term_2 == False:
            ordered_modules.append(["spacer", -1])

        for module in compatible_modules:
            if module.height[2] == 1:
                ordered_modules.append(module.module_information())
                compatible_modules.remove(module)

        return ordered_modules


class DiagBoxes:
    '''
    This class is used to store and manipulate data in the generation of the diagram
    '''

    def __init__(self, module):

        self.database = module

        self.dept_number = None
        self.category_num_unordered = None

        self.year_index = None
        self.term_identifier = None
        self.height = [1, 1, 1]

        self.set_diagram_row()

    def __str__(self):
        return self.database.name

    def set_diagram_row(self):
        '''
        Determine the box's vertical position in the diagram, from its year and term
        '''
        year = self.database.year
        term = self.database.term

        if year.isnumeric():
            self.year_index = int(year)-1
        else:
            self.year_index = 'na'

        if term.isnumeric():
            self.term_identifier = int(term)
        else:
            term_mod = 'na'

        self.set_diagram_height()

    def set_diagram_height(self):
        '''
        Work out the vertical width that the module will take up, by the terms that it takes up
        '''

        if self.term_identifier == 1:
            self.height = [1, 0, 0]
        elif self.term_identifier == 2:
            self.height = [0, 1, 0]
        elif self.term_identifier == 3:
            self.height = [0, 0, 1]
        elif self.term_identifier == 12:
            self.height = [1, 1, 0]
        elif self.term_identifier == 123:
            self.height = [1, 1, 1]
        else:
            self.height = [1, 1, 1]

    def module_information(self):
        return [self.database.name, self.term_identifier, self.database.website, self.database.credits, self.database.pre_req, self.database.co_req, self.database.code]

class Module(models.Model):
    '''
    This class is used to store information about the modules in the database
    '''

    def __str__(self):
        return self.code

    uni_years = [('1','1'),('2','2'),('3','3'),('4','4'),('na','N/A')]
    uni_terms = [('1','1'),('2','2'),('3','3'),('12','1 and 2'),('123','1, 2 and 3'),('Other','Other')]
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
