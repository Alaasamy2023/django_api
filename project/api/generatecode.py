import datetime
import random
from django.http import JsonResponse
from django.views import View

# وظائف أخرى  
#    do it 
def generate_code_view(request):
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S%f")
    random.seed(int(now_str))
    unique_code = random.randint(1000, 9999)
    return JsonResponse({'unique_code': unique_code})

class GenerateCodeView_cbv(View):
    def get(self, request):
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S%f")
        random.seed(int(now_str))
        unique_code = random.randint(1000, 9999)
        return JsonResponse({'unique_code': unique_code})