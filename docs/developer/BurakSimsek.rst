###########################################
Burak Şimşek Tarafından Tamamlanan Bölümler
###########################################

Bu projede benim tarafımdan ElephantSQL kullanılarak 3 tablo yaratılmıştır.
Bu tablolar sırasıyla Maindata,FriendRequest,FriendList olarak adlandırılmışlardır.
Bu geliştirici rehberinde bütün bu tabloların özellikleri ve kullanılan metodlar anlatılacaktır.Bu projede CSS,HTML,Python ve PostgreSQL
kullanılarak nesne tabanlı programlama yaklaşımıyla bir web-uygulaması oluşturulmuş ve kullanıma sunulmuştur.

Maindata Tablosu
================

Maindata tablosu 5 nitelik içermektedir. Bu nitelikler ID,e-mail,password,name ve surname olarak isimlendirilmişlerdir. Bu tabloda
web-uygulamasına kayıt olan kullanıcıların en temel özellikleri tutulmakta, ayrıca session için bu tabloda arama özelliği kullanılarak
giriş kontrolü sağlanmaktadır. Ayrıca uygulamadaki diğer tablolar da dış anahtar(id) ile maindata tablosuna bağlıdır.

**FONKSIYONLAR**

Geliştirmiş olduğumuz web-uygulamasında bu tabloya ait 4 ana fonksiyon yani Ekleme,Silme,Güncelleme ve Arama fonksiyonları kullanılmaktadır.

EKLEME
------

Kullanıcı kayıt olmak için kayıt ol sekmesine tıkladığında signup.html sayfasına yönlendirilir ve orada doldurması gereken metin kutularını
doldurarak "kayıt ol" butonuna basar. Böylece girdiği bilgiler signup_page() fonksiyonuna gönderilir.Aşağıda bu işleyişe dair kodlar verilmiştir.

.. code-block:: python

       <form action="{{ url_for('signup_page')}}" method= "POST">
       <h1 name="signupheader"> Lutfen asagidaki bilgileri doldurunuz </h1>
       E-Posta: <br>
       <input type="text"  name="email" <br>
       Sifre: <br>
       <input type="password" name="password"> <br>
       <br>
       Isim:<br>
       <input type="text" name="name" <br>
       Soyisim: <br>
       <input type="password" name="surname"> <br>
       <br>
       <button style="height:50px;width:100px" type="submit" name="Submit" value="register" class="btn btn-info">Kayit Ol</button>
       </form>



Yukarıda da bahsedildiği gibi maindata tablosu kullanıcıların bilgilerini tutmaktadır, bu bilgiler kullanıcıya üye olurken kullandıkları
kullanıcılara ait kimlik belirleyici bilgilerdir.

.. code-block:: python

     @app.route('/signup',methods=['POST','GET'])
     def signup_page():

     if request.method=='POST':
      mssg=request.form['email']
      psswrd=request.form['password']
      name=request.form['name']
      surname=request.form['surname']
      with dbapi2.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
      query= """ INSERT INTO MAINDATA(EMAIL,PASSWORD,NAME,SURNAME) VALUES ('%s','%s','%s','%s')"""  %       (mssg,psswrd,name,surname)
      cursor.execute(query)
      connection.commit()
     return render_template('signup.html')

Signup_page() fonksiyonu POST metodu ile signup.html üzerinden kullanıcıya ait verileri alarak, maindata tablosunda bu verileri kullanarak bir varlık yaratılmasını
sağlıyor ve signup.html değerini döndürmektedir.
Maindata tablosunda ID niteliği, Veritabanı tarafından otomatik olarak arttırılan ve emsalsiz(unique) bir değeri temsil ediyor.

SİLME
-----

Eğer web-uygulaması üzerinde kullanıcıların hesaplarının silinmesi gerekirse,maindata üzerinden o kullanıcıya ait
varlık silinerek o kullanıcıya ait hesap silinmektedir.Bu işlemi gerçekleştirebilmek için admin.html üzerinden silinmek istenen kullanıcıya
ait e-mail gerekli metin kutusuna yazıldıktan sonra onunla ilişik olan "sil" butonuna tıklanır.
.. code-block:: python

   <form action="{{url_for('delete_user')}}" method="POST") >
   Silmek istediginiz e-postayi giriniz:
   <input type="text" name="email" class="form-control"  required autofocus/>
   <input style="height:50px;width:100px" type="submit" name="Delete"
   class="btn btn-error" value="Sil"></>
   </form>

