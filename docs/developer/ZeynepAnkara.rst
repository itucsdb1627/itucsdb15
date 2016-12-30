#############################################
Zeynep Ankara Tarafından Oluşturulan Bölümler
#############################################

Bu bölümde, kullanıcının iş ilanlarıyla ilgili işlemler yapılmaktadır. Bu sayfa için bir tane tablo kullanılmıştır. Bu tablo üzerinden gerçekleştrilmek istenen işlemler fonksiyonlara sayesinde erişilmektedir. Tablo ile ilgili bu işlemler burada anlatılacaktır.  Sayfada bulunanan genel anlamda üç bölüm için; HTML kodları CSS ler ve Bootstap formlar, tablolar, butonlar ve redirect, request, url_for, render_template gibi Flask uzantıları ve  PostgreSQL+Python olan psycopg2 paketi kullanılmıştır.

İşler sayfası için network.html sayfası oluşturulmuştur. Kullanıcının güncelleme yapabilmesi için ise; network_edit.html sayfası oluşturulmuştur. 


Network.HTML Sayfası
=====================

Kullanıcı bu sayfaya anasayfada yer alan "İşler" alanına tıklayarak ulaşır. 

Kullanıcı bu sayfaya ulaşırken; parametre olarak personid ile geçiş yapabilmektedir. Sayfaya ulaşabilmek için aşağıdaki kod yazılmıştır. 

		..code-block::html
		
		<li> <a href="{{ url_for('network_page',personid=personid) }}">İşler</a> </li>
		
		
		
Sayfaya giriş yapan kullanıcının işlem yapabileceği tablo için network tablosu oluşturulmuştur. Tabloda beş adet nitelik bulunmaktadır. Bunlar; "id", "il", "sektor", "sirket" ve Maindata tablosundan çekilen "personid" dir. 
Network tablosu ile yapılan işlemler için network.py dosyası oluşturulmuştur. Network tablosunun oluşmasını sağlayan SQL kodları aşağıdaki gibidir:

		
		..code-block::sql
		  
		CREATE TABLE IF NOT EXISTS NETWORK (
    	ID SERIAL PRIMARY KEY,
    	IL VARCHAR(90),
    	SIRKET VARCHAR(30) NULL,
    	PERSONID INTEGER,
    	SEKTOR VARCHAR(30) NULL,
    	FOREIGN KEY (PERSONID)
    	REFERENCES MAINDATA (ID)
    	ON DELETE CASCADE)  
    	
Sayfaya giriş yapıldığında kullanıcı; daha önce verdiği ilanları görebileceği bir tablo ile karşılaşır. Bu tabloda network tablosundan çekilen; il, sektor, sirket bilgilerini ve personid dış anahtarı ile Maindata tablosundan erişilen "name" bilgisi ve Educatin tablosundan erişilen "schoolname" bilgilerini görebilir. Kullanıcya ait olan bu tablo aşağıdaki HTML kodları ile oluşturulmuştur. 

		
		..code-block::html
		
	1	<table class="table-style-two">
	2	<tr>
	3	    <th>Il</th>
	4	    <th>Sırket</th>
	5	    <th>Sektor</th>
	6	    <th>Okul Adı</th>
	7	    <th>Adı</th>
	8	    <th>Processes</th>
	9	 </tr>
	10	{% for key, Il, Sırket,Personid ,Sektor, SchoolName,FirstName in network %}
	11	<tr>
	12		<td> {{ Il }} </td>
	13		<td> {{ Sırket }} </td>
	14		<td> {{ Sektor }} </td>
	15		<td> {{ SchoolName }} </td>
	16		<td> {{ FirstName }} </td>
	17		<td>
	18		<form action="{{ url_for('network_page',personid=personid) }}" method="post" role="form" style="display: inline">
	19						<input value="{{key}}" name="id" type="hidden" />
	20						<button class="btn btn-default" name="Delete" type="submit">Sil</button>
	21		</form>
	22		<form action="{{url_for('network_page',personid=personid)}}" method="post" role="form" style="display: inline">
	23						<input value="{{key}}" name="id" type="hidden" />
	24						<button class="btn btn-default" name="Update" type="submit">Duzenle</button>
	25		</form>
	26		</td>
	27	</tr>
	28	{% endfor %}
	29	</table>
 
 
