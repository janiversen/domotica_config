
###############
# Configuration
###############
POWER_METER = "sensor.power_meter"
PRODUCTION = "sensor.production"
CONSUMPTION = "sensor.casa_consumo"


#######################
# Calculate consumption
#######################
@state_trigger(f"{POWER_METER} != '9999'")
def calculate_consumption(value=None):
    try:
        load = int(state.get(PRODUCTION)) - int(value)
    except ValueError:
        return
    state.set("sensor.casa_consumo", value=load)

