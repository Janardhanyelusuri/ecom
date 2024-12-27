from flask import Flask,render_template,request,flash,session,redirect,url_for
import mysql.connector
from itemid import itemotp
from otp import genotp
from cmail import sendmail
import os
import razorpay
RAZORPAY_KEY_ID = 'rzp_test_x3klII7JCQkyBJ'
RAZORPAY_KEY_SECRET ='T4zPh7WIKk8UxEkzWOSW4azc'
client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Frds@1234',
    database='ecom'
)
app=Flask(__name__)
app.secret_key='hfbfe78hjefk'



@app.route('/')
def homepage():
    return render_template('homepage.html')

#admin------------

@app.route('/adminpage')
def adminpage():
    username=session.get('admin')
    if username:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM signup")
        users = cursor.fetchall()
        return render_template('adminpage.html',username=username,users=users)
    return render_template('adminlogin.html')

@app.route('/adminregister',methods=['GET','POST'])
def adminregister():
    if request.method=="POST":
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        password=request.form['password'] 
        cursor=mydb.cursor()
        cursor.execute('select email from admin')
        data=cursor.fetchall()
        cursor.execute('select mobile from admin')
        edata=cursor.fetchall()
        if(mobile,) in edata:
            flash('User already exist')
            return render_template('adminregister.html')
        if(email,)in data:
            flash('Email address already exists')
            return render_template('adminregister.html')
        cursor.close()
        otp=genotp()
        subject='thanks for registering to the application'
        body=f'use this otp to register {otp}'
        sendmail(email,subject,body)
        return render_template('adminotp.html',otp=otp,name=name,mobile=mobile,email=email,password=password)
    else:
        return render_template('adminregister.html')
    
@app.route('/adminotp/<otp>/<name>/<mobile>/<email>/<password>',methods=['GET','POST'])
def adminotp(otp,name,mobile,email,password):
    if request.method=="POST":
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mydb.cursor()
            lst=[name,mobile,email,password]
            query='insert into admin values(%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect(url_for('adminlogin'))
        else:
            flash('Wrong otp')
            return render_template('adminotp.html',otp=otp,name=name,mobile=mobile,email=email,password=password)
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from admin where name=%s \
        and password=%s',[username,password])
        count=cursor.fetchone()[0]
        print(count)
        if count==0:
            flash('Invalid email or password')
            return render_template('adminlogin.html')
        else:
            session['admin']=username
            if not session.get(username):
                session[username]={}
            return redirect(url_for('adminpage'))
    return render_template('adminlogin.html')

@app.route('/adminlogout')
def adminlogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('adminlogin'))
    else:
        flash('already logged out!')
        return redirect(url_for('adminlogin'))



#usrer-----------


@app.route('/userpage')
def userpage():
    username=session.get('user')
    if username:
        cursor = mydb.cursor()
        cursor.execute('select * from addition')
        items = cursor.fetchall()
        session['items']=items
        return render_template('userpage.html')
    return render_template('login.html',loginfirst='* Please login first ')

@app.route('/register',methods=['GET','POST'])

def register():
    if request.method=="POST":
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password'] 
        cursor=mydb.cursor()
        cursor.execute('select email from signup')
        data=cursor.fetchall()
        cursor.execute('select mobile from signup')
        edata=cursor.fetchall()
        if(mobile,) in edata:
            flash('User already exist')
            return render_template('register.html')
        if(email,)in data:
            flash('Email address already exists')
            return render_template('register.html')
        cursor.close()
        otp=genotp()
        subject='thanks for registering to the application'
        body=f'use this otp to register {otp}'
        sendmail(email,subject,body)
        return render_template('otp.html',otp=otp,name=name,mobile=mobile,email=email,address=address,password=password)
    else:
        return render_template('register.html')
@app.route('/otp/<otp>/<name>/<mobile>/<email>/<address>/<password>',methods=['GET','POST'])
def otp(otp,name,mobile,email,address,password):
    if request.method=="POST":
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mydb.cursor()
            lst=[name,mobile,email,address,password]
            query='insert into signup values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect(url_for('login'))
        else:
            flash('Wrong otp')
            return render_template('otp.html',otp=otp,name=name,mobile=mobile,email=email,address=address,password=password,wrong='entered otp wrong, please renter')
    
