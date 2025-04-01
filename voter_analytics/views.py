from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView
from .models import Voter
from .forms import VoterFilterForm
from django.db.models import Q

from django.db import models


class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth']:
                queryset = queryset.filter(date_of_birth__gte=form.cleaned_data['min_birth'])
            if form.cleaned_data['max_birth']:
                queryset = queryset.filter(date_of_birth__lte=form.cleaned_data['max_birth'])
            voter_score = form.cleaned_data['voter_score']
            if voter_score not in (None, ''):
                queryset = queryset.filter(voter_score=int(voter_score))
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field):
                    queryset = queryset.filter(**{field: True})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        import plotly.express as px
        from django.utils.html import mark_safe
        from .forms import VoterFilterForm
        from .models import Voter

        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET)
        voters = Voter.objects.all()

        if form.is_valid():
            cd = form.cleaned_data
            if cd['party_affiliation']:
                voters = voters.filter(party_affiliation=cd['party_affiliation'])
            if cd['min_birth']:
                voters = voters.filter(date_of_birth__gte=cd['min_birth'])
            if cd['max_birth']:
                voters = voters.filter(date_of_birth__lte=cd['max_birth'])
            if cd['voter_score'] not in (None, ''):
                voters = voters.filter(voter_score=int(cd['voter_score']))
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if cd.get(field):
                    voters = voters.filter(**{field: True})

        # Birth year histogram
        birth_years = voters.values_list('date_of_birth', flat=True)
        birth_years = [d.year for d in birth_years if d]

        fig1 = px.histogram(
            x=birth_years,
            nbins=60,
            title=f"Voter distribution by Year of Birth (n={voters.count()})",
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
        )

        fig1.update_traces(marker_color='rgba(50, 100, 255, 0.8)')

        fig1.update_layout(
            height=500,
            width=900,
            bargap=0.1,
            xaxis=dict(tickangle=-45, title='Year of Birth'),
            yaxis=dict(title='Number of Voters'),
            margin=dict(t=80, l=40, r=40, b=60),
        )
        birth_histogram = mark_safe(fig1.to_html(full_html=False))

        # Party affiliation pie chart
        party_counts = voters.values('party_affiliation').annotate(count=models.Count('id'))
        fig2 = px.pie(
            names=[p['party_affiliation'] for p in party_counts],
            values=[p['count'] for p in party_counts],
            title=f"Voter distribution by Party Affiliation (n={voters.count()})",
            hole=0  # You can change to 0.3 for a donut
        )

        fig2.update_traces(
            textinfo='percent+label',
            textposition='inside',
            marker=dict(line=dict(color='#000000', width=1))
        )

        fig2.update_layout(
            height=600,
            width=600,
            showlegend=True,
            margin=dict(t=80, l=20, r=20, b=20),
            legend=dict(orientation="v", x=1.05, y=0.5),
        )

        party_pie = mark_safe(fig2.to_html(full_html=False))

        # Election participation bar chart
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        participation_counts = [voters.filter(**{e: True}).count() for e in elections]
        fig3 = px.bar(x=elections, y=participation_counts, title="Election Participation")
        election_bar = mark_safe(fig3.to_html(full_html=False))

        context['form'] = form
        context['charts'] = {
            'birth_histogram': birth_histogram,
            'party_pie': party_pie,
            'election_bar': election_bar,
        }

        return context

