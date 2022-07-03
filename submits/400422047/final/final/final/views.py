from rest_framework.response import Response
from rest_framework.views import APIView

from final.hw1 import interpolate1
from final.hw2 import interpolate2
from final.hw3 import handle_outlier
from final.hw4 import over_under_sample
from final.serializers import YegInputSerializer


class HW1View(APIView):
    """
    Interpolates missing values
    """

    def post(self, request):
        data = request.data
        res = interpolate1(data)
        return Response(res)


class HW2View(APIView):

    def post(self, request):
        data = request.data
        res = interpolate2(data)
        return Response(res)


class HW3View(APIView):

    def post(self, request):
        data = request.data
        res = handle_outlier(data)
        return Response(res)


class HW4View(APIView):

    def post(self, request):
        data = request.data
        res = over_under_sample(data)
        return Response(res)
