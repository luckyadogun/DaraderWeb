from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404

from users.decorators import staff_or_manager_required
from .helpers import hotel_email_booking_request, user_hotel_email_booking_request
from .forms import HotelForm, RoomForm, HotelPhotosForm, FAQForm, HotelBookingRequestForm, HotelUpdateForm, HotelPhotosUpdateForm
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


# @login_required
def hotel_details(request, name):
    context = {}

    obj = Hotel.objects.get(name=name)

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
    context["images"] = [x.photo.url for x in obj.hotelPhotos.all()]    
    context["hotel_bookingform"] = hotel_bookingform

    return render(request, 'hotels/single_hotel.html', context)

@method_decorator([staff_or_manager_required], name='dispatch')
class MyHotelView(LoginRequiredMixin, ListView):
    template_name = "hotels/my_hotels.html"
    context_object_name = "hotels"
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_staff:
            return Hotel.objects.filter(creator=self.request.user)

@login_required(login_url='properties:login')
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
        hotel_email_booking_request(hotel_email, hotel_name, user_name, room_name, user_email)        
        user_hotel_email_booking_request(user_email, user_name, room_name, hotel_name)
        return JsonResponse({"result": "Success"})
    except Room.DoesNotExist:
        return JsonResponse({"result": "Failed"})
    except Hotel.DoesNotExist:
        return JsonResponse({"result": "Failed"})

@login_required
@staff_or_manager_required
def hotel_delete_view(request):
    if request.is_ajax and request.method == "POST":
        hotel_id = request.POST.get("hotelID")
        hotel_obj = get_object_or_404(Hotel, pk=hotel_id)

        if hotel_obj.creator == request.user:
            hotel_obj.delete()
            return JsonResponse({"result": "Success!"})
        return JsonResponse({"result": "Unauthorized Access!"})
    raise Http404("Page Doesn't Exist!")

@login_required
@staff_or_manager_required
def update_hotel(request, name=None):
    context = {}

    hotel_obj = get_object_or_404(Hotel, name=name)

    if not hotel_obj.creator == request.user:
        raise Http404("Unauthorized access!")

    if request.is_ajax and request.method == "POST":

        hotel_form = HotelUpdateForm(request.POST, instance=hotel_obj)
        hotel_photos_form = HotelPhotosUpdateForm(request.POST, request.FILES)
        forms = all([
                hotel_form.is_valid(),
                hotel_photos_form.is_valid()])
        if forms:
            hotel_instance = hotel_form.save()
            uploaded_images = request.FILES.getlist('photo')
            if uploaded_images:
                for image in uploaded_images:
                    uploaded_image = HotelPhotos(photo=image, hotel=hotel_instance)
                    uploaded_image.save()
            faq_ids = request.POST.getlist('faq_id')
            questions = request.POST.getlist('question')
            answers = request.POST.getlist('answer')
            room_ids = request.POST.getlist('room_id')
            room_names = request.POST.getlist('room_name')
            prices = request.POST.getlist('price')
            infos = request.POST.getlist('information')
            for room_id, room_name, room_price, room_info in zip(room_ids, room_names, prices, infos):
                # If the room has an id, then update its details
                if room_id:
                    room_instance = Room.objects.get(id=room_id)
                    room_instance.room_name = room_name
                    room_instance.price = room_price
                    room_instance.information = room_info
                    room_instance.save()
                # If it doesn't have an id, create a new room as it doesn't exist
                else:
                    room_instance = Room(room_name=room_name, price=room_price, information=room_info, hotel=hotel_instance)
                    room_instance.save()
            for faq_id, question, answer in zip(faq_ids, questions, answers):
                # If the faq has an id, update the room details
                if faq_id:
                    faq_instance = FAQ.objects.get(id=faq_id)
                    faq_instance.question = question
                    faq_instance.answer = answer
                    faq_instance.save()
                # If the faq doesn't have an id, create a new room
                else:
                    faq_instance = FAQ(question=question, answer=answer, hotel=hotel_instance)
                    faq_instance.save()            
            return JsonResponse({"result": "Success"})
    else:
        hotel_form = HotelUpdateForm(instance=hotel_obj)
        hotel_photos_form = HotelPhotosUpdateForm()
    context["hotel_form"] = hotel_form
    context["hotel_photos_form"] = hotel_photos_form
    context["hotel"] = hotel_obj

    return render(request, 'hotels/update_hotel.html', context)

