import json
from django.shortcuts import render,redirect
from .models import person_collection,cart,products,orders
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import base64
from bson.objectid import ObjectId
from django.http import JsonResponse

# Create your views here.

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = person_collection.find_one({"email" : email})
        if user and user["password"]==password:
            messages.success(request,"Login Successfull")
            user["_id"] = str(user["_id"])
            request.session['user'] = user
            return redirect("home")
    messages.error(request,"Login Failed")
    return render(request,"login.html")

def register(request):
    if request.method == 'POST' :
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        user = person_collection.find_one({"email" : email})
        if user : 
            return render(request,"redirect.html")
        user_data = {
            "firstname" : firstname,
            "lastname" : lastname,
            "email" : email,
            "password" : password,
            "phone" : phone,
            "address" : address
        }
        person_collection.insert_one(user_data)

        return redirect("/members/")
    return render(request,"login.html",{})

def index(request):
    featured_product = []
    new_arrival = []
    user = request.session["user"]
    product = list(products.find({}))
    for i in range(8):
        product[i]["image"] = base64.b64encode(product[i]["image"]).decode('utf-8')
        ratting = int(product[i]["ratting"])
        stars = range(ratting)
        product[i]["ratting"] = stars 
        featured_product.append(product[i])
        
    for i in range(8,16):
        product[i]["image"] = base64.b64encode(product[i]["image"]).decode('utf-8')
        ratting = int(product[i]["ratting"])
        stars = range(ratting)
        product[i]["ratting"] = stars
        new_arrival.append(product[i])
    return render(request,'index.html',{"user_name" : user["firstname"],"item1":featured_product,"item2":new_arrival})

def shop(request):
    items = list(products.find({}))
    user = request.session["user"]
    if items :
        for i in range(len(items)):
            items[i]["image"] = base64.b64encode(items[i]["image"]).decode('utf-8')
            items[i]["id"] = str(items[i]["_id"])
            ratting = int(items[i]["ratting"])
            stars = range(ratting)
            items[i]["ratting"] = stars
        return render(request,"shop.html",{"items":items,"user_name" : user["firstname"]})
    else :
        return render(request,"shop.html",{"items":items,"user_name" : user["firstname"]})

def blog(request):
   user = request.session["user"]
   return render(request,'blog.html',{"user_name" : user["firstname"]})

def about(request):
    user = request.session["user"]
    return render(request,'about.html',{"user_name" : user["firstname"]})

def contact(request):
    user = request.session["user"]
    return render(request,'contact.html',{"user_name" : user["firstname"]})

def sproduct(request,product_id):
    print(product_id)
    return render(request,"sproduct.html",{})

def user(request):
    user = request.session["user"]
    user_id = str(user["_id"])
    order = list(orders.find({"user_id":user_id}))
    for i in range(len(order)):
        order[i]["id"] = str(order[i]["_id"])
    return render(request,"user.html",{"firstname":user["firstname"],"lastname":user["lastname"],"email":user["email"],"phone":user["phone"],"id":user["_id"],"address":user["address"],"orders":order})

def add_to_cart(request):
    try : 
        user1 = request.session["user"]
        id = request.POST.get("item_id")
        product = products.find_one({'_id': ObjectId(id)})
        cart_item = {
            "user_id" : user1["_id"],
            "product_id" : id,
            "image" : product["image"],
            "name" : product["name"],
            "price" : product["price"],
            "quantity" : "1"
        }
        cart.insert_one(cart_item)
        return redirect("shop")
    except :
        return redirect("shop")

def view_cart(request):
    user = request.session["user"]
    user1 = request.session["user"]
    product = list(cart.find({"user_id" : str(user1["_id"])}))
    for i in range(len(product)):
        product[i]["image"] = base64.b64encode(product[i]["image"]).decode('utf-8')
    return render(request,"cart.html",{"items":product,"user_name":user["firstname"]})

def delete_from_cart(request):
    user = request.session["user"]
    product_id = request.POST.get("product_id")
    user_id = str(user["_id"])
    cart.delete_many({"user_id":user_id,"product_id":product_id})
    return redirect("cart")


def update_cart(request):
    if request.method == 'POST':
        user = request.session["user"]
        product_id = request.POST.getlist('product_id')
        quantity = request.POST.getlist("quantity")
        user_id = str(user["_id"])

        for i in range(len(quantity)):
            id = product_id[i]
            quan = quantity[i]
            myquery = {"user_id":user_id,"product_id":id}
            update = {"$set": { "quantity": quan }}
            cart.update_one(myquery,update)

        return redirect("check_out")

    return JsonResponse({'error': 'GET method not supported'})


def check_out(request):
    user = request.session["user"]
    user_id = user["_id"]
    cart_item = list(cart.find({"user_id" : user_id}))
    total = 0
    for i in range(len(cart_item)):
        p_id = cart_item[i]["product_id"]
        product = products.find_one({"_id" : ObjectId(p_id)})
        quantp = product["quantity"]
        quant = cart_item[i]["quantity"]
        quan = int(quantp) - int(quant)

        if quan < 0 :
            return render(request,"redirect_quantity.html",{"quantity" : quantp})

        cart_item[i]["image"] = base64.b64encode(cart_item[i]["image"]).decode('utf-8')   
        cart_item[i]["subtotal"] = int(cart_item[i]["price"]) * int(cart_item[i]["quantity"])
        total = total + int(cart_item[i]["price"]) * int(cart_item[i]["quantity"])
    return render(request,"checkout.html",{"items" : cart_item,"total" : total,"address":user["address"]})

def order_placed(request):
    user = request.session["user"]
    user_id = str(user["_id"])
    cart_item = list(cart.find({"user_id" : user_id}))
    for i in range(len(cart_item)):
        cart_item[i]["subtotal"] = int(cart_item[i]["price"]) * int(cart_item[i]["quantity"])
        quant = cart_item[i]["quantity"]
        p_id = cart_item[i]["product_id"]
        product = products.find_one({"_id" : ObjectId(p_id)})
        quantp = product["quantity"]
        quan = int(quantp) - int(quant)
        myquery = {"_id":ObjectId(p_id)}
        update = {"$set": { "quantity": quan }}
        products.update_one(myquery,update)
        
        orders.insert_one(cart_item[i])
    cart.delete_many({"user_id":user_id})
    return render(request,"order_placed.html",{})

def logout(request):
    del request.session["user"]
    return redirect("index")

def forgot_password(request):
    if request.method=="POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        request.session["email"] = email
        user = person_collection.find_one({"email" : email,"phone":str(phone)})
        if user:
            return render(request,"reset_password.html",{})
        else : 
            return render(request,"forget_password_redirect.html",{})
        
    return render(request,"forget_password.html",{})

def reset_password(request):
    if request.method=="POST":
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        email = request.session["email"]
        if password==password1 :
            myquery = {"email":email}
            update = {"$set": { "password": password }}
            person_collection.update_one(myquery,update)
            return redirect("index")
        else :
            return render(request,"password_mismatched.html",{})
    return render(request,"reset_password.html",{})