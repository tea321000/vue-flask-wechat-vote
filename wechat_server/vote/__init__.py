from flask import Blueprint

vote=Blueprint('vote',__name__)

from .views import *
from .api import *

