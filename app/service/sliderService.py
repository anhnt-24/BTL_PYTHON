from ..models import Slider

def getAllSlider():
    return Slider.objects.all()