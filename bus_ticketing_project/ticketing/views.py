from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Bus

class BusListView(ListView):
    model = Bus
    template_name = 'ticketing/bus_list.html'  # This template will be created later
    context_object_name = 'buses'

class BusDetailView(DetailView):
    model = Bus
    template_name = 'ticketing/bus_detail.html'  # This template will be created later
    context_object_name = 'bus'

class BusCreateView(CreateView):
    model = Bus
    template_name = 'ticketing/bus_form.html'  # This template will be created later
    fields = ['bus_name', 'source', 'destination', 'departure_time', 'arrival_time', 'price']
    success_url = reverse_lazy('bus_list')  # This URL name will be defined in urls.py

class BusUpdateView(UpdateView):
    model = Bus
    template_name = 'ticketing/bus_form.html' # Reuses the form template
    fields = ['bus_name', 'source', 'destination', 'departure_time', 'arrival_time', 'price']
    success_url = reverse_lazy('bus_list')

class BusDeleteView(DeleteView):
    model = Bus
    template_name = 'ticketing/bus_confirm_delete.html'  # This template will be created later
    success_url = reverse_lazy('bus_list')

# Workflow test trigger comment
