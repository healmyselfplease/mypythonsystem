from django.http import HttpResponseRedirect,request,JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import pymysql
from http import cookies
import json

def Login(request):
    return render(request,"login.html")

def Login_Home(request):
    user=request.POST.get("username")
    pwd=request.POST.get("password")
    sql_select="select {what} from {table} where user_name=\'{u_n}\'and password=\'{passwd}\'".format(what="user_name,authority",table="user_info",u_n=user,passwd=pwd)
    data=SQL_m(sql_select).SQL_select()
    if data:
        data={"name":data[0][0],"authority":data[0][1]}
        data=json.dumps(data)
    return HttpResponse(data)

def Home(request):
    if request.COOKIES.get("name"):
        add=1
        if request.COOKIES.get("authority")=="all":
            sql_select="select a.name,a.job_number,a.nation,a.sex,a.age,a.id_card,a.telephone_number,a.email,a.address,c.department,c.department_number,c.job,c.entry_time,c.iswork,b.authority from personal_information a left join user_info b on a.name=b.name left join people_001 c on b.name=c.name"
        elif request.COOKIES.get("authority")=="1":
            add=0
            sql_select = "select a.name,a.job_number,a.nation,a.sex,a.age,a.id_card,a.telephone_number,a.email,a.address,c.department,c.department_number,c.job,c.entry_time,c.iswork,b.authority from personal_information a left join user_info b on a.name=b.name left join people_001 c on b.name=c.name where b.user_name={name}".format(name=request.COOKIES.get("name"))
        else:
            sql_select = "select a.name,a.job_number,a.nation,a.sex,a.age,a.id_card,a.telephone_number,a.email,a.address,c.department,c.department_number,c.job,c.entry_time,c.iswork,b.authority from personal_information a left join user_info b on a.name=b.name left join people_001 c on b.name=c.name where c.department_number={authority}".format(authority=request.COOKIES.get("authority"))
        message=SQL_m(sql_select).SQL_select()
        print(message)
        return render(request, "Home.html",{"name":request.COOKIES.get("name"),"authority":request.COOKIES.get("authority"),"mess":message,"add":add})
    else:
        return render(request,"Home.html",{"name":""})

class SQL_m:
    def __init__(self,sql):
        self.sql=sql
        self.conn = pymysql.connect(host="localhost", user="root", password="892434969", db="my")
        self.cursor = self.conn.cursor()
    def SQL_select(self):
        self.cursor.execute(self.sql)
        data=self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        return list(data)
# ('admin', '123456', 'all')
# ('11180010000', '123456', '1118001')
# ('11180010001', '123456', '')user_info
# ('11180010002', '123456', '')
# ('11180010003', '123456', '')
# ('11180010004', '123456', '')
# ('11180010005', '123456', '')
# ('11180010006', '123456', '')
# ('11180010007', '123456', '')