Tablo oluşturulurken 1. satırda CSS kullanılmıştır. Tablonun başlıklarını belirleyen satırlar 3-8 arasında yer almaktadır. 10. satırda; kullanıcının her bir ilanı için tabloya yerleştirme işlemi yapması istendiği için for döngüsü kullanılmak üzere açılmış ve bu döngü 28. satırda kapatılmıştır. Bu sayede kullanıcının network tablosuna kayıtlı bütün verileri listelenebilmektedir. Network  tablosundan 12,13 ve 14. satırlarda il, sirket ve sektor bilgileri çekilirken, education tablosundan 15. satırda bulunan schoolname ve 16. satırda bulunan name bilgisi de maindata tablosundan çekilmektedir. 18 ve 22 satırlarda kullanıcının silme ve güncelleme işlemi yapabilmesi için her bir varlık için buton eklenmiştir.
Tabloda kullanılan CSS aşağıdaki gibidir. 

		
		
		..code-block::css
		
		table.table-style-two {
		font-family: verdana, arial, sans-serif;
		font-size: 11px;
		color: #333333;
		border-width: 1px;
		border-color: #3A3A3A;
		border-collapse: collapse;
		}
 
		table.table-style-two th {
		border-width: 1px;
		padding: 8px;
		border-style: solid;
		border-color: #517994;
		background-color: #B2CFD8;
		}
 
		table.table-style-two tr:hover td {
		background-color: #DFEBF1;
		}
 
		table.table-style-two td {
		border-width: 1px;
		padding: 8px;
		border-style: solid;
		border-color: #517994;
		background-color: #ffffff;
		}
		

Bu kodlar ile; tablonun yazı tipi, karakter büyüklüğü, satır/sutun genişliği ve rengi belirlenmiştir. 


Sayfanın diğer bir bölümü ise yukarıda anlattılan tablonun altında yer almaktadır. Bu alan; kullanıcının network tablosuna veri ekleyebilmesi için tasarlanmıştır ve Bootstrap kullanılarak bir form oluşturulmuştur. 


		..code-block::html
		
		<!-- FORM SECTION -->
     		     <div class="col-sm-7">
            	 <div class="login-sec"> 
              
              		<!-- TABS -->
              		<div class="uou-tabs">
					<li class="active"><a href="#log-in">Oluşturmak İstediğiniz İlan İle İlgili Bilgiler</a></li>
					<form action="{{ url_for('network_page',personid=personid) }}" name="zeynepForm"  method="post" role="form" onsubmit="return(validate());">
						<!-- LOGIN -->
                  		<div id="log-in" class="active">
                    		<form>
					
				  				<input type="text" name="Sirket" placeholder="Şirket Adı"  autofocus />
			        			<input type="text" name="Sektor" placeholder="Sektör Bilgisi"  autofocus />
                    			<input type="text" name="Il" placeholder="Şehir"  autofocus />
            					<button name="Add" type="submit" >Kaydet</button>
							</form>
	 					</div>
					</div>
              	</div>
            </div>
            
          </div>
          
   		<section class="pro-mem">
    	<div class="container pb30">   
    	

Bu kod bloğu ile kullanıcının veri girebilmesi düşülmüştür. 12. satırda sirket, 13.satırda sektor, 14. satırda ise il bilgisini girebilmesi için kullanıcıya text alanları oluşturulmuştur. 15. satırda yer alan buton ise "Add" fonsiyonunu çağırmaktadır.   Bu işlem sonrasında form "POST" edildiğinde "validate()" adlı bir javascript kodu ile alanların boş geçilmemesi için mesaj verilmiştir. İlgili JavaScript kodu aşağıdaki gibidir. 


		..code-block:: javascript 
		
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js">

		<script type="text/javascript">
		function validate() {
	
			if (document.zeynepForm.Sirket.value=="") {
			alert('Şirket alanı bos birakilamaz')
			return false;
			}
			if (document.zeynepForm.Sektor.value=="") {
			alert('Sektör alanı bos birakilamaz')
			return false;
			}
			if (document.zeynepForm.Il.value=="") {
			alert('İl alanı bos birakilamaz')
			return false;
			}
			return true;
			}
		</script>
		
		

Yukarıdaki kod ile; kullanıcının boş veri girişi yapması engellenmiştir. 


Sayfanın en alt kısmında yer alan ve diğer kullanıcıların da eklediği ilanları listelememizi sağlayan alan için kullanılan HTML kodlar aşağıdaki gibidir. 


		..code-block::hmtl

		 <h3>İş İlanları </h3>
      		{% for key, Il, Sırket, Personid , Sektor, SchoolName,FirstName in network2 %}
     		 <div class="row">
        		<div   class="col-sm-3">
          			<div class="uou-block-6a"> 
            			<h6>  {{ Sırket }}  <span>  {{ Sektor }} </span></h6>
            			<p><i class="fa fa-map-marker"></i> {{ Il }} </p>
          			</div>
	    		</div>
    		{% endfor %}    
        	</div>


