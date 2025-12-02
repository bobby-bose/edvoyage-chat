import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.conf import settings

from .models import UserSimple, Conversation, Message


def _get_or_create_user(email):
    user, _ = UserSimple.objects.get_or_create(email=email)
    return user


def conversations_get(request):
    try:
        email = request.GET.get('email') or settings.STATIC_CURRENT_USER_EMAIL
        # default to STATIC_CURRENT_USER_EMAIL if no email provided by client
        current = _get_or_create_user(email)

        # Get conversations where current user is user_a OR user_b
        convs_as_a = Conversation.objects.filter(user_a=current)
        convs_as_b = Conversation.objects.filter(user_b=current)

        data = []
        seen_other_emails = set()
        
        # Process conversations where current user is user_a
        for c in convs_as_a:
            # Only include if there's at least one message
            if c.messages.exists():
                last_msg = c.messages.order_by('-timestamp').first()
                last_text = last_msg.text or ''
                last_time = last_msg.timestamp.isoformat()
                unread = c.messages.filter(seen=False).exclude(sender=current).count()

                data.append({
                    'conversation_id': c.id,
                    'other_email': c.user_b.email,
                    'other_name': c.user_b.name,
                    'last_text': last_text,
                    'last_time': last_time,
                    'unread': unread,
                })
                seen_other_emails.add(c.user_b.email)
        
        # Process conversations where current user is user_b
        for c in convs_as_b:
            # Only include if there's at least one message and we haven't already added this user
            if c.messages.exists() and c.user_a.email not in seen_other_emails:
                last_msg = c.messages.order_by('-timestamp').first()
                last_text = last_msg.text or ''
                last_time = last_msg.timestamp.isoformat()
                unread = c.messages.filter(seen=False).exclude(sender=current).count()

                data.append({
                    'conversation_id': c.id,
                    'other_email': c.user_a.email,
                    'other_name': c.user_a.name,
                    'last_text': last_text,
                    'last_time': last_time,
                    'unread': unread,
                })
                seen_other_emails.add(c.user_a.email)

        # sort by last_time desc
        data.sort(key=lambda x: x['last_time'], reverse=True)

        return JsonResponse({'status': True, 'email': current.email, 'conversations': data})
    except Exception as e:
        print("ERROR /api/conversations:", e)
        return JsonResponse({'status': False, 'error': str(e)})


def messages_get(request):
    try:
        # Clients can omit the `email` parameter; use server-side static user instead
        email = request.GET.get('email') 
        other_email = request.GET.get('other_email')
        if not other_email:
            return JsonResponse({'status': False, 'error': 'other_email required'})

        current = _get_or_create_user(email)
        other = _get_or_create_user(other_email)
        # Ensure the conversation record for current user exists (as per spec)
        conv, _ = Conversation.objects.get_or_create(user_a=current, user_b=other)

        # Also fetch the reverse conversation (where the other user may have been 'user_a')
        rev_conv = Conversation.objects.filter(user_a=other, user_b=current).first()

        # Collect messages from both conversations (if reverse exists)
        msgs = list(conv.messages.order_by('timestamp').all())
        if rev_conv:
            msgs += list(rev_conv.messages.order_by('timestamp').all())

        # sort combined messages by timestamp asc
        msgs.sort(key=lambda mm: mm.timestamp)

        results = []
        # Update delivered/seen where sender != current
        for m in msgs:
            if m.sender != current:
                if not m.delivered or not m.seen:
                    m.delivered = True
                    m.seen = True
                    m.save(update_fields=['delivered', 'seen'])

            image_url = ''
            if m.image:
                image_url = request.build_absolute_uri(m.image.url)

            results.append({
                'id': m.id,
                'sender': m.sender.email,
                'text': m.text or '',
                'image_url': image_url,
                'timestamp': m.timestamp.isoformat(),
                'delivered': m.delivered,
                'seen': m.seen,
            })

        return JsonResponse({'status': True, 'conversation_id': conv.id, 'messages': results})
    except Exception as e:
        print("ERROR /api/messages:", e)
        return JsonResponse({'status': False, 'error': str(e)})


@csrf_exempt
def send_message(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': False, 'error': 'POST required'})
        # allow clients to omit the sender; fall back to STATIC_CURRENT_USER_EMAIL
        from_email = request.POST.get('from_email') or request.POST.get('from') or request.POST.get('fromEmail') or settings.STATIC_CURRENT_USER_EMAIL
        to_email = request.POST.get('to_email') or request.POST.get('to') or request.POST.get('toEmail')
        text = request.POST.get('text', '')
        image = request.FILES.get('image')

        if not from_email or not to_email:
            return JsonResponse({'status': False, 'error': 'from_email and to_email required'})

        sender = _get_or_create_user(from_email)
        recipient = _get_or_create_user(to_email)

        conv, _ = Conversation.objects.get_or_create(user_a=sender, user_b=recipient)

        msg = Message(conversation=conv, sender=sender, text=text)
        if image:
            msg.image = image
        msg.save()

        image_url = ''
        if msg.image:
            image_url = request.build_absolute_uri(msg.image.url)

        res = {
            'id': msg.id,
            'conversation_id': conv.id,
            'sender': sender.email,
            'text': msg.text or '',
            'image_url': image_url,
            'timestamp': msg.timestamp.isoformat(),
            'delivered': msg.delivered,
            'seen': msg.seen,
        }

        return JsonResponse({'status': True, 'message': res})
    except Exception as e:
        print("ERROR /api/send:", e)
        return JsonResponse({'status': False, 'error': str(e)})


def users_list(request):
    try:
        email = request.GET.get('email') or settings.STATIC_CURRENT_USER_EMAIL
        current = _get_or_create_user(email)
        
        # Get all users except current user
        all_users = UserSimple.objects.exclude(id=current.id).order_by('email')
        
        users = []
        for u in all_users:
            users.append({
                'email': u.email,
                'name': u.name or '',
            })
        
        return JsonResponse({'status': True, 'users': users})
    except Exception as e:
        print("ERROR /api/users:", e)
        return JsonResponse({'status': False, 'error': str(e)})


def index_page(request):
    email= request.GET.get('email') 
    # pass the server-side current user email into the template context
    return render(request, 'conversations.html', {'current_user_email': email})


def chat_page(request):
    # the frontend JS reads `other_email` from the querystring
    return render(request, 'chat_messages.html', {'current_user_email': settings.STATIC_CURRENT_USER_EMAIL})
