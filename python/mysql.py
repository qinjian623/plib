
import MySQLdb

try:
    conn = MySQLdb.connect(host='127.0.0.1', user='root',
                           passwd='111qqq,,,', db='my_wiki',
                           port=3306, charset='utf8')
    cur = conn.cursor()
    n = cur.execute('insert into text(old_text, old_flags) values("1111", "")')
    print n
    # for row in cur.fetchall():
    #     for r in row:
    #         print r
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error, e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def insert_page():
    pass


# 流程
# 1. 插入page、revision
# 2. 手动指定text的id【全局变量，加锁】
# 3. DONE