Bu kod bloğu; için yeni bir connection oluştururak sayfanın üst bölümünde yer alan tablonun connection işleminin çakışmaması sağlanmıştır. Bootstrap formu kullanılmış ve kullanıcıların yanlızca network tablosundaki bilgileri birerküçük container şeklinde sıralanmıştır. Bu işlemi yapabilmek için ise; yerleştirme işlemi for döngüsü içinde yapılmıştır. Bu panel üzerinde kullanıcının ilanın üzerine geldiğinde; görselliğin değişmesi amacıyla jquery kullanılmıştır. Kodları aşağıdaki gibidir. 


		..code-block::jquery 
		
		<script>
		$(document).ready(function(){
    	$(".uou-block-6a").hover(function(){
        $(this).css("background-color", "#808080");
        }, function(){
        $(this).css("background-color", "white");
    	});
		});
		</script>
		

Bu kod bloğu ile; kullanıcı "uou-block-6a" ile ifade edilen alana geldiğinde arka planın değişmesi ve sayfaya görsellik katması amaçlanmıştır. 

Network.html sayfasına girildiğinde network.py dosyasına yönelendirilir. "GET" metodu oluşunca sayfada yer alması istenen veriler tablolardan çekilerek kullanıcı için; yukarıda anlatılan tabolaların doldurulması sağlanır, "POST" metodu oluşursa isteklere bağlı olarak ilgili işlem döndürülür ve sayfaya uygulanır.


		..code-block::python
		
		@app.route('/network/<personid>', methods=['GET', 'POST'])
		def network_page(personid):
    	if request.method == 'GET':
        	connection = dbapi2.connect(app.config['dsn'])
        	cursor = connection.cursor()
        	cursor.execute("""select distinct a.*,b.schoolname,c.name from network a, education b,maindata c where a.personid=b.personid and  c.id=a.personid and  a.PERSONID = %s """,[personid])
        	connection.commit()
        	network = [(key, Il,Sirket,Personid ,Sektor, SchoolName,FirstName)
                        for key, Il,Sirket,Personid ,Sektor, SchoolName,FirstName in cursor]
        
        	connection2 = dbapi2.connect(app.config['dsn'])
        	cursor2 = connection2.cursor()
        	cursor2.execute("""select distinct a.*,b.schoolname,c.name from network a, education b,maindata c where a.personid=b.personid and  c.id=a.personid """)
        	connection2.commit()
        	network2 = [(key, Il,Sirket,Personid ,Sektor, SchoolName,FirstName)
                        for key, Il,Sirket,Personid ,Sektor, SchoolName,FirstName in cursor2]
        
        	return render_template('network.html', network = network,network2=network2,personid=personid)
        
        
    	else:
        if 'Add' in request.form:
            Il = request.form['Il']
            Sirket = request.form['Sirket']
            Sektor = request.form['Sektor']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO NETWORK (IL, SIRKET,SEKTOR, PERSONID)
            VALUES (%s, %s, %s, %s) """,
            (Il,Sirket,Sektor,personid))
            connection.commit()   
            return redirect(url_for('network_page',personid=personid))
        
        elif 'Delete' in request.form:
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM NETWORK WHERE ID =%s """,[id])
            connection.commit()   
            return redirect(url_for('network_page',personid=personid))
        elif 'Update' in request.form:
            networkid = request.form['id']
            return render_template('network_edit.html', key = networkid,personid=personid)
        elif 'Search' in request.form:
            Il = request.form['Il']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM NETWORK WHERE IL LIKE %s",(Il,))
            connection.commit() 
            network = [(key, Il,Sirket,Personid ,Sektor)
                        for key, Il,Sirket,Personid ,Sektor in cursor]
            return render_template('network.html',network = network,personid=personid)
		 

Network Tablosu
===============


Bu tabloya ait ekleme, silme, güncelleme işlemleri network.py üzerinden gerçekleşir. 


Ekleme
------

Ekleme işlemi için; sayfada bulunan "Kaydet" butonu tıklanır. Eğer verilerin hepsi eksiksiz girildiyse (girilmediği durumda JavaScript ile alanların boş geçilemeyeceği uayarı verilir ve bu kod yukarıda incelenmiştir.) "Add" isteği oluşur ve network_page fonksiyonuna yönlendirilir. Bu işlemi yapan kod; 


		..code-block:: hmtl

		<form action="{{ url_for('network_page',personid=personid) }}" name="zeynepForm"  method="post" role="form" onsubmit="return(validate());">
		