admin.html üzerinden çağrılan delete_user() fonksiyonu GET methodu ile çağrılır ve maindatadb.py dosyasında bulunan delete_user() fonksiyonu
çağrılarak silme işlemi gerçekleştirilir.


.. code-block:: python

          @app.route('/admin/deleteuser',methods=['POST','GET'])
          def delete_user():
          connection = dbapi2.connect(app.config['dsn'])
          cursor = connection.cursor()
          if request.method=='POST':
          eposta=request.form['email']
          cursor.execute("DELETE FROM MAINDATA WHERE EMAIL= %s",(eposta,))
          cursor.execute("SELECT * FROM MAINDATA")
          backupmaindata=cursor.fetchall()
          connection.commit()
          return redirect(url_for('admin_page',maindata=backupmaindata))
          elif request.method == 'GET':
          return redirect(url_for('admin_page',maindata=backupmaindata))
          @app.route('/admin/searchuser',methods=['POST','GET'])

GÜNCELLEME&ARAMA
----------------

Maindata tablosunun her bir varlığının güncellemesi admin.html sayfası üzerinden gerçekleşmektedir.Site Yöneticisi(Administrator) gerekli
durumlarda admin.html de bulunan metin kutusu ve "ara ve güncelle" butonunu kullanarak önce tabloda arama işlemini gerçekleştirir ardından
da güncelleme işlemini yapar.

.. code-block:: html

    <form action= "{{ url_for('search_user')}}" method="POST")>
    Guncellemek istediginiz e-postayı giriniz:
    <input type="text" name="emailaddress" >
    <input style="height:50px;width:100px" type="submit" name="search" class="btn btn-warning" value="Ara& Guncelle"></button>
    </form>

Yönetici bu işlemleri gerçekledikten sonra search_user() fonksiyonu çağrılır;search_user() fonksiyonu aşağıda verilmiştir.

.. code-block:: python

     @app.route('/admin/searchuser',methods=['POST','GET'])
     def search_user():
     if request.method=='POST':
     emailadd=request.form['emailaddress']
     connection = dbapi2.connect(app.config['dsn'])
     cursor = connection.cursor()
     cursor.execute("SELECT * FROM MAINDATA WHERE EMAIL=%s",(emailadd,))
     connection.commit()
     backupmaindata=[(key,email,password,name,surname)
                      for key,email,password,name,surname in cursor]
   return render_template('updateuser.html',backupmaindata=backupmaindata)

Search_user() fonksiyonu updateuser.html i döndürür ve updateuser.html sayfasındaki gerekli metin kutuları doldurulduktan sonra ve
"Guncelle" butonuna basıldıktan sonra update_user(key) çağrılır.

.. code-block:: html

    <form action= "{{ url_for('search_user')}}" method="POST")>
    Guncellemek istediginiz e-postayı giriniz:
     <input type="text" name="emailaddress" >
    <input style="height:50px;width:100px" type="submit" name="search" class="btn btn-warning" value="Ara& Guncelle"></button>
    </form>

Yukarıda update_user() fonksiyonun admin.html üzerinden çağrılışını gösteren kod bloğunun gerçekleşmesinin ardından maindata.py dosyasının
içinde bulunan update_user(key) fonksiyonu çağrılarak güncelleme gerçeklenir. update_user() fonksiyonun tanımlaması aşağıda verilmiştir.

.. code-block:: python

      @app.route('/admin/updateuser/<asdid>',methods=['POST','GET'])
      def update_user(asdid):
      connection = dbapi2.connect(app.config['dsn'])
       cursor = connection.cursor()
      if request.method=='POST':
      posta=request.form['email']
      psswd=request.form['password']
      name=request.form['name']
      surname=request.form['surname']
      cursor.execute("""UPDATE MAINDATA SET EMAIL=%s,PASSWORD=%s,NAME=%s,SURNAME=%s  WHERE ID= %s""" ,(posta,psswd,name,surname,asdid))
      connection.commit()
      return redirect(url_for('admin_page'))
      elif request.method=='GET':
      return render_template('updateuser.html')


