import decimal
import logging
import smtplib
import textwrap
import urllib
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, loader, redirect
from django.template import Context, RequestContext
from django.template.loader import render_to_string

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
# from django.core.mail import send_mail, EmailMessage
from freelance_utils.comms import MailComm, SMSComm
from freelance_utils.utils import random_text_generator
from freelance_utils.models import *
from freelance_utils.money.forms import OnlinePaymentForm