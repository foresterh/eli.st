from django.template import RequestContext
from django.shortcuts import render_to_response
from item.models import Item, Attribute
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from utils.nlp import Parser
import json
import pdb


def get_friendly_message(item):
    response = [item.name]
    for item_attribute in item.get_attributes():
        response.push(item_attribute)
    return response.join(' ')


def inbox(request):
    if request.user.is_authenticated():
        return render_to_response('item/item_list.html', {},
             context_instance=RequestContext(request))
    else:
        return render_to_response('account/authentication.html', {},
            RequestContext(request))


def add_item(request):
    if request.method == 'POST':
        parser = Parser()
        chunks = parser.parse(text_input)
        item.name, item.value = chunks
        item = Item(name=request.POST["new_item"], created_by=request.user, details=request.POST["item_details"])

        item.save()

        attribute_name = request.POST["item_attribute"]
        attribute_value = request.POST["attribute_value"]

        item.add_attribute(attribute_name, attribute_value)

        result = {"name": item.name, "pk": item.pk, "alert": "Added " + get_friendly_message(item)}
        return HttpResponse(simplejson.dumps(result))


def add_attribute(request):
    if request.method == 'POST':
        attribute_type = request.POST["attribute_type"]
        name = request.POST["new_attribute"]

        attribute, created = Attribute.objects.get_or_create(name=name, datatype=attribute_type)

        result = {"name": attribute.name, "pk": attribute.pk}
        return HttpResponse(simplejson.dumps(result))


def get_items(request):
    items = Item.objects.filter(created_by=request.user)
    results = serializers.serialize('json', items, fields=('name', 'pk'))
    return HttpResponse(results)


def get_attributes(request):
    items = Attribute.objects.all()
    results = serializers.serialize('json', items, fields=('name', 'pk'))
    return HttpResponse(results)


def get_item(request, item_pk):
    item = Item.objects.get(pk=item_pk)
    items = item.itemattribute_set.all()
    results = serializers.serialize('json', items)
    return HttpResponse(results)


def run_command(request):
    if request.method == 'POST':
        parser = Parser()
        command = request.POST['command_text']
        response_data = parser.parse_command(command)
        #results = serializers.serialize('json', response_data)
        return HttpResponse(json.dumps(response_data))
        #return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
        return render_to_response('item/command_parser.html', {},
             context_instance=RequestContext(request))
