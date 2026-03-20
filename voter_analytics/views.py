# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 3/20/2026
# Description: View definitions for the voter_analytics application.
# This file defines views for listing voters, viewing one voter, and
# displaying graphs of aggregate voter data.

from django.views.generic import DetailView, ListView
import plotly
import plotly.graph_objs as go

from .models import Voter


class VoterListView(ListView):
    """Display a paginated list of voters and allow filtering."""

    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """Return the queryset of voters after applying filters."""
        voter_list = super().get_queryset().order_by("last_name",
                                                     "first_name")

        # Filter by party affiliation if the user selected one.
        if "party_affiliation" in self.request.GET:
            party_affiliation = self.request.GET["party_affiliation"]
            if party_affiliation:
                voter_list = voter_list.filter(
                    party_affiliation=party_affiliation
                )

        # Filter by minimum year of birth if the user selected one.
        if "min_dob" in self.request.GET:
            min_dob = self.request.GET["min_dob"]
            if min_dob:
                voter_list = voter_list.filter(
                    date_of_birth__year__gte=min_dob
                )

        # Filter by maximum year of birth if the user selected one.
        if "max_dob" in self.request.GET:
            max_dob = self.request.GET["max_dob"]
            if max_dob:
                voter_list = voter_list.filter(
                    date_of_birth__year__lte=max_dob
                )

        # Filter by voter score if the user selected one.
        if "voter_score" in self.request.GET:
            voter_score = self.request.GET["voter_score"]
            if voter_score:
                voter_list = voter_list.filter(voter_score=voter_score)

        # Filter by election participation checkboxes.
        if "v20state" in self.request.GET:
            voter_list = voter_list.filter(v20state=True)

        if "v21town" in self.request.GET:
            voter_list = voter_list.filter(v21town=True)

        if "v21primary" in self.request.GET:
            voter_list = voter_list.filter(v21primary=True)

        if "v22general" in self.request.GET:
            voter_list = voter_list.filter(v22general=True)

        if "v23town" in self.request.GET:
            voter_list = voter_list.filter(v23town=True)

        return voter_list

    def get_context_data(self, **kwargs):
        """Return the template context for the voter list page."""
        context = super().get_context_data(**kwargs)

        # Provide values needed by the filtering form.
        party_choices = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .distinct()
            .order_by("party_affiliation")
        )
        birth_years = range(1900, 2027)
        voter_scores = [0, 1, 2, 3, 4, 5]

        context["party_choices"] = party_choices
        context["birth_years"] = birth_years
        context["voter_scores"] = voter_scores

        # Keep track of previously selected form values.
        context["current_party_affiliation"] = self.request.GET.get(
            "party_affiliation", ""
        )
        context["current_min_dob"] = self.request.GET.get("min_dob", "")
        context["current_max_dob"] = self.request.GET.get("max_dob", "")
        context["current_voter_score"] = self.request.GET.get(
            "voter_score", ""
        )

        context["current_v20state"] = "v20state" in self.request.GET
        context["current_v21town"] = "v21town" in self.request.GET
        context["current_v21primary"] = "v21primary" in self.request.GET
        context["current_v22general"] = "v22general" in self.request.GET
        context["current_v23town"] = "v23town" in self.request.GET

        context["clear_url"] = "/voter_analytics/"
        
        query_dict = self.request.GET.copy()

        # Remove the existing page number so pagination links can add the
        # new page number without duplicating the parameter.
        if "page" in query_dict:
            del query_dict["page"]

        context["current_query"] = query_dict.urlencode()

        return context


class VoterDetailView(DetailView):
    """Display the detail page for a single voter."""

    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        """Return the template context for one voter detail page."""
        context = super().get_context_data(**kwargs)
        voter = context["voter"]

        # Build a full address string for the Google Maps link.
        if voter.apartment_number:
            full_address = (
                f"{voter.street_number} {voter.street_name}, "
                f"Apt {voter.apartment_number}, Newton, MA "
                f"{voter.zip_code}"
            )
        else:
            full_address = (
                f"{voter.street_number} {voter.street_name}, "
                f"Newton, MA {voter.zip_code}"
            )

        context["full_address"] = full_address
        return context


