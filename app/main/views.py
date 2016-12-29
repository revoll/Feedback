# encoding: utf-8
import os
import uuid
from time import strftime
from flask import render_template, redirect, abort, url_for, flash, request, current_app, send_from_directory
from flask_wtf import Form
from wtforms import TextAreaField, FileField, SelectField, SubmitField, StringField  # , validators
from . import main
from .. import db
from ..models import Feedback


class FeedbackForm(Form):
    subject = SelectField(u'类型', coerce=int)
    content = TextAreaField(u'意见及建议')  # validators=[validators.Length(min=12, message=u'至少输入12个字符')]
    images = FileField(u'上传图片')
    submit = SubmitField(u'提交')
    author_name = StringField(u'姓名')
    author_id = StringField(u'身份证号')
    author_dept = StringField(u'部门')
    author_contact = StringField(u'联系方式')

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        subjects_list = current_app.config['FEEDBACK_SUBJECTS']
        self.subject.choices = [(i, subjects_list[i]) for i in range(0, len(subjects_list))]


@main.route('/')
def index():
    return redirect(url_for('.add_feedback'))


@main.route('/feedback/', methods=['GET', 'POST'])
def add_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(subject=form.subject.data, content=form.content.data,
                            author_name=form.author_name.data, author_id=form.author_id.data,
                            author_dept=form.author_dept.data, author_contact=form.author_contact.data)
        appendix = u''
        file_list = request.files
        for i in file_list:
            img = file_list[i]
            if '.' in img.filename and img.filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']:
                folder = strftime("%Y-%m")
                filename = uuid.uuid1().hex + '.' + img.filename.rsplit('.', 1)[1]
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
                if not os.path.exists(path):
                    os.makedirs(path)
                img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename))
                appendix = appendix + u'<img src="/uploads/' + os.path.join(folder, filename) + u'"/>'
        feedback.appends = appendix
        db.session.add(feedback)
        flash(u'反馈意见已提交，谢谢！')
        return render_template('post-success.html', name=feedback.author_name, id_number=feedback.author_id,
                               dept=feedback.author_dept, contact=feedback.author_contact)
    arg_values = request.args if request.method == 'GET' else request.values
    form.author_name.data = arg_values.get(u'name', type=unicode)
    form.author_id.data = arg_values.get(u'id_number', type=unicode)
    form.author_dept.data = arg_values.get(u'dept', type=unicode)
    form.author_contact.data = arg_values.get(u'contact', type=unicode)
    if form.author_name.data is None or form.author_id.data is None or \
            form.author_dept.data is None or form.author_contact.data is None:
        abort(403)
    else:
        admin = True if form.author_id.data in current_app.config['FEEDBACK_ADMIN_LIST'] else False
        return render_template('post-feedback.html', form=form, admin=admin)


@main.route('/uploads/<folder>/<filename>/')
def uploaded_file(folder, filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], os.path.join(folder, filename))


@main.route('/manage/')
def manage_index():
    return redirect(url_for('.manage_feedback'))


@main.route('/manage/feedback/')
def manage_feedback():
    page = request.args.get('page', 1, type=int)
    pagination = Feedback.query.order_by(Feedback.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_FEEDBACKS_PER_PAGE'], error_out=False)
    for i in range(0, len(pagination.items)):
        pagination.items[i].time = pagination.items[i].timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('manage-feedback.html', feedbacks=pagination.items, pagination=pagination,
                           subjects=current_app.config['FEEDBACK_SUBJECTS'])


@main.route('/manage/feedback/<int:id>/')
def feedback_detail(id):
    feedback = Feedback.query.get_or_404(id)
    feedback.time = feedback.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('feedback-detail.html', feedback=feedback,
                           subjects=current_app.config['FEEDBACK_SUBJECTS'])


@main.route('/manage/mark-solved/<int:id>/')
def mark_solved(id):
    feedback = Feedback.query.get_or_404(id)
    feedback.read_flag = True
    db.session.add(feedback)
    return 'success - mark solved'


@main.route('/manage/mark-unsolved/<int:id>/')
def mark_unsolved(id):
    feedback = Feedback.query.get_or_404(id)
    feedback.read_flag = False
    db.session.add(feedback)
    return 'success - mark unsolved'


@main.route('/manage/delete/<int:id>/')
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    return 'success - delete feedback'
