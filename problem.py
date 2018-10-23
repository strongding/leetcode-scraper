import os
import json
import auth

ALL_ALGORITHMS_URL='https://leetcode.com/api/problems/algorithms'
ALL_TAGS_URL='https://leetcode.com/problems/api/tags/'

DIFFICULTY = {1: "Easy", 2: "Medium", 3: "Hard"}

class Problem():
    def __init__(self, problem_json):
        self.question_id = problem_json['stat']['question_id']
        self.question_title_slug = problem_json['stat']['question__title_slug']
        self.question_title = problem_json['stat']['question__title']
        self.frontend_question_id = problem_json['stat']['frontend_question_id']
        self.difficulty = DIFFICULTY[problem_json['difficulty']['level']]
        self.frequency = float(problem_json['frequency'])
    
    def convert_to_markdown(self):
        return '- [ ] {} {}\t ({})\n'.format(self.frontend_question_id, self.question_title, self.difficulty)


def load():
    auth.login_in()
    
    r = auth.retrieve(ALL_ALGORITHMS_URL)
    if r.status_code!=200:
        print('cannot load the info of all algorithm problems')
        return False
    text = r.text.encode('utf-8')
    json_data = json.loads(text)
    all_problems = {}
    for item in json_data['stat_status_pairs']:
        all_problems[item['stat']['question_id']]=Problem(item)

    r = auth.retrieve(ALL_TAGS_URL)
    if r.status_code!=200:
        print('cannot load the info of all tags')
        return False
    text = r.text.encode('utf-8')
    json_data = json.loads(text)
    google_algorithms = None
    for item in json_data['companies']:
        if item['slug']=='google':
            google_algorithms=set(item['questions'])
    
    all_topics=json_data['topics']
    all_algorithms_by_topic={}
    for item in all_topics:
        topic_name = item['name']
        problem_list = []
        for question_id in item['questions']:
            problem_list.append(all_problems[question_id])
        problem_list.sort(key=lambda x: x.frequency, reverse=True)
        all_algorithms_by_topic[topic_name]=problem_list

    with open('all.md', 'w') as f:
        for key, value in all_algorithms_by_topic.items():
            f.write('# {}\n'.format(key))
            for problem in value:
                f.write(problem.convert_to_markdown())
            f.write('\n')
    
    with open('google.md', 'w') as f:
        for key, value in all_algorithms_by_topic.items():
            f.write('# {}\n'.format(key))
            for problem in value:
                if problem.question_id in google_algorithms:
                    f.write(problem.convert_to_markdown())
            f.write('\n')


if __name__ == '__main__':
    load()
        
