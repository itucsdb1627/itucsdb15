############################################
Hilal Gülşen Tarafından Gerçeklenen Kısımlar
############################################

   Bu bölümün konusu kullanıcının ilgi alanlarına yönelik kayıtları tutmaktır.
   Burada 3 tablo yer almakta ve bu tablolar üzerinde 4 fonksiyon gerçeklenebilmektedir.
   Bu fonksiyonların nasıl çalıştığı bu kısımda anlatılacaktır.
   redirect, request, url_for, render_template gibi Flask uzantıları, PostgreSQL+Python olan psycopg2 paketi kullanılmıştır.
   Tasarımda HTML ve CSS için Bootstrap tabloları,formları,butonları kullanılmıştır.
   İlgi Alanları sayfasına girildiğinde 3 tane buton karşımıza çıkmaktadır. Bu butonların her biri bir tablo ile bağlıdır.

   .. code-block:: html

         <button type="button" class="btn btn-primary btn-lg btn-block" onclick="showhidegroup(); scrolltogroup();">Gruplar</button>
         <button type="button" class="btn btn-default btn-lg btn-block" onclick="showhidepublish(); scrolltopublish();">Yayinlar</button>
         <button type="button" class="btn btn-info btn-lg btn-block" onclick="showhideevent(); scrolltoevent();">Etkinlikler</button>

   Butonlara tıklandığında ilgili tabloyu gösteren ve bulunduğu kısma yönlendiren JavaScript fonksiyonları yazılmıştır.

   .. code-block:: javascript

         <script>
            function showhidegroup()
            {
               var div = document.getElementById("groupsection");
               if (div.style.display !== "none") {
                  div.style.display = "none";
               }
               else {
                  div.style.display = "block";
               }
            }
            function scrolltogroup(){
               document.getElementById("groupsection").scrollIntoView();
            }
         </script>
         <script>
            function showhidepublish()
            {
               var div = document.getElementById("publishsection");
               if (div.style.display !== "none") {
                  div.style.display = "none";
               }
               else {
                  div.style.display = "block";
               }
            }
            function scrolltopublish(){
               document.getElementById("publishsection").scrollIntoView();
            }
         </script>
         <script>
            function showhideevent()
            {
               var div = document.getElementById("eventsection");
               if (div.style.display !== "none") {
                  div.style.display = "none";
               }
               else {
                  div.style.display = "block";
               }
            }
            function scrolltoevent(){
               document.getElementById("eventsection").scrollIntoView();
            }
         </script>

   İlgi alanları sayfası için ilgialanlari.html sayfası kullanılmıştır.
   Bunun dışında tablolar üzerinde güncelleme işlemleri için updategroups.html, updateactivities.html ve updatepublishes.html sayfaları da kullanılmıştır.
   Html kodları her tablo için benzer yapıda olduğu için grup tablosu üzerinden giderek anlatacağım.


   .. code-block:: html

         1  <table class="table table-bordered table-striped table-hover">
         2        <tr>
         3            <th>Grup Adi</th>
         4            <th>Aciklama</th>
         5            <th>Kurulus Yili</th>
         6            <th>Sektor</th>
         7        </tr>
         8        {% for key, GroupName, Explanation,StartDate ,Sector, Personid in grup %}
         9         <tr>
         10            <td> {{ GroupName }} </td>
         11            <td> {{ Explanation }} </td>
         12            <td> {{ StartDate }} </td>
         13            <td> {{ Sector }} </td>
         14            <td>
         15       <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form" style="display: inline">
         16           <input value="{{key}}" name="id" type="hidden" />
         17            <button class="btn btn-error" name="Delete" type="submit">Gruplarimdan Cikar</button>
         18       </form>
         19       <form action="{{url_for('ilgialanlari_page',personid=personid)}}" method="post" role="form" style="display: inline">
         20             <input value="{{key}}" name="id" type="hidden" />
         21             <button class="btn btn-info" name="Update" type="submit">Duzenle</button>
         22       </form>
         23             </td>
         24       </tr>
         25       {% endfor %}
         26  </table>

   1.satırda tablo için Bootstrap kullanılmıştır. 2-7 satırları arasında tablo için başlıklar bastırılmıştır.
   8-25 satırları arasında for döngüsü gerçeklenmiş ve her dönüşte bir grup bilgisi alınıp ekrana bastırılmıştır.
   15-22 satırları arasında tablodaki her varlık için yanına silme ve düzenleme işlemleri için butonlar eklenmiştir.

   .. code-block:: html

         <div class="page-header">
               <h1>Grup Kur</h1>
            </div>
            <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form">
               <div class="col-sm-3">
                  <div class="form-group">
                     <div class="row">
                        <label class="control-label" for="GroupName">Grup Adi:</label>
                        <input type="text" style="color:black" name="GroupName" class="form-control" required autofocus />
                     </div>
                  </div> <!-- End of form-group -->
                  <div class="form-group">
                     <div class="row">
                        <label class="control-label" for="Explanation">Aciklama:</label>
                        <input type="text" style="color:black" name="Explanation" class="form-control"  />
                     </div>
                  </div> <!-- End of form-group -->
                  <div class="form-group">
                     <div class="row">
                        <label class="control-label" for="StartDate">Kurulus Tarihi(GG-AA-YYYY):</label>
                        <input type="date" name="StartDate" class="form-control"  />
                     </div>
                  </div> <!-- End of form-group -->
                  <div class="form-group">
                     <div class="row">
                        <label class="control-label" for="Sector">Sektor:</label>
                        <input type="text" style="color:black" name="Sector" class="form-control"  />
                     </div>
                  </div> <!-- End of form-group -->

                  <br>
                  <div class="pull-right">
                        <button name="Add" type="submit" class="btn btn-success">Olustur</button>
                  </div> <!-- End of form-group -->
               </div>
             </form>

             <div class="col-sm-3">
               <form action ="{{url_for('ilgialanlari_page',personid=personid)}}" method="post">
                  <b>Grup Ara:</b><br>
                  <input type="text" style="color:black" name="GroupName">&nbsp
                  <input class="btn btn-primary" type="submit" value="Ara" name="Search">
               </form>
             </div>
            </div>

   Kullanıcının yeni grup eklemesi için, gerekli bilgileri girmesini sağlayan Bootstrap formu kullanılmıştır.
   Formun altına ekleme işlemi için Oluştur butonu eklenmiştir.
   Formun sağ tarafına grup aratabileceği başka bir form daha eklenmiş ve Ara butonuna bastığında aranılan grubu ekrana getirmek için tekrar ilgialanlari_page'e döndürülmüştür.

   ilgialanlari.py dosyasına grup.py, publishes.py, activities.py dosyaları aktarılmıştır.
   Tablolara ait fonksiyonlar kendi py dosyasında bulunmakta ve yapılan isteklere göre o fonksiyonlara yönlendirilmektedir.
   İlgi alanları sayfasına girildiğinde ilgialanlari.py dosyasına yönlendirilir.
   "GET" metodu oluşursa expressgrup_page(personid),expresspublishes_page(personid),expressactivities_page(personid) fonksiyonları aşağıdaki gibi çağrılarak grup,publishes,activities tabloları alınıp ilgialanlari.html'e gönderilerek sayfada görünmesi sağlanır.
   Eğer "POST" metodu oluşursa isteklere bağlı olarak ilgili tablonun ilgili işlemi çağrılır ve belli sayfalara döndürülür.

   .. code-block:: python

         @app.route('/ilgialanlari/<personid>', methods=['GET', 'POST'])
         def ilgialanlari_page(personid):
             if request.method == 'GET':
                 grup=expressgrup_page(personid)
                 publishes=expresspublishes_page(personid)
                 activities=expressactivities_page(personid)
                 return render_template('ilgialanlari.html',grup=grup,publishes=publishes,activities=activities,personid=personid)

             else:
                 if 'Addpublishes' in request.form:
                     addpublishes_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))
                 elif 'Add' in request.form:
                     addgrup_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))
                 elif 'Addactivities' in request.form:
                     addactivities_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))
                 elif 'Deletepublishes' in request.form:
                     deletepublishes_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))
                 elif 'Delete' in request.form:
                     deletegrup_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))
                 elif 'Deleteactivities' in request.form:
                     deleteactivities_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))
                 elif 'Updatepublishes' in request.form:
                     publishesid=updatepublishes_page(personid)
                     return render_template('updatepublishes.html', key = publishesid,personid=personid)
                 elif 'Update' in request.form:
                     grupid=updategrup_page(personid)
                     return render_template('updategroups.html', key = grupid,personid=personid)
                 elif 'Updateactivities' in request.form:
                     activitiesid=updateactivities_page(personid)
                     return render_template('updateactivities.html', key = activitiesid,personid=personid)
                 elif 'Searchpublishes' in request.form:
                     publishes=searchpublishes_page(personid)
                     return render_template('ilgialanlari.html',publishes=publishes,personid=personid)
                 elif 'Search' in request.form:
                     grup=searchgrup_page(personid)
                     return render_template('ilgialanlari.html',grup = grup,personid=personid)
                 elif 'Searchactivities' in request.form:
                     activities=searchactivities_page(personid)
                     return render_template('ilgialanlari.html',activities = activities,personid=personid)

