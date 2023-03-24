from rest_framework_simplejwt.tokens import RefreshToken
from customer.models import Customer

# get the tokens


def generate_token(user: Customer):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access_token": str(refresh.access_token),
        "refresh": str(refresh),
    }
    return tokens
