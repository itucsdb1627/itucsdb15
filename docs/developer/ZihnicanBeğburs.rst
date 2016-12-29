#############################################
Zihni Beğburs Tarafından Gerçeklenen Kısımlar
#############################################

Profil Sayfası 3 tablodan oluşmaktadır. Bu tablolar Education, Experience ve Languages tablolarıdır.

3 tablo için de ekleme,silme,düzenleme ve arama işlemleri gerçekleştirilmiştir.

Bu tabloların oluşumda HTML, Python, PostgreSQL kodları kullanılmıştır. Bunun yanında redirect,request,url_for,render_template gibi flask uzantıları kullanılmıştır.

Arayüz için html'e ek olarak css ve javascript kullanılmıştır.

Site geneli için hazırlanan css layout bu sayfaya eklenmiştir.

.. code-block:: python

      {% extends "layout.html" %}

      {% endblock %}

Her tablonun fonksiyonları kendi adlarını taşıyan "education.py","experience.py","language.py" adlı dosyalarda yer almaktadır. Bütün bu Python sayfaları profil.py'a import edilerek "GET" ve "POST" metodlarına göre gerekli fonksiyonlar buradan çağrılmıştır.

Profil sayfası açıldığında profil.py'a gelen "GET" metodu  profil_page() fonksiyonuna giderek showeducation_page(),s howexperience_page, showlanguage fonksiyonlarını çağırır.

Not: profil_page() fonksiyonu sayfalardan gelen tüm isteklerin girip gerekli olan fonksiyona yönlendiği ana fonksiyondur bütün ekleme,silme,düzenleme ve arama işlemlerinde bu fonksiyona değinilecektir.

.. code-block:: python

   @app.route('/profil/<personid>', methods=['GET', 'POST'])
   def profil_page(personid):
       if request.method == 'GET':
           education = showeducation_page(personid)
           experience = showexperience_page(personid)
           language  = showlanguage(personid)
           return render_template('profil.html', education = education,experience=experience,language=language,personid=personid)

       else:

           if 'AddEducation' in request.form:
                   addeducation_page(personid)
                   return redirect(url_for('profil_page',personid=personid))

           elif 'DeleteEducation' in request.form:
                   deleteeducation_page(personid)
                   return redirect(url_for('profil_page',personid=personid))

           elif 'UpdateEducation' in request.form:
                   educationid=updateeducation_page(personid)
                   UpdateEducationValue = show_education_update_value(educationid);
                   return render_template('education_edit.html', key = educationid,personid=personid,UpdateEducationValue=UpdateEducationValue)

           elif 'SearchEducation' in request.form:
                   education=searcheducation_page(personid)
                   return render_template('profil.html',education = education,personid=personid)

           elif 'AddExperience' in request.form:
                   addexperience_page(personid)
                   return redirect(url_for('profil_page',personid=personid))

           elif 'DeleteExperience' in request.form:
                   deleteexperience_page(personid)
                   return redirect(url_for('profil_page',personid=personid))

           elif 'UpdateExperience' in request.form:
                   experienceid=updateexperience_page(personid)
                   UpdateExperienceValue=show_experience_update_value(experienceid)
                   return render_template('experience_edit.html', key = experienceid,personid=personid,UpdateExperienceValue=UpdateExperienceValue)

           elif 'SearchExperience' in request.form:
                   experience=searchexperience_page(personid)
                   return render_template('profil.html',experience = experience,personid=personid)

           elif 'AddLanguage' in request.form:
                   addlanguage(personid)
                   return redirect(url_for('profil_page',personid=personid))
           elif 'DeleteLanguage' in request.form:
                   deletelanguage(personid)
                   return redirect(url_for('profil_page',personid=personid))

           elif 'UpdateLanguage' in request.form:
                   languageid=updateexperience_page(personid)
                   UpdateLanguageValue=show_language_update_value(languageid)
                   return render_template('language_edit.html', key = languageid,personid=personid,UpdateLanguageValue=UpdateLanguageValue)

           elif 'SearchLanguage' in request.form:
                   language=searchlanguage(personid)
                   return render_template('profil.html',language = language,personid=personid)


