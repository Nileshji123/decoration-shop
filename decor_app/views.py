from django.shortcuts import render, redirect
from .models import Inventory
from django.shortcuts import render, redirect, get_object_or_404



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
def inventory_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')
        online_url = request.POST.get('online_url')
        description = request.POST.get('description')

        # फाइल्स पकड़ना
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        # डेटाबेस में नई रो क्रिएट करना
        if title and price:
            Inventory.objects.create(
                title=title,
                price=price,
                category=category,
                image=image,
                video=video,
                online_url=online_url,
                description=description
            )
            return redirect('inventory')

    # डेटाबेस से सारी इन्वेंटरी निकाल कर पेज को भेजना
    items = Inventory.objects.all().order_by('-created_at')
    return render(request, 'inventory.html', {'items': items})

# बुकिंग / डिटेल पेज का फंक्शन
def booking_page(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'booking_page.html', {'item': item})