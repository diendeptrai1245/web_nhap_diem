import os 
from dotenv import load_dotenv
from model import db, students, subjects, scores
from flask import Flask, render_template, request, redirect, url_for, session

def signup():
    if request.method == "POST":
        user_name = 