from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Record
from .serializers import RecordSerializer
from .permissions import IsAdmin, IsAnalyst
from django.http import HttpResponse



# def home(request):
#     return HttpResponse("Finance API is running")



def home(request):
    return render(request, "api_test.html")

def add_record_page(request):

    if request.method == "POST":

        Record.objects.create(

            amount=request.POST['amount'],
            type=request.POST['type'],
            category=request.POST['category'],
            date=request.POST['date'],
            description=request.POST['description'],
            created_by=request.user

        )

        return redirect('/api/test/')

    return render(request,'add_record.html')




def api_test_page(request):
    return render(request, 'api_test.html')

# CREATE record (Admin only)
@api_view(['POST'])
@permission_classes([IsAdmin])
def create_record(request):

    serializer = RecordSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data)

    return Response(serializer.errors)


# GET records with filtering (Analyst or Admin)
@api_view(['GET'])
@permission_classes([IsAnalyst])
def get_records(request):

    records = Record.objects.all()

    type = request.GET.get('type')
    category = request.GET.get('category')
    date = request.GET.get('date')

    if type:
        records = records.filter(type=type)

    if category:
        records = records.filter(category=category)

    if date:
        records = records.filter(date=date)

    serializer = RecordSerializer(records, many=True)

    return Response(serializer.data)


# Update record (Admin only)
@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_record(request, id):

    try:
        record = Record.objects.get(id=id)
    except Record.DoesNotExist:
        return Response({"error":"Record not found"}, status=404)

    serializer = RecordSerializer(record, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# Delete record (Admin only)
@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_record(request, id):

    try:
        record = Record.objects.get(id=id)
    except Record.DoesNotExist:
        return Response({"error":"Record not found"}, status=404)

    record.delete()

    return Response({'message': 'deleted'})


# Summary API
@api_view(['GET'])
def summary(request):

    income = Record.objects.filter(type='income').aggregate(Sum('amount'))

    expense = Record.objects.filter(type='expense').aggregate(Sum('amount'))

    total_income = income['amount__sum'] or 0
    total_expense = expense['amount__sum'] or 0

    return Response({

        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense

    })



@api_view(['GET'])
def check_role(request):

    if request.user.is_authenticated:

        return Response({

            "username": request.user.username,

            "role": request.user.role

        })

    return Response({"message":"not logged in"})



from django.http import HttpResponse

def api_home(request):
    return HttpResponse("""
    <h2>Finance API Links</h2>

    <a href="/api/add/">Add Record</a><br><br>

    <a href="/api/test/">Dashboard</a><br><br>

    <a href="/api/summary/">Summary</a><br><br>

    <a href="/api/records/">Records</a><br><br>

    <a href="/admin/">Admin Panel</a><br><br>

    """)