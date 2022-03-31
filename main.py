import aiohttp
import json
import matplotlib.pyplot as plt
from flask import Flask
from flask import request
from flask.templating import render_template
from mysql.connector import connect
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decimal import *


app = Flask(__name__)

bitcoinDay = 0
ethereumDay = 0
rippleDay = 0
bitcoinYesterday = 0
ethereumYesterday = 0
rippleYesterday = 0
sumBtcPositive = 0
sumBtcNegative = 0
sumEtcPositive = 0
sumEtcNegative = 0
sumXrpPositive = 0
sumXrpNegative = 0
sumBitcoinBdd = 0
sumEthereumBdd = 0
sumRippleBdd = 0
start = True
add = False
remove = False
bitcoinGraphic = {}
ethereumGraphic = {}
rippleGraphic = {}
xBtc = []
yBtc = []
xEtc = []
yEtc = []
xXrp = []
yXrp = []


async def recupValueDay():
    try:
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            crypto = ["bitcoin", "ethereum", "ripple"]
            
            global bitcoinDay
            global ethereumDay
            global rippleDay
            
            for value in crypto:
                verif = "SELECT price FROM "+value+" where date = curdate() AND quantity IS NULL;"
                with connection.cursor() as cursor:
                    cursor.execute(verif)
                    data = cursor.fetchall()
                    if value == "bitcoin":
                        if data:
                            for result in data:
                                bitcoinDay = round(result[0],2)
                        else:
                            bitcoinDay = await recordValue(1, 1, value)   
                                
                    elif value == "ethereum":
                        if data:
                            for result in data:
                                ethereumDay = round(result[0],2)
                        else:
                            ethereumDay = await recordValue(1, 1027, value)   
                    else:
                        if data:
                            for result in data:
                                rippleDay = round(result[0],2)
                        else:
                            rippleDay = await recordValue(1, 52, value)
                              
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de la récupération des valeurs des crypto d'aujourd'hui sur la base de données")


async def recupGraphic():
    try:
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            crypto = ["bitcoin", "ethereum", "ripple"]
            
            global xBtc
            global yBtc
            global xEtc
            global yEtc
            global xXrp
            global yXrp 
            
            for value in crypto:
                verif = "SELECT price, date FROM "+value+" WHERE date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND CURRENT_DATE() AND quantity IS NULL;"
                with connection.cursor() as cursor:
                    cursor.execute(verif)
                    data = cursor.fetchall()
                    if value == "bitcoin":
                        if data:
                            for result in data:
                                xBtc.append(str(result[1])[-2:])
                                yBtc.append(round(result[0]))
                                
                    elif value == "ethereum":
                        if data:
                            for result in data:
                                xEtc.append(str(result[1])[-2:])
                                yEtc.append(round(result[0]))
                                
                    else:
                        if data:
                            for result in data:
                                xXrp.append(str(result[1])[-2:])
                                yXrp.append(round(result[0]))
                              
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de la récupération des valeurs sur la base de données pour créer les graphiques")


async def sumCryptoBdd():
    try:
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            crypto = ["bitcoin", "ethereum", "ripple"]
         
            global sumBtcPositive
            global sumBtcNegative
            global sumEtcPositive
            global sumEtcNegative
            global sumXrpPositive
            global sumXrpNegative
            global sumBitcoinBdd
            global sumEthereumBdd
            global sumRippleBdd
            global start
            global add
            global remove
            
            for value in crypto:
                sumCryptoPositive = "SELECT SUM(price) FROM "+value+" WHERE quantity IS NOT NULL AND QUANTITY = 1;"
                sumCryptoNegative = "SELECT SUM(price) FROM "+value+" WHERE quantity IS NOT NULL AND QUANTITY = -1;"
                
                with connection.cursor() as cursor:
                    cursor.execute(sumCryptoPositive)
                    data = cursor.fetchall()
              
                if value == "bitcoin":
                    if data:
                        for result in data:
                            if result[0] is not None:
                                sumBtcPositive += result[0]
                    else:
                        sumBtcPositive = 0  
                            
                elif value == "ethereum":
                    if data:
                        for result in data:
                            if result[0] is not None:
                                sumEtcPositive += result[0]
                    else:
                        sumEtcPositive = 0
                
                else:
                    if data:
                        for result in data:
                            if result[0] is not None:
                                sumXrpPositive += result[0]
                    else:
                        sumXrpPositive = 0
                        
                with connection.cursor() as cursor:
                    cursor.execute(sumCryptoNegative)
                    data = cursor.fetchall()
                    
                if value == "bitcoin":
                    if data:
                        for result in data:
                            if result[0] is not None:
                                sumBtcNegative += result[0]
                    else:
                        sumBtcNegative = 0  
                            
                elif value == "ethereum":
                    if data:
                        for result in data:
                            if result[0] is not None:
                                sumEtcNegative += result[0]
                    else:
                        sumEtcNegative = 0
                
                else:
                    if data:
                        for result in data:
                            if result[0] is not None:
                                sumXrpNegative += result[0]
                    else:
                        sumXrpNegative = 0
                        
                sumBitcoinBdd = round(sumBtcPositive - sumBtcNegative, 2)
                sumEthereumBdd = round(sumEtcPositive - sumEtcNegative, 2)
                sumRippleBdd = round(sumXrpPositive - sumXrpNegative, 2)
                
            sumBtcPositive = 0
            sumEtcPositive = 0
            sumXrpPositive = 0
            sumBtcNegative = 0
            sumEtcNegative = 0
            sumXrpNegative = 0
            add = False
            remove = False
                        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de la récupération des sommes des crypto à la base de données")
        
        
