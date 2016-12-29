Geliştirici Kılavuzu
====================

Veritabanı Dizaynı
------------------

   Projemizin veritabanı dizaynı ayrı ayrı gerçeklenmiştir. Her takım elemanı kendi veritabanını dizayn etmiştir.

   Bu yüzden, veritabanı dizaynı ve E/R diyagramı ayrı olarak ele alınacaktır.

   Veritabanı tablolarımız ElephantSQL'de tutulmaktadır.

   Projemizde sorgulama dili olarak PostgreSQL kullanılmıştır.


3. Hilal Gülşen'in Veritabanı ve E/R diagramı
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3.1. Veritabanı Dizaynı
"""""""""""""""""""""""
GRUP tablosu 6 niteliğe sahiptir. ID, GROUPNAME, EXPLANATION, STARTDATE, SECTOR, PERSONID bu tablonun nitelikleridir. ID ve PERSONID değerleri kullanıcıya görünmemektedir. Bu tablo PERSONID dış anahtarı ile MAINDATA tablosuna bağlıdır. GRUP tablosu aşağıdaki SQL kodu ile yaratılmaktadır:

        .. code-block:: sql

                 CREATE TABLE IF NOT EXISTS GRUP (
                 ID SERIAL PRIMARY KEY,
                 GROUPNAME VARCHAR(90) NOT NULL,
                 EXPLANATION VARCHAR(400) NOT NULL,
                 STARTDATE DATE NOT NULL,
                 SECTOR VARCHAR(90) NOT NULL,
                 PERSONID INTEGER,
                 FOREIGN KEY (PERSONID)
                 REFERENCES MAINDATA (ID)
                 ON DELETE CASCADE)

PUBLISHES tablosu 6 niteliğe sahiptir. ID, ESSAYTYPE, PUBLISHNAME, PUBLISHCONTENT, PUBLISHDATE, PERSONID bu tablonun nitelikleridir. ID ve PERSONID değerleri kullanıcıya görünmemektedir. Bu tablo PERSONID dış anahtarı ile MAINDATA tablosuna bağlıdır. PUBLISHES tablosu aşağıdaki SQL kodu ile yaratılmaktadır:

    .. code-block:: sql

             CREATE TABLE IF NOT EXISTS PUBLISHES (
             ID SERIAL PRIMARY KEY,
             ESSAYTYPE VARCHAR(90) NOT NULL,
             PUBLISHNAME VARCHAR(90) NOT NULL,
             PUBLISHCONTENT VARCHAR(500) NOT NULL,
             PUBLISHDATE DATE NOT NULL,
             PERSONID INTEGER,
             FOREIGN KEY (PERSONID)
             REFERENCES MAINDATA (ID)
             ON DELETE CASCADE)

ACTIVITIES tablosu 5 niteliğe sahiptir. ID, ACTIVITYNAME, ACTIVITYCONTENT, ACTIVITYDATE, PERSONID bu tablonun nitelikleridir. ID ve PERSONID değerleri kullanıcıya görünmemektedir. Bu tablo PERSONID dış anahtarı ile MAINDATA tablosuna bağlıdır. ACTIVITIES tablosu aşağıdaki SQL kodu ile yaratılmaktadır:


      .. code-block:: sql

             CREATE TABLE IF NOT EXISTS ACTIVITIES (
             ID SERIAL PRIMARY KEY,
             ACTIVITYNAME VARCHAR(150) NOT NULL,
             ACTIVITYCONTENT VARCHAR(400) NOT NULL,
             ACTIVITYDATE DATE NOT NULL,
             PERSONID INTEGER,
             FOREIGN KEY (PERSONID)
             REFERENCES MAINDATA (ID)
             ON DELETE CASCADE)


3.2. E/R Diyagram
"""""""""""""""""

   Tablolarım için E/R diyagramı :

   .. figure:: ERDiyagramı.jpg
      :scale: 75 %
      :alt:

      *Grup, Publishes, Activities tabloları için E/R Diyagramı*


Kod
---

   Veritabanı ile olan bağlantımız ve projemiz, Python kodları için ana dosya olan server.py dosyası üzerinde yapılmıştır.

   Aşağıda verilen Python kodları projemizi veritabanına bağlar.

   .. code-block:: python

         def get_elephantsql_dsn(vcap_services):
          """Returns the data source name for ElephantSQL."""
          parsed = json.loads(vcap_services)
          uri = parsed["elephantsql"][0]["credentials"]["uri"]
          match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
          user, password, host, _, port, dbname = match.groups()
          dsn = """user='{}' password='{}' host='{}' port={}
                   dbname='{}'""".format(user, password, host, port, dbname)
          return dsn

    .. code-block:: python

            if __name__ == '__main__':
                VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
                if VCAP_APP_PORT is not None:
                    port, debug = int(VCAP_APP_PORT), False
                else:
                    port, debug = 5001, True

                VCAP_SERVICES = os.getenv('VCAP_SERVICES')
                if VCAP_SERVICES is not None:
                    app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
                else:
                    app.config['dsn'] = """user='vagrant' password='vagrant'
                                           host='localhost' port=1234 dbname='itucsdb'"""

                app.run(host='0.0.0.0', port=port, debug=debug)


.. toctree::

   BurakSimsek
   ZihnicanBeğburs
   HilalGulsen
   ZeynepAnkara
