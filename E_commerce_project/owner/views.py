from django.shortcuts import render,redirect
from .models import person_collection,cart,products,orders
from bson.objectid import ObjectId
import base64

# Create your views here.

def admin_login(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        admin = person_collection.find_one({"name":username})
        if admin and admin["password"]==password:
            return redirect("add_item") 
    return render(request,"admin.html")

def add_item(request):
    if request.method=='POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.FILES['photo'].read()
        ratting = request.POST.get("ratting")
        user_data = {
            "name" : name,
            "description" : description,
            "image" : image,
            "quantity":quantity,
            "price" : price,
            "ratting" : ratting
        }
        products.insert_one(user_data)
        return redirect("add_item")
    return render(request,"add_product_admin.html")

def view_items(request):
    items = list(products.find({}))
    if items :
        for i in range(len(items)):
            items[i]["image"] = base64.b64encode(items[i]["image"]).decode('utf-8')
            items[i]["id"] = str(items[i]["_id"])
            ratting = int(items[i]["ratting"])
            stars = range(ratting)
            items[i]["ratting"] = stars
        return render(request,"view_items_admin.html",{"items":items})
    else :
        return render(request,"view_items_admin.html",{"items":items})

def delete_item(request):
    id = request.POST.get("item_id")
    products.delete_one({'_id': ObjectId(id)})
    return redirect("view_items")

def view_orders(request):
    order = list(orders.find({}))
    for i in range(len(order)):
        order[i]["id"] = str(order[i]["_id"])
    return render(request,"view_order.html",{"orders":order})

def logout(request):
    return redirect("admin_login")