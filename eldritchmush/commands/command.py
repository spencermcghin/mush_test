"""
Commands

Commands describe the input the account can do to the game.

"""
# Global imports
import random
from django.conf import settings

# Local imports
from evennia import Command as BaseCommand
from evennia import default_cmds, utils, search_object
from commands.combat import Helper
from commands.fortunestrings import FORTUNE_STRINGS

_SEARCH_AT_RESULT = utils.object_from_module(settings.SEARCH_AT_RESULT)


# Helper class

# class CommandHelper():
#     """
#     Basic functions to avoid a bunch of repeated code.
#     """
#
#     # Random text generation for battle wounds when a limb or torso is struck
#     def


# from evennia import default_cmds

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """

    pass


# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super().has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None

class SetArmorValue(Command):
    """Set the armor level of a character

    Usage: setarmorvalue <value>

    This sets the armor of the current character. This command is available to all characters.
    """

    key = "setarmorvalue"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setarmorvalue <value>|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            armor_value = int(self.args)
            # Error handling to keep from going below 0.
            if armor_value < 0:
                self.caller.msg("|rYou may not set a value lower than 0.|n")
                return

        except ValueError:
            self.caller.msg(errmsg)
            return

        else:
            # Track hits by getting current armor value and looking at difference to return message.
            current_armor = self.caller.db.armor
            # at this point the argument is tested as valid. Let's set it.
            self.caller.db.armor = armor_value
            # Messages to emote that caller is taking damage
            if current_armor > armor_value:
                # Get amount of damage taken
                damage = current_armor - armor_value
                self.caller.location.msg_contents(f"|r{self.caller.key} takes {damage} damage to their armor.|n")

            if armor_value == 0:
                self.caller.msg("|rYour armor is now badly damaged and needs to be repaired.\nPlease see a blacksmith.|n")

            # Get vals for armor value calc
            tough = self.caller.db.tough
            shield_value = self.caller.db.shield_value if self.caller.db.shield == True else 0
            armor_specialist = 1 if self.caller.db.armor_specialist == True else 0

            # Add them up and set the curent armor value in the database
            currentArmorValue = armor_value + tough + shield_value + armor_specialist
            self.caller.db.av = currentArmorValue

            # Return armor value to console.
            self.caller.msg(f"|yYour current Armor Value is {currentArmorValue}:\nArmor: {armor_value}\nTough: {tough}\nShield: {shield_value}\nArmor Specialist: {armor_specialist}")


class SetTracking(Command):
    """Set the tracking of a character

    Usage: settracking <1-3>

    This sets the tracking of the current character. This can only be
    used during character generation.
    """

    key = "settracking"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: settracking <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            tracking = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= tracking <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.tracking = tracking
        self.caller.msg("|yYour Tracking was set to %i.|n" % tracking)



class SetPerception(Command):
    """Set the perception of a character

    Usage: setperception <1-3>

    This sets the perception of the current character. This can only be
    used during character generation.
    """

    key = "setperception"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setperception <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            perception = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= perception <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.perception = perception
        self.caller.msg("|yYour Perception was set to %i.|n" % perception)


class SetMasterOfArms(Command):
    """Set the tracking of a character

    Usage: setmasterofarms <1-3>

    This sets the master of arms of the current character. This is available to all characters.
    """

    key = "setmasterofarms"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setmasterofarms <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            master_of_arms = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= master_of_arms <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.master_of_arms = master_of_arms
        self.caller.msg("|yYour Master of Arms was set to %i.|n" % master_of_arms)


class SetTough(Command):
    """Set the tough of a character

    Usage: settough <value>

    This sets the tough of the current character. This is available to all characters.
    """

    key = "settough"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: settough <value>|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            tough = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return

        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.tough = tough
        self.caller.msg("|yYour Tough was set to %i.|n" % tough)

        # Get armor value objects
        armor = self.caller.db.armor
        tough = self.caller.db.tough
        shield_value = self.caller.db.shield_value if self.caller.db.shield == True else 0
        armor_specialist = 1 if self.caller.db.armor_specialist == True else 0

        # Add them up and set the curent armor value in the database
        currentArmorValue = armor + tough + shield_value + armor_specialist
        self.caller.db.av = currentArmorValue

        # Return armor value to console.
        self.caller.msg(f"|yYour current Armor Value is {currentArmorValue}:\nArmor: {armor}\nTough: {tough}\nShield: {shield_value}\nArmor Specialist: {armor_specialist}|n")


class SetShieldValue(Command):
    """Set the shield value of a shield item.

    Usage: setshieldvalue <value>

    Available to all characters. Adds to total Armor Value db object.
    """
    key = "setshieldvalue"
    help_category = "mush"

    def func(self):
        """Performs the command"""
        errmsg = "|yUsage: setshieldvalue <value>|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            shield_value = int(self.args)
            # Error handling to keep from going below 0.
            if shield_value < 0:
                self.caller.msg("|rYou may not set a value lower than 0.|n")
                return

            if shield_value == 0:
                self.caller.msg("|rYour shield is now badly damaged and needs to be repaired.\nPlease see a blacksmith.|n")

        except ValueError:
            self.caller.msg(errmsg)
            return

        else:
            # at this point the argument is tested as valid. Let's set it.
            self.caller.db.shield_value = shield_value
            self.caller.msg("|yYour Shield Value was set to %i.|n" % shield_value)

            # Get armor value objects
            shield_value = self.caller.db.shield_value if self.caller.db.shield == True else 0
            armor_specialist = self.caller.db.armor_specialist
            armor = self.caller.db.armor
            tough = self.caller.db.tough

            # Add them up and set the curent armor value in the database
            currentArmorValue = armor + tough + shield_value + armor_specialist
            self.caller.db.av = currentArmorValue

            # Return armor value to console.
            self.caller.msg(f"|yYour current Armor Value is {currentArmorValue}:\nArmor: {armor}\nTough: {tough}\nShield: {shield_value}\nArmor Specialist: {armor_specialist}|n")



class SetBody(Command):
    """Set the body of a character

    Usage: setbody <value>

    This sets the tough of the current character. This is available to all characters.
    """

    key = "setbody"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setbody <value>|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            body = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return

        current_body = self.caller.db.body

        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.body = body
        self.caller.msg("|yYour Body was set to %i.|n" % body)
        if current_body > body:
            damage = current_body - body
            self.caller.location.msg_contents(f"|r{self.caller.key} takes {damage} damage to their body.|n")
        if body == 0:
            self.caller.location.msg_contents(f"|r{self.caller.key} is now bleeding profusely from many wounds.|n")

class SetArmorSpecialist(Command):
    """Set the armor specialist property of a character

    Usage: setarmorspecialist <1,2,3,4>

    This sets the armor specialist of the current character. This can only be
    used during character generation.
    """

    key = "setarmorspecialist"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setarmorspecialist <1-4>|n\n|rYou must supply a value between 1 and 4.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            armor_specialist = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        # Extending range for knight ability
        if not (1 <= armor_specialist <= 4):
            self.caller.msg(errmsg)
            return

        self.caller.db.armor_specialist = armor_specialist

        # Get armor value objects
        armor = self.caller.db.armor
        tough = self.caller.db.tough
        shield_value = self.caller.db.shield_value if self.caller.db.shield == True else 0

        # Add them up and set the curent armor value in the database
        currentArmorValue = armor + tough + shield_value + armor_specialist
        self.caller.db.av = currentArmorValue

        # Return armor value to console.
        self.caller.msg(f"|yYour current Armor Value is {currentArmorValue}:\nArmor: {armor}\nTough: {tough}\nShield: {shield_value}\nArmor Specialist: {armor_specialist}|n")

class SetWyldingHand(Command):
    """Set the wylding hand level of a character

    Usage: setwyldinghand <1-3>

    This sets the wylding hand level of the current character. This can only be
    used during character generation.
    """

    key = "setwyldinghand"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setwyldinghand <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            wyldinghand = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= wyldinghand <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.wyldinghand = wyldinghand
        self.caller.msg(f"Your level of Wylding Hand was set to {wyldinghand}")


class SetWeaponValue(Command):
    """Set the weapon level of a character

    Usage: setweaponvalue <value>

    This sets the weapon level of the current character. This can only be
    used during character generation.
    """

    key = "setweaponvalue"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setweaponvalue <value>|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            weapon_value = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.weapon_level = weapon_value
        self.caller.msg("Your Weapon Value was set to %i." % weapon_value)


class SetBow(Command):
    """Set the bow property of a character

    Usage: setbow <0/1>

    This sets the bow of the current character. This can be used at any time during the game.
    """

    key = "setbow"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setbow <0/1>|n\n|rYou must supply a value of either 0 or 1.|n"
        hasMelee = self.caller.db.melee

        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            bow = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if bow not in (0,1):
            self.caller.msg(errmsg)
            return
        else:
            # Bow/melee error handling
            if hasMelee:
                self.caller.msg("|yBefore using a bow, you must first unequip your melee weapon using the command setmelee 0.|n")
            else:
                self.caller.db.bow = bow

                # Quippy message when setting a shield as 0 or 1.
                if bow:
                    self.caller.msg("|gYou have equipped your bow.|n")
                    self.caller.location.msg_contents(f"|025{self.caller.key} has equipped their bow.|n")
                else:
                    self.caller.msg("|rYou have unequipped your bow.|n")
                    self.caller.location.msg_contents(f"|025{self.caller.key} unequips their bow.|n")


class SetMelee(Command):
    """Set the melee property of a character

    Usage: setmelee <0/1>

    This sets the melee of the current character. This can be used at any time during the game.
    """

    key = "setmelee"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setmelee <0/1>|n\n|rYou must supply a value of 0 or 1.|n"
        hasBow = self.caller.db.bow
        hasWeapon = self.caller.db.weapon_level

        # Check for valid arguments
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            melee = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if melee not in (0,1):
            self.caller.msg(errmsg)
        else:
            # Bow/melee error handling
            if hasBow:
                self.caller.msg("|yBefore using a melee weapon, you must first unequip your bow using the command setbow 0.|n")
            else:
                self.caller.db.melee = melee

                # Quippy message when setting a weapon as 0 or 1.
                if melee and hasWeapon:
                    self.caller.msg("|gYou are now ready to fight.|n")
                    self.caller.location.msg_contents(f"|025{self.caller.key} has equipped their weapon.|n")
                elif melee and not hasWeapon:
                    self.caller.location.msg_contents(f"|025{self.caller.key} assumes a defensive posture.")
                else:
                    if not melee and hasWeapon:
                        self.caller.location.msg_contents(f"|025{self.caller.key} sheathes their weapon.|n")
                    elif not melee and not hasWeapon:
                        self.caller.location.msg_contents(f"|025{self.caller.key} relaxes their defensive posture.|n")


class SetResist(Command):
    """Set the resist level of a character

    Usage: setresist <1,2,3,4,5>

    This sets the resist level of the current character. This can only be
    used during character generation.
    """

    key = "setresist"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setresist <1-5>|n\n|rYou must supply a number between 1 and 5.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            resist = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= resist <= 5):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.resist = resist
        self.caller.msg("Your resist level was set to %i." % resist)


class SetDisarm(Command):
    """Set the disarm level of a character

    Usage: setdisarm <1,2,3>

    This sets the disarm level of the current character. This can only be
    used during character generation.
    """

    key = "setdisarm"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setdisarm <1-3>|n\n|rYou must supply a number between 1 and 5.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            disarm = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= disarm <= 5):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.disarm = disarm
        self.caller.msg("Your disarm level was set to %i." % disarm)


class SetCleave(Command):
    """Set the cleave level of a character

    Usage: setcleave <1,2,3>

    This sets the cleave level of the current character. This can only be
    used during character generation.
    """

    key = "setcleave"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setcleave <1-3>|n\n|rYou must supply a number between 1 and 5.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            cleave = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= cleave <= 5):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.cleave = cleave
        self.caller.msg("Your cleave level was set to %i." % cleave)


class SetStun(Command):
    """Set the stun level of a character

    Usage: setstun <1,2,3,4,5>

    This sets the stun level of the current character. This can only be
    used during character generation.
    """

    key = "setstun"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setstun <1-5>|n\n|rYou must supply a number between 1 and 5.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            stun = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= stun <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.stun = stun
        self.caller.msg("Your stun level was set to %i." % stun)


class SetStagger(Command):
    """Set the stagger level of a character

    Usage: setstun <1,2,3,4,5>

    This sets the stagger level of the current character. This can only be
    used during character generation.
    """

    key = "setstagger"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setstagger <1-5>|n\n|rYou must supply a number between 1 and 5.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            stagger = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= stagger <= 5):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.stagger = stagger
        self.caller.msg("Your stagger level was set to %i." % stagger)


"""
Combat settings
"""

class SetShield(Command):
    """Set the shield property of a character

    Usage: setshield <0/1>

    This sets the shield of the current character. This can only be
    used during character generation.
    """

    key = "setshield"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setshield <0/1>|n\n|rYou must supply a value of 0 or 1.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            shield = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if shield not in (0,1):
            self.caller.msg(errmsg)
            return

        self.caller.db.shield = shield

        # Quippy message when setting a shield as 0 or 1.
        if shield:
            self.caller.msg("|gYou now have a shield.|n")
            self.caller.location.msg_contents(f"|025{self.caller.key} equips their shield.|n")
        else:
            self.caller.msg("|rYou have unequipped or lost your shield.|n")
            self.caller.location.msg_contents(f"|025{self.caller.key} unequips their shield.|n")

        # Get armor value objects
        armor = self.caller.db.armor
        tough = self.caller.db.tough
        shield_value = self.caller.db.shield_value if self.caller.db.shield == True else 0
        armor_specialist = 1 if self.caller.db.armor_specialist is 1 else 0

        # Add them up and set the curent armor value in the database
        currentArmorValue = armor + tough + shield_value + armor_specialist
        self.caller.db.av = currentArmorValue

        # Return armor value to console.
        self.caller.msg(f"|yYour current Armor Value is {currentArmorValue}:\nArmor: {armor}\nTough: {tough}\nShield: {shield_value}\nArmor Specialist: {armor_specialist}|n")


class SetTwoHanded(Command):
    """Set the two handed weapon status of a character

    Usage: settwohander <0,1>

    This sets the two handed weapon status of the current character.
    """

    key = "settwohanded"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: settwohanded <0/1>|n\n|rYou must supply a value of either 0 or 1.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            twohanded = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if twohanded not in (0,1):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.twohanded = twohanded

        if twohanded:
            self.caller.msg("|gYour have equipped a two-handed melee weapon.|n")
        else:
            self.caller.msg("|rYou have unequipped a two-handed melee weapon.|n")


"""
General commands
"""


class CmdPerception(default_cmds.MuxCommand):
    """
    sets a detail on a room
    Usage:
        @perception <level> <key> = <description>
        @perception <level> <key>;<alias>;... = description
    Example:
        @perception 1 walls = The walls are covered in ...
        @perception 3 castle;ruin;tower = The distant ruin ...
    This sets a "perception" on the object this command is defined on
    . This detail can be accessed with
    the TutorialRoomLook command sitting on TutorialRoom objects (details
    are set as a simple dictionary on the room). This is a Builder command.
    We custom parse the key for the ;-separator in order to create
    multiple aliases to the detail all at once.
    """

    key = "@perception"
    locks = "cmd:perm(Builder)"
    help_category = "mush"

    def func(self):
        """
        All this does is to check if the object has
        the set_perception method and uses it.
        """
        # No args error handler
        if not self.args or not self.rhs:
            self.caller.msg("Usage: @perception level key = description")
            return

        # Get level of perception
        try:
            level = int(self.args[0])

        except:
            self.caller.msg("|yUsage: @perception level key = description|n")

        else:
            if level in (1,2,3):
                # Get perception setting objects
                equals = self.args.index("=")
                object = str(self.args[1:equals]).strip()
            if not object:
                self.caller.msg("|rNothing here by that name or description|n")
                return
            # if not hasattr(self.obj, "set_perception"):
            #     self.caller.msg("Perception cannot be set on %s." % self.obj)
            #     return
            # self.obj = object
            looking_at_obj = self.caller.search(
                object,
                # note: excludes room/room aliases
                # look for args in room and on self
                # candidates=self.caller.location.contents + self.caller.contents,
                use_nicks=True,
                quiet=True,
            )
            if looking_at_obj:
                self.obj = looking_at_obj[0]
                # self.caller.msg(f"You are looking at {self.obj}")
                # Set the perception object in the database
                self.obj.set_perception(self.obj.name, level, self.rhs)
                # Message to admin for confirmation.
                self.caller.msg(f"|yPerception set on {self.obj.name}\nLevel: {level}\nDescription: {self.rhs}|n")
            else:
                self.caller.msg("|rSearch didn't return anything.|n")

class CmdTracking(default_cmds.MuxCommand):
    """
    sets a detail on a room
    Usage:
        @tracking <level> <key> = <description>
        @tracking <level> <key>;<alias>;... = description
    Example:
        @tracking 1 walls = The walls are covered in ...
        @tracking 3 castle;ruin;tower = The distant ruin ...
    This sets a "perception" on the object this command is defined on
    . This detail can be accessed with
    the TutorialRoomLook command sitting on TutorialRoom objects (details
    are set as a simple dictionary on the room). This is a Builder command.
    We custom parse the key for the ;-separator in order to create
    multiple aliases to the detail all at once.
    """

    key = "@tracking"
    locks = "cmd:perm(Builder)"
    help_category = "mush"


    def func(self):
        """
        All this does is to check if the object has
        the set_perception method and uses it.
        """
        errmsg = "|yUsage: @tracking level key = description|n"

        if not self.args or not self.rhs:
            self.caller.msg(errmsg)
            return

        # Get level of perception
        try:
            level = int(self.args[0])

        except:
            self.caller.msg(errmsg)

        else:
            if level in (1,2,3):
                # Get perception setting objects
                equals = self.args.index("=")
                object = str(self.args[1:equals]).strip()
            if not object:
                self.caller.msg("|rNothing here by that name or description|n")
                return
            # if not hasattr(self.obj, "set_perception"):
            #     self.caller.msg("Perception cannot be set on %s." % self.obj)
            #     return
            # self.obj = object
            looking_at_obj = self.caller.search(
                object,
                # note: excludes room/room aliases
                # look for args in room and on self
                # candidates=self.caller.location.contents + self.caller.contents,
                use_nicks=True,
                quiet=True,
            )
            if looking_at_obj:
                self.obj = looking_at_obj[0]
                # self.caller.msg(f"You are looking at {self.obj}")
                # Set the perception object in the database
                self.obj.set_tracking(self.obj.name, level, self.rhs)
                # Message to admin for confirmation.
                self.caller.msg(f"|yTracking set on {self.obj.name}\nLevel: {level}\nDescription: {self.rhs}|n")
            else:
                self.caller.msg("|rSearch didn't return anything.|n")


class CmdSmile(Command):
    """
    A smile command

    Usage:
      smile [at] [<someone>]
      grin [at] [<someone>]

    Smiles to someone in your vicinity or to the room
    in general.

    (This initial string (the __doc__ string)
    is also used to auto-generate the help
    for this command)
    """

    key = "smile"
    aliases = ["smile at", "grin", "grin at"]
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller

        if not self.target or self.target == "here":
            string = f"{caller.key} smiles"
        else:
            target = caller.search(self.target)
            if not target:
                return
            string = f"{caller.key} smiles at {target.key}"

        caller.location.msg_contents(string)


"""
Carnival commands
"""
# Fortune teller in Carnival
class CmdPull(Command):
    """
    Usage: pull crank

    Should get a fortune from the Artessa machine in the room. Command tied to room only.
    """

    key = "pull"

    def func(self):
        # Try and find caller key in fortuneStrings. If found, return fortune Value
        # Remove it from the fortuneString dict
        # If not found return a default fortune string
        args = self.args

        err_msg = "|yUsage: pull crank|n"
        fortuneStrings = {'eldritchadmin':'|yThis is a test fortune.|n',
                          'jess':'|yYou will marry a very handsome man who love you very much.|n',
                          'Lovecraft':'|yI am aware John. Spencer does not know that I can generate my own fortunes.|n'}

        if not self.args:
            self.caller.msg(err_msg)
            return
        try:
            args == "crank"
        except ValueError:
            self.caller.msg(err_msg)
            return
        else:
            if self.caller.key in FORTUNE_STRINGS:
                return self.caller.msg(FORTUNE_STRINGS[self.caller.key])
            else:
                return self.caller.msg("You get nothing.")

class CmdThrow(Command):
    """
    Usage: throw dagger

    Should get a fortune from the Artessa machine in the room. Command tied to room only.
    """

    key = "throw"

    def func(self):
        # Try and find caller key in fortuneStrings. If found, return fortune Value
        # Remove it from the fortuneString dict
        # If not found return a default fortune string
        h = Helper()
        args = self.args

        err_msg = "|yUsage: throw dagger|n"

        # Generate dc for target.
        target_dc = random.randint(1,6)

        # Generate throw result
        master_of_arms = self.caller.db.master_of_arms
        die_result = h.masterOfArms(master_of_arms)

        if not self.args:
            self.caller.msg(err_msg)
            return
        try:
            args == "dagger"
        except ValueError:
            self.caller.msg(err_msg)
            return
        else:
            if die_result > target_dc:
                # If the caller has done this before they will always get a skull ticket. Update their pariticpant status in the db as 1.
                # If the caller has not done this before, they should get a result from the random ticket chance.
                # Check the database to make sure that the jester ticket hasn't been chosen yet.
                # If a player gets the random jester ticket from this booth, it should log the entry in the database and not allow it to be generated again.
                self.caller.location.msg_contents(f"|025{self.caller.key} picks up a dagger from the table, takes aim, and hurls the dagger downfield striking true.|n")
            else:
                self.caller.location.msg_contents(f"|025{self.caller.key} picks up a dagger from the table, takes aim, and hurls the dagger downfield wide of the target.|n")


class CmdPushButton(Command):
    """
    Usage: push button

    Pushes button on the box in each carnival attraction.
    Generates either a jester or skull card object. Each box only has one jester card with a 1/30 chance to draw it.
    Once the jester card has been drawn, update the corresponding database entry to True for the box object.
    If anyone tries to push the button once a winner has been chosen, only skull tickets are generated.
    """

    key = "push button"
    aliases = ["push", "button", "press button"]
    locks = "cmd:all()"

    def func(self):
        """
        Push the button. Check the database for a winner.
        If none, there's 1/30 chance you'll draw the jester card.
        If drawn, update entry with hasWinner = 1. Drop card object with description of jester on it.
        If not, player gets a skull ticket.
        """
        hasWinner = self.obj.db.hasWinner

        # Commands to generate tickets
        button_emote = f"|025{self.caller} pushes the button. After a brief pause, a ticket pops up from a small slit on the top of the box.|n"
        get_ticket_emote = "|yA ticket pops up from a small slit in the top of the box.|n\n|yUse the |nget ticket|ycommand to pick it up|n\n|yUse the |nlook ticket|ycommand to examine it.|n"

        # Ticket objects
        jester_command = "create/drop A Small Paper Ticket:typeclasses.objects.ObjJesterTicket"
        skull_command = "create/drop A Small Paper Ticket:typeclasses.objects.ObjSkullTicket"

        if not hasWinner:
            draw = random.randint(1,30)
            if draw == 30:
                self.obj.db.hasWinner = True
                # Generate and drop a ticket object with a jester description.
                # Should indicate that character picks it up.
                self.caller.msg(get_ticket_emote)
                self.caller.location.msg_contents(button_emote)
                self.execute_cmd(skull_command)
            else:
                # Drop a ticket object with a skull description
                self.caller.location.msg_contents(button_emote)
                self.execute_cmd(jester_command)
        else:
            self.caller.msg("|yUsage: push button|n")

"""
Healing commands
"""

class CmdMedicine(Command):
    key = "medicine"
    help_category = "mush"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        # Check for correct command
        if not self.args:
            self.caller.msg("|yUsage: medicine <target>|n")
            return

        target = self.caller.search(self.target)

        if not target:
            self.caller.msg("|rThere is nothing here by that description.|n")
            return

        # Get caller level of medicine and emote how many points the caller will heal target that round.
        # May not increase targets body past 1
        # Only works on targets with body <= 0

        target_body = target.db.body
        medicine = self.caller.db.medicine

        # Check for using on self
        if (- 3 <= target_body <= 0) and medicine:
            # Return message to area and caller
            if target == self.caller:
                self.caller.location.msg_contents(f"|025{self.caller} pulls bandages and ointments from their bag, and starts to mend their wounds.\n|y{self.caller} heals |g{medicine}|n |ybody points per round as long as their work remains uninterrupted for the round.|n")
            elif target != self.caller:
                self.caller.location.msg_contents(f"|025{self.caller.key} comes to {target.key}'s rescue, healing {target.key}.|n\n|y{self.caller.key} heals {target.key} for|n |g{medicine}|n |ybody points per round as long as their work remains uninterrupted for the round.|n")
        # Apply stabilize to other target
        elif (-6 <= target_body <= -4) and medicine:
            if target == self.caller:
                self.caller.msg(f"|r{self.caller} You are too fargone to attempt this action.|n")
            elif target != self.caller:
                self.caller.location.msg_contents(f"|025{self.caller.key} comes to {target.key}'s rescue, though they are too fargone. {target.key} may require the aid of more advanced chiurgical techniques.|n")
        elif target_body > 0 and medicine:
            self.caller.msg(f"|025{target.key} doesn't require the application of your chiurgical skills. They seem to be healthy enough.|n")
        else:
            self.caller.msg("|yBetter not. You aren't quite that skilled.|n")


class CmdStabilize(Command):
    key = "stabilize"
    help_category = "mush"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        # Check for correct command
        if not self.args:
            self.caller.msg("|yUsage: stabilize <target>|n")
            return

        target = self.caller.search(self.target)

        if not target:
            self.caller.msg("|rThere is nothing here by that description.|n")
            return

        # Get caller level of stabilize and emote how many points the caller will heal target that round.
        # May not increase targets body past 1
        # Only works on targets with body <= 0
        target_body = target.db.body
        stabilize = self.caller.db.stabilize

        # Check for using on self
        if (- 3 <= target_body <= 0) and stabilize:
            # Return message to area and caller
            if target == self.caller:
                self.caller.location.msg_contents(f"|025{self.caller} pulls bandages and ointments from their bag, and starts to mend their wounds.\n|y{self.caller} heals|n |g{stabilize}|n |ybody points per round as long as their work remains uninterrupted.|n")
            elif target != self.caller:
                self.caller.location.msg_contents(f"|025{self.caller.key} comes to {target.key}'s rescue, healing {target.key} for|n |g{stabilize}|n |025body points.|n")
        # Apply stabilize to other target
        elif (-6 <= target_body <= -4) and stabilize:
            if target == self.caller:
                self.caller.msg(f"|r{self.caller} You are too fargone to attempt this action.|n")
            elif target != self.caller:
                self.caller.location.msg_contents(f"|025{self.caller.key} comes to {target.key}'s rescue, healing {target.key} for|n |r{stabilize}|n |ybody points per round as long as their work remains uninterrupted.|n")
        elif target_body > 0 and stabilize:
            self.caller.msg(f"|025{target.key} doesn't require the application of your chiurgical skills. They seem to be healthy enough.|n")
        else:
            self.caller.msg("|yBetter not. You aren't quite that skilled.|n")


# class CmdBattlefieldMedicine(Command):
#     key = "battlefieldmedicine"
#     help_category = "mush"
#
#     def parse(self):
#         "Very trivial parser"
#         self.target = self.args.strip()
#
#     def func(self):
#         "This actually does things"
#         # Check for correct command
#         if not self.args:
#             self.caller.msg("|yUsage: battlefieldmedicine <target>|n")
#             return
#
#         target = self.caller.search(self.target)
#
#         if not target:
#             self.caller.msg("|yThere is nothing here by that description.|n")
#             return
#
#         # Get caller level of stabilize and emote how many points the caller will heal target that round.
#         # May not increase targets body past 1
#         # Only works on targets with body <= 0
#         target_body = target.db.body
#         battlefieldmedicine = self.caller.db.battlefieldmedicine
#
#         # Check for using on self
#         if (- 3 <= target_body <= 0) and stabilize:
#             # Return message to area and caller
#             if target == self.caller:
#                 self.caller.location.msg_contents(f"|b{self.caller} pulls bandages and ointments from their bag, and starts to mend their wounds.\n|y{self.caller} heals |r{stabilize}|n |ybody points per round as long as their work remains uninterrupted.|n")
#             elif target != self.caller:
#                 self.caller.location.msg_contents(f"|b{self.caller.key} comes to {target.key}'s rescue, healing {target.key} for|n |r{stabilize}|n |bbody points.|n")
#         # Apply stabilize to other target
#         elif (-6 <= target_body <= -4) and stabilize:
#             if target == self.caller:
#                 self.caller.msg(f"|b{self.caller} You are too fargone to attempt this action.|n")
#             elif target != self.caller:
#                 self.caller.location.msg_contents(f"|b{self.caller.key} comes to {target.key}'s rescue, healing {target.key} for|n |r{stabilize}|n |ybody points per round as long as their work remains uninterrupted.|n")
#         elif target_body > 0 and stabilize:
#             self.caller.msg(f"|b{target.key} doesn't require the application of your chiurgical skills. They seem to be healthy enough.|n")
#         else:
#             self.caller.msg("Better not. You aren't quite that skilled.")


class SetStabilize(Command):
    """Set the stun level of a character

    Usage: setstabilize <1,2,3>

    This sets the stabilize level of the current character. This can only be
    used during character generation.
    """

    key = "setstabilize"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setstabilize <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            stabilize = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= stabilize <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.stabilize = stabilize
        self.caller.msg(f"Your stabilize level was set to {stabilize}")


class SetMedicine(Command):
    """Set the medicine level of a character

    Usage: setmedicine <1,2,3>

    This sets the medicine level of the current character. This can only be
    used during character generation.
    """

    key = "setmedicine"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setmedicine <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            medicine = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= medicine <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.medicine = medicine
        self.caller.msg(f"Your medicine level was set to {medicine}")


class SetBattleFieldMedicine(Command):
    """Set the medicine level of a character

    Usage: setbattlefieldmedicine <0,1>

    This sets the medicine level of the current character. This can only be
    used during character generation.
    """

    key = "setbattlefieldmedicine"
    help_category = "mush"

    def func(self):
        key = "setbattlefieldmedicine"
        help_category = "mush"

        def func(self):
            "This performs the actual command"
            errmsg = "|yUsage: setbattlefieldmedicine <0/1>|n\n|rYou must supply a number of either 0 or 1.|n"
            if not self.args:
                self.caller.msg(errmsg)
                return
            try:
                battlefieldmedicine = int(self.args)
            except ValueError:
                self.caller.msg(errmsg)
                return
            if battlefieldmedicine not in (0,1):
                self.caller.msg(errmsg)
                return
            # at this point the argument is tested as valid. Let's set it.
            self.caller.db.battlefieldmedicine = battlefieldmedicine

            if battlefieldmedicine:
                self.caller.msg("|gYou have activated the battlefield medicine ability.|n")
            else:
                self.caller.msg("|rYou have deactivated the battlefield medicine ability.|n")


"""
Knight skills
"""

class SetBattleFieldCommander(Command):
    """Set the battlefield commander level of a character

    Usage: setbattlefieldcommander <1,2,3>

    This sets the battlefield commander level of the current character. This can only be
    used during character generation.
    """

    key = "setbattlefieldcommander"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setbattlefieldcommander <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            battlefieldcommander = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= battlefieldcommander <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.battlefieldcommander = battlefieldcommander
        self.caller.msg(f"Your battlefield commander was set to {battlefieldcommander}")


class SetRally(Command):
    """Set the rally level of a knight character

    Usage: setrally <1,2,3>

    This sets the rally level of the current character. This can only be
    used during character generation.
    """

    key = "setrally"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setrally <1-3>|n\n|rYou must supply a number between 1 and 3.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            rally = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (1 <= rally <= 3):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.rally = rally
        self.caller.msg(f"Your rally was set to {rally}")


"""
Effects status commands
"""

class SetWeakness(Command):
    """
    Sets the weakness status on a character. If set to 0, it also sets activemartialskill in db to 0.
    Likewise, if set to 1, it also sets activemartialskills to 1.
    """

    key = "setweakness"
    help_category = "mush"

    def func(self):
        "This performs the actual command"
        errmsg = "|yUsage: setweakness <0/1>|n\n|rYou must supply a number of either 0 or 1.|n"
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            weakness = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if weakness not in (0,1):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.db.weakness = weakness

        if weakness:
            self.caller.db.activemartialskill = 0
            self.caller.msg("|rYou have become weakened, finding it difficult to run or use your active martial skills.|n\n|yAs long as you are weakened you may not run or use active martial skills.|n")
        else:
            self.caller.db.activemartialskill = 1
            self.caller.msg("|gYour weakened state has subsided.|n\n|yYou may now run and use your active martial skills.|n")
