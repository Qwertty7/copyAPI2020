from lib.recruit_career.base import BaseClient


class Candidates(BaseClient):

    def get_candidate_positions(self, user_id):
        return self.session.get(self.base_url + '/candidates/' + str(user_id) + '/positions')

# create new candidate and check that data exist

    def create_new_candidate(self, candidate_data):
        url = self.base_url + '/candidates'
        print(self.session.headers)
        return self.session.post(url, json=candidate_data)
