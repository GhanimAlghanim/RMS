from flask import Blueprint, render_template, request, url_for, session, flash, redirect, send_file
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import Group, User, Report, User_groups, Tag
from sqlalchemy import or_

report = Blueprint('report', __name__)


@report.route('/', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form['search']
        searchReports = search_reports(data)
        reports = []
        for report in searchReports:
            report_dic = {}
            report_dic['id'] = report.Report.id
            report_dic['name'] = report.Report.name
            report_dic['description'] = report.Report.description
            report_dic['group'] = report.Group.name
            report_dic['tag'] = report.Tag.name
            reports.append(report_dic)
        return render_template("home.html", submitted=True, user=current_user,reports=reports)
    return render_template("home.html", submitted=False, user=current_user)



def search_reports(data):
    return (db.session.query(Report, User, User_groups, Group, Tag)
                        .filter(Group.id == Report.group_id)
                        .filter(Tag.id == Report.tag_id)
                        .filter(User.id == Report.creator_id)
                        .filter(User_groups.group_id == Group.id)
                        .filter(User_groups.user_id == session.get("user_id"))
                        .filter(or_(Report.name.like("%{}%".format(data)),
                                    Report.description.like("%{}%".format(data)),
                                    Tag.name.like("%{}%".format(data)),
                                    Group.name.like("%{}%".format(data))))
                        .all())