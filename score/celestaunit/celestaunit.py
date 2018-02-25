# coding=UTF-8
from functools import partial

from ru.curs.celesta import Celesta
from ru.curs.celesta import SessionContext
import testparams
import sys
import importlib
from unittest import TestCase

props = testparams.CELESTA_PROPERTIES

celesta = Celesta.createDebugInstance(props)
sessionContext = SessionContext('super', 'debug')
createCallContext = partial(celesta.callContext, sessionContext)

callContext = createCallContext()
sys.modules['initcontext'] = lambda: callContext

try:
    for grain in celesta.getScore().getGrains().values():
        # Когда в testparams заданы модули для инициализации, пропускаем не указанные
        if grain.getName() == "celesta" or \
                (testparams.INITIALIZING_GRAINS and grain.getName() not in testparams.INITIALIZING_GRAINS):
            continue

        importlib.import_module(grain.getName())
finally:
    sys.modules.pop('initcontext', None)
    callContext.close()

def clean_db(context):
    """Выполняет полную очистку базы данных."""
    score = context.getCelesta().getScore()
    for g in list(filter(lambda x: x != 'celesta', score.grains)):
        grain = score.getGrain(g)
        for t in grain.tables:
            orm = importlib.import_module('%s._%s_orm' % (g, g))
            cursor = getattr(orm, '%sCursor' % t)(context)
            cursor.deleteAll()

            cursor.close()


class CelestaUnit(TestCase):
    """Класс-предок для тестирования работы celesta"""

    @classmethod
    def getInitContext(cls):
        return createCallContext()

    def getCelesta(self):
        return celesta

    def setUp(self):
        self.context = createCallContext()
        self.__conn = self.context.getConn()

        self.cleanDB = False

    def tearDown(self):
        # Доп. заглушка, чтобы не удалились данные из реальной бд
        if self.cleanDB and props.get('h2.in-memory') == 'true':
            clean_db(self.context)
        self.context.close()

    def setReferentialIntegrity(self, integrity):
        sql = "SET REFERENTIAL_INTEGRITY " + str(integrity)
        stmt = self.__conn.createStatement()
        try:
            stmt.execute(sql)
        finally:
            stmt.close()

    def setCleanDB(self, value):
        self.cleanDB = value
