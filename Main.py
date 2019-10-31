# -*- coding: utf-8 -*-

from ContentFactory import *

# a simple demo for the Whatsapp content manager

def whatsappDemo():
    contact = "ofek tal"
    wcm = ContentFactory.getContentManager("whatsapp", contact=contact)
    wcm.startAutolFetch(1)
    #wcm.analyzeTimeFrames()
    #wcm.showGraph()
    #time.sleep(500)


def main():
    whatsappDemo()


if __name__ == '__main__':
    main()