Yukarıda verilen örneklerin dışında tüm projede bu fonksiyonların kullanıldığı başka alanlar da oldu.Fakat onları fazla detay olacağı için
tekrardan yazma gereğinde bulunmadım. Kodun tamamı incelendiği takdirde Maindata tablosuyla bağlantılı fonksiyonlar bulmak mümkündür.


FriendRequest Tablosu
=====================

 FriendRequest Tablosu kullanıcılar arası bağlantı kurma isteklerini tutan bir tablodur. 2 niteliği vardır; bunlar personid ve friendrequestid olarak isimlendiril
 mişlerdir. Personid sütununda bağlantı isteği gönderen kişinin id si, friendrequestid sütününda ise bağlantı isteği gönderilen kişinin id si tutulmaktadır.
 Bu tablonun amacı web-uygulamasını daha kaliteli hale getirmek ve farklı üyeler arasındaki ilişkilerin sağlanmasıdır.Ayrıca bu tablo
 maindata tablosuna personid dış anahtarı aracılığı ile bağlıdır. Son olarak
 Bu tabloya erişim baglantilar.html sayfası üzerinden gerçekleştirilmektedir.

**FONKSIYONLAR**

Kullanıcı baglantilar.html sayfasında yer alan önerilerin yanında bulunan "Arkadaslık Istegi Gonder" butonunu kullanarak bağlantı isteği oluşturur yani bu tabloya bir varlık eklemiş olur.Bu tablonun Güncelleme fonksiyonu yazılmamıştır,çünkü gerek yoktur.
Güncelleme yapılırsa tablo amacı dışında kullanılmış olacaktır.

EKLEME
------

Üst satırlar da belirtildiği gibi bu tabloya varlık ekleme baglantılar.html sayfasından gerçekleşmektedir.

.. code-block:: html

   <form>
   <table class="table-striped"  border="2px">
      <tr>

         <h1>ARKADAS ONERILERI</h1>

         <th>E-mail</th>
         <th>Name</th>
         <th>Surname</th>
         <th>Secenekler</th>
   </tr>
      {% for key,email,password,name,surname in maindata %}
      <tr>

         <td>{{email}}</td>
         <td>{{name}}</td>
         <td>{{surname}}</td>
         <td>
         <form action="{{ url_for('baglantilar_page',personid=personid,key=key) }}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />

                     <input class="btn btn-info" onclick="change({{key}})" name="AddRequest" type="submit" value="Arkadaslik Istegi Gonder" id="{{key}}" ></input>
                     <script>
                     function change(key)
                     {
                     document.getElementById(key).value="Istek Gonderildi";
                     }


                     </script>
         </form>

Kullanıcı "Arkadaslik Istegi Gonder butonuna bastığında baglantılar_page() fonksiyonu çağrılır, ve bu fonksiyona gerekli olan veriler html
aracılığı ile iletilir. Bu bilgiler FriendRequest tablosuna eklenecek varlığın elemanları olarak kullanılacaklardır.

