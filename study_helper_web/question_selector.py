import numpy as np
from scipy import stats


class QuestionSelector:
    def __init__(self, all_questions):
        columns = [col.key for col in all_questions[0].__table__.c]
        self.all_questions = {col: np.array([getattr(question, col) for question in all_questions]) for col in columns}

    def select_next(self):
        pass

    def update_questions(self):
        pass  # будет нужно, если хранить селектор на сервере


class BayesianSelector(QuestionSelector):
    def __init__(self, all_questions, thompson=False, quantile=0.7):
        super(BayesianSelector, self).__init__(all_questions)
        self.a_priors = None
        self.b_priors = None
        self._calc_priors()

        self.alphas = None
        self.betas = None
        self._calc_parameters()

        self.thompson = thompson
        self.quantile = quantile

    def select_next(self):
        if self.thompson:
            samples = np.random.beta(self.alphas, self.betas)
            next_question_id = self.all_question['id'][np.argmax(samples)]
        else:
            quantiles = stats.beta.ppf(self.quantile, self.alphas, self.betas)
            next_question_id = self.all_questions['id'][np.argmax(quantiles)]
        return int(next_question_id)

    def print_stats(self):
        pass

    def _calc_parameters(self):
        self.alphas = self.a_priors + np.array(self.all_questions['incorrect_cnt'])
        self.betas = self.b_priors + np.array(self.all_questions['correct_cnt'])

    def _calc_priors(self):
        self.a_priors = np.ones(len(self.all_questions['id']))
        self.b_priors = np.ones(len(self.all_questions['id']))


class HardCodedSelector(QuestionSelector):

    def __init__(self, all_questions, t=1):
        super().__init__(all_questions)
        self.t = t

    def select_next(self):
        weights = np.ones(len(self.all_questions['id']))
        weights[self.all_questions['correct_cnt'] > 0] += 1
        weights[self.all_questions['correct_cnt'] > 1] += 1
        weights[self.all_questions['incorrect_cnt'] > 0] -= 0.5
        weights[(self.all_questions['correct_cnt'] == 0) & (self.all_questions['incorrect_cnt'] == 0)] = 0.2
        weights = 1 / weights
        probs = np.exp(weights / self.t) / np.exp(weights / self.t).sum()
        print(probs)
        next_question_id = np.random.choice(self.all_questions['id'], p=probs)
        return int(next_question_id)
