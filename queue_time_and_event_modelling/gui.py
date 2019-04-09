from  pprint import pprint

#from time_and_event_modelling import time_model
import delta_time_modelling
import events_modelling

t, q, m = delta_time_modelling.model(2, 5, 1.0, 1.0, 200.0, 0.7)
pprint(t, compact=True)
pprint(q, compact=True)
print(m)

t, q, m = events_modelling.model(2, 5, 1.0, 1.0, 200.0, 0.7)
pprint(t, compact=True)
pprint(q, compact=True)
print(m)