Bu 3 fonksiyon da aynı şekilde kendi tablolarının tüm bilgileri çekmektedir. Aşağıda sadece showlanguage() fonksiyonunun tablodan veri çekmesi gösterilmiştir.

.. code-block:: python

   def showlanguage(personid):
           connection = dbapi2.connect(app.config['dsn'])
           cursor = connection.cursor()
           cursor.execute("""SELECT * FROM LANGUAGE WHERE PERSONID = %s """,[personid])
           connection.commit()
           language = [(key, LanguageName,Level,Personid )
                           for key, LanguageName, Level,Personid  in cursor]
           return language

Çekilen veriler profil sayfasına geri döndürülür.

.. code-block:: python

   return render_template('profil.html', education = education,experience=experience,language=language,personid=personid)

 Yukarıdaki kodla, çekilen verilen profil.html sayfasına aktarılır.


 Profil.html sayfasına gönderilen değerler aşağıdaki kodla kullanıcıya aktarılır. Bu kod sadece Education tablosu için gösterilmiştir. Diğer tablolar için de aynı metot kullanılmıştır.

.. code-block:: html

    {% for key, SchoolName, YearStart,YearEnd,Personid ,Gpa in education %}
         <tr>
            <td bgcolor="#F0F0F0" > {{ SchoolName }} </td>
            <td bgcolor="#F0F0F0"> {{ YearStart }} </td>
            <td bgcolor="#F0F0F0"> {{ YearEnd }} </td>
            <td bgcolor="#F0F0F0"> {{ Gpa }} </td>
            <td bgcolor="#F0F0F0">

            <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form" style="display: inline">
                        <input  value="{{key}}" name="id" type="hidden" />
                        <button class="btn btn-error" name="DeleteEducation" type="submit">Sil</button>
            </form>
            <form action="{{url_for('profil_page',personid=personid)}}" method="post" role="form" style="display: inline">
                        <input value="{{key}}" name="id" type="hidden" />
                        <button class="btn btn-warning" name="UpdateEducation" type="submit">Duzenle</button>
            </form>
            </td>
         </tr>
         </tbody>
      {% endfor %}



Education Tablosu
=================

Bu tablonun tüm ekle, çıkar , düzenle ve arama fonksiyonları education.py dosyasında bulunmaktadır.

Ekleme
------

Ekleme işlemi için "Yeni Okul Ekle & Ara" butonuna basılır ve aşağıdaki java Script kodu çalışır.

.. code-block:: javascript

   var div1 = document.getElementById('tecrubeDiv');
           div1.style.display = 'none';

          var div2 = document.getElementById('egitimDiv');
           div2.style.display = 'none';

          var div3 = document.getElementById('dilDiv');
           div3.style.display = 'none';

Bu kod ekleme formunun açılmasını sağlar. Bu form doldurulup ekleme butonuna basıldığında aşağıdaki kodla birlikte profil_page() fonksiyonuna "POST" metoduyla "AddEducation" isteği gönderilir.

.. code-block:: html

   <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form">

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek addeducation_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   if 'AddEducation' in request.form:
                   addeducation_page(personid)
                   return redirect(url_for('profil_page',personid=personid))

Aşağıdaki addeducation_page fonksiyonu ekleme işlemini gerçekleştirir.

