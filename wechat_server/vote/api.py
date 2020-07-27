from werkzeug.utils import secure_filename
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_httpauth import HTTPBasicAuth
from app import app
import sys
import os
from vote import vote
from .sql import db
from .models import User, UserList, Vote, Option, VoteHistory, Feedback
import datetime
import time
auth = HTTPBasicAuth()
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
academies = ["机电工程学院", "信息与通信学院", "计算机与信息安全学院",
             "艺术与设计学院", "商学院", "外国语学院", "数学与计算科学学院", "电子工程与自动化学院"]

#400:未填写用户名或密码；401:用户名或密码错误；402：用户名已存在；405:非法的token; 406:学号/编号和姓名输入错误;  407:Token 过期了;410:找不到详情

@vote.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username, password, file=sys.stderr)
    if username is None or password is None:
        # abort(400)    # missing arguments
        abort(400)
    success = verify_password(username, password)
    if not success:
        abort(401)
    token = g.user.generate_auth_token()
    resp = jsonify(
        {'data': {'token': token.decode('ascii')}})
    resp.status_code = 200
    return resp


@vote.route('/register', methods=['POST'])
def new_user():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')
    birthday = request.json.get('birthday')
    phone = request.json.get('phone')
    role = request.json.get('role')
    if role == 'student':    
        permission = 1
    elif role=='teacher':
        permission=2
    elif role=='administrator':
        permission=4
    else:
        abort(405)
    
    if username is None or password is None:
         # 缺少参数
        abort(400)
    if User.query.filter_by(id=username).first() is not None:
         #用户已存在
        abort(402)
    if UserList.query.filter_by(id=username, name=name, role=role).first() is None:
        # 数据库寻找用户列表是否存在该用户
        abort(406)
    else:
        user = User(id=username, name=name,
                    birthday=birthday, phone=phone, role=role, permission=permission)
        user.hash_password(password)
        from app import db
        db.session.add(user)
        db.session.commit()
        resp = jsonify({'username': user.id})
        resp.status_code = 201
        return resp


@auth.verify_password
def verify_password(username_or_token, password):
    # 尝试用token登录
    user = User.verify_auth_token(username_or_token)
    if not user:
        # 尝试用用户名和密码登录
        user = User.query.filter_by(id=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# 请求用户信息
@auth.login_required
@vote.route('/info', methods=['POST'])
def information():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    # 调试用
    # print('token-------------',file=sys.stderr)
    # print(token,file=sys.stderr)
    # print('id-------------',file=sys.stderr)
    # print(user.id,file=sys.stderr)
    # print('role-------------',file=sys.stderr)
    # print([user.role],file=sys.stderr)
    # print('birthday-------------', file=sys.stderr)
    # print(user.birthday, file=sys.stderr)
    # print('phone-------------', file=sys.stderr)
    # print(user.phone, file=sys.stderr)
    # print('end-------------', file=sys.stderr)

    if user is None:
        abort(405)
    else:
        birthday=str(user.birthday)
        print('birthday-------------', file=sys.stderr)
        print(birthday, file=sys.stderr)
        print('-------------', file=sys.stderr)
        resp = jsonify(
            {'data': {'roles': [user.role], 'name': user.name, 'id': user.id, 'birthday':birthday , 'phone': user.phone}})
        return resp


@auth.login_required
@vote.route('/feedback', methods=['POST'])
def feedback():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    if user.role is not 'student' and user.role is not 'teacher':
        abort(405)
    title=request.json.get('theme')
    content=request.json.get('content')
    feedback=Feedback(id=int(round(time.time() * 1000)),user_id=user.id,title=title,content=content)
    db.session.add(feedback)
    db.session.commit()
    resp=jsonify({})
    resp.status_code=200
    return resp


@auth.login_required
@vote.route('/watchfeedback', methods=['POST'])
def watchFeedback():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    if user.role is not 'administrator':
        abort(405)
    feedbacks=db.session.query(Feedback)
    # 调试用
    # print('feedbacks-------------', file=sys.stderr)
    # print(feedbacks, file=sys.stderr)
    # print('end-------------', file=sys.stderr)
    feedbacks_json={'data':[]}
    if feedbacks:
        for feedback in feedbacks:
            
            feedback_json = {'user_id': feedback.user_id, 'user_name': feedback.user.name,
                             'feedback_theme': feedback.title, 'feedback_content': feedback.content}
            feedbacks_json['data'].append(feedback_json)
    return jsonify(feedbacks_json)
    
    
    



#创建投票选项过滤学生时用
@auth.login_required
@vote.route('/students', methods=['POST'])
def queryStudents():
    result = {'data': {'person': []}}
    for id, name, role in db.session.query(User.id, User.name, User.role):
        if(role is 'student'):
            result['data']['person'].append(id+" "+name)
    resp = jsonify(result)
    return resp

#投票详情时显示图片
@auth.login_required
@vote.route('/show/<filename>')
def uploaded_file(filename):
    g.filename = filename
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#限制用户名
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#点击图片加号时上传
@auth.login_required
@vote.route('/upload', methods=['POST'])
def upload_file():
    # 检查传过来的内容是否含有文件部分
    if 'file' not in request.files:
        abort(410)
    file = request.files['file']
    if file.filename == '':
        abort(411)
    if file and allowed_file(file.filename):
        filename_split = os.path.splitext(file.filename)
        filename = secure_filename(
            filename_split[0]+str(int(round(time.time() * 1000)))+filename_split[1])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'link': 'http://www.yourdomain.xyz:yourport/vote/show/'+filename})


