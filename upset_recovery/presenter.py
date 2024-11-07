import time
import os
import json

from .config import GameCnst


class Presenter:
    def __init__(self, centralwidget, upset_recovery_window):
        self.centralwidget = centralwidget
        self.upset_recovery_window = upset_recovery_window
        self.centralwidget.startTestBtnPressed.connect(self.prepare_for_test)
        self.centralwidget.startTrainBtnPressed.connect(self.start_train)
        self.logged = False
        self.cur_dir = os.path.abspath(os.path.dirname(__file__))
        self.home_dir = os.path.dirname(self.cur_dir)
        self.result_dir = self.home_dir + os.sep + 'results'
        if not os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)
        self.user_credentials = {'name': 'default'}
        self.experiment_conditions = {'roll': 0, 'pitch': 0}
        self.load_config()

    def set_default_config(self):
        with open(self.cur_dir + os.sep + 'default_config.py', mode='r') as source:
            f = open(self.cur_dir + os.sep + 'config.py', mode='w+')
            f.write(source.read())
            f.close()

    def load_config(self, config='default_experiment_config'):
        self.config_dict = {}
        with open(os.path.abspath(os.path.dirname(__file__)) + os.sep + config) as conf:
            for line in conf:
                if line != '\n':
                    variable = line.split('=')
                    self.__dict__[variable[0]] = variable[1].rstrip('\n')
            if self.UPSET_POSITIONS:
                self.CYCLE_NUMBER = len(self.UPSET_POSITIONS)

    def write_experiment_data(self, data: dict):
        self.experiment_conditions = {
            exp_number: {'roll': position[0], 'pitch': position[1]}
            for exp_number, position in enumerate(GameCnst.UPSET_POSITIONS)
        }
        pth = self.result_dir + os.sep + 'experiment_js'
        txt_pth = self.result_dir + os.sep + 'experiment_text.txt'
        prepared_data = {
            'user': self.user_credentials,
            'experiment_conditions': self.experiment_conditions,
            'experiment_results': data
        }
        with open(pth, mode='a') as f:
            json.dump(prepared_data, fp=f)
            f.write('\n')
        with open(txt_pth, mode='a') as f:
            json.dump(prepared_data, fp=f)
            f.write('\n')

    def prepare_for_test(self):
        self.centralwidget.login_user()
        self.centralwidget.log_window.startBtnPressed.connect(self.get_login_data)

    def start_test(self):
        field_names = ('group', 'last_name', 'first_name', 'middle_name')
        self.user_credentials = dict(zip(field_names, self.login_data))
        upset_recovery = self.upset_recovery_window(presenter=self)
        results = upset_recovery.run()
        self.write_experiment_data(results)

    def start_train(self):
        upset_recovery = self.upset_recovery_window(test=False)
        upset_recovery.run()
        self.centralwidget.close

    def get_login_data(self):
        self.login_data = self.centralwidget.log_window.get_login_data()
        self.experiment_time = time.time()
        if self.login_data:
            self.start_test()
        print(self.login_data)
        return self.login_data