.. code-block:: Python

   def addeducation_page(personid):
        SchoolName = request.form['SchoolName']
        YearStart = request.form['YearStart']
        YearEnd = request.form['YearEnd']
        Gpa = request.form['Gpa']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO EDUCATION (SCHOOLNAME, YEARSTART,YEAREND,PERSONID,GPA)
        VALUES (%s, %s, %s, %s, %s) """,
        (SchoolName, YearStart,YearEnd,personid ,Gpa))
        connection.commit()

 Bu işlemden sonra profil_page fonksiyonuna dönülür ve "GET" metoduyla profil.html sayfasına gidilir.

Silme
-----

Silme işlemi için silinmek istenen verinin hemen sağındaki "SİL" butonuna tıklandıktan sonra aşağıdaki kod profil_page sayfasına "POST" metoduyla DeleteEducation isteğini gönderir.

.. code-block:: html

   <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form" style="display: inline">
                        <input  value="{{key}}" name="id" type="hidden" />
                        <button class="btn btn-error" name="DeleteEducation" type="submit">Sil</button>
            </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek deleteeducation_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'DeleteEducation' in request.form:
                   deleteeducation_page(personid)
                   return redirect(url_for('profil_page',personid=personid))

Aşağıdaki deleteeducation_page() fonksiyonu silinmek istenen verinin "id" değerini alır ve silme işlemini gerçekleştirir.

.. code-block:: Python

   def deleteeducation_page(personid):
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM EDUCATION WHERE ID =%s """,[id])
            connection.commit()

Bu işlemden sonra profil_page fonksiyonuna dönülür ve "GET" metoduyla profil.html sayfasına gidilir.

Güncelleme
----------

Güncelleme işlemi için güncellenmek istenen verinin hemen sağındaki "Güncelle" butonuna tıklanmasıyla aşağıdaki kod profil_page sayfasına "POST" metoduyla UpdateEducation isteğini gönderir.

.. code-block:: html

   <form action="{{url_for('profil_page',personid=personid)}}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-warning" name="UpdateEducation" type="submit">Duzenle</button>
         </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek updateeducation_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'UpdateEducation' in request.form:
                educationid=updateeducation_page(personid)
                UpdateEducationValue = show_education_update_value(educationid);
                return render_template('education_edit.html', key = educationid,personid=personid,UpdateEducationValue=UpdateEducationValue)

Aşağıdaki updateeducation_page() fonksiyonu düzenlenmek istenen verinin "id" değerini çeker. Ayrıca show_education_update_value fonksiyonuyla güncellenmek istenen veri çekilir.

.. code-block:: Python

         def updateeducation_page(personid):
            educationid = request.form['id']
            return educationid

Çekilen bu veriler education_edit.html sayfasına gönderilir. Kullanıcı burada düzenlemeyi yapar ve "Düzenle" butonuna basarak "POST" metoduyla aşağıdaki edit_education fonksiyonunu çağırarak güncelleme işlemini tamamlar.

