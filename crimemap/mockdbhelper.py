class MockDBHelper:

    def connect(self, database="crimemap"):
        pass

    def get_all_inputs(self):
        pass

    def add_input(self, data):
        pass

    def clear_all(self):
        pass

    def add_crime(self, category, date, latitude, longitude, description):
        pass

    def get_all_crimes(self):
        return [{
            'latitude': -33.30359593054658,
            'longitude': 26.511640548706055,
            'date': "2000-01-01",
            'category': "mugging",
            'description': "mock description",
        }]
