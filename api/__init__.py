from flask import Flask , blueprints, Blueprint
from database import models
from .utils import Register
from typing import Dict



bp = Blueprint('api' , __name__ , url_prefix='/api/v1')




#registration

@bp.post('/register/<string:name>/<string:number>')
def registration(name : str, number: str) -> Dict:
    try:
        user_to_check = Register(name=name, phone_number = number)
        user_id = models.register_or_get_user_id(user_to_check)
    except AttributeError:
        return {'status' : 0, 'message' : 'Fault loading data'}
    return {'status': 1, 'user_id' : user_id}

# getting the table of leaders

@bp.get('/leaders/<string:level>')
def get_leaders(level):
    if level == 'all':
        leaders_list = models.get_table_of_leaders()
        result_list = [{i[0]: i[1] for i in leaders_list}]
        result_dict = {'level' : level, 'leaders': result_list}

    else:
        leaders_list = models.get_table_of_leaders(level)
        result_list = [{i[0]: i[1] for i in leaders_list}]
        result_dict = {'level': level, 'leaders': result_list}

    return result_dict


#gettting questions

@bp.get('/get-questions/<string:level>/<string:q_set>')
def get_questions(level : str , q_set : str)-> Dict:
    questions = models.get_questions(level , q_set)

    result = {'timer' : 45, 'questions': [{'question_id': i[0], i[1]: i[2:6]} for i in questions]}

    return result





# checking answer
@bp.post('/check-answer/<int:question_id>/<int:user_id>/<string:user_answer>')
def check_user_answer(question_id: int , user_id: int , user_answer:str)-> Dict:
    answer = models.check_user_answer(question_id, user_id, user_answer)

    return {'status': answer}

# ending the test
@bp.post('/done/<int:user_id>/<int:corrects>/<string:level>/<string:q_set>')
def get_result_and_end(user_id: int , corrects: int , level: str, q_set: str)-> Dict:
    position = models.test_complete_get_position(user_id, corrects, level , q_set)





    result = {'status':1 , 'correct_answer': corrects, 'position_on_top': position }

    return result