1.GRUP TABLOSU
##############
   Grup tablosuna ait işlemler grup.py dosyasında yer almakta ve ilgialanlari.py dosyası tarafından çağrılmaktadır.

1.1.Ekleme İşlemi
=================
   Grup için gerekli bilgiler doldurulduktan sonra "Oluştur" butonuna tıklandığında "Add" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form">

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla addgrup_page fonksiyonuna gönderilir.

   .. code-block:: python

           elif 'Add' in request.form:
            addgrup_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))

   addgrup_page fonksiyonunda INSERT INTO SQL komutuyla aşağıdaki gibi ekleme işlemi gerçeklenmiş olur.

   .. code-block:: python

            def addgrup_page(personid):
             GroupName = request.form['GroupName']
             Explanation = request.form['Explanation']
             StartDate = request.form['StartDate']
             Sector = request.form['Sector']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute("""
             INSERT INTO GRUP (GROUPNAME, EXPLANATION,STARTDATE,SECTOR,PERSONID)
             VALUES (%s, %s, %s, %s, %s) """,
             (GroupName, Explanation,StartDate,Sector,personid))
             connection.commit()

1.2.Silme İşlemi
================
   Silinmek istenen varlığın yanında bulunan Gruplarımdan Çıkar butonuna basıldığında "Delete" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

            <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="Delete" type="submit">Gruplarimdan Cikar</button>
            </form>

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla deletegrup_page fonksiyonuna gönderilir.

   .. code-block:: python

         elif 'Delete' in request.form:
                     deletegrup_page(personid)
                     return redirect(url_for('ilgialanlari_page',personid=personid))

   deletegrup_page fonksiyonunda DELETE FROM SQL komutuyla aşağıdaki gibi silme işlemi gerçeklenmiş olur.

   .. code-block:: python

            def deletegrup_page(personid):
             id = request.form['id']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute( """ DELETE FROM GRUP WHERE ID =%s """,[id])
             connection.commit()

