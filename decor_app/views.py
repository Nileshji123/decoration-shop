from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from decor_app.models import Inventory, DecorationMedia


OWNER_USER = "piyush"
OWNER_PASS = "piyush123"

# 1. मुख्य होमपेज (जहाँ पब्लिक को सारी एक्टिव इन्वेंटरी दिखेगी)
def home(request):
    category_slug = request.GET.get('cat')

    if category_slug and category_slug != 'all':
        items = Inventory.objects.filter(category=category_slug).order_by('-created_at')
    else:
        items = Inventory.objects.all().order_by('-created_at')

    context = {
        'items': items,
        'current_category': category_slug or 'all',
    }
    return render(request, 'index.html', context)

# 2. Piyush लॉगिन
def login(request):
    error = None
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        if u == OWNER_USER and p == OWNER_PASS:
            return redirect('dashboard')
        else:
            error = "गलत यूज़रनेम या पासवर्ड!"

    return render(request, 'login.html', {'error': error})

# 3. मेन कमांड डैशबोर्ड (चारों कार्ड्स वाला पेज)
def dashboard(request):
    return render(request, 'dashboard.html')

# 4. इन्वेंटरी पेज (अपलोड फॉर्म + डेटाबेस लिस्टिंग

def inventory_view(request):
    if request.method == 'POST':
        action = request.POST.get('action') # फॉर्म से एक्शन चेक करेंगे कि क्या करना है
        item_id = request.POST.get('item_id') # अगर एडिट या डिलीट करना हो तो आईडी मिलेगी

        # --- 1. DELETE STOCK ---
        if action == 'delete' and item_id:
            item = get_object_or_404(Inventory, pk=item_id)
            item.delete()
            return redirect('inventory')

        # कॉमन डेटा जो Add और Update दोनों में चाहिए
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        online_url = request.POST.get('online_url')
        description = request.POST.get('description')
        gallery_files = request.FILES.getlist('gallery_images')

        # --- 2. UPDATE STOCK ---
        if action == 'update' and item_id:
            item = get_object_or_404(Inventory, pk=item_id)
            item.title = title
            item.price = price
            item.category = category
            item.online_url = online_url
            item.description = description
            
            if request.FILES.get('image'):
                item.image = request.FILES.get('image')
            if request.FILES.get('video'):
                item.video = request.FILES.get('video')
            item.save()

            # नई गैलरी फाइल्स जोड़ना चाहें तो
            for f in gallery_files:
                is_vid = f.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm'))
                DecorationMedia.objects.create(inventory=item, media_file=f, is_video=is_vid)

            return redirect('inventory')

        # --- 3. ADD NEW STOCK (Default) ---
        else:
            image = request.FILES.get('image')
            video = request.FILES.get('video')

            if not image and gallery_files:
                for f in gallery_files:
                    if not f.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                        image = f
                        break

            item = Inventory.objects.create(
                title=title,
                price=price,
                category=category,
                image=image,
                video=video,
                online_url=online_url,
                description=description
            )
            
            for f in gallery_files:
                is_vid = f.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm'))
                DecorationMedia.objects.create(inventory=item, media_file=f, is_video=is_vid)

            return redirect('inventory')

    # GET रिक्वेस्ट पर इन्वेंट्री लिस्ट दिखाना
    items = Inventory.objects.all().order_by('-id')
    return render(request, 'inventory.html', {'items': items})

# बुकिंग / डिटेल पेज का फंक्शन
def booking_page(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'booking_page.html', {'item': item})

def reset_admin_password(request):
    try:
        user = User.objects.get(username='piyush')
        user.set_password('Piyush@98765')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return HttpResponse("Arey Piyush bhai! Admin password successfully reset to: Piyush@98765")
    except User.DoesNotExist:
        User.objects.create_superuser('piyush', 'admin@example.com', 'Piyush@98765')
        return HttpResponse("Superuser 'piyush' created successfully with password: Piyush@98765")

def my_profile(request):
    return render(request, 'piyushprofile.html')