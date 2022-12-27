import numpy as np
from scipy import stats
from sqlalchemy import func, select, table, column

from telegram_model import Bundle, Question


class Selector:
    def __init__(self, db_session=None):
        self.db = db_session

    def get_q_probs(self, bundle_id):
        pass


class RandomSelector(Selector):
    def __init__(self, db_session=None):
        super().__init__()
        self.db_session = db_session

    def get_question(self, bundle_id):
        question = self.db_session.query(Question).order_by(func.random()).first()
        return question