@auth.login_required
@vote.route('/history', methods=['POST'])
def voteHistory():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    votes_json = {'data': []}
    
    if(user.role is not 'teacher'):
        vote_id = []
        for vote_history in user.vote_history:
            # 调试用
            # print('----vote_history', file=sys.stderr)
            # print(vote_history, file=sys.stderr)
            # print('----vote_history.vote', file=sys.stderr)
            vote = vote_history.vote
            # 调试用
            # print(vote_history.vote, file=sys.stderr)
            # print('----end', file=sys.stderr)
            if vote.id not in vote_id:
                vote_id.append(vote.id)
                vote_json = {"id": vote.id, "title": vote.title, "time_start": vote.time_start,
                            "time_end": vote.time_end, "anonymous": vote.anonymous, "multiple": vote.multiple}
                votes_json['data'].append(vote_json)
    else:
        for vote in user.vote:
            vote_json = {"id": vote.id, "title": vote.title, "time_start": vote.time_start,
                         "time_end": vote.time_end, "anonymous": vote.anonymous, "multiple": vote.multiple}
            votes_json['data'].append(vote_json)
    votes_json['data'].reverse()
    resp = jsonify(votes_json)
    return resp

#学生参与投票时列表（开放投票）
@auth.login_required
@vote.route('/attend', methods=['POST'])
def attendVoteList():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    if(user.role is not 'student'):
        abort(405)
    votes_json = {'data': []}
    now = datetime.datetime.now()
    for id, title, time_start, time_end, anonymous, multiple in Vote.query.order_by(desc(Vote.id)).filter(Vote.time_start < now, Vote.time_end > now).with_entities(Vote.id, Vote.title, Vote.time_start, Vote.time_end, Vote.anonymous, Vote.multiple):
        vote_json = {"id": id, "title": title,
                     "time_start": time_start, "time_end": time_end, "anonymous": anonymous, "multiple": multiple}
        votes_json['data'].append(vote_json)
    resp = jsonify(votes_json)
    return resp


@auth.login_required
@vote.route('/detail/<id>/', methods=['POST'])
def voteDetail(id=None):
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    vote = Vote.query.filter_by(id=id).one()
    if not vote:
        abort(410)
    if vote:
        vote_json = {'data': {'title': vote.title, 'content': vote.content, 'time_start': vote.time_start, 'time_end': vote.time_end,
                              'anonymous': vote.anonymous, 'multiple': vote.multiple, 'academy': vote.academy, 'grade': vote.grade, 'person': vote.person, 'pic': vote.pic}}
        if user.role is 'teacher':
            permission = False
        elif user.role is 'student':
            permission = True
            if vote.academy:
                # 调试用
                # print(user.id[2:5], file=sys.stderr)
                # print(vote.academy, file=sys.stderr)
                # print('------academy', file=sys.stderr)
                if academies[int(user.id[2:5])-1] not in vote.academy:
                    permission = False
            if vote.grade:
                # 调试用
                # print(user.id[:2], file=sys.stderr)
                # print(vote.grade, file=sys.stderr)
                # print('------grade', file=sys.stderr)
                if int('20'+user.id[:2]) not in vote.grade:
                    permission = False
            if vote.person:
                # 调试用
                # print(user.id, file=sys.stderr)
                # print(user.id, file=sys.stderr)
                # print(vote.person, file=sys.stderr)
                # print('------person', file=sys.stderr)
                if user.id+' '+user.name not in vote.person:
                    permission = False
            if VoteHistory.query.filter_by(user_id=user.id,vote_id=id).first():
                permission = False
        vote_json['data']['permission'] = permission

        time_limit = True
        now = datetime.datetime.now()
        if vote.time_start > now or vote.time_end < now:
            time_limit = False
        vote_json['data']['time_limit'] = time_limit

        vote_json['data']['options'] = []
        vote_json['data']['group'] = []
        for option in vote.option:
            if option.group not in vote_json['data']['group']:
                vote_json['data']['group'].append(option.group)
            vote_json['data']['options'].append(
                {'name': option.content, 'value': option.count,'group':option.group})
        if not vote.anonymous:
                vote_json['data']['history'] = []
                try:
                    for vote_history in vote.vote_history:
                        # print("------vote_history.user", file=sys.stderr)
                        # print(vote_history.user, file=sys.stderr)
                        # print('------vote_history.option', file=sys.stderr)
                        # print(vote_history.option, file=sys.stderr)
                        # print('------end', file=sys.stderr)
                        vote_json['data']['history'].append(
                            {'user_id': vote_history.user.id, 'user_name': vote_history.user.name, 'vote_content': vote_history.option.content, 'vote_count': vote_history.option.count})
                except:
                    vote_json['data']['history'] =None
        resp = jsonify(vote_json)
    else:
        abort(410)
    return resp

