# -*- coding: utf-8 -*-
"""Настройки приложения."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dictionary_v7.db")

# Секрет для Flask (для flash-сообщений)
SECRET_KEY = "mt-lab4-v7-human-friendly-key"
