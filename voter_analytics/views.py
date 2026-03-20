# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 3/20/2026
# Description: View definitions for the voter_analytics application.
# This file defines the ListView for showing/filtering voters and
# the DetailView for showing one voter record.

from django.views.generic import DetailView, ListView

from .models import Voter


class VoterListView(ListView):
    """Display a paginated list of voters and allow filtering."""

    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """Return the queryset of voters after applying filters."""
        # Start with all voters ordered in a readable way.
        voter_list = super().get_queryset().order_by("last_name",
                                                     "first_name")

        # Filter by party affiliation if the user selected one.
        if "party_affiliation" in self.request.GET:
            party_affiliation = self.request.GET["party_affiliation"]
            if party_affiliation:
                voter_list = voter_list.filter(
                    party_affiliation=party_affiliation
                )

        # Filter by minimum year of birth if one was selected.
        if "min_dob" in self.request.GET:
            min_dob = self.request.GET["min_dob"]
            if min_dob:
                voter_list = voter_list.filter(
                    date_of_birth__year__gte=min_dob
                )

        # Filter by maximum year of birth if one was selected.
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

        # Filter by participation in each election checkbox.
        # Each checked box means the voter must have voted in that election.
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
        # Start with the superclass context data.
        context = super().get_context_data(**kwargs)

        # Provide all distinct party affiliations for the drop-down menu.
        party_choices = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .distinct()
            .order_by("party_affiliation")
        )

        # Provide a list of years for the date of birth drop-downs.
        birth_years = range(1900, 2027)

        # Provide the allowable voter scores.
        voter_scores = range(0, 6)

        # Add these lists to the template context.
        context["party_choices"] = party_choices
        context["birth_years"] = birth_years
        context["voter_scores"] = voter_scores

        # Save the user's current filter selections so the form keeps
        # previously selected values after the search is submitted.
        context["current_party_affiliation"] = self.request.GET.get(
            "party_affiliation", ""
        )
        context["current_min_dob"] = self.request.GET.get("min_dob", "")
        context["current_max_dob"] = self.request.GET.get("max_dob", "")
        context["current_voter_score"] = self.request.GET.get(
            "voter_score", ""
        )

        # Store checkbox state so checked boxes stay checked.
        context["current_v20state"] = "v20state" in self.request.GET
        context["current_v21town"] = "v21town" in self.request.GET
        context["current_v21primary"] = "v21primary" in self.request.GET
        context["current_v22general"] = "v22general" in self.request.GET
        context["current_v23town"] = "v23town" in self.request.GET

        return context


class VoterDetailView(DetailView):
    """Display the detail page for a single voter."""

    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "voter"

    def get_context_data(self, **kwargs):
        """Return the template context for one voter detail page."""
        # Start with the superclass context data.
        context = super().get_context_data(**kwargs)
        voter = context["voter"]

        # Build the full street address for display and Google Maps.
        full_address = (
            f"{voter.street_number} {voter.street_name}, "
            f"Newton, MA {voter.zip_code}"
        )

        # If there is an apartment number, include it in the address.
        if voter.apartment_number:
            full_address = (
                f"{voter.street_number} {voter.street_name}, "
                f"Apt {voter.apartment_number}, Newton, MA {voter.zip_code}"
            )

        # Add the formatted address to the context.
        context["full_address"] = full_address

        return context
