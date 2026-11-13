from django.shortcuts import render, redirect, get_object_or_404
from decor_app.models import Inventory
from django.contrib.auth.models import User
from django.http import HttpResponse
OWNER_USER = "piyush"
OWNER_PASS = "piyush123"

# 1. मुख्य होमपेज (जहाँ पब्लिक को सारी एक्टिव इन्वेंटरी दिखेगी)
def home(request):
    # URL से चुनी हुई कैटेगरी निकालें (उदा: ?cat=birthday)
    category_slug = request.GET.get('cat')

    if category_slug and category_slug != 'all':
        # सिर्फ चुनी हुई कैटेगरी के आइटम्स निकालें
        items = Inventory.objects.filter(category=category_slug).order_by('-created_at')
    else:
        # अगर 'सभी' चुना है या कोई फ़िल्टर नहीं है तो सब दिखाएँ
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

# 4. इन्वेंटरी पेज (अपलोड फॉर्म + डेटाबेस लिस्टिंग)
from django.shortcuts import render, redirect
from .models import Inventory, DecorationMedia

from django.shortcuts import render, redirect
from .models import Inventory, DecorationMedia

def inventory_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        online_url = request.POST.get('online_url')
        description = request.POST.get('description')
        
        gallery_files = request.FILES.getlist('gallery_images')
        
        # Agar main image nahi di hai, toh gallery ki pehli image ko hi main image bana lo
        if not image and gallery_files:
            for f in gallery_files:
                if not f.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                    image = f
                    break

        # 1. Inventory item save karein
        item = Inventory.objects.create(
            title=title,
            price=price,
            category=category,
            image=image,
            video=video,
            online_url=online_url,
            description=description
        )
        
        # 2. Saari files/videos gallery me save karein
        for f in gallery_files:
            is_vid = f.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm'))
            DecorationMedia.objects.create(
                inventory=item,
                media_file=f,
                is_video=is_vid
            )
            
        return redirect('inventory')
        
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