async def recupValueYesterday():
    try:
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            crypto = ["bitcoin", "ethereum", "ripple"]
         
            global bitcoinYesterday
            global ethereumYesterday
            global rippleYesterday
            
            for value in crypto:
                sum = "SELECT price from "+value+" where date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) AND quantity IS NULL;"
                with connection.cursor() as cursor:
                    cursor.execute(sum)
                    data = cursor.fetchall()
              
                if value == "bitcoin":
                    if data:
                        for result in data:
                            if result[0] is not None:
                                bitcoinYesterday = round(result[0],2)
                    else:
                        getcontext().prec = 12
                        bitcoinYesterday = Decimal(0)  
                            
                elif value == "ethereum":
                    if data:
                        for result in data:
                            if result[0] is not None:
                                ethereumYesterday = round(result[0],2)
                    else:
                        getcontext().prec = 12
                        ethereumYesterday = Decimal(0)  
                
                else:
                    if data:
                        for result in data:
                            if result[0] is not None:
                                rippleYesterday = round(result[0],2)
                    else:
                        getcontext().prec = 12
                        rippleYesterday = Decimal(0)         
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de la récupération des valeurs des crypto d'hier sur la base de données")
        
        
async def recordValue(amount, id, crypto):
  async with aiohttp.ClientSession() as session:

    url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
  
    parameters = {
    'amount': amount,
    'id': id,
    'convert':'EUR'
    }
    
    headers = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY':'a30e9c71-4781-4e63-8787-dae5e4e482c5',
    }
    
    session.headers.update(headers)
    
    async with session.get(url, params=parameters) as response:
      try:
        data = await response.content.read()
        data = json.loads(data)
        
        price = data["data"]["quote"]["EUR"]["price"]
          
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            insert = "INSERT INTO "+crypto+" (price) VALUES ('"+str(price)+"');"
            with connection.cursor() as cursor:
              cursor.execute(insert)
              connection.commit()
        
      except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de l'implémentation du prix")
      
      getcontext().prec = 12  
      return Decimal(price)
    
    
async def convert(amount, id):
    async with aiohttp.ClientSession() as session: 
            
        url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
        
        parameters = {
        'amount': amount,
        'id': id,
        'convert':'EUR'
        }
        
        headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'a30e9c71-4781-4e63-8787-dae5e4e482c5',
        }
        
        session.headers.update(headers)
        
        async with session.get(url, params=parameters) as response:
            try:
                data = await response.content.read()
                data = json.loads(data)
                
                price = data["data"]["quote"]["EUR"]["price"]
                return price
            
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                print("Un problème est survenu lors de la récupération du prix")
               
                
async def addBdd(quantity, id, crypto):
    async with aiohttp.ClientSession() as session: 
            
        url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'
        
        parameters = {
        'amount': quantity,
        'id': id,
        'convert':'EUR'
        }
        
        headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'a30e9c71-4781-4e63-8787-dae5e4e482c5',
        }
        
        session.headers.update(headers)
        
        async with session.get(url, params=parameters) as response:
            try:
                data = await response.content.read()
                data = json.loads(data)
                
                price = data["data"]["quote"]["EUR"]["price"]
            
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                print("Un problème est survenu lors de la récupération du prix")
    try:
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            insert = "INSERT INTO "+crypto+" (quantity, price) VALUES ('"+quantity+"', '"+str(price)+"');"
            with connection.cursor() as cursor:
                cursor.execute(insert)
                connection.commit()
                
                global add
                add = True
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de l'ajout à la base de données")
        
        
async def removeBdd(id, crypto, quantity):
    
    price = await convert(quantity, id)
    
    try:
        with connect(
            host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
            user="zn4ssay8kv019vdj",
            password="xktfzs1n6lud4ith",
            database="jfhqjvw2yw2b6kw1",
        ) as connection:
            
            verif = "SELECT SUM(quantity) FROM "+crypto+";"
    
            with connection.cursor() as cursor:
                cursor.execute(verif)
                verif = cursor.fetchall()
                for result in verif:
                    if result[0] is not None and int(result[0]) > 0:
                        delete = "INSERT INTO "+crypto+" (price, quantity) VALUES ('"+str(price)+"', '-"+quantity+"');"
                        cursor.execute(delete)
                        connection.commit()
                        
                        global remove
                        remove = True
                        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("Un problème est survenu lors de la suppression de la quantitée du crypto sur la base de données")            
        
        