class GraphsView(ListView):
    """Display graphs of aggregate voter data."""

    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_queryset(self):
        """Return the queryset of voters after applying filters."""
        voter_list = super().get_queryset().order_by("last_name",
                                                     "first_name")

        # Filter by party affiliation if the user selected one.
        if "party_affiliation" in self.request.GET:
            party_affiliation = self.request.GET["party_affiliation"]
            if party_affiliation:
                voter_list = voter_list.filter(
                    party_affiliation=party_affiliation
                )

        # Filter by minimum year of birth if the user selected one.
        if "min_dob" in self.request.GET:
            min_dob = self.request.GET["min_dob"]
            if min_dob:
                voter_list = voter_list.filter(
                    date_of_birth__year__gte=min_dob
                )

        # Filter by maximum year of birth if the user selected one.
        if "max_dob" in self.request.GET:
            max_dob = self.request.GET["max_dob"]
            if max_dob:
                voter_list = voter_list.filter(
                    date_of_birth__year__lte=max_dob
                )

        # Filter by voter score if the user selected one.
        if "voter_score" in self.request.GET:
            voter_score = self.request.GET["voter_score"]
            if voter_score:
                voter_list = voter_list.filter(voter_score=voter_score)

        # Filter by election participation checkboxes.
        if "v20state" in self.request.GET:
            voter_list = voter_list.filter(v20state=True)

        if "v21town" in self.request.GET:
            voter_list = voter_list.filter(v21town=True)

        if "v21primary" in self.request.GET:
            voter_list = voter_list.filter(v21primary=True)

        if "v22general" in self.request.GET:
            voter_list = voter_list.filter(v22general=True)

        if "v23town" in self.request.GET:
            voter_list = voter_list.filter(v23town=True)

        return voter_list

    def get_context_data(self, **kwargs):
        """Return the template context for the graphs page."""
        context = super().get_context_data(**kwargs)

        # Provide values needed by the filtering form.
        party_choices = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .distinct()
            .order_by("party_affiliation")
        )
        birth_years = range(1900, 2027)
        voter_scores = [0, 1, 2, 3, 4, 5]

        context["party_choices"] = party_choices
        context["birth_years"] = birth_years
        context["voter_scores"] = voter_scores

        # Keep track of previously selected form values.
        context["current_party_affiliation"] = self.request.GET.get(
            "party_affiliation", ""
        )
        context["current_min_dob"] = self.request.GET.get("min_dob", "")
        context["current_max_dob"] = self.request.GET.get("max_dob", "")
        context["current_voter_score"] = self.request.GET.get(
            "voter_score", ""
        )

        context["current_v20state"] = "v20state" in self.request.GET
        context["current_v21town"] = "v21town" in self.request.GET
        context["current_v21primary"] = "v21primary" in self.request.GET
        context["current_v22general"] = "v22general" in self.request.GET
        context["current_v23town"] = "v23town" in self.request.GET

        # Use the filtered queryset to build all graphs.
        voters = self.get_queryset()

        
        # Graph 1: Distribution of voters by year of birth.
        year_counts = {}

        # Count how many voters were born in each year.
        for voter in voters:
            birth_year = voter.date_of_birth.year

            if birth_year in year_counts:
                year_counts[birth_year] += 1
            else:
                year_counts[birth_year] = 1

        # Sort the years so the bars appear in chronological order.
        x_years = sorted(year_counts.keys())
        y_year_counts = []

        # Build the y-values in the same order as the sorted years.
        for year in x_years:
            y_year_counts.append(year_counts[year])

        fig_year = go.Bar(x=x_years, y=y_year_counts)
        graph_div_year = plotly.offline.plot(
            {
                "data": [fig_year],
                "layout": {
                    "title": (
                        f"Voter Distribution by Year of Birth "
                        f"(n={len(voters)})"
                    ),
                    "xaxis": {
                        "type": "category",
                    },
                },
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_year"] = graph_div_year

      
        # Graph 2: Distribution of voters by party affiliation.
        party_counts = {}

        # Count how many voters belong to each party affiliation.
        for voter in voters:
            party = voter.party_affiliation

            if party in party_counts:
                party_counts[party] += 1
            else:
                party_counts[party] = 1

        x_parties = list(party_counts.keys())
        y_party_counts = list(party_counts.values())

        fig_party = go.Pie(labels=x_parties, values=y_party_counts)
        graph_div_party = plotly.offline.plot(
            {
                "data": [fig_party],
                "layout_title_text":
                    f"Voter Distribution by Party Affiliation "
                    f"(n={len(voters)})",
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_party"] = graph_div_party

       
        # Graph 3: Count of voters who voted in each election.

        # Store the election field names in the order they should appear
        # on the x-axis of the bar chart.
        election_names = [
            "v20state",
            "v21town",
            "v21primary",
            "v22general",
            "v23town",
        ]

        # Count how many voters in the filtered queryset voted in each
        # of the five elections.
        election_counts = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]

        # Create a bar chart showing the count of voters who voted in
        # each election.
        fig_election = go.Bar(x=election_names, y=election_counts)

        # Convert the bar chart into an HTML div so it can be displayed
        # in the template.
        graph_div_election = plotly.offline.plot(
            {
                "data": [fig_election],
                "layout_title_text":
                    f"Vote Count by Election (n={len(voters)})",
            },
            auto_open=False,
            output_type="div",
        )

        # Add the graph div to the template context.
        context["graph_div_election"] = graph_div_election

        context["clear_url"] = "/voter_analytics/graphs"

        query_dict = self.request.GET.copy()

        # Remove the existing page number so pagination links can add the
        # new page number without duplicating the parameter.
        if "page" in query_dict:
            del query_dict["page"]

        context["current_query"] = query_dict.urlencode()

        return context