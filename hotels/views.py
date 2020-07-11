from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from users.decorators import staff_or_manager_required
from .forms import HotelForm, RoomForm, HotelPhotosForm, FAQForm
from .models import Hotel, HotelPhotos, Room, FAQ


@login_required
@staff_or_manager_required
def add_hotel_view(request):
    context = {}
    if request.is_ajax and request.method == "POST":
        hotel_form = HotelForm(request.POST)
        hotel_photos_form = HotelPhotosForm(request.POST, request.FILES)
        room_form = RoomForm(request.POST)
        faq_form = FAQForm(request.POST)
        forms = all(
            [hotel_form.is_valid(), hotel_photos_form.is_valid(),
                room_form.is_valid(), faq_form.is_valid()])
        if forms:
            hotel_instance = hotel_form.save(commit=False)
            hotel_instance.creator = request.user
            hotel_instance.save()
            # We don't need the or the getlist will retrn a list even if it contains a single item
            # uploaded_images = request.FILES.getlist('photo') or request.FILES.get('photo')
            uploaded_images = request.FILES.getlist('photo')
            # Since the form accept submission without images
            # Make sure you don't loop when the image list is empty
            if uploaded_images:
                for image in uploaded_images:
                    uploaded_image = HotelPhotos(photo=image, hotel=hotel_instance)
                    uploaded_image.save()
            room_names = request.POST.getlist('room_name')
            prices = request.POST.getlist('price')
            infos = request.POST.getlist('information')
            for name, price, info in zip(room_names, prices, infos):
                room = Room(
                    room_name=name,
                    price=price,
                    information=info,
                    hotel=hotel_instance
                )
                room.save()
            questions = request.POST.getlist('question')
            answers = request.POST.getlist('answer')
            for question, answer in zip(questions, answers):
                faq = FAQ(
                    question=question,
                    answer=answer,
                    hotel=hotel_instance
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
