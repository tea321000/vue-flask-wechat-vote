from .wechat import robot
from flask import Blueprint, render_template, redirect, request, jsonify
from flask.views import MethodView
from werobot.contrib.flask import make_view
from vote import vote
import sys


vote.add_url_rule(rule='/wechat/',
                  endpoint='wechat',
                  view_func=make_view(robot),
                  methods=['GET', 'POST'])
