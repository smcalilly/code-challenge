import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        address = request.query_params.get('address')

        if not address:
            raise ParseError('Query did not contain an address.')
        else:
            parsed_address = self.parse(address)
            return Response(parsed_address)


    def parse(self, address):
        try:
            parsed_address_results = usaddress.tag(address)

            parsed_address = {
                'input_string': address,
                'address_components': parsed_address_results[0],
                'address_type': parsed_address_results[1]
            }

            return parsed_address
        except usaddress.RepeatedLabelError:
            raise ParseError(f"Unable to process address: {address}")