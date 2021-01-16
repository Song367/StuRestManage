import os, uuid
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest.models import Canteen, FoodList, Store, Login


def create_canteen(request):
    if request.method == "POST":
        canteen_name = request.POST.get("name", "")
        secret = uuid.uuid1()
        try:
            obj = Canteen.objects.create(name=canteen_name, secret=secret)
        except:
            return JsonResponse({"code": -1, "data": "", "error": "创建食堂数据出错"})
        return JsonResponse({"code": 0, "data": {"canteen_id": obj.CID, "canteen_name": obj.name}, "error": ""})


def query_canteen(request):
    if request.method == "POST":
        cans = Canteen.objects.all()
        print(cans)
        can_name = []
        for can in cans:
            can_name.append(can.name)
        return JsonResponse({"data": can_name})


def login_canteen(request):
    if request.method == "POST":
        canteen_name = request.POST.get("canteen_name")
        secret = request.POST.get("secret", "")
        can_obj = Canteen.objects.get(name=canteen_name)
        if can_obj.secret == secret:
            return JsonResponse({"login_code": 1})
        else:
            return JsonResponse({"login_code": -1})


def create_store(request):
    if request.method == "POST":
        canteen_id = request.POST.get("canteen_id", "")
        store_name = request.POST.get("store_name")
        try:
            store_obj = Store.objects.create(StoreName=store_name)
            canteen_obj = Canteen.objects.get(CID=canteen_id)
            store_obj.canteen_set.add(canteen_obj)
            canteen_obj.canteen_store.add(store_obj)
            canteen_obj.save()
            store_obj.save()
        except:
            return JsonResponse({"code": -1, "data": "", "error": "创建店铺数据出错"})
        return JsonResponse({"code": 0, "data": {"store_id": store_obj.SID}, "error": ""})


def query_store(request):
    if request.method == "POST":
        canteen_id = request.POST.get("canteen_id", "")
        # canteen_obj = Canteen.objects.get(CID=canteen_id)
        store_list = list(Store.objects.filter(canteen__CID=canteen_id).values())
        return JsonResponse({"data": store_list})


def remove_store(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id", 0)
        canteen_id = request.POST.get("canteen_id", 0)
        can_obj = Canteen.objects.get(CID=canteen_id)
        print(store_id)
        store_obj = Store.objects.filter(SID=int(store_id))
        store_obj[0].canteen_set.remove(can_obj)
        store_obj[0].save()
        store_obj.delete()
        return JsonResponse({"code": 0, "data": "", "error": ""})


def update_store(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id", "")
        store_name = request.POST.get("store_name", "")
        store_obj = Store.objects.get(SID=store_id)
        store_obj.StoreName = store_name
        store_obj.save()
        return JsonResponse({"code": 0, "data": "", "error": ""})


def query_food_store_by_id(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id", "")
        store_obj = Store.objects.get(SID=store_id)
        food_list = list(FoodList.objects.filter(store=store_obj).values())
        return JsonResponse({"data": food_list})


def insert_food(request):
    if request.method == "POST":
        store_id = request.POST.get("store_id", "")
        food_name = request.POST.get("food_name", "")
        food_img = request.FILES.get("food_img", "")
        price = request.POST.get("price", "")
        path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'img'), str(food_img))
        with open(path, "wb+") as f:
            for c in food_img.chunks():
                f.write(c)
        food_obj = FoodList.objects.create(FName=food_name, Image=food_img, Price=price)
        store_obj = Store.objects.get(SID=store_id)
        store_obj.food.add(food_obj)
        food_obj.store_set.add(store_obj)
        store_obj.save()
        food_obj.save()
        return JsonResponse({"code": 0, "data": {"food_id": food_obj.FID}, "error": ""})


def remove_food(request):
    if request.method == "POST":
        food_id = request.POST.get("food_id", 0)
        store_id = request.POST.get("store_id", 0)
        food_obj = FoodList.objects.filter(FID=food_id)
        store_obj = Store.objects.get(SID=store_id)
        store_obj.food.remove(food_obj[0])
        food_obj.delete()
        store_obj.save()
        return JsonResponse({"code": 0, "data": "", "error": ""})


def update_food(request):
    if request.method == "POST":
        food_id = request.POST.get("food_id", "")
        food_name = request.POST.get("food_name", "")
        food_img = request.FILES.get("food_img", "")
        price = request.POST.get("price", "")
        food_obj = FoodList.objects.get(FID=food_id)
        food_obj.FName = food_name
        food_obj.Image = food_img
        food_obj.Price = price
        food_obj.save()
        return JsonResponse({"code": 0, "data": "", "error": ""})


def login_insert(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        canteen_id = request.POST.get("canteen_id", "")
        lid = uuid.uuid1()
        Login.objects.create(LID=lid, username=username)
        login_obj = Login.objects.get(LID=lid)
        canteen_obj = Canteen.objects.get(CID=canteen_id)
        login_obj.canteen_set.add(canteen_obj)
        canteen_obj.stu.add(login_obj)
        login_obj.save()
        canteen_obj.save()
        return JsonResponse({"data": lid})


def query_quantity(request):
    if request.method == "POST":
        canteen_id = request.POST.get("canteen_id", 0)
        can_obj = Canteen.objects.get(CID=canteen_id)
        login_amount = Login.objects.filter(canteen=can_obj).count()

        return JsonResponse({"amount": login_amount})


def delete_login(request):
    if request.method == "POST":
        login_id = request.POST.get("lid", 0)
        canteen_id = request.POST.get("canteen_id", 0)
        login_obj = Login.objects.filter(LID=login_id)
        can_obj = Canteen.objects.get(CID=canteen_id)
        can_obj.stu.remove(login_obj[0])
        login_obj.delete()
        can_obj.save()
        return JsonResponse({"code": 0, "data": "", "error": ""})