.. code-block:: python

            if 'AddRequest' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDREQUEST (PERSONID,REQUESTID)
            VALUES (%s, %s) """,
            (personid,key,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

baglantılar_page() fonksiyonu oldukça kapsamlı bir fonksiyon olduğundan sadece FriendRequest tablosuna varlık eklemek için gereken koşul bloğu
gösterildi,Bu fonksiyonun diğer blokları gerektiği yerlerde bu dökümanda verilecektir.

SILME
-----

Kullanıcı baglantılar.html dosyasından kendisine gelen baglantı isteklerini baglantı istekleri bölümünde görebilmektedir. Gelen baglantı isteğinin yanındaki
"Arkadaslik İstegini Sil" butonunu kullanarak gelen bağlantı isteğini silebilir. Bu işlem geliştirme açısından aşağıdaki şekilde dizayn edilmiştir:

.. code-block:: html

         </form>
         <form action="{{ url_for('baglantilar_page',personid=personid,key=key2) }}" method="post" role="form" style="display: inline">
                     <input value="{{key2}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteRequest" type="submit"  >Arkadaslik Istegini Sil</button>
         </form>

Bu işlem baglantılar_page() fonksiyonuna DeleteRequest isimli istek olarak gönderilir; baglantılar_page() fonksiyonu çağrılır ve
ve DeleteRequest isimli blokta işlem yapılır.Bu işlem aşağıda verilmiştir:

.. code-block:: python

    elif 'DeleteRequest' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

Ayrıca kullanıcı gelen bağlantı isteğini kabul ettiğinde de artık kullanıcı ile istek gönderen kullanıcı arasında bağlantı kurulacak
olduğundan yine bu varlık FriendRequest tablosundan silinecektir. Bu işlemlerin gerçekleşmesini sağlayan kod blokları aşağıda verilmiştir.

HTML:

.. code-block:: html

         <form action="{{ url_for('baglantilar_page',personid=personid,key=key2,title=title) }}" method="post" role="form" style="display: inline">
                     <input value="{{key2}}" name="id" type="hidden" />
                     <input type="text" style="color:black" name="title" <br>
                     <button class="btn btn-primary" name="AddFriend" type="submit"  >Title Ekle&Onayla</button>

PYTHON&SQL:

.. code-block:: python

    elif 'AddFriend' in request.form:
            key = request.form['id']
            title=request.form['title']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID,TITLE)
            VALUES (%s, %s ,%s) """,
            (personid,key,title))
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID)
            VALUES (%s, %s) """,
            (key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

Yukarıda verilen python kodunda bir diğer tabloya ekleme yapılırken(aşağıda ayrıca anlatılacaktır.), FriendRequest tablosundan varlık
silinmektedir.

ARAMA
-----

FriendRequest tablosunda arama fonksiyonu yine baglantılar.html üzerinden,baglantılar.html sayfasının Gelen Bağlantı İstekleri
kısmında gerçekleşmektedir. Arama fonksiyonu kullanılarak kullanıcıya gelen baglantı isteklerini göstermektedir.

.. code-block:: html

   <table class=table  border="2px">
      <tr>

         <h1>GELEN BAGLANTI ISTEKLERI</h1>

         <th>Isim Soyisim</th>
         <th>Secenekler</th>

   </tr>
      {% for key2,name,surname in maindata4 %}


         <td> {{name}} {{surname}}</td>
         <td>
         <form action="{{ url_for('baglantilar_page',personid=personid,key=key2,title=title) }}" method="post" role="form" style="display: inline">
                     <input value="{{key2}}" name="id" type="hidden" />
                     <input type="text" style="color:black" name="title" <br>
                     <button class="btn btn-primary" name="AddFriend" type="submit"  >Title Ekle&Onayla</button>
         </form>
         <form action="{{ url_for('baglantilar_page',personid=personid,key=key2) }}" method="post" role="form" style="display: inline">
                     <input value="{{key2}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteRequest" type="submit"  >Arkadaslik Istegini Sil</button>
         </form>
         </td>

         <table class=table  border="2px">
      <tr>



Gösterme işlemi, baglantilar.html de yukarıdaki şekilde implement edilmiştir, fakat burada önemli olan nokta veritabanından çekilen verilerin maindata4 e atanmasıdır.baglantılar.html
de ise bu veri üzerinde for döngüsü ile dolaşılarak tüm gelen bağlantı isteklerinin gösterilmesi sağlanmıştır. maindata4 adlı veri yapısının elde edilmesi sırasında
iç katma kullanılarak, maindata tablosundan id üzerinden isim ve soyisim niteliklerine erişilmiş, baglantı isteklerinin isim ve soyisim olarak
gösterilmesi sağlanmıştır. Bu işlem de baglantılar_page() fonksiyonun içerisinde gerçekleştirmiştir.

.. code-block:: python

   connection=dbapi2.connect(app.config['dsn'])
        cursor=connection.cursor()
        cursor.execute("""SELECT FRIENDREQUEST.PERSONID,MAINDATA.NAME,MAINDATA.SURNAME
        FROM FRIENDREQUEST INNER JOIN MAINDATA ON FRIENDREQUEST.PERSONID=MAINDATA.ID WHERE REQUESTID=%s""",(personid))
        backupmaindata4=cursor.fetchall()
        connection.commit()
        maindata4=[(key2,name,surname)
                    for key2,name,surname in cursor]


Böylece kullanıcı arayüzü anlamlı ve anlaşılabilir bir hale getirilmiş,kullanıcı için çok daha iyi bir arayüz sunulmuştur.
Ayrıca bu kod bloğunun ardından bu bloğun bağlı olduğu üst blok baglantilar.html sayfasını döndürmekte,baglantilar.html sayfasına da
yukarıdaki sorgudan elde edilen veriyi göndermektedir.

.. code-block:: python

      return render_template('baglantilar.html',personid=personid,
      maindata=backupmaindata,maindata3=backupmaindata3,maindata4=backupmaindata4)

FriendList Tablosu
==================

FriendList tablosunun 3 niteliği bulunmaktadır ;bunlar Personid,Friendid ve Title olarak adlandırılmışlardır.FriendList tablosunun oluşturulma amacı site üyelerinin arkadaşlarını varlıklar halinde saklamaktır.
Personid kullanıcının kendi id sini saklarken friendid arkadaş olduğu kullanıcının idsini,title ise kullanıcının bağlantı kurduğu kullanıcıya isterse atayabildiği kelimeyi ifade etmektedir.
Ayrıca bu tablo maindata tablosuna personid dış anahtarı aracılığı ile bağlıdır. Bu tablonun arayüz kısmı yine baglantilar.html sayfasında bulunmakta, ekleme,silme,güncelleme ve arama fonksiyonları
baglantilar.html sayfası üzerinden gerçekleşmektedir.

**FONKSIYONLAR**

Kullanıcı bağlantılar sayfasında, baglantı isteğini onaylarsa, ya da baglantı isteği gönderildiği kişi
tarafından onaylanırsa ekleme fonksiyonu gerçekleşir. Eğer baglantilar.html sayfasında bağlantılar
bölümü içerisinde bulunan bir bağlantıyı silerse FriendList tablosundan varlıklar silinecektir.
Kullanıcı arkadaşına verdiği ünvanı değiştirmek isterse bu da güncelleme fonksiyonu aracılığıyla gerçekleşir.

EKLEME
------

Yukarıda da bahsedildiği gibi ekleme operasyonu kullanıcı gelen bağlantı isteğini kabul ettiğinde tabloya varlıklar ekler.Çünkü
baglantı kurmak karşılıklı gerçekleştiği için kullanıcı karşı tarafın isteğini kabul ettiğinde bu işlemin iki şekilde karşılıklı olarak
çalışması gerekir. Aşağıda ekleme fonksiyonları gösterilmiştir.

.. code-block:: html

   {% for key2,name,surname in maindata4 %}


         <td> {{name}} {{surname}}</td>
         <td>
         <form action="{{ url_for('baglantilar_page',personid=personid,key=key2,title=title) }}" method="post" role="form" style="display: inline">
                     <input value="{{key2}}" name="id" type="hidden" />
                     <input type="text" style="color:black" name="title" <br>
                     <button class="btn btn-primary" name="AddFriend" type="submit"  >Title Ekle&Onayla</button>
         </form>
         <form action="{{ url_for('baglantilar_page',personid=personid,key=key2) }}" method="post" role="form" style="display: inline">
                     <input value="{{key2}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteRequest" type="submit"  >Arkadaslik Istegini Sil</button>
         </form>
         </td>

         <table class=table  border="2px">
      <tr>

         </td>
      </tr>
      {% endfor %}

Kullanıcı gelen baglanti isteklerini onaylarsa baglantılar_page() fonksiyonun AddFriend bloku çağrılır ve ekleme işlemi gerçekleşir.SQL ve Python kodları
aşağıda verilmiştir.

.. code-block:: python

    elif 'AddFriend' in request.form:
            key = request.form['id']
            title=request.form['title']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID,TITLE)
            VALUES (%s, %s ,%s) """,
            (personid,key,title))
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID)
            VALUES (%s, %s) """,
            (key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

SILME
-----

FriendList tablosundan bir varlık silme işlemi baglantilar.html sayfasının baglantılar bölmesi içerisinden gerçekleşir. Kullanıcı
"Arkadaşı Sil" butonunu kullanarak karşısında bulunan bağlantıyı siler, ekleme gibi bu fonksiyon da çift taraflı çalışmaktadır. Aşağıda
bu fonksiyonun gerçekleşmesini sağlayan kodlar verilmiştir.

.. code-block:: html

   <form action="{{ url_for('baglantilar_page',personid=personid,requestid=requestid) }}" method="post" role="form" style="display: inline">
                     <input value="{{requestid}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteFriend" type="submit"  >Arkadasi Sil</button>
         </form>


baglantilar.html sayfasından silme işlemi için komut verildiğinde baglantilar_page() fonksiyonu çağrılarak "DeleteFriend" bloğu
çalıştırılır.

.. code-block:: python

      elif 'DeleteFriend' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            DELETE FROM FRIENDLIST WHERE PERSONID=%s AND FRIENDID=%s
             """,
            (personid,key,))
            cursor.execute("""
            DELETE FROM FRIENDLIST WHERE PERSONID=%s AND FRIENDID=%s
             """,
            (key,personid,))

            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

