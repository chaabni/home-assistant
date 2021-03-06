""" Support for Tellstick switches. """
import logging

from homeassistant.helpers import ToggleDevice
from homeassistant.const import ATTR_FRIENDLY_NAME

try:
    import tellcore.constants as tc_constants
except ImportError:
    # Don't care for now. Warning will come when get_switches is called.
    pass


def get_devices(hass, config):
    """ Find and return Tellstick switches. """
    try:
        import tellcore.telldus as telldus
    except ImportError:
        logging.getLogger(__name__).exception(
            "Failed to import tellcore")
        return []

    core = telldus.TelldusCore()
    switches = core.devices()

    return [TellstickSwitch(switch) for switch in switches]


class TellstickSwitch(ToggleDevice):
    """ represents a Tellstick switch within home assistant. """
    last_sent_command_mask = (tc_constants.TELLSTICK_TURNON |
                              tc_constants.TELLSTICK_TURNOFF)

    def __init__(self, tellstick):
        self.tellstick = tellstick
        self.state_attr = {ATTR_FRIENDLY_NAME: tellstick.name}

    @property
    def name(self):
        """ Returns the name of the switch if any. """
        return self.tellstick.name

    @property
    def state_attributes(self):
        """ Returns optional state attributes. """
        return self.state_attr

    @property
    def is_on(self):
        """ True if switch is on. """
        last_command = self.tellstick.last_sent_command(
            self.last_sent_command_mask)

        return last_command == tc_constants.TELLSTICK_TURNON

    def turn_on(self, **kwargs):
        """ Turns the switch on. """
        self.tellstick.turn_on()

    def turn_off(self, **kwargs):
        """ Turns the switch off. """
        self.tellstick.turn_off()
