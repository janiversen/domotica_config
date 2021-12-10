from datetime import date

###############
# Configuration
###############
BOILER_SWITCH = "switch.calentador"

last_switch = None

######################################
# Boiler is only active if we are here
######################################
@state_trigger(f"{BOILER_SWITCH} == 'on'")
def check_boiler(value=None):
    global last_switch

    now_date = date.today()
    if last_switch == now_date:
        return
    last_switch = now_date
    if state.get('person.jan') == "home" or state.get('person.belen') == "home":
        return

    homeassistant.turn_off(entity_id=BOILER_SWITCH)

