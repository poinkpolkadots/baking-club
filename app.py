from flask import Flask, redirect, url_for, render_template, request, flash, send_file, session, Response, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from model import *