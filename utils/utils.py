# assuming sorted by time
import pandas as pd

class Counter:
    def __init__(self,seed):

        self.counter = {
            "page_counter": seed,
            "video_counter": seed,
            "act_counter":seed
        }

        self.prev_video_problem_name = ''
        self.previous_video_page = ''
        self.prev_act_problem_name = ''



    def counter_reset(self,seed):
      self.counter = {
            "page_counter": seed,
            "video_counter": seed,
            "act_counter":seed
        }

    """ This function evaluates if this is a page with non-content or content events in the log"""
    def verify_status(self,level,problem_name,sublevel):
      return not(pd.isna(level)) and \
        level.startswith('Unit') and \
        not(pd.isna(sublevel)) and \
            not(sublevel.strip() in ['ptest1','growthMindset','survey',
                                         'javaIDEs','csptransition','aboutcsa',
                                         'index','toctree',
                            'topic-1-1-getting-started','preface','','Unit 1 Assignments','Complete Unit 1',
                            'U01 Intro'])

    def update_counter(self,counter_type, previous_page,curr_page,prev_problem_name,problem_name,prev_selection,selection):
        # page_counter when selection == 'page'

        if counter_type == "page_counter" and previous_page == curr_page: return self.counter[counter_type]


        if counter_type == "page_counter" and previous_page != curr_page:  #Any time there is a page we increment counter

            self.counter[counter_type] += 1
            self.counter["video_counter"] = 0
            self.counter["act_counter"] = 0
            return self.counter[counter_type]

      # if there is a page_turn then reset video counter
        if counter_type == "video_counter" and previous_page != curr_page and prev_problem_name != problem_name:
            self.counter[counter_type] += 1
            return self.counter[counter_type]


    # if it is same page, but video changes
        if counter_type == "video_counter" and previous_page == curr_page and prev_problem_name != problem_name:
            self.counter[counter_type] += 1
            return self.counter[counter_type]

      # same page, same video
        if counter_type == "video_counter" and previous_page == curr_page and prev_problem_name == problem_name:
            return self.counter[counter_type]

      # if not same page reset act
        if counter_type == "act_counter" and previous_page != curr_page:# and prev_problem_name != problem_name and selection != prev_selection:
            self.counter[counter_type] = 0
            return self.counter[counter_type]

      # if same page different act increment
        if counter_type == "act_counter" and previous_page == curr_page and prev_problem_name != problem_name and selection != prev_selection:
            self.counter[counter_type] += 1
            return self.counter[counter_type]

      # if same page different act increment; problem name changes but selection doesn't change.
        if counter_type == "act_counter" and previous_page == curr_page and prev_problem_name != problem_name and selection == prev_selection:
            return self.counter[counter_type]

      # if same page different act increment, different actitiy type on the same problem
        if counter_type == "act_counter" and previous_page == curr_page and prev_problem_name == problem_name and selection != prev_selection:
            self.counter[counter_type] += 1
            return self.counter[counter_type]

      # same page same act, same activity type on same problem
        if counter_type == "act_counter" and previous_page == curr_page and prev_problem_name == problem_name and selection == prev_selection:
            return self.counter[counter_type]



    def initialize_params(self, row, df, index):
        student_id = row['Anon Student Id']
        problem_name = row['Problem Name']
        level = row['Level (Chapter)']
        sublevel = row['Level (SubChapter)']


        index = row.name

        prev_row = df.loc[index-1] if index > 0 else row

        prev_student_id = prev_row['Anon Student Id']
        prev_problem_name = prev_row['Problem Name']
        prev_level = prev_row['Level (Chapter)']
        prev_sublevel = prev_row['Level (SubChapter)']
        prev_selection = prev_row['Selection']
        selection = row['Selection']

        previous_page = f'{prev_level}/{prev_sublevel}'
        curr_page = f'{level}/{sublevel}'


        return student_id, problem_name, level, sublevel, index, prev_row,\
                prev_student_id, prev_problem_name, prev_level, previous_page,\
                curr_page,prev_selection, selection


    def return_counter_type_by_selection(self,sublevel,selection):
      return \
      "page_counter" if selection == 'page' \
      else "video_counter" if selection == "video" and not(sublevel.strip() in ['growthMindset']) \
      else "act_counter" if not(pd.isna(sublevel)) and \
        not(sublevel.strip()[:-1] in ['ptest','posttest'] or sublevel.strip() in ['survey']) and \
          selection in ['timedExam', 'mChoice', 'poll', 'shortanswer',
                             'unittest', 'livecode', 'activecode','ac_error',
                             'parsonsMove','parsons', 'clickableArea', 'fillb',
                             'codelens', 'dragNdrop'] \
      else ""



    def increment_counter(self, row, df, index, only_page=False, only_video=False, only_act=False):
        student_id, problem_name, level, sublevel, index, prev_row, \
          prev_student_id, prev_problem_name, prev_level, previous_page, \
          curr_page, prev_selection, selection = self.initialize_params(row, df, index)

        counter_type = self.return_counter_type_by_selection(sublevel,selection) if not(only_page) else 'page_counter'
        other_counters = [x for x in self.counter.keys() if x != counter_type] # whatever is not this counter type

        if counter_type != '':
          new_value = 0

          if prev_student_id == student_id and self.verify_status(level,problem_name,sublevel):
            new_value = self.update_counter(counter_type,previous_page,curr_page, prev_problem_name,problem_name,prev_selection,selection)


          if prev_student_id != student_id:  ### Student transition in the logs
              if False and student_id == 244: print("not same",prev_student_id, student_id,counter_type,self.counter[counter_type])
              self.counter_reset(0) # TODO why are we doing this? -- reset only that specific counter type?
              if self.verify_status(level,problem_name,sublevel): # TODO why are we doing this?
                new_value = self.update_counter(counter_type,previous_page,curr_page, prev_problem_name,problem_name,prev_selection,selection)

          row[counter_type] = new_value
          if False and prev_student_id == 243 and student_id == 244: print("updated",prev_student_id, student_id,counter_type,self.counter,row[counter_type])

          for key in other_counters:
            row[key] = self.counter[key]
            if counter_type == "page_counter" and new_value == 0:   ## non content page; so make other two keys also zero if page counter zero
                row[key] = new_value

          """ If page counter is zero when other counters are non zero"""
          # # line below if conditional  solution to TODO handle the case of student 113 - 114 transition student 114 transitions
          # # directly to activity so page counter doesn't increment
          if 'page_counter' in other_counters and self.counter['page_counter'] == 0:
            self.counter['page_counter'] += 1
            row["page_counter"] = self.counter["page_counter"]

        return row