.. code-block:: Python

   def edit_education(educationid,personid):
    if request.method == 'GET':
        return render_template('education_edit.html')
    else:
         if 'Update' in request.form:
             SchoolName = request.form['SchoolName']
             YearStart = request.form['YearStart']
             YearEnd = request.form['YearEnd']
             Gpa = request.form['Gpa']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE EDUCATION SET SCHOOLNAME = %s, YEARSTART= %s,YEAREND= %s, GPA= %s WHERE ID = %s """,
             (SchoolName, YearStart,YearEnd, Gpa, educationid))
             connection.commit()
             return redirect(url_for('profil_page',personid=personid))

Arama
-----

Arama formunda aranmak istenen değer girildikten sonra arama butonuna basıldığında aşağıdaki kodla birlikte profil_page() fonksiyonuna "POST" metoduyla "SearchEducation" isteği gönderilir.

.. code-block:: Python

   <form action ="{{url_for('profil_page',personid=personid)}}" method="post">
         <b>Okul Ara:</b><br>
         <input type="text" style="color:black" name="SchoolName">&nbsp
         <input class="btn btn-primary" type="submit" value="Ara" name="SearchEducation">
      </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek searcheducation_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'SearchEducation' in request.form:
                education=searcheducation_page(personid)
                return render_template('profil.html',education = education,personid=personid)

Aşağıdaki searcheducation_page() fonksyionu arama işlemini tamamlar ve bulunan değeri profil_page() fonksiyonuna döndürür. Daha sonra profil.html sayfasına bulunan değer gönderilerek kullanıcıya gösterilir.

.. code-block:: Python

      def searcheducation_page(personid):
            SchoolName = request.form['SchoolName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EDUCATION WHERE SCHOOLNAME LIKE %s",(SchoolName,))
            connection.commit()
            education = [(key, SchoolName,YearStart,YearEnd,personid ,Gpa)
                        for key, SchoolName, YearStart,YearEnd,personid , Gpa in cursor]
            return education

Experience Tablosu
==================

Bu tablonun tüm ekle, çıkar , düzenle ve arama fonksiyonları experience.py dosyasında bulunmaktadır.

Ekleme
------

Ekleme işlemi için "Yeni Şirket Ekle & Ara" butonuna basılır ve aşağıdaki java Script kodu çalışır.

.. code-block:: javascript

   var button2 = document.getElementById('button2');
       button2.onclick = function() {
             var div = document.getElementById('tecrubeDiv');
             if (div.style.display !== 'none') {
                 div.style.display = 'none';
             }
             else {
                 div.style.display = 'block';
             }
         };

Bu kod ekleme formunun açılmasını sağlar. Bu form doldurulup ekleme butonuna basıldığında aşağıdaki kodla birlikte profil_page() fonksiyonuna "POST" metoduyla "AddExperience" isteği gönderilir.

.. code-block:: html

   <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form">

Gelen istek profil_page() fonkyionunda aşağıdaki koşula girerek addeducation_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'AddExperience' in request.form:
                addexperience_page(personid)
                return redirect(url_for('profil_page',personid=personid))

Aşağıdaki addexperience_page fonksiyonu ekleme işlemini gerçekleştirir.

.. code-block:: Python

   def addexperience_page(personid):
        CompanyName = request.form['CompanyName']
        YearStart = request.form['YearStart']
        YearEnd = request.form['YearEnd']
        Position = request.form['Position']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO EXPERIENCE (COMPANYNAME, YEARSTART,YEAREND,POSITION,PERSONID)
        VALUES (%s, %s, %s,%s, %s) """,
        (CompanyName, YearStart,YearEnd,Position,personid ))
        connection.commit()

 Bu işlemden sonra profil_page fonksiyonuna dönülür ve "GET" metoduyla profil.html sayfasına gidilir.

Silme
-----

Silme işlemi için silinmek istenen verinin hemen sağındaki "SİL" butonuna tıklanmasıyla aşağıdaki kod profil_page sayfasına "POST" metoduyla DeleteExperience isteğini gönderir.

.. code-block:: html

   <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteExperience" type="submit">Sil</button>
         </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek deleteexperience_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'DeleteExperience' in request.form:
                deleteexperience_page(personid)
                return redirect(url_for('profil_page',personid=personid))

Aşağıdaki deleteexperience_page() fonksiyonu silinmek istenen verinin "id" değerini alır ve silme işlemini gerçekleştirir.

.. code-block:: Python

   def deleteexperience_page(personid):
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM EXPERIENCE WHERE ID =%s """,[id])
            connection.commit()

Bu işlemden sonra profil_page fonksiyonuna dönülür ve "GET" metoduyla profil.html sayfasına gidilir.

Güncelleme
----------

Güncelleme işlemi için güncellenmek istenen verinin hemen sağındaki "Güncelle" butonuna tıklanmasıyla aşağıdaki kod profil_page sayfasına "POST" metoduyla UpdateExperience isteğini gönderir.

.. code-block:: html

   <form action="{{url_for('profil_page',personid=personid)}}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-warning" name="UpdateExperience" type="submit">Duzenle</button>
         </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek updateexperience_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'UpdateExperience' in request.form:
                experienceid=updateexperience_page(personid)
                UpdateExperienceValue=show_experience_update_value(experienceid)
                return render_template('experience_edit.html', key = experienceid,personid=personid,UpdateExperienceValue=UpdateExperienceValue)

Aşağıdaki updateexperience_page() fonksiyonu düzenlenmek istenen verinin "id" değerini çeker. Ayrıca show_experience_update_value() fonksiyonuyla güncellenmek istenen veri çekilir.

.. code-block:: Python

         def updateexperience_page(personid):
            experience = request.form['id']
            return experience

Çekilen bu veriler experience_edit.html sayfasına gönderilir. Kullanıcı burada düzenlemeyi yapar ve "Düzenle" butonuna basarak "POST" metoduyla aşağıdaki edit_experience fonksiyonunu çağırarak güncelleme işlemini tamamlar.

.. code-block:: Python

   def edit_experience(experienceid,personid):
    if request.method == 'GET':
        return render_template('experience_edit.html')
    else:
         if 'UpdateExperience' in request.form:
             SchoolName = request.form['CompanyName']
             YearStart = request.form['YearStart']
             YearEnd = request.form['YearEnd']
             Position = request.form['Position']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE EXPERIENCE SET COMPANYNAME = %s, YEARSTART= %s,YEAREND= %s,POSITION= %s WHERE ID = %s """,
             (SchoolName, YearStart,YearEnd,Position, experienceid))
             connection.commit()
             return redirect(url_for('profil_page',personid=personid))

