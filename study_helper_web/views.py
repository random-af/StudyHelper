import json
import random

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import User, Theme, Question
from .question_selector import BayesianSelector, HardCodedSelector

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'themeToEdit' in request.form:
            return redirect(url_for('views.edit_theme', theme_name=request.form['themeToEdit']))
        if 'themeToDelete' in request.form:
            theme_name = request.form['themeToDelete']
            theme = Theme.query.filter_by(user_id=current_user.id, name=theme_name).first()
            db.session.delete(theme)
            db.session.commit()
            return render_template('home.html', user=current_user)
        theme_name = request.form.get('themeName')
        if Theme.query.filter_by(user_id=current_user.id, name=theme_name).first():
            flash(f'Theme {theme_name} already exists', category='error')
        else:
            if theme_name == '':
                flash('Theme name can\'t be empty', category='error')
                return render_template('home.html', user=current_user)
            new_theme = Theme(user_id=current_user.id, name=theme_name)
            db.session.add(new_theme)
            db.session.commit()
            flash(f'Theme {theme_name} created!', category='success')
    return render_template('home.html', user=current_user)


@views.route('/edit-theme/<theme_name>', methods=['GET', 'POST'])
def edit_theme(theme_name):
    theme = Theme.query.filter_by(user_id=current_user.id, name=theme_name).first()
    if theme is None:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if 'deleteQuestion' in request.form:
            question = Question.query.filter_by(id=request.form['deleteQuestion']).first()
            db.session.delete(question)
            db.session.commit()
        else:
            question_question = request.form.get('newQuestion')
            question_answer = request.form.get('answer')
            new_question = Question(theme_id=theme.id, question=question_question, answer=question_answer, comment='')
            db.session.add(new_question)
            db.session.commit()

    return render_template('edit_theme.html', user=current_user, theme=theme)


@views.route('/practice/<theme_name>', methods=['GET', 'POST'])
def practice_theme(theme_name):
    theme = Theme.query.filter_by(user_id=current_user.id, name=theme_name).first()
    if request.method == 'POST':
        if 'checkAnswer' in request.form:
            question_id = request.form['checkAnswer']
            question = Question.query.filter_by(id=question_id).first()
            user_answer = request.form['userAnswer']
            return render_template('practice_theme.html', user=current_user, question=question, theme=theme,
                                   check_answer=True, user_answer=user_answer)
        elif 'isCorrect' in request.form:
            question_id = request.form['isCorrect']
            question = Question.query.filter_by(id=question_id).first()
            question.correct_cnt += 1
            db.session.commit()
        elif 'isIncorrect' in request.form:
            question_id = request.form['isIncorrect']
            question = Question.query.filter_by(id=question_id).first()
            question.incorrect_cnt += 1
            db.session.commit()
    all_questions = theme.questions
    # Добавить проверку на пустую тему!
    selector = HardCodedSelector(all_questions, t=1)
    next_question_id = selector.select_next()
    next_question = Question.query.filter_by(id=next_question_id).first()  # Можно просто возвращать номер вопроса и брать ворос из all_questions
    # переделать! Хранить инициализированную версию селектора на сервере
    return render_template('practice_theme.html', user=current_user, question=next_question, theme=theme,
                           check_answer=False)


@views.route('/delete-theme', methods=['POST'])
def delete_theme():
    data = json.loads(request.data)
    theme_id = data['themeId']
    theme = Theme.query.get(theme_id)
    if theme:
        if theme.user_id == current_user.id:
            db.session.delete(theme)
            db.session.commit()
    return jsonify({})


