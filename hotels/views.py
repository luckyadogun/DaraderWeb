from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import HotelForm, RoomForm, HotelPhotosForm, FAQForm
from users.decorators import staff_or_manager_required
from .models import Hotel, HotelPhotos, Room, FAQ
# Create your views here.

@login_required
@staff_or_manager_required
def add_hotel_view(request):
    context = {}
    if request.is_ajax and request.method == "POST":
        hotel_form = HotelForm(request.POST)
        hotel_photos_form = HotelPhotosForm(request.POST, request.FILES)
        room_form = RoomForm(request.POST)
        faq_form = FAQForm(request.POST)
        forms = all([hotel_form.is_valid(), hotel_photos_form.is_valid(), room_form.is_valid(), faq_form.is_valid()])
        if forms:
            hotel_instance = hotel_form.save(commit=False)
            hotel_instance.creator = request.user
            hotel_instance.save()
            uploaded_images = request.FILES.getlist('photo') or request.FILES.get('photo')
            for image in uploaded_images:
                uploaded_image = HotelPhotos(photo=image, hotel=hotel_instance)
                uploaded_image.save()
            room = Room(
                room_name = room_form.cleaned_data['room_name'],
                price = room_form.cleaned_data['price'],
                information = room_form.cleaned_data['information'],
                hotel = hotel_instance
            )
            room.save()
            faq = FAQ(
                question = faq_form.cleaned_data['question'],
                answer = faq_form.cleaned_data['answer'],
                hotel = hotel_instance
            )
            faq.save()
            return JsonResponse({"result": "Success"})

        else:
            return JsonResponse({"result": "Failed"})
    else:
        print("get")
        hotel_form = HotelForm
        hotel_photos_form = HotelPhotosForm
        room_form = RoomForm
        faq_form = FAQForm
    context['hotel_form'] = hotel_form
    context['hotel_photos_form'] = hotel_photos_form
    context['room_form'] = room_form
    context['faq_form'] = faq_form

    return render(request, 'hotels/add_hotel.html', context)