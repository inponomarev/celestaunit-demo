# coding=UTF-8
from java.util import Properties
import os

CELESTA_PROPERTIES = Properties()
CELESTA_PROPERTIES.put('score.path', os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
CELESTA_PROPERTIES.put('pylib.path', '/')  # Данная настройка необходима только в контексте запуска java приложения
CELESTA_PROPERTIES.put("h2.in-memory", "true")

# Список модулей для импорта модулем celestaunit.py
INITIALIZING_GRAINS = []