1.3.Güncelleme İşlemi
=====================
   Güncellenmek istenen varlığın yanında bulunan Düzenle butonuna basıldığında "Update" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

            <form action="{{url_for('ilgialanlari_page',personid=personid)}}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-info" name="Update" type="submit">Duzenle</button>
            </form>

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla updategrup_page fonksiyonuna gönderilir.

   .. code-block:: python

         elif 'Update' in request.form:
                     grupid=updategrup_page(personid)
                     return render_template('updategroups.html', key = grupid,personid=personid)

   updategrup_page fonksiyonunda aşağıdaki gibi ilgili grubun grupid değeri döndürülür. Üstteki kodla updategroups.html sayfasına gidilir.

   .. code-block:: python

         def updategrup_page(personid):
             grupid = request.form['id']
             return grupid

   updategroups.html sayfasında gerekli bilgiler doldurulup Değiştir butonuna tıklandığında aşağıdaki kodla update_groups fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{url_for('update_groups', grupid=key,personid=personid)}}" method="post" role="form">

   update_groups fonksiyonunda UPDATE GRUP SQL komutuyla ilgili grup aşağıdaki gibi güncellenmiş olur.

   .. code-block:: python

         @app.route('/ilgialanlari/updategroups/<grupid>,<personid>', methods=['GET', 'POST'])
         def update_groups(grupid,personid):
             if request.method == 'GET':
                 return render_template('updategroups.html')
             else:
                  if 'Update' in request.form:
                      GroupName = request.form['GroupName']
                      Explanation = request.form['Explanation']
                      StartDate = request.form['StartDate']
                      Sector = request.form['Sector']
                      connection = dbapi2.connect(app.config['dsn'])
                      cursor = connection.cursor()
                      cursor.execute(""" UPDATE GRUP SET GROUPNAME = %s, EXPLANATION= %s, STARTDATE= %s, SECTOR= %s WHERE ID = %s """,
                      (GroupName, Explanation, StartDate, Sector, grupid))
                      connection.commit()
                      return redirect(url_for('ilgialanlari_page',personid=personid))

