import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .models import Item, Review


REVIEW_SCHEMA_GOODS = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 64,
        },
        'description': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 1024,
        },
        'price': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 1000000
        },
    },
    'required': ['title', 'description', 'price'],
}


REVIEW_SCHEMA_REVIEW = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 1024,
        },
        'grade': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 10
        },
    },
    'required': ['text', 'grade'],
}


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            validate(data, REVIEW_SCHEMA_GOODS)

            item = Item(title=data['title'], description=data['description'], price=data['price'])
            item.save()
            data = {'id': item.id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            data = json.loads(request.body)
            validate(data, REVIEW_SCHEMA_REVIEW)
            item = Item.objects.get(pk=item_id)
            post = Review(item=item, grade=data['grade'], text=data['text'])
            post.save()
            data = {'id': post.id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)
        except Item.DoesNotExist:
            return JsonResponse({'errors': 'Good does not exist'}, status=404)


class GetItemView(View):
    """View для получения информации о товаре.
    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """
    def get(self, request, item_id):
        try:
            # from pdb import set_trace; set_trace()
            item = Item.objects.get(pk=item_id)
            reviews = Review.objects.filter(item__review=item_id).order_by('-id')[:5]
            data = {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "price": item.price,
                "reviews": []
            }

            for review in reviews:
                data['reviews'].append({"id": review.id, "text": review.text, "grade": review.grade})

            return JsonResponse(data, status=200)
        except Item.DoesNotExist:
            return JsonResponse({'errors': 'Good does not exist'}, status=404)
