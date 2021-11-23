# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.types import DomainDict
#
#
# global variables


out_of_scoope = False
table_available = ['2','4','6','8','10']

closing_time = { 0:'10 pm', 1:'10 pm', 2:'10 pm', 3:'10 pm',4:'midnght',5:'midnight',6:'10pm' }
opening_time = { 0:'10 am', 1:'10 am', 2:'10 am', 3:'10 am',4:'11 am',5:'11 am',6:'11 am' }
booked_list = [ 'Harouna', 'Santiago', 'Amen']
booked_list_ready = [ 'Harouna', 'Santiago']



class ActionBookTableForm(Action):
    def name(self) -> Text:
        return "booked_table_action"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)

        if entities[0]['value']   in booked_list:

            if entities[0]['value'] in booked_list_ready:
                dispatcher.utter_message(text=f" Yes Your table is ready ! please follow me")
            else:
                dispatcher.utter_message(text=f" Your table is not ready yet but be patient it won't take too long")  

  
        else:
        
            dispatcher.utter_message(text=f"Sorry we don't have any booked table on the name of " + entities[0]['value'])


        return []




class ActionPickUp(Action):
    def name(self) -> Text:
        return "pick_up_action"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        entities = tracker.latest_message['entities']
        print(entities)

        if entities[0]['value']  in booked_list:

            if entities[0]['value'] in booked_list_ready:
                dispatcher.utter_message(text=" Yes Your order is ready ! A waiter will bring it to you")
            else:
                dispatcher.utter_message(text=" Your order is not ready yet but be patient it won't take too long")  

             
        else:
        
            dispatcher.utter_message(text="Sorry we don't have any order on the name of  " + entities[0]['value'] )
        
        return []
        
            

class ActionCustomFallback(Action):
    
    
    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        global out_of_scoope
             
        if  not out_of_scoope :
               dispatcher.utter_message(text=" Sorry I didn't get that please repeat again ! " )
               out_of_scoope = True
        else: 
                dispatcher.utter_message(text=" Sorry I'm not understanding what you saying! Please wait, I'm going to find a waiter to help you ! " )
                out_of_scoope = False


         

        return []



class ActionSearchTable(Action):

    def name(self) -> Text:
        return "search_for_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        #print(entities)

        for e in range(len(entities)):
            if entities[e]['entity'] == 'person':
                name = entities[e]


        if name['value'] in table_available:

            dispatcher.utter_message(text=" Yes we have a table available for " + name['value'] + " poeple.  Please follow me ")

        else:
            dispatcher.utter_message(text=" we don't have any available table for " + name['value'] + " do you mind to wait !")
        return []

class ActionSearchRestaurant(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'hotel':
                name = e['value']

            if name == "indian":
                message = " Idian1, Idian2, Indian3"
            if name == "chineese":
                message = "chineese1, chineese2, chineese3"

        dispatcher.utter_message(text=message)

        return []

class ActionHowToOrder(Action):

    def name(self) -> Text:
        return "how_to_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)

        for e in range(len(entities)):
            if entities[e]['entity'] == 'order':
                name = entities[e]

            if name['value'] == "tablet":
                message = " Make your order and press submit button when you are done! "
            if name['value'] == "human":
                message = "One of the waiters will be with you soon!"

        dispatcher.utter_message(text=message)

        return []
class ActionSearchDrinks(Action):

    def name(self) -> Text:
        return "search_drinks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        drinks = tracker.get_slot("drink")
        my_drinks = ""

        j=0
        for s in drinks:

            my_drinks = my_drinks + s
            if j != (len(drinks)-1):
                if j == (len(drinks)-2):
                    my_drinks += " and "
                else:
                    my_drinks += ", "
            j = j + 1

        dispatcher.utter_message(text= " I'll be right back with " + my_drinks)


        return []

class ActionClosingTime(Action):

    def name(self) -> Text:
        return "check_closing_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        day = tracker.latest_message['entities']
        print(day)

        if day[1]['value'] == 'today':

            the_day = datetime.today().weekday()

        if day[1]['value'] == 'tomorrow':

            the_day = datetime.today().weekday() +1

        if day[1]['value'] == 'yesterday':
            
            the_day = datetime.today().weekday() -1 

            if the_day == -1:
                the_day = 6   

        closingtime = str(closing_time[the_day])
        dispatcher.utter_message(text= " The restaurant closes at " + closingtime + " " +str(day[1]['value']))


        return []      

          
class ActionOpeningTime(Action):

    def name(self) -> Text:
        return "check_opening_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        day = tracker.latest_message['entities']


        if day[1]['value'] == 'today':

            the_day = datetime.today().weekday()

        if day[1]['value'] == 'tomorrow':

            the_day = datetime.today().weekday() +1

        if day[1]['value'] == 'yesterday':
            
            the_day = datetime.today().weekday() -1 

            if the_day == -1:
                the_day = 6   

        closingtime = str(opening_time[the_day])
        dispatcher.utter_message(text= " The restaurant openss at " + closingtime +" "+ str(day[1]['value']))


        return []