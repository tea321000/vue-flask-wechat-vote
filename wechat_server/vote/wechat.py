from werobot import WeRoBot
import re
from werobot.replies import ArticlesReply, Article
import sys
robot = WeRoBot(token='')
robot.config["APP_ID"] = ""
robot.config['ENCODING_AES_KEY'] = ''


@robot.subscribe
def subscribe(message):
    return '欢迎来到基于微信的校园投票系统的设计与开发功能列表系统！'


@robot.text
@robot.voice
def watchFeedback(message):
    try:
        if message.content:
            if re.compile(".*?查看.*?反馈.*?").match(message.content):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="查看用户反馈",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/watchfeedback"
                )
                reply.add_article(article)
                return reply
    except AttributeError:

        if message.recognition:
            if re.compile(".*?查看.*?反馈.*?").match(message.recognition):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="查看用户反馈",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/watchfeedback"
                )
                reply.add_article(article)
                return reply


@robot.text
@robot.voice
def feedback(message):
    try:
        if message.content:
            if re.compile(".*?反馈.*?信息.*?").match(message.content):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="用户反馈",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/feedback"
                )
                reply.add_article(article)
                return reply
    except AttributeError:
        if message.recognition:
            if re.compile(".*?反馈.*?信息.*?").match(message.recognition):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="查看用户反馈",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/watchfeedback"
                )
                reply.add_article(article)
                return reply


@robot.text
@robot.voice
def personal(message):
    try:
        if message.content:
            if re.compile(".*?更改.*?资料.*?").match(message.content):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="更改个人资料",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/personal"
                )
                reply.add_article(article)
                return reply
    except AttributeError:
        if message.recognition:
            if re.compile(".*?更改.*?资料.*?").match(message.recognition):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="更改个人资料",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/personal"
                )
                reply.add_article(article)
                return reply


@robot.text
@robot.voice
def createVote(message):
    try:
        if message.content:
            if re.compile(".*?创建.*?投票.*?").match(message.content):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="创建投票",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/vote"
                )
                reply.add_article(article)
                return reply
    except AttributeError:
        if message.recognition:
            if re.compile(".*?创建.*?投票.*?").match(message.recognition):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="创建投票",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/vote"
                )
                reply.add_article(article)
                return reply


@robot.text
@robot.voice
def attend(message):
    try:
        if message.content:
            if re.compile(".*?参与.*?投票.*?").match(message.content):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="参与投票",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/attend"
                )
                reply.add_article(article)
                return reply
    except AttributeError:
        if message.recognition:
            if re.compile(".*?参与.*?投票.*?").match(message.recognition):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="参与投票",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/attend"
                )
                reply.add_article(article)
                return reply


@robot.text
@robot.voice
def voteHistory(message):
    try:
        if message.content:
            if re.compile(".*?投票.*?历史.*?").match(message.content):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="投票历史",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/history"
                )
                reply.add_article(article)
                return reply
    except AttributeError:
        if message.recognition:
            if re.compile(".*?投票.*?历史.*?").match(message.recognition):
                reply = ArticlesReply(message=message)
                article = Article(
                    title="投票历史",
                    description="基于微信的校园投票系统",
                    img="https://github.com/apple-touch-icon-144.png",
                    url="http://www.yourdomain.xyz:yourport/history"
                )
                reply.add_article(article)
                return reply
