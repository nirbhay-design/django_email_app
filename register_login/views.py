from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Users, Inbox, Deleted, Sent
from django.db import connection
import datetime
# Create your views here.
def home(request):
    msg = request.session.get('msg',False)
    if msg:
        request.session['msg'] = {}
        return render(request,'home.html',msg)
    return render(request,'home.html')

def login(request):
    if (request.method == 'GET'):
        return redirect('/')
    email = request.POST['email']
    password = request.POST['password']
    to_send = {}
    auth_query = f"SELECT id FROM register_login_users where email='{email}' and password='{password}';"
    res = Users.objects.raw(auth_query)

    if len(res) == 0:
        to_send['message'] = 'email or password is incorrect'
        to_send['color'] = 'crimson'
        to_send['color1'] = 'white'
        request.session['msg'] = to_send
        return redirect('/')
        
    else:
        return redirect(f'/login/{email}/')

def register(request):
    if (request.method == "GET"):
        return redirect('/')
    cursor = connection.cursor()
    to_send = {}
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm_password']
    query_check = f"SELECT id, email FROM register_login_users where email='{email}';"
    result = Users.objects.raw(query_check)
    if len(result) >= 1:
        to_send['message'] = 'email already taken'
        to_send['color'] = 'crimson'
        to_send['color1'] = 'white'
        request.session['msg'] = to_send
        return redirect('/')

    if password == confirm:
        query = f"INSERT INTO register_login_users (name,email,password) VALUES ('{name}','{email}','{password}');"
        cursor.execute(query)
        to_send['message'] = f'user {email} is successfully registered'
        to_send['color'] = '#97BC62FF'
        to_send['color1'] = 'black'
        request.session['msg'] = to_send
        return redirect('/')

    else:
        to_send['message'] = 'passwords not matching'
        to_send['color'] = 'crimson'
        to_send['color1'] = 'white'
        request.session['msg'] = to_send
        return redirect('/')

def mainapp(request,email_id):
    to_send = {}
    query = f"SELECT id,name from register_login_users where email='{email_id}';"
    res = Users.objects.raw(query)
    if len(res) == 0:
        to_send['message'] = f'email {email_id} does not exists'
        to_send['color'] = 'crimson'
        to_send['color1'] = 'white'
        request.session['msg'] = to_send
        return redirect ('/')
    request.session[email_id] = res[0].name
    return redirect('inbox/')
    # return render(request,'email_page.html',{'email':email_id,'name':res[0].name,'inbox':True})

def inbox(request,email_id):
    name = request.session.get(email_id,False)
    if name:
        query1 = f"select id, from_email, to_email, recv_time, subj, from_name from register_login_inbox where to_email='{email_id}' ORDER BY id DESC;"
        res = Inbox.objects.raw(query1)
        return render(request,'email_page.html',{'email':email_id,'name':name,'inbox':True,'mails':res,'len_mail':len(res),'type':"Inbox"})
    return redirect("/")

def sent(request,email_id):
    name = request.session.get(email_id,False)
    if name:
        query1 = f"select id, from_email, to_email, recv_time, subj, to_name from register_login_sent where from_email='{email_id}' ORDER BY id DESC;"
        res = Sent.objects.raw(query1)
        return render(request,'email_page.html',{'email':email_id,'name':name,'sent':True,'mails':res,'len_mail':len(res),'type':"Sent"})
    return redirect('/')

def deleted(request,email_id):
    name = request.session.get(email_id,False)
    if name:
        query1 = f"select id, from_email, to_email, recv_time, subj, from_name from register_login_deleted where to_email='{email_id}' ORDER BY id DESC;"
        res = Deleted.objects.raw(query1)
        return render(request,'email_page.html',{'email':email_id,'name':name,'mails':res,'len_mail':len(res),'type':"Deleted"})
    return redirect('/')

def compose(request,email_id):
    if request.method == "GET":
        compose_msg = request.session.get('compose_msg',False)
        if compose_msg:
            request.session['compose_msg'] = {}
            return render(request,'compose.html',{'email':email_id,**compose_msg})    
        return render(request,'compose.html',{'email':email_id})
    elif request.method == "POST":
        to_email = request.POST.get('email').strip()
        subject = request.POST.get('subject')
        content = request.POST.get('content__area')
        now_time = datetime.datetime.now()
        validate = f"SELECT id from register_login_users where email='{to_email}';"
        res = Users.objects.raw(validate)
        if (len(res) == 0):
            request.session['compose_msg'] = {'msg':'user does not exists'}
            return redirect(f'/login/{email_id}/compose/')
        
        to_name_query = f"select id, name from register_login_users where email='{to_email}';"
        from_name_query = f"select id, name from register_login_users where email='{email_id}';"

        to_name = Users.objects.raw(to_name_query)[0].name
        from_name = Users.objects.raw(from_name_query)[0].name

        cursor = connection.cursor()
        insert_query = f"INSERT INTO register_login_inbox (from_email, to_email, recv_time, subj, content, from_name) VALUES ('{email_id}','{to_email}','{now_time}','{subject}','{content}','{from_name}');"
        cursor.execute(insert_query)

        insert_query_sent = f"INSERT INTO register_login_sent (from_email, to_email, recv_time, subj, content, to_name) VALUES ('{email_id}','{to_email}','{now_time}','{subject}','{content}','{to_name}');"
        cursor.execute(insert_query_sent)
        
        return redirect(f'/login/{email_id}/inbox/')

def InboxReadMail(request,email_id,id):
    query = f"select * from register_login_inbox where id={int(id)}"
    res = Inbox.objects.raw(query)

    return render(request,'readmails.html',{'from_email':res[0].from_email,'subj':res[0].subj,"content":res[0].content,'from_to':'from'})

def SentReadMail(request,email_id,id):
    query = f"select * from register_login_sent where id={int(id)}"
    res = Sent.objects.raw(query)

    return render(request,'readmails.html',{'from_email':res[0].to_email,'subj':res[0].subj,"content":res[0].content,'from_to':'to'})

def DeleteReadMail(request,email_id,id):
    query = f"select * from register_login_deleted where id={int(id)}"
    res = Deleted.objects.raw(query)

    return render(request,'readmails.html',{'from_email':res[0].from_email,'subj':res[0].subj,"content":res[0].content,'from_to':'from'})

def DeleteMail(request,email_id,id):
    query1 = f"select * from register_login_inbox where id={int(id)}"
    res = Inbox.objects.raw(query1)
    
    from_email = res[0].from_email
    to_email = res[0].to_email
    recv = res[0].recv_time
    subj = res[0].subj
    content = res[0].content
    from_name = res[0].from_name

    cursor = connection.cursor()
    query2 = f"insert into register_login_deleted (from_email, to_email, recv_time, subj, content, from_name) values ('{from_email}','{to_email}','{recv}','{subj}','{content}','{from_name}')"
    query = f"delete from register_login_inbox where id={int(id)}"
    cursor.execute(query)
    cursor.execute(query2)

    return redirect(f'/login/{email_id}/')