ARAMA
-----

FriendList tablosunda arama fonksiyonu baglantilar.html de baglantiları gösterme amacı ile kullanılmaktadır. Burada da iç katma
yapılarak maindata tablosundan o id ye sahip kullanıcının ismi ve soyisimini alarak kullanıcı arayüzünün kalitesi arttırılmış, karışıklıkların
önüne geçilmiştir.

 HTML:

.. code-block:: html


   <table class=table  border="2px">
   <tr>
         <h1>BAGLANTILAR</h1>

         <th>Isim Soyisim</th>
         <th>Unvan</th>
         <th>Secenekler</th>

   </tr>
      {% for key1,requestid,name,surname,title in maindata3 %}
   <tr>

         <td>{{name}} {{surname}}</td>
         <td>{{title}}</td>
         <td>
         <form action="{{ url_for('baglantilar_page',personid=personid,requestid=requestid) }}" method="post" role="form" style="display: inline">
                     <input value="{{requestid}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteFriend" type="submit"  >Arkadasi Sil</button>
         </form>
         <form action="{{ url_for('baglantilar_guncelle',personid=personid,key1=key1,requestid=requestid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key1}}" name="id" type="hidden" />
                     <button class="btn btn-warning" name="UpdateFriend" type="submit"  >Arkadasi Guncelle</button>
         </form>
         </td>
         </tr>


         {% endfor %}
         </table>