@app.route('/login',methods=['GET','POST']) 
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from signup where name=%s \
        and password=%s',[username,password])
        count=cursor.fetchone()[0]
        print(count)
        if count==0:
            flash('Invalid email or password')
            return render_template('login.html')
        else:
            session['user']=username
            if not session.get(username):
                session[username]={}
            return redirect(url_for('userpage'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user',None)
        session.pop('items',None)
        return redirect(url_for('login'))
    else:
        flash('already logged out!')
        return redirect(url_for('login'))
    


# admin controls items (CRUD) ---------
    




@app.route('/additems',methods=['GET','POST'])

def additems():
    if request.method=='POST':
        name = request.form['name']
        discription = request.form['discription']
        quantity = request.form['quantity']
        category = request.form['category']
        price = request.form['price']
        image = request.files['image']
        idotp = itemotp()
        filename = idotp+'.jpg'
        cursor = mydb.cursor()
        query = "insert into addition(itemid,name,discription,qty,category,price) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(idotp,name,discription,quantity,category,price))
        mydb.commit()
        path = os.path.dirname(os.path.abspath(__file__))
        static_path=os.path.join(path,'static')
        image.save(os.path.join(static_path,filename))
        flash('item added sucessfuly')
    return render_template('items.html')


@app.route('/status',methods=['GET','POST'])
def status():
    cursor=mydb.cursor()
    query="select * from addition order by category"
    cursor.execute(query)
    items=cursor.fetchall()
    mydb.commit()
    return render_template('status.html',items=items)

@app.route('/updateproducts/<itemid>',methods=['GET','POST'])
def updateproducts(itemid):
    cursor=mydb.cursor()
    cursor.execute('select name,discription,qty,category,price from addition where itemid=%s',[itemid])
    items=cursor.fetchone()
    cursor.close()
    if request.method=='POST':
        name = request.form['name']
        discription = request.form['discription']
        quantity = request.form['quantity']
        category = request.form['category']
        price = request.form['price']
        cursor=mydb.cursor()
        query = "update addition set name=%s,discription=%s,qty=%s,category=%s,price=%s where itemid=%s"
        cursor.execute(query,(name,discription,quantity,category,price,itemid))
        mydb.commit()
        cursor.close()
        return redirect(url_for('status'))
    return render_template('updateproducts.html',items=items)

@app.route('/deleteproducts/<itemid>')
def deleteproducts(itemid):
    cursor=mydb.cursor()
    cursor.execute('delete from addition where itemid=%s',[itemid])
    mydb.commit()
    path = os.path.dirname(os.path.abspath(__file__))
    static_path=os.path.join(path,'static')
    filename= itemid+'.jpg'
    os.remove(os.path.join(static_path,filename))
    flash('item deleted')
    return redirect(url_for('status'))

#cart-------------




# categories--------------


@app.route('/fashion')
def fashion():
    username=session.get('user')
    if username:
        items = session.get('items')
        return render_template('fashion.html',items=items)
    return redirect(url_for('userpage'))

@app.route('/electronics')
def electronics():
    username=session.get('user')
    if username:
        items = session.get('items')
        return render_template('electronics.html',items=items)
    return redirect(url_for('userpage'))


@app.route('/groceries')
def groceries():
    username=session.get('user')
    if username:
        items = session.get('items')
        return render_template('groceries.html',items=items)
    return redirect(url_for('userpage'))

#cart-2-------------------

@app.route('/addcart/<itemid>/<name>/<category>/<price>/<quantity>',methods=['GET','POST'])

def addcart(itemid,name,category,price,quantity):
    if not session.get('user'):
        return redirect(url_for('login'))
    else:
        if itemid  not in  session.get(session['user'],{}):
            session[session['user']][itemid]=[name,price,1,f'{itemid}.jpg',category,itemid]
            session.modified=True
            flash(f'{name} added to cart')
            return '<h2> added to cart </h2>'
    session[session['user']][itemid][2] +=1
    session.modified=True
    flash(f'{name} quantity increased in the cart')
    return '<h2> quantity increased in the cart</h2>'

@app.route('/viewcart')
def viewcart():
    if not session.get('user'):
        return redirect(url_for('login'))

    user_cart=session.get(session.get('user'))
    if not user_cart:
        items='empty'
    else:
        items=user_cart
    if items=='empty':
        return '<h1> your cart is empty</h1>'
    return render_template('cart.html',items=items)
    
@app.route('/cartpop/<itemid>')
def cartpop(itemid):
    print(itemid)
    if session.get('user'):
        session[session.get('user')].pop(itemid)
        session.modified=True
        flash('item removed')
        return redirect(url_for('viewcart'))
    else:
        return redirect(url_for('login'))


@app.route('/category/<category>',methods=['GET','POST'])

def category(category):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from addition where category=%s',[category])
        data = cursor.fetchall()
        return render_template('category.html',data=data)
    else:
        return redirect(url_for('login'))
 
 #payement

@app.route('/pay/<item_id>/<name>/<int:price>', methods=['POST'])
def pay(item_id, name, price):
    try:
        # Get the quantity from the form
        qty = int(request.form['qty'])
        print(qty,item_id,name,price)
        # Calculate the total amount in paise (price is in rupees)
        total_price = int(price) * qty  # Ensure integer multiplication

        print(f"Creating payment for Item ID: {item_id}, Name: {name}, Total Price: {total_price}")

        # Create Razorpay order
        order = client.order.create({
            'amount': total_price,
            'currency': 'INR',
            'payment_capture': '1'
        })

        print(f"Order created: {order}")
        return render_template('pay.html', order=order, itemid=item_id, name=name, price=total_price, qty=qty)
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return str(e), 400



@app.route('/success',methods=['POST'])

def success():
    if session.get('user'):
        payment_id=request.form.get('razorpay_payment_id')
        order_id=request.form.get('razorpay_order_id')
        signature=request.form.get('razorpay_signature')
        name=request.form.get('name')
        itemid=request.form.get('itemid')
        total_price=request.form.get('total_price')
        qyt=request.form.get('qyt')

        if not qyt or not qyt.isdigit():
            flash('Invalid quantity provided!')
            return 'Invalid Quantity'
        qyt=int(qyt)


        params_dict={
            'razorpay_order_id':order_id,
            'razorpay_payment_id':payment_id,
            'razorpay_signature':signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into orders(item_id,item_name,total_price,user,qty) values(%s,%s,%s,%s,%s)',[itemid,name,total_price,session.get('user'),qyt])
            mydb.commit()
            cursor.close()
            flash('Order Placed Sucessfully')
            return redirect(url_for('orders'))
        except razorpay.errors.SignatureVerificationError:
            return 'Payment verification failed!',400
    else:
        return redirect(url_for('login'))

#orders

@app.route('/orders')
def orders():
    if session.get('user'):
        user=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from orders where user=%s',[user])
        data=cursor.fetchall()
        cursor.close()
        return render_template('orderdisplay.html',data=data)
    else:
        return redirect(url_for('login'))
    
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        search=request.form.get('search')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from addition where name=%s',[search])
        data=cursor.fetchall()
        cursor.close()
        return render_template('homepage.html',data=data)


app.run(debug=True)