# ALL HOTELS
class AllHotelView(ListView):
    template_name = "hotels/all_hotels.html"
    context_object_name = "hotels"
    paginate_by = 5

    def get_queryset(self):
        return Hotel.objects.order_by("created").reverse()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_hotels"] = Hotel.objects.order_by("created").reverse()[:3]
        return context

# class SearchResultView(ListView):

#     template_name = "properties/serp.html"
#     context_object_name = "properties"
#     paginate_by = 5

#     def get_queryset(self):

#         search_title = self.request.GET.get("location", "")
#         property_type = self.request.GET.get("property-type", "")
#         property_category = self.request.GET.get("property-category", "")
#         bedrooms = self.request.GET.get("bedrooms", 1)
#         bathrooms = self.request.GET.get("bathrooms", 1)
#         budget = self.request.GET.get("budget", "200000 - 300000").split("-")
#         basketball = self.request.GET.get("basketball")
#         swimming_pool = self.request.GET.get("swimming-pool")
#         gym = self.request.GET.get("gym")
#         wheelchair = self.request.GET.get("wheelchair")

#         submit_action = self.request.GET.get("submit")

#         new_query = PropertyDetails.objects.filter(
#             Q(property_obj__title__icontains=search_title) |
#             Q(property_obj__property_type=property_type) |
#             Q(property_obj__property_category=property_category) |
#             Q(bedrooms=int(bedrooms)) | Q(bathrooms=int(bathrooms)) |
#             Q(property_obj__price__range=(int(budget[0]), int(budget[1]))) |
#             Q(has_basketball_court=bool(basketball)) |
#             Q(has_swimming_pool=bool(swimming_pool)) | Q(has_gym=bool(gym)) |
#             Q(is_wheelchair_friendly=bool(wheelchair))
#             )

#         category_param = ["rent", "sale", "lease", ]

#         type_param = [
#             "flat", "land",
#             "house", "commercial",
#             "event centre", ]

#         if self.kwargs["queryset"] == "search":
#             if submit_action:
#                 return new_query
#             else:
#                 try:
#                     return [PropertyDetails.objects.get(pk=qs) for qs in self.request.session["query"]]
#                 except KeyError:
#                     return ""

#         if self.kwargs["queryset"] in category_param:
#             if submit_action:
#                 return new_query
#             else:
#                 return PropertyDetails.objects.filter(
#                     property_obj__property_category=self.kwargs["queryset"])

#         if self.kwargs["queryset"] in type_param:
#             if submit_action:
#                 return new_query
#             else:
#                 return PropertyDetails.objects.filter(
#                     property_obj__property_type=self.kwargs["queryset"])

#         if self.kwargs["queryset"] == "all":
#             if submit_action:
#                 return new_query
#             else:
#                 return PropertyDetails.objects.all()

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs"] = self.request.META["QUERY_STRING"]
#         context["recent_properties"] = Property.objects.order_by("created")[:5]
#         context["total_flats"] = Property.objects.filter(
#                                     property_type="flat").count()
#         context["total_houses"] = Property.objects.filter(
#                                     property_type="house").count()
#         context["total_lands"] = Property.objects.filter(
#                                     property_type="land").count()
#         context["total_commercials"] = Property.objects.filter(
#                                     property_type="commercial").count()
#         context["total_event_centres"] = Property.objects.filter(
#                                     property_type="event centre").count()
#         return context
