from BBCContentManager import *
from FlightsContentManager import *
from WhatsappContentManager import *

class ContentFactory:
    # a simple factory for content managers
    def getContentManager(str,**kwargs):
        if(str == "whatsapp"):
            return WhatsappContentManager(kwargs["contact"])

        return None

    def listTypes(*args):
        return ("bbc", "flights", "whatsapp")
