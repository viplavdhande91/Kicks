from .models import *
from django.db import models




casualshoes ='casualshoes'
formalshoes ='formalshoes'
sneakers = "sneakers"
studds = "studds"

    
CATEGORY_CHOICES = [
    (casualshoes, 'casualshoes'),
    (formalshoes, 'formalshoes'),
    (sneakers, 'sneakers'),
    (studds, 'studds'),

   
    ]






INSTOCK = 1
OUTOFSTOCK = 0

  
AVAILABILITY = [
    (INSTOCK, 'INSTOCK'),
    (OUTOFSTOCK, 'OUTOFSTOCK'),
   
   
    ]




addidas ='addidas'
puma ='puma'
nike ='nike'
sketchers ='sketchers'

  
BRANDS = [
    (addidas, 'addidas'),
    (puma, 'puma'),
    (nike, 'nike'),

    (sketchers, 'sketchers'),

   
   
    ]



turquoise ='turquoise'
gray ='gray'
orange ='orange'
yellow ='yellow'
green ='green'
purple ='purple'
blue ='blue'
white = 'white'



  
COLORS = [
    (turquoise, 'turquoise'),
    (gray, 'gray'),
    (orange, 'orange'),

    (yellow, 'yellow'),

    (green, 'green'),

    (purple, 'purple'),
    (blue, 'blue'),
    (white, 'white'),




   
   
    ]





ordered ='ordered'
packed ='packed'
shipped ='shipped'
delivered ='delivered'

  
TRACKING = [
    (ordered, 'ordered'),
    (packed, 'packed'),
    (shipped, 'shipped'),

    (delivered, 'delivered'),

   
   
    ]