#删除投票
@auth.login_required
@vote.route('/deletevote', methods=['POST'])
def deleteVote():
    token = request.json.get('token')
    if not token:
        abort(405)
    id=request.json.get('vote_id')
    # print('------vote_id-----', file=sys.stderr)
    # print(id, file=sys.stderr)
    # print('------end', file=sys.stderr)
    user = User.verify_auth_token(token)
    vote = Vote.query.filter_by(id=id).one()
    if not vote:
        abort(410)
    if vote:
        for vote_history in vote.vote_history:
            db.session.delete(vote_history)
        for vote_option in vote.option:
            db.session.delete(vote_option)
        db.session.delete(vote)
        db.session.commit()
        resp = jsonify()
        resp.status_code = 200
        return resp
        


#在详情中投票
@auth.login_required
@vote.route('/submit', methods=['POST'])
def submitVote():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    id = request.json.get('id')
    choice = request.json.get('choice')
    choice_sum=[]
    vote = Vote.query.filter_by(id=id).one()
    if vote.multiple:
        for item in choice:
            choice_sum+=item
    else:
        choice_sum=choice
    print('-----chioce', file=sys.stderr)
    print(choice, file=sys.stderr)
    print('-----chioce_sum', file=sys.stderr)
    print(choice_sum, file=sys.stderr)
    print('-----end', file=sys.stderr)
    if not vote:
        abort(410)
    if user.role is 'teacher':
        permission = False
    elif user.role is 'student':
        permission = True
        if vote.academy:
                # 调试用
                # print(user.id[2:5], file=sys.stderr)
                # print(vote.academy, file=sys.stderr)
                # print('------academy', file=sys.stderr)
            if academies[int(user.id[2:5])-1] not in vote.academy:
                permission = False
        if vote.grade:
            # 调试用
            # print(user.id[:2], file=sys.stderr)
            # print(vote.grade, file=sys.stderr)
            # print('------grade', file=sys.stderr)
            if int('20'+user.id[:2]) not in vote.grade:
                permission = False
        if vote.person:
            # 调试用
            # print(user.id, file=sys.stderr)
            # print(vote.person, file=sys.stderr)
            # print('------person', file=sys.stderr)
            if user.id+' '+user.name not in vote.person:
                permission = False
    time_limit = True
    now = datetime.datetime.now()
    if vote.time_start > now or vote.time_end < now:
        time_limit = False
    if permission and time_limit:
        if vote.multiple:
            if VoteHistory.query.filter_by(user_id=user.id,vote_id=id).first():
                abort(411)  # 已经投过票
            else:
                for checked in choice_sum:
                    vote.option[checked].count += 1
                    vote_history = VoteHistory(
                        user_id=user.id, vote_id=vote.id, option_id=vote.option[checked].id)
                    db.session.add(vote_history)
                db.session.commit()
                resp = jsonify()
                resp.status_code = 200
                return resp
        else:
            if VoteHistory.query.filter_by(user_id=user.id,vote_id=id).first():
                abort(411)  # 已经投过票
            else:
                for checked in choice_sum:
                    vote.option[checked].count += 1
                    vote_history = VoteHistory(
                        user_id=user.id, vote_id=vote.id, option_id=vote.option[checked].id)
                    db.session.add(vote_history)
                db.session.commit()
                resp = jsonify({})
                resp.status_code = 200
                return resp
    else:
        abort(412)