Network_page e yönlendirildikten sonra; verileri tabloya eklenmesi aşağaıdaki kod ile geröekleşir. 

		..code-block:: python
		
		 if 'Add' in request.form:
            Il = request.form['Il']
            Sirket = request.form['Sirket']
            Sektor = request.form['Sektor']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO NETWORK (IL, SIRKET,SEKTOR, PERSONID)
            VALUES (%s, %s, %s, %s) """,
            (Il,Sirket,Sektor,personid))
            connection.commit()   
            return redirect(url_for('network_page',personid=personid))

Böylelikle network tablosuna yeni bir valık eklenmiş olur. 


Silme
------

Silme işlemi için; sayfada bulunan tabloda yer alan "Sil" butonuna tıklamak gerekir. Bu buton tıklandığı durumda "Delete" isteiği oluşur ve tekrar netwrok_page fonskiyonuna gönderilir. Silme işlemini gerçekleştiren kod aşağıdaki gibidir. 


		..code-block:: python 
		
		 elif 'Delete' in request.form:
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM NETWORK WHERE ID =%s """,[id])
            connection.commit()   
            return redirect(url_for('network_page',personid=personid))
            
            
Güncelleme
-------

Güncelleme işlemi için; sayfada bulunan tabloda yer alan "Düzenle" butonuna tıklamak gerekir. Bu buton tıklandığı durumda "Update" isteiğini oluşturur ve network_page fonsiyonuna yönelendirlir. Bu yönelendisirlme doğrutusunda güncelleme işlemini yapabilmek için network_edit.html(network_edit.html sayfası aşağıda anlatılmıştır.) sayfasına yönlendirilme yapılır.  


		..code-block:: python 
		
		elif 'Update' in request.form:
            networkid = request.form['id']
            return render_template('network_edit.html', key = networkid,personid=personid)

            
Yukarıdaki kod ile network_edit.html sayfasına yönlendirilme gerçekleşir. 

Güncelleme işlemi gerçekleşebilmesi için; network_edit.html sayfasında gerekli değişiklikler yapılır ve "Kaydet" butonuna tıklanır. Böyle olduğunda network.html sayfasına yönlendirilmiş oluruz. Bu değişiklikleri yapan kod aşağıdaki gibidir. 


		..code-block:: python 
		
		@app.route('/network/editnetwork/<networkid>,<personid>', methods=['GET', 'POST'])
		def edit_network(networkid,personid):
   			if request.method == 'GET': 
        	return render_template('network_edit.html')
    	else:
         if 'Update' in request.form:
             Il = request.form['Il']
             Sirket = request.form['Sirket']
             Sektor = request.form['Sektor']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE NETWORK SET IL = %s, SIRKET= %s, SEKTOR= %s WHERE ID = %s """,
             (Il,Sirket,Sektor , networkid))
             connection.commit()   
             return redirect(url_for('network_page',personid=personid))
             

Network_edit.HTML
===================

Bu sayfa kullanıcının güncelleme yapması için oluşturulmuştur. Yanlızca network tablosuna güncelleyeceği alanları girebileceği alanlar yer almaktadır. Kullanıcı yukarıda anlatılmış olan kendine ait bilgilerin yer aldığı tablodan "Düzenle" btuonuna tıklaığından gerekli yönlendirme ile bu sayfaya ulaşır. Sayfa için kullanılan kod aşağıda verilmiştir. 


		..code-block:: html 
		
		<!-- FORM SECTION -->
     		     <div class="col-sm-7">
            	 <div class="login-sec"> 
              
              		<!-- TABS -->
              		<div class="uou-tabs">
					<li class="active"><a href="#log-in">Bilgileri Düzenle...</a></li>
					
						<form action="{{url_for('edit_network', networkid=key,personid=personid)}}" method="post" role="form">
						<!-- LOGIN -->
                  		<div id="log-in" class="active">
                    		<form>
								<input type="text" name="Il" placeholder="Şehir	" required autofocus />
			        			<input type="text" name="Sirket" placeholder="Şirket" required autofocus />
                    			<input type="text" name="Sektor" placeholder="Sektör" required autofocus />
            					<button name="Update" type="submit">Kaydet</button>
							</form>
							
			
					</div>
              	</div>
            </div>
            </div>
            
            

13, 14 ve 15. satırlarda kullanıcının herhangi bir alanı boş geçmemesi için uyarı verilmesi sağlanmıştır. 


