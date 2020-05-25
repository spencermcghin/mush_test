"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from evennia import CmdSet, default_cmds
from commands.default_cmdsets import ChargenCmdset, RoomCmdSet
from commands import command


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        """
        Called when room is first created
        """

        self.cmdset.add_default(RoomCmdSet)

    def return_perception(self, perceptionkey, perceptionlevel):
        """
        This looks for an Attribute "obj_perception" and possibly
        returns the value of it.
        Args:
            perceptionkey (str): The perception detail being looked at. This is
                case-insensitive.
        """
        perception_details = self.db.perception_details

        look_results = []

        if perception_details.get(perceptionkey.lower(), None) is not None:
            for details in perception_details[perceptionkey.lower()]:
                if details[0] <= perceptionlevel:
                    look_results.append(details[1])

            return look_results
        else:
            return "There is nothing matching that description."

    def return_tracking(self, trackingkey, trackinglevel):
        """
        This looks for an Attribute "obj_tracking" and possibly
        returns the value of it.
        Args:
            trackingkey (str): The perception detail being looked at. This is
                case-insensitive.
        """
        tracking_details = self.db.tracking_details

        look_results = []

        if tracking_details.get(trackingkey.lower(), None) is not None:
            for details in tracking_details[trackingkey.lower()]:
                if details[0] <= trackinglevel:
                    look_results.append(details[1])

            return look_results
        else:
            return "There is nothing matching that description."


    def set_perception(self, perceptionkey, level, description):
        """
        This sets a perception on the room.
        Args:
            perceptionkey (str): The detail identifier to add (for
                aliases you need to add multiple keys to the
                same description). Case-insensitive.
            level (int): Level of the perception needed to access the information.
            description (str): The text to return when looking
                at the given perceptionkey.
        """
        if self.db.perception_details:
            self.db.perception_details[perceptionkey.lower()].append((level, description))
        else:
            self.db.perception_details = {perceptionkey.lower(): [(level, description)]}

    def set_tracking(self, trackingkey, level, description):
        """
        This sets a perception on the room.
        Args:
            trackingkey (str): The detail identifier to add (for
                aliases you need to add multiple keys to the
                same description). Case-insensitive.
            level (int): Level of the perception needed to access the information.
            description (str): The text to return when looking
                at the given perceptionkey.
        """
        if self.db.tracking_details:
            self.db.tracking_details[trackingkey.lower()].append((level, description))
        else:
            self.db.tracking_details = {trackingkey.lower(): [(level, description)]}

class ChargenRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(ChargenCmdset, permanent=True)