@auth.login_required
@vote.route('/personal', methods=['POST'])
def personalChange():
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    if(user is None):
        abort(405)
    password = request.json.get('password')
    birthday = request.json.get('birthday')
    phone = request.json.get('phone')
    if(password is not None):
        user.hash_password(password)
    user.birthday = birthday
    user.phone = phone
    db.session.commit()
    resp = jsonify()
    resp.status_code = 200
    return resp


@auth.login_required
@vote.route('/logout', methods=['POST'])
def logout():
    resp = jsonify()
    resp.status_code = 202
    return resp


@auth.login_required
@vote.route('/create', methods=['POST'])
def createVote():
    # 传递过来的字段：
    # theme,
    # startDate1,
    # startDate2,
    # endDate1,
    # endDate2,
    # selectMode,
    # anonymous,
    # filter,
    # selectedAcademy,
    # selectedGrade,
    # selectedPerson,
    # content,
    # image,
    # multipleSelected,
    # singleSelected
    token = request.json.get('token')
    if not token:
        abort(405)
    user = User.verify_auth_token(token)
    theme = request.json.get('theme')
    startDate1 = request.json.get('startDate1')
    startDate2 = request.json.get('startDate2')
    startDate = datetime.datetime.strptime(
        startDate1+" "+startDate2, '%Y/%m/%d %H:%M:%S')
    endDate1 = request.json.get('endDate1')
    endDate2 = request.json.get('endDate2')
    endDate = datetime.datetime.strptime(
        endDate1+" "+endDate2, '%Y-%m-%d %H:%M:%S')
    anonymous = request.json.get('anonymous')
    content = request.json.get('content')
    image = request.json.get('image')
    selectMode = request.json.get('selectMode')
    vote = Vote(id=int(round(time.time() * 1000)), user_id=user.id,
                title=theme, content=content, time_start=startDate, time_end=endDate, anonymous=anonymous, multiple=selectMode)
    if(image):
        vote.pic = image

    filter = request.json.get('filter')
    if(filter is not '全校'):
        selectedAcademy = request.json.get('selectedAcademy')
        if(selectedAcademy):
            vote.academy = selectedAcademy
        selectedGrade = request.json.get('selectedGrade')
        if(selectedGrade):
            vote.grade = selectedGrade
        selectedPerson = request.json.get('selectedPerson')
        if(selectedPerson):
            vote.person = selectedPerson
    from app import db
    db.session.add(vote)

    if(selectMode):
        options = request.json.get('multipleSelected')
    else:
        options = request.json.get('singleSelected')
    for item in options:
        group_num=item.find('_')
        if group_num>0:
            option = Option(group=item[:group_num],content=item[group_num+1:], vote_id=vote.id, count=0)
        else:
            option = Option(content=item, vote_id=vote.id, count=0)
        db.session.add(option)
    db.session.commit()
    resp = jsonify()
    resp.status_code = 200
    return resp
    # 调试用
    # print('theme-------------', file=sys.stderr)
    # print(theme, file=sys.stderr)
    # print('startDate1-------------', file=sys.stderr)
    # print(startDate1, file=sys.stderr)
    # print('startDate2-------------', file=sys.stderr)
    # print(startDate2, file=sys.stderr)
    # print('endDate1-------------', file=sys.stderr)
    # print(endDate1, file=sys.stderr)
    # print('endDate2-------------', file=sys.stderr)
    # print(endDate2, file=sys.stderr)
    # print('anonymous-------------', file=sys.stderr)
    # print(anonymous, file=sys.stderr)
    # print('content-------------', file=sys.stderr)
    # print(content, file=sys.stderr)
    # print('image-------------', file=sys.stderr)
    # print(image, file=sys.stderr)
    # print('selectMode-------------', file=sys.stderr)
    # print(selectMode, file=sys.stderr)
    # print('options-------------', file=sys.stderr)
    # print(options, file=sys.stderr)
    # print('filter-------------', file=sys.stderr)
    # print(filter, file=sys.stderr)
    # print('selectedAcademy-------------', file=sys.stderr)
    # print(selectedAcademy, file=sys.stderr)
    # print('selectedGrade-------------', file=sys.stderr)
    # print(selectedGrade, file=sys.stderr)
    # print('selectedPerson-------------', file=sys.stderr)
    # print(selectedPerson, file=sys.stderr)
    # print('end-------------', file=sys.stderr)
    resp = jsonify()
    resp.status_code = 200
    return resp