1.4.Arama İşlemi
================
   Bulunmak istenen grubun adı Grup Ara kısmına girilip Ara butonuna tıklandığında "Search" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

          <form action ="{{url_for('ilgialanlari_page',personid=personid)}}" method="post">

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla searchgrup_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Search' in request.form:
            grup=searchgrup_page(personid)
            return render_template('ilgialanlari.html',grup = grup,personid=personid)

   searchgrup_page fonksiyonunda SELECT* FROM SQL komutuyla aşağıdaki gibi arama işlemi gerçeklenmiş olur. Aranılan grup bilgisi döndürülür.

   .. code-block:: python

         def searchgrup_page(personid):
             GroupName = request.form['GroupName']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute( "SELECT * FROM GRUP WHERE GROUPNAME LIKE %s",(GroupName,))
             connection.commit()
             grup = [(key, GroupName,Explanation, StartDate, Sector,personid)
                     for key, GroupName, Explanation, StartDate, Sector,personid in cursor]
             return grup

2.PUBLISHES TABLOSU
###################
   Publishes tablosuna ait işlemler publishes.py dosyasında yer almakta ve ilgialanlari.py dosyası tarafından çağrılmaktadır.

2.1.Ekleme İşlemi
=================
   Yayın için gerekli bilgiler doldurulduktan sonra "Kur" butonuna tıklandığında "Addpublishes" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form">

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla addpublishes_page fonksiyonuna gönderilir.

   .. code-block:: python

        if 'Addpublishes' in request.form:
            addpublishes_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))

   addpublishes_page fonksiyonunda INSERT INTO SQL komutuyla aşağıdaki gibi ekleme işlemi gerçeklenmiş olur.

   .. code-block:: python

         def addpublishes_page(personid):
             EssayType = request.form['EssayType']
             PublishName=request.form['PublishName']
             PublishContent = request.form['PublishContent']
             PublishDate = request.form['PublishDate']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute("""
             INSERT INTO PUBLISHES (ESSAYTYPE,PUBLISHNAME,PUBLISHCONTENT,PUBLISHDATE,PERSONID)
             VALUES (%s, %s, %s, %s,%s) """,
             (EssayType,PublishName,PublishContent,PublishDate,personid))
             connection.commit()

2.2.Silme İşlemi
================
   Silinmek istenen varlığın yanında bulunan Yayını Sil butonuna basıldığında "Deletepublishes" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="Deletepublishes" type="submit">Yayini Sil</button>
         </form>

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla deletepublishes_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Deletepublishes' in request.form:
            deletepublishes_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))

   deletepublishes_page fonksiyonunda DELETE FROM SQL komutuyla aşağıdaki gibi silme işlemi gerçeklenmiş olur.

   .. code-block:: python

            def deletepublishes_page(personid):
                id = request.form['id']
                connection = dbapi2.connect(app.config['dsn'])
                cursor = connection.cursor()
                cursor.execute( """ DELETE FROM PUBLISHES WHERE ID =%s """,[id])
                connection.commit()

