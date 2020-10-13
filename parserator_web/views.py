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

        try:
            if not address:
                raise ParseError('Query did not contain an address.')
            else:
                address_components, address_type = self.parse(address)

                address_components_response = {
                    'input_string': address,
                    'address_components': address_components,
                    'address_type': address_type
                }

                return Response(address_components_response)
        except usaddress.RepeatedLabelError:
            raise ParseError(f"Unable to process address: {address}")


    def parse(self, address):
        address_components, address_type = usaddress.tag(address)
        return address_components, address_type