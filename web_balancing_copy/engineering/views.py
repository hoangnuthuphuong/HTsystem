from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from sqlalchemy import create_engine
import mysql.connector
from django.views.decorators.csrf import csrf_exempt

hostname='pbvweb01v'

engine_hbi = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/linebl_2024', echo=False)
mydb=mysql.connector.connect(host=hostname, user='LaDat', passwd='l4d4t5', database="pr2k")
myCursor=mydb.cursor()

def engineering(request):
  template = loader.get_template('hello.html')
  return HttpResponse(template.render())


@csrf_exempt
def update_sah_by_operation(request):
  print('handle post update SAM')
  if request.method == 'POST':
    # idnv = request.POST.get('idnv')
    anetlot=request.POST.get("anetlot")
    assortlot=request.POST.get("assortlot")
    gmt=request.POST.get("gmt")
    oprn=request.POST.get("oprn")
    sam=request.POST.get("sam")

    print(anetlot,assortlot,gmt,oprn,sam)

    sql_update=f"""
      update pr2k.bundleticket_active set earned_hours={sam}/36*units
      where work_lot in ('{anetlot}','{assortlot}') and operation_code='{oprn}'
      and TRIM(style)='{gmt}'
    """
    print(sql_update)
    myCursor.execute(sql_update)
    mydb.commit()
    row_count=myCursor.rowcount

    notes='server have updated '+str(row_count)+' records in bundleticket active\n'

    sql_update=f"""
      update pr2k.employee_scanticket set earned_hours={sam}/36*units
      where work_lot in ('{anetlot}','{assortlot}') and operation_code='{oprn}'
      and DATE(timeupdate)>=DATE(DATE_SUB(DATE(NOW()),INTERVAL 30 DAY))
    """
    myCursor.execute(sql_update)
    mydb.commit()
    row_count=myCursor.rowcount
    notes+='server have updated '+str(row_count)+' records in employee_scanticket'

    return JsonResponse({'notes': notes})
  else:
    return JsonResponse({'error': 'Invalid request method'})