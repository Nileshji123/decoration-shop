from django.db import models

class Inventory(models.Model):
    CATEGORY_CHOICES = [
        ('birthday', 'बर्थडे पार्टी (Birthday)'),
        ('wedding', 'वेडिंग व स्टेज (Wedding)'),
        ('anniversary', 'एनिवर्सरी (Anniversary)'),
        ('baby_shower', 'बेबी शॉवर / नामकरण'),
    ]

    title = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='birthday')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    online_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.price}"

# ==========================================
# MULTIPLE MEDIA GALLERY MODEL (PHOTO / VIDEO)
# ==========================================
class DecorationMedia(models.Model):
    # मुख्य इन्वेंटरी आइटम के साथ कनेक्शन
    inventory = models.ForeignKey(
        Inventory, 
        related_name='gallery', 
        on_delete=models.CASCADE
    )
    
    # यह फील्ड फोटो और वीडियो दोनों फाइलों को एक्सेप्ट करेगी
    media_file = models.FileField(upload_to='gallery/')
    
    # यह चेक करने के लिए कि फाइल वीडियो है या इमेज (वैकल्पिक)
    is_video = models.BooleanField(default=False)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory.title} - Media #{self.id}"