2.3.Güncelleme İşlemi
=====================
   Güncellenmek istenen varlığın yanında bulunan Düzenle butonuna basıldığında "Updatepublishes" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{url_for('ilgialanlari_page',personid=personid)}}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-info" name="Updatepublishes" type="submit">Duzenle</button>
         </form>

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla updatepublishes_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Updatepublishes' in request.form:
            publishesid=updatepublishes_page(personid)
            return render_template('updatepublishes.html', key = publishesid,personid=personid)

   updatepublishes_page fonksiyonunda aşağıdaki gibi ilgili yayının publishes değeri döndürülür. Üstteki kodla updatepublishes.html sayfasına gidilir.

   .. code-block:: python

         def updatepublishes_page(personid):
             publishes = request.form['id']
             return publishes

   updatepublishes.html sayfasında gerekli bilgiler doldurulup Değiştir butonuna tıklandığında aşağıdaki kodla update_publishes fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{url_for('update_publishes', publishesid=key,personid=personid)}}" method="post" role="form">

   update_publishes fonksiyonunda UPDATE PUBLISHES SQL komutuyla ilgili yayın aşağıdaki gibi güncellenmiş olur.

   .. code-block:: python

            @app.route('/ilgialanlari/updatepublishes/<publishesid>,<personid>', methods=['GET', 'POST'])
            def update_publishes(publishesid,personid):
                if request.method == 'GET':
                    return render_template('updatepublishes.html')
                else:
                     if 'Updatepublishes' in request.form:
                         EssayType = request.form['EssayType']
                         PublishName=request.form['PublishName']
                         PublishContent = request.form['PublishContent']
                         PublishDate = request.form['PublishDate']
                         connection = dbapi2.connect(app.config['dsn'])
                         cursor = connection.cursor()
                         cursor.execute(""" UPDATE PUBLISHES SET ESSAYTYPE = %s, PUBLISHNAME= %s, PUBLISHCONTENT= %s, PUBLISHDATE= %s WHERE ID = %s """,
                         (EssayType,PublishName,PublishContent,PublishDate, publishesid))
                         connection.commit()
                         return redirect(url_for('ilgialanlari_page',personid=personid))

2.4.Arama İşlemi
================
   Bulunmak istenen yayının adı Yayın Ara kısmına girilip Ara butonuna tıklandığında "Searchpublishes" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

          <form action ="{{url_for('ilgialanlari_page',personid=personid)}}" method="post">

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla searchpublishes_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Searchpublishes' in request.form:
            publishes=searchpublishes_page(personid)
            return render_template('ilgialanlari.html',publishes=publishes,personid=personid)

   searchpublishes_page fonksiyonunda SELECT* FROM SQL komutuyla aşağıdaki gibi arama işlemi gerçeklenmiş olur. Aranılan yayın bilgisi döndürülür.

   .. code-block:: python

         def searchpublishes_page(personid):
             PublishName = request.form['PublishName']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute( "SELECT * FROM PUBLISHES WHERE PUBLISHNAME LIKE %s",(PublishName,))
             connection.commit()
             publishes = [(key, EssayType,PublishName,PublishContent,PublishDate,personid)
                     for key, EssayType,PublishName,PublishContent,PublishDate,personid in cursor]
             return publishes

3.ACTIVITIES TABLOSU
####################
   Activities tablosuna ait işlemler activities.py dosyasında yer almakta ve ilgialanlari.py dosyası tarafından çağrılmaktadır.

3.1.Ekleme İşlemi
=================
   Etkinlik için gerekli bilgiler doldurulduktan sonra "Oluştur" butonuna tıklandığında "Addactivities" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form">

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla addactivities_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Addactivities' in request.form:
            addactivities_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))

   addactivities_page fonksiyonunda INSERT INTO SQL komutuyla aşağıdaki gibi ekleme işlemi gerçeklenmiş olur.

   .. code-block:: python

         def addactivities_page(personid):
             ActivityName=request.form['ActivityName']
             ActivityContent = request.form['ActivityContent']
             ActivityDate = request.form['ActivityDate']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute("""
             INSERT INTO ACTIVITIES (ACTIVITYNAME,ACTIVITYCONTENT,ACTIVITYDATE,PERSONID)
             VALUES (%s, %s, %s, %s) """,
             (ActivityName,ActivityContent,ActivityDate,personid))
             connection.commit()