@app.route('/')	
async def home():
    await recupValueDay()
    
    global start
    global add
    global remove
   
    if start or add or remove:
        await sumCryptoBdd()
    
    await recupValueYesterday()
    
    if bitcoinYesterday != 0:
        tendencyBtc = round((bitcoinDay - bitcoinYesterday) * 100 / bitcoinDay, 2)
    
    else:
        tendencyBtc = 0    
    
    if ethereumYesterday != 0:    
        tendencyEtc = round((ethereumDay - ethereumYesterday) * 100 / ethereumDay, 2)
        
    else:
        tendencyEtc = 0
    
    if rippleYesterday != 0:        
        tendencyXrp = round((rippleDay - rippleYesterday) * 100 / rippleDay, 2)
        
    else:
        tendencyXrp = 0
    
    start = False       
     
    return render_template('home.html', sumBitcoinBdd=sumBitcoinBdd, sumEthereumBdd=sumEthereumBdd, sumRippleBdd=sumRippleBdd, tendencyBtc=tendencyBtc, tendencyEtc=tendencyEtc, tendencyXrp=tendencyXrp)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/add", methods = ['POST'])
async def testAdd():
        
    if 'add' in request.form:
        if request.form['id'] == "1":
            crypto = "bitcoin"
        
        elif request.form['id'] == "1027":
            crypto = "ethereum"
        
        else:
            crypto = "ripple"
            
        await addBdd(request.form['quantity'], request.form['id'], crypto) 
        return render_template("add.html")
    
    else:
        price = await convert(request.form['quantity'], request.form['id'])
        return render_template("add.html", quantity=request.form['quantity'], price=price)
    
    
@app.route("/remove")
def remove():
    return render_template("remove.html")


@app.route("/remove", methods = ['POST'])
async def testRemove():
    if int(request.form['quantity']) >= 1: 
        if request.form['id'] == "1":
            crypto = "bitcoin"
            
        elif request.form['id'] == "1027":
            crypto = "ethereum"
            
        else:
            crypto = "ripple"
            
    else:
        print("Votre saisie est incorrecte. Veuillez réessayer s'il vous plaît.")    
        return render_template("remove.html")
    
    await removeBdd(request.form['id'], crypto, request.form['quantity']) 
    return render_template("remove.html")


@app.route("/preview_graph_btc")
async def preview_graph_btc():

    await recupGraphic()

    plt.title('Vos gains', fontsize=20, fontweight='bold', color='white')
    plt.xlabel('Date', fontsize=13, fontweight='bold', color='white')
    plt.ylabel('€', fontsize=13, fontweight='bold', color='white')
    plt.tick_params(colors='white')
    plt.plot(xBtc,yBtc, c = 'g', label="croissance")
    plt.axis([1, 31, 30000, 50000])
    plt.legend(loc="lower right")
    plt.savefig('static/graphic_btc.png', transparent = True)
    plt.close()
    return render_template("preview_graph_btc.html")


@app.route("/preview_graph_etc")
async def preview_graph_etc():

    await recupGraphic()

    plt.title('Vos gains', fontsize=20, fontweight='bold', color='white')
    plt.xlabel('Date', fontsize=13, fontweight='bold', color='white')
    plt.ylabel('€', fontsize=13, fontweight='bold', color='white')
    plt.tick_params(colors='white')
    plt.plot(xEtc,yEtc, c = 'g', label="croissance")
    plt.axis([1, 31, 2500, 5000])
    plt.legend(loc="lower right")
    plt.savefig('static/graphic_etc.png', transparent = True)
    plt.close()
    return render_template("preview_graph_etc.html")


@app.route("/preview_graph_xrp")
async def preview_graph_xrp():
    
    await recupGraphic()

    plt.title('Vos gains', fontsize=20, fontweight='bold', color='white')
    plt.xlabel('Date', fontsize=13, fontweight='bold', color='white')
    plt.ylabel('€', fontsize=13, fontweight='bold', color='white')
    plt.tick_params(colors='white')
    plt.plot(xXrp, yXrp, c = 'g', label="croissance")
    plt.axis([1, 31, 1, 5])
    plt.legend(loc="lower right")
    plt.savefig('static/graphic_xrp.png', transparent = True)
    plt.close()
    return render_template("preview_graph_xrp.html")


@app.errorhandler(404)
def page_not_found(error):
    return ("Cette page n'existe pas. Peut être voudriez-vous la créer ? ^_-!"), 404


if __name__ == "__main__":
    app.run()