Bu şekilde kullanıcının bütün bağlantıları veritabanından çekilerek gösterilmekte kullanıcı diğer fonksiyonları görünen
bağlantıları üzerinde uygulayabilmektedir.



PYTHON&POSTRGRESQL

.. code-block:: python

   connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        SELECT FRIENDLIST.FRIENDID,MAINDATA.ID,MAINDATA.NAME,MAINDATA.SURNAME,FRIENDLIST.TITLE FROM
        FRIENDLIST INNER JOIN MAINDATA ON FRIENDLIST.FRIENDID=MAINDATA.ID WHERE PERSONID=%s""",(personid,))
        backupmaindata3=cursor.fetchall()
        connection.commit()
        maindata3 = [(key1,requestid,name,surname,title)
                for key1,requestid,name,surname,title in cursor]

        return render_template('baglantilar.html',personid=personid,maindata=backupmaindata,maindata3=backupmaindata3,
        maindata4=backupmaindata4)

GUNCELLEME
----------

FriendList tablosunun Title isimli niteliği güncellenebilir,baglantilar.html sayfasının baglantilar kısmından güncellenebilmektedir.
Aşağıda FriendList tablosunun güncellenmesine yönelik kodlar bulunmaktadır.

 HTML:

.. code-block:: html

   <form action="{{ url_for('baglantilar_guncelle',personid=personid,key1=key1,requestid=requestid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key1}}" name="id" type="hidden" />
                     <button class="btn btn-warning" name="UpdateFriend" type="submit"  >Arkadasi Guncelle</button>
         </form>

baglantilar.html sayfasi baglantilar_guncelle() fonksiyonunu çağırarak güncelleme sayfasına yönlenir.

PYTHON&POSTRGRESQL

.. code-block:: python

   @app.route('/baglantilar/titleguncelle/<personid>,<requestid>', methods=['GET', 'POST'])
   def title_guncelle(personid,requestid):
         title=request.form['title']
         connection = dbapi2.connect(app.config['dsn'])
         cursor = connection.cursor()
         cursor.execute("""UPDATE FRIENDLIST SET TITLE=%s WHERE PERSONID= %s AND FRIENDID=%s""" ,(title,personid,requestid))
         connection.commit()

         return redirect(url_for('baglantilar_page',personid=personid))

baglantilar_guncelle() fonksiyonu, baglantilar.html aracılığıyla gönderilen varlık bilgisinin güncellenebilmesi için baglantilarupdate.html
sayfasını döndürür, yukarıdaki fonksiyonlardan da anlaşılabileceği gibi güncellenme operasyonu tamamlanır.

Baglantilar_Page() Fonksiyonu
=============================

Yukarıdaki kod bloklarında baglantılar_page fonksiyonu bloklar halinde gösterildi, Anlaşılabilirliğini kolaylaştırabileceği için
baglantilar_page() fonksiyonu aşağıda verilmiştir.

.. code-block:: python

   @app.route('/baglantilar/<personid>', methods=['GET', 'POST'])
   def baglantilar_page(personid):
    if request.method=='GET':
        connection=dbapi2.connect(app.config['dsn'])
        cursor=connection.cursor()
        cursor.execute("""SELECT * FROM MAINDATA WHERE %s!=MAINDATA.ID ORDER BY  EMAIL""",(personid))
        backupmaindata=cursor.fetchall()
        connection.commit()
        maindata = [(key,email,password,name,surname)
                for key,email,password,name,surname in cursor]





        connection=dbapi2.connect(app.config['dsn'])
        cursor=connection.cursor()
        cursor.execute("""SELECT FRIENDREQUEST.PERSONID,MAINDATA.NAME,MAINDATA.SURNAME
        FROM FRIENDREQUEST INNER JOIN MAINDATA ON FRIENDREQUEST.PERSONID=MAINDATA.ID WHERE REQUESTID=%s""",(personid))
        backupmaindata4=cursor.fetchall()
        connection.commit()
        maindata4=[(key2,name,surname)
                    for key2,name,surname in cursor]

        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        SELECT FRIENDLIST.FRIENDID,MAINDATA.ID,MAINDATA.NAME,MAINDATA.SURNAME,FRIENDLIST.TITLE FROM  FRIENDLIST INNER JOIN MAINDATA ON FRIENDLIST.FRIENDID=MAINDATA.ID WHERE PERSONID=%s""",(personid,))
        backupmaindata3=cursor.fetchall()
        connection.commit()
        maindata3 = [(key1,requestid,name,surname,title)
                for key1,requestid,name,surname,title in cursor]

        return render_template('baglantilar.html',personid=personid,maindata=backupmaindata,maindata3=backupmaindata3,maindata4=backupmaindata4)



    else:

      if 'AddRequest' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDREQUEST (PERSONID,REQUESTID)
            VALUES (%s, %s) """,
            (personid,key,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))
      elif 'DeleteRequest' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))
      elif 'AddFriend' in request.form:
            key = request.form['id']
            title=request.form['title']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID,TITLE)
            VALUES (%s, %s ,%s) """,
            (personid,key,title))
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID)
            VALUES (%s, %s) """,
            (key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

       elif 'DeleteFriend' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            DELETE FROM FRIENDLIST WHERE PERSONID=%s AND FRIENDID=%s
             """,
            (personid,key,))
            cursor.execute("""
            DELETE FROM FRIENDLIST WHERE PERSONID=%s AND FRIENDID=%s
             """,
            (key,personid,))

            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

      @app.route('/baglantilar/update/<personid>,<requestid>', methods=['GET', 'POST'])
      def baglantilar_guncelle(personid,requestid):



         return render_template('baglantilarupdate.html',personid=personid,requestid=requestid)


