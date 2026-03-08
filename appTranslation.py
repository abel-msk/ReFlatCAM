# ##########################################################
# FlatCAM: 2D Post-processing for Manufacturing            #
# File Author: Marius Adrian Stanciu (c)                   #
# Date: 3/10/2019                                          #
# MIT Licence                                              #
# ##########################################################
import importlib
import locale
import os
# ##########################################################
# File modified by: vika-sonne, 2023, 2024                 #
# ##########################################################

from os import execl
from sys import executable, argv
from appLogger import getLogger
from pathlib import Path
from typing import Iterator, Callable
from importlib import resources
# from importlib.abc import Traversable
from importlib.resources.abc import Traversable
from pickle import loads
# Qt imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSettings
# misc imports
from langcodes import Language
import gettext

SEARCH_PATH = 'translate'  # path for .bin files
DEFAULT_LANGUAGE = 'English'

log = getLogger('appTranslation')

translation_dict = {}  # translated phrases
language_code = None  # current language code
language_name = None  # current language name

# def gettext(text: str) -> str:
#     return translation_dict.get(text, text)

def get_languages_names() -> tuple[str]:
    the_list = sorted(tuple(Language.get(c).autonym().capitalize() for c, _ in iter_locales()))
    return sorted(tuple(Language.get(c).autonym().capitalize() for c, _ in iter_locales()))

def iter_locales() -> Iterator[tuple[str, Traversable]]:
    """iterates over allowed locales: ISO639-1 language code, Traversable"""
    for p, f in ((x.name,Path(x)) for x in resources.files(SEARCH_PATH).iterdir() if x.is_dir()):
        if f_files := list(f.glob('**/*.mo')):
            yield p, f_files[0]

import builtins

if '_' not in builtins.__dict__:
    _ = gettext.gettext

def on_language_apply_click(app, restart=False):
    """
    Using instructions from here:
    https://inventwithpython.com/blog/2014/12/20/translate-your-python-3-program-with-the-gettext-module/

    :return:
    """
    name = app.ui.general_defaults_form.general_app_group.language_cb.currentText()

    # do nothing if trying to apply the language that is the current language (already applied).
    settings = QSettings("Open Source", "FlatCAM")
    if settings.contains("language"):
        current_language = settings.value('language', type=str)
        if current_language == name:
            return

    if restart:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText(_("The application will restart."))
        msgbox.setInformativeText('%s %s?' %
                                  (_("Are you sure do you want to change the current language to"), name.capitalize()))
        msgbox.setWindowTitle('%s ...' % _("Apply Language"))
        msgbox.setWindowIcon(QtGui.QIcon(':/images/language32.png'))
        msgbox.setIcon(QtWidgets.QMessageBox.Question)

        bt_yes = msgbox.addButton(_("Yes"), QtWidgets.QMessageBox.YesRole)
        bt_no = msgbox.addButton(_("No"), QtWidgets.QMessageBox.NoRole)

        msgbox.setDefaultButton(bt_yes)
        msgbox.exec_()
        response = msgbox.clickedButton()

        if response == bt_no:
            return
        else:
            settings = QSettings("Open Source", "FlatCAM")
            saved_language = name
            settings.setValue('language', saved_language)
            # This will write the setting to the platform specific storage.
            del settings

            restart_program(app=app)

def get_current_language_name() -> str:
    'returns language name from settings; default: English'

    settings = QSettings('Open Source', 'FlatCAM')
    if ret := settings.value('language', None):
        return ret

    ret = DEFAULT_LANGUAGE
    # in case the 'language' parameter is not in QSettings add it to QSettings and it's value is
    # the default language
    settings.setValue('language', ret)

    del settings  # this will write the setting to the platform specific storage

    return ret

# def apply_language() -> Callable[[str], str]:
def apply_language():
    'loads locale to buildins; returns translation function'
    global translation_dict, language_code, language_name
    lang_name = get_current_language_name()
    # current_locale, encoding = locale.getlocale()
    # log.debug(f"Applying language {current_locale}, {encoding}")

    try:
        lang = Language.find(lang_name)
        lang_code = '_'.join((lang.language, lang.territory)) if lang.territory else lang.language
        if language_code == lang_code:
            # language already installed
            return gettext.gettext

        lang_f = next(t for c, t in iter_locales() if c == lang_code)
        with resources.as_file(resources.files(SEARCH_PATH)) as local_path:
            new_lang = gettext.translation('strings',  localedir=local_path,  languages=[lang_code])
            new_lang.install()
    except:
        log.exception  (f'Language not found: Lang={lang_name}, path={lang_f}')
        # log.error(_('Language not found'))
        return gettext.gettext
        # raise

    language_code, language_name = language_code, lang_name
    log.debug(f'Set language: {lang_code} ({lang_name})')
    return gettext.gettext


def restart_program(app, ask=None):
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function.
    """
    log.debug("FlatCAMTranslation.restart_program()")

    # try to quit the Socket opened by ArgsThread class
    try:
        app.new_launch.stop.emit()
        # app.new_launch.thread_exit = True
        # app.new_launch.listener.close()
    except Exception as err:
        log.debug("FlatCAMTranslation.restart_program() --> %s" % str(err))

    # try to quit the QThread that run ArgsThread class
    try:
        app.listen_th.quit()
    except Exception as err:
        log.debug("FlatCAMTranslation.restart_program() --> %s" % str(err))

    if app.should_we_save and app.collection.get_list() or ask is True:
        msgbox = QtWidgets.QMessageBox()
        msgbox.setText(_("There are files/objects modified in FlatCAM. "
                         "\n"
                         "Do you want to Save the project?"))
        msgbox.setWindowTitle(_("Save changes"))
        msgbox.setWindowIcon(QtGui.QIcon(':/images/save_as.png'))
        msgbox.setIcon(QtWidgets.QMessageBox.Question)

        bt_yes = msgbox.addButton(_('Yes'), QtWidgets.QMessageBox.YesRole)
        bt_no = msgbox.addButton(_('No'), QtWidgets.QMessageBox.NoRole)

        msgbox.setDefaultButton(bt_yes)
        msgbox.exec_()
        response = msgbox.clickedButton()

        if response == bt_yes:
            app.f_handlers.on_file_saveprojectas(use_thread=True, quit_action=True)

    app.preferencesUiManager.save_defaults()
    python = executable
    execl(python, python, *argv)
