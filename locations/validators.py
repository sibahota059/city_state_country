from rest_framework import serializers
from .models import Country, State


def validate_country_id(country_id):
    """
    Validate that the country with the given ID exists.
    """
    try:
        return Country.objects.get(id=country_id)
    except Country.DoesNotExist:
        raise serializers.ValidationError(f"Country with ID {country_id} does not exist.")
    except ValueError:
        raise serializers.ValidationError("Country ID must be a valid integer.")


def validate_state_id(state_id, country_id=None):
    """
    Validate that the state with the given ID exists and optionally belongs to the specified country.
    """
    try:
        state = State.objects.get(id=state_id)
        if country_id and state.country_id != country_id:
            raise serializers.ValidationError(
                f"State with ID {state_id} does not belong to country with ID {country_id}."
            )
        return state
    except State.DoesNotExist:
        raise serializers.ValidationError(f"State with ID {state_id} does not exist.")
    except ValueError:
        raise serializers.ValidationError("State ID must be a valid integer.")