Arama
-----

Arama formunda aranmak istenen değer girildikten sonra arama butonuna basıldığında aşağıdaki kodla birlikte profil_page() fonksiyonuna "POST" metoduyla "SearchExperience" isteği gönderilir.

.. code-block:: Python

   <form action ="{{url_for('profil_page',personid=personid)}}" method="post">
         <b>Sirket Ara:</b><br>
         <input type="text" style="color:black" name="CompanyName">&nbsp
         <input class="btn btn-primary" type="submit"  value="Ara" name="SearchExperience">
      </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek searchexperience_page(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'SearchExperience' in request.form:
                experience=searchexperience_page(personid)
                return render_template('profil.html',experience = experience,personid=personid)

Aşağıdaki searchexperience_page() fonksiyonu arama işlemini tamamlar ve bulunan değeri profil_page() fonksiyonuna döndürür. Daha sonra profil.html sayfasına bulunan değer gönderilerek kullanıcıya gösterilir.

.. code-block:: Python

      def searchexperience_page(personid):
            CompanyName = request.form['CompanyName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EXPERIENCE WHERE COMPANYNAME LIKE %s",(CompanyName,))
            connection.commit()
            experience = [(key, CompanyName,YearStart,YearEnd,Position,personid )
                        for key, CompanyName, YearStart,YearEnd,Position,personid  in cursor]
            return experience

Language Tablosu
================

Bu tablonun tüm ekle, çıkar , düzenle ve arama fonksiyonları language.py dosyasında bulunmaktadır.

Ekleme
------

Ekleme işlemi için "Yeni Dil Ekle & Ara" butonuna basılır ve aşağıdaki java Script kodu çalışır.

.. code-block:: javascript

   var button3 = document.getElementById('button3');
          button3.onclick = function() {
                var div = document.getElementById('dilDiv');
                if (div.style.display !== 'none') {
                    div.style.display = 'none';
                }
                else {
                    div.style.display = 'block';
                }
            };

Bu kod ekleme formunun açılmasını sağlar. Bu form doldurulup ekleme butonuna basıldığında aşağıdaki kodla birlikte profil_page() fonksiyonuna "POST" metoduyla "AddEducation" isteği gönderilir.

.. code-block:: html

   <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form">

Gelen istek profil_page() fonkysiyonunda aşağıdaki koşula girerek addlanguage(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'AddLanguage' in request.form:
                addlanguage(personid)
                return redirect(url_for('profil_page',personid=personid))

Aşağıdaki addlanguage() fonksiyonu ekleme işlemini gerçekleştirir.

.. code-block:: Python

   def addlanguage(personid):
        LanguageName = request.form['LanguageName']
        Level = request.form['Level']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO LANGUAGE (LANGUAGENAME, LEVEL,PERSONID)
        VALUES (%s, %s, %s) """,
        (LanguageName, Level,personid ))
        connection.commit()

 Bu işlemden sonra profil_page fonksiyonuna dönülür ve "GET" metoduyla profil.html sayfasına gidilir.

Silme
-----

Silme işlemi için silinmek istenen verinin hemen sağındaki "SİL" butonuna tıklanmasıyla aşağıdaki kod profil_page sayfasına "POST" metoduyla DeleteLanguage isteği gönderilir.

.. code-block:: html

   <form action="{{ url_for('profil_page',personid=personid) }}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-error" name="DeleteLanguage" type="submit">Sil</button>
         </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek deletelanguage(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'DeleteLanguage' in request.form:
                deletelanguage(personid)
                return redirect(url_for('profil_page',personid=personid))

Aşağıdaki deletelanguage() fonksiyonu silinmek istenen verinin "id" değerini alır ve silme işlemini gerçekleştirir.

.. code-block:: Python

   def deletelanguage(personid):
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM LANGUAGE WHERE ID =%s """,[id])
            connection.commit()

Bu işlemden sonra profil_page fonksiyonuna dönülür ve "GET" metoduyla profil.html sayfasına gidilir.

Güncelleme
----------

Güncelleme işlemi için güncellenmek istenen verinin hemen sağındaki "Güncelle" butonuna tıklanmasıyla aşağıdaki kod profil_page sayfasına "POST" metoduyla UpdateLanguage isteğini gönderir.

.. code-block:: html

   <form action="{{url_for('profil_page',personid=personid)}}" method="post" role="form" style="display: inline">
                     <input value="{{key}}" name="id" type="hidden" />
                     <button class="btn btn-warning" name="UpdateLanguage" type="submit">Duzenle</button>
         </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek updatelanguage(personid) fonksiyonunu çağırır.

.. code-block:: Python

   elif 'UpdateLanguage' in request.form:
                languageid=updatelanguage(personid)
                UpdateLanguageValue=show_language_update_value(languageid)
                return render_template('language_edit.html', key = languageid,personid=personid,UpdateLanguageValue=UpdateLanguageValue)

Aşağıdaki updatelanguage() fonksiyonu düzenlenmek istenen verinin "id" değerini çeker. Ayrıca show_language_update_value() fonksiyonuyla güncellenmek istenen veri çekilir.

.. code-block:: Python

         def updatelanguage(personid):
            language = request.form['id']
            return language

Çekilen bu veriler language_edit.html sayfasına gönderilir. Kullanıcı burada düzenlemeyi yapar ve "Duzenle" butonuna basarak "POST" metoduyla aşağıdaki edit_language fonksiyonunu çağırarak güncelleme işlemini tamamlar.

.. code-block:: Python

   def edit_language(languageid,personid):
    if request.method == 'GET':
        return render_template('language_edit.html')
    else:
         if 'UpdateLanguage' in request.form:
             LanguageName = request.form['LanguageName']
             Level = request.form['Level']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE LANGUAGE SET LANGUAGENAME = %s, LEVEL= %s WHERE ID = %s """,
             (LanguageName, Level, languageid))
             connection.commit()
             return redirect(url_for('profil_page',personid=personid))

Arama
-----

Arama formunda aranmak istenen değer girildikten sonra arama butonuna basıldığında aşağıdaki kodla birlikte profil_page() fonksiyonuna "POST" metoduyla "SearchLanguage" isteği gönderilir.

.. code-block:: Python

   <form action ="{{url_for('profil_page',personid=personid)}}" method="post">
         <b>Dil Ara:</b><br>
         <input type="text" style="color:black" name="LanguageName">&nbsp
         <input class="btn btn-primary" type="submit"  value="Ara" name="SearchLanguage">
      </form>

Gelen istek profil_page() fonksiyonunda aşağıdaki koşula girerek searchlanguage(personid) fonksiyonunu çağırır.

.. code-block:: Python

    elif 'SearchLanguage' in request.form:
                language=searchlanguage(personid)
                return render_template('profil.html',language = language,personid=personid)

Aşağıdaki searchlanguage() fonksiyonu arama işlemini tamamlar ve bulunan değeri profil_page() fonksiyonuna döndürür. Daha sonra profil.html sayfasına bulunan değer gönderilerek kullanıcıya gösterilir.

.. code-block:: Python

      def searchlanguage(personid):
            LanguageName = request.form['LanguageName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM LANGUAGE WHERE LANGUAGENAME LIKE %s",(LanguageName,))
            connection.commit()
            language = [(key, LanguageName,Level,personid )
                        for key, LanguageName, Level,personid  in cursor]
            return language