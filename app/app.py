
from flask import Flask, render_template, request
import mysql.connector
from waitress import serve

def dbConnect():
    con = mysql.connector.connect(
        host="db_1",
        user="user",
        passwd="password",
        database="CCLoanLaptops")

    return con



def GetDateTime(delta):
        from time import gmtime, strftime, localtime
        import datetime
        dateToday = (strftime("%Y-%m-%d", localtime()))
        timeNow = (strftime("%H:%M:%S", localtime()))
        today = datetime.datetime.now()
        DD = datetime.timedelta(days= delta)
        earlier = today - DD
        earlier_str = earlier.strftime("%Y-%m-%d")

        return timeNow, dateToday, earlier_str

app = Flask(__name__)

@app.route('/alllist')
def list():
   con = dbConnect()
    
   cur = con.cursor(dictionary=True)

   cur.execute("select * from LoanedLaptops ORDER BY ID DESC ")
   
   rows = cur.fetchall()

   con.close()
   return render_template("alllist.html",rows = rows)

@app.route('/')
def loanedlist():
   con = dbConnect()
  
   
   cur = con.cursor(dictionary=True)

   cur.execute("select * from LoanedLaptops where ReturnedBy = 'Null'")
   
   rows = cur.fetchall()

   con.close()
   return render_template("loanedlist.html",rows = rows)

@app.route('/search', methods=['GET', 'POST'])

def search():
    count = 0 
    if request.method == "POST":
        
        details = request.form
        assetTag = details['assetTag']
        #assetTag = 'Null'
        con = dbConnect()
        cur = con.cursor(dictionary=True)
        cur.execute("select * from LoanedLaptops where assetTag = %s or CCassetTag = %s order by ID DESC",(assetTag,assetTag))
        rows = cur.fetchall()

        return render_template("search.html",rows = rows)
        con.close()
            
    else:
        return render_template("search.html")
        con.close()



@app.route('/assetoutgoing', methods=['GET', 'POST'])

def resultOut():
    import noUI
    if request.method=='POST':
        result = request.form
        customerNameOut=result['customerNameOut']
        staffNameOut=result['staffNameOut']
        laptopAssetTagOut=result['laptopAssetTagOut']

        noUI.SaveOutgoing(customerNameOut, staffNameOut, laptopAssetTagOut)   
        return render_template('assetoutgoing.html', result = result)  
    else:
        return render_template('assetoutgoing.html')

@app.route('/assetincoming', methods=['GET', 'POST'])

def resulIn():
    import noUI
    if request.method=='POST':
        result = request.form
        customerNameIn=result['customerNameIn']
        staffNameIn=result['staffNameIn']
        laptopAssetTagIn=result['laptopAssetTagIn']

        noUI.SaveIncoming(customerNameIn, staffNameIn, laptopAssetTagIn)     
        return render_template('assetincoming.html', result = result)
    else:
        return render_template('assetincoming.html')



@app.route('/alllist-1')
def list1():
      
   DateToday = GetDateTime(0)
   var1 = (DateToday[1])
   var2 = "'"+var1+"'"
   con = dbConnect()
  
   
   cur = con.cursor(dictionary=True)
   query = "select * from LoanedLaptops where DateBorrowed = " + var2 + " ORDER BY ID DESC"

   cur.execute(query)
   
   rows = cur.fetchall()

   return render_template("alllist-1.html",rows = rows)


@app.route('/alllist-7')
def list7():

   DateToday = GetDateTime(7)
   var1 = (DateToday[2])
   var2 = (DateToday[1])
   var3 = "'"+var1+"'"
   var4 = "'"+var2+"'"
   con = dbConnect()

   cur = con.cursor(dictionary=True)


   query = "SELECT * from LoanedLaptops where DateBorrowed BETWEEN " + var3 + " AND " + var4 +" ORDER BY ID DESC"
   
   cur.execute(query)

   rows = cur.fetchall()

   return render_template("alllist-7.html", rows=rows)


@app.route('/alllist-30')
def list30():


   DateToday = GetDateTime(30)
   var1 = (DateToday[2])
   var2 = (DateToday[1])
   var3 = "'"+var1+"'"
   var4 = "'"+var2+"'"

   con = dbConnect()

   cur = con.cursor(dictionary=True)

   query = "SELECT * from LoanedLaptops where DateBorrowed BETWEEN " + var3 + " AND " + var4 +" ORDER BY ID DESC"

   cur.execute(query)
   rows = cur.fetchall()

   return render_template("alllist-30.html", rows=rows)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True, threaded=True, port=8080)
    serve(app, host='0.0.0.0', port=5000, url_scheme='https')
    

 