3.2.Silme İşlemi
================
   Silinmek istenen varlığın yanında bulunan Etkinliği Sil butonuna basıldığında "Deleteactivities" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{ url_for('ilgialanlari_page',personid=personid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="Deleteactivities" type="submit">Etkinligi Sil</button>
         </form>

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla deleteactivities_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Deleteactivities' in request.form:
            deleteactivities_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))

   deleteactivities_page fonksiyonunda DELETE FROM SQL komutuyla aşağıdaki gibi silme işlemi gerçeklenmiş olur.

   .. code-block:: python

         def deleteactivities_page(personid):
             id = request.form['id']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute( """ DELETE FROM ACTIVITIES WHERE ID =%s """,[id])
             connection.commit()

3.3.Güncelleme İşlemi
=====================
   Güncellenmek istenen varlığın yanında bulunan Düzenle butonuna basıldığında "Updateactivities" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

         <form action="{{url_for('ilgialanlari_page',personid=personid)}}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-info" name="Updateactivities" type="submit">Duzenle</button>
         </form>

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla updateactivities_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Updateactivities' in request.form:
            activitiesid=updateactivities_page(personid)
            return render_template('updateactivities.html', key = activitiesid,personid=personid)

   updateactivities_page fonksiyonunda aşağıdaki gibi ilgili etkinliğin activities değeri döndürülür. Üstteki kodla updateactivities.html sayfasına gidilir.

   .. code-block:: python

         def updateactivities_page(personid):
             activities = request.form['id']
             return activities

   updateactivities.html sayfasında gerekli bilgiler doldurulup Değiştir butonuna tıklandığında aşağıdaki kodla update_activities fonksiyonuna gönderilir.

   .. code-block:: html

        <form action="{{url_for('update_activities', activitiesid=key,personid=personid)}}" method="post" role="form">

   update_activities fonksiyonunda UPDATE ACTIVITIES SQL komutuyla ilgili etkinlik aşağıdaki gibi güncellenmiş olur.

   .. code-block:: python

         @app.route('/ilgialanlari/updateactivities/<activitiesid>,<personid>', methods=['GET', 'POST'])
         def update_activities(activitiesid,personid):
             if request.method == 'GET':
                 return render_template('updateactivities.html')
             else:
                  if 'Updateactivities' in request.form:
                      ActivityName = request.form['ActivityName']
                      ActivityContent = request.form['ActivityContent']
                      ActivityDate = request.form['ActivityDate']
                      connection = dbapi2.connect(app.config['dsn'])
                      cursor = connection.cursor()
                      cursor.execute(""" UPDATE ACTIVITIES SET ACTIVITYNAME= %s, ACTIVITYCONTENT= %s, ACTIVITYDATE= %s WHERE ID = %s """,
                      (ActivityName,ActivityContent,ActivityDate, activitiesid))
                      connection.commit()
                      return redirect(url_for('ilgialanlari_page',personid=personid))

3.4.Arama İşlemi
================
   Bulunmak istenen etkinliğin adı Etkinlik Ara kısmına girilip Ara butonuna tıklandığında "Searchactivities" isteği oluşur ve aşağıdaki kodla ilgialanlari_page fonksiyonuna gönderilir.

   .. code-block:: html

          <form action ="{{url_for('ilgialanlari_page',personid=personid)}}" method="post">

   ilgialanlari_page fonksiyonuna geldiğinde aşağıdaki kodla searchactivities_page fonksiyonuna gönderilir.

   .. code-block:: python

        elif 'Searchactivities' in request.form:
            activities=searchactivities_page(personid)
            return render_template('ilgialanlari.html',activities = activities,personid=personid)

   searchactivities_page fonksiyonunda SELECT* FROM SQL komutuyla aşağıdaki gibi arama işlemi gerçeklenmiş olur. Aranılan etkinlik bilgisi döndürülür.

   .. code-block:: python

         def searchactivities_page(personid):
             ActivityName = request.form['ActivityName']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute( "SELECT * FROM ACTIVITIES WHERE ACTIVITYNAME LIKE %s",(ActivityName,))
             connection.commit()
             activities = [(key, ActivityName,ActivityContent,ActivityDate,personid)
                     for key, ActivityName,ActivityContent,ActivityDate,personid in cursor]
             return activities


