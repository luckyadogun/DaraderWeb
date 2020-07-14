from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from users.decorators import staff_or_manager_required
from .helpers import hotel_email_booking_request, user_hotel_email_booking_request
from .forms import HotelForm, RoomForm, HotelPhotosForm, FAQForm, HotelBookingRequestForm
from .models import Hotel, HotelPhotos, Room, FAQ, HotelBookingRequest, BookmarkedHotel


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
        hotel_form = HotelForm
        hotel_photos_form = HotelPhotosForm
        room_form = RoomForm
        faq_form = FAQForm
    context['hotel_form'] = hotel_form
    context['hotel_photos_form'] = hotel_photos_form
    context['room_form'] = room_form
    context['faq_form'] = faq_form

    return render(request, 'hotels/add_hotel.html', context)

# @method_decorator([login_required], name='dispatch')
# class MyHotelBookingsView(LoginRequiredMixin, ListView):
#     template_name = "hotels/my_hotel_bookings.html"
#     context_object_name = "hotel_bookings"
#     paginate_by = 10

#     def get_queryset(self):
#         return HotelBookingRequest.objects.filter(
#             client=self.request.user,
#             status="booked")

@login_required
def hotel_details(request, pk):
    context = {}

    obj = Hotel.objects.get(id=pk)

    if request.method == "POST":
        hotel_bookingform = HotelBookingRequestForm(request.POST)

        if hotel_bookingform.is_valid():
            booking_obj = bookingform.save(commit=False)
            booking_obj.company = obj.property_obj.owner
            booking_obj.property_details = obj
            booking_obj.client = request.user
            booking_obj.status = "booked"
            booking_obj.save()
            email_booking_request(request, obj.property_obj.owner.manager)
            messages.success(request, "Successfully Booked!")
        else:
            messages.error(request, hotel_bookingform.errors)

    else:
        hotel_bookingform = HotelBookingRequestForm()

    context["object"] = obj
    context["recent_hotels"] = Hotel.objects.order_by("created").reverse()[:3]
    # context["featured"] = get_currently_featured()
    context["images"] = [x.photo.url for x in obj.hotelPhotos.all()]
    # context["similar"] = PropertyDetails.objects.filter(
    #     Q(property_obj__title__icontains=obj.property_obj.title) |
    #     Q(property_obj__property_type=obj.property_obj.property_type) |
    #     Q(property_obj__lga=obj.property_obj.lga) |
    #     Q(property_obj__owner=obj.property_obj.owner)
    # )
    context["hotel_bookingform"] = hotel_bookingform

    return render(request, 'hotels/single_hotel.html', context)

@login_required
def hotel_booking_view(request):
    room_id = request.POST.get('room_id')
    hotel_id = request.POST.get('hotel_id')
    try:
        room = Room.objects.get(pk=room_id)
        hotel = Hotel.objects.get(pk=hotel_id)
        hotel_email = hotel.creator.email
        hotel_name = hotel.name
        room_name = room.room_name
        user_name = request.user.username
        user_email = request.user.email
        # Send the mail containing the user, room and hotel to the management
        hotel_email_booking_request(hotel_email, hotel_name, user_name, room_name, user_email)
        # Send the mail containing the hotel and room to the user
        user_hotel_email_booking_request(user_email, user_name, room_name, hotel_name)
        return JsonResponse({"result": "Success"})
    except Room.DoesNotExist:
        return JsonResponse({"result": "Failed"})
    except Hotel.DoesNotExist:
        return JsonResponse({"result": "Failed"})