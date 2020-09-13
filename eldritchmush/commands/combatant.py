from commands.combat import Helper
from pprint import pprint

class Combatant:
    """
    A helper class used to ease readability and flow of combat functions
    Should be rewritten ultimately to use properties/getters/setters
    """

    def __init__(self, caller):
        self.caller = caller
        self.helper = Helper(caller)
        self.name = self.caller.key
        self.combatStats = self.helper.getMeleeCombatStats(self.caller)
        self.target = None

    def canFight(self):
        return self.helper.canFight(self.caller)

    def cantFight(self):
        return not self.canFight()

    def message(self,msg):
        self.caller.msg(msg)

    def debugMessage(self,msg):
        #Is there a way we can broadcast this only to admins?
        self.caller.msg(msg)

    def broadcast(self, msg):
        self.caller.location.msg_contents(msg)

    def hasTurn(self,message=None):
        if message and not self.caller.db.combat_turn:
            self.message(message)
        return self.caller.db.combat_turn

    def stabilize(self):
        return self.caller.db.stabilize

    def hasStabilize(self,message=None):
        if message and not self.caller.db.stabilize:
            self.message(message)
        return self.stabilize()

    def medicine(self):
        return self.caller.db.medicine

    def battlefieldMedicine(self):
        return self.caller.db.battlefieldmedicine

    #Syntactic Sugar
    def hasMoreBodyThan(self, value):
        return self.body() > value

    def hasBody(self, value = None):
        if value:
            return self.body() == value

        return self.body() > 0

    def setBody(self, value):
        self.caller.db.body = value

    def addBody(self, value):
        if (self.caller.db.body + value) <= 3:
            self.caller.db.body += value
        else:
            self.setBody(3)

    def body(self):
        #self.caller.message(f"Debug body is {self.caller.db.body}")
        return self.caller.db.body

    def resilience(self):
        return self.caller.db.resilience

    def bleedPoints(self):
        return self.caller.db.bleed_points

    def atMaxBleedPoints(self):
        return self.bleedPoints() == self.totalBleedPoints()

    #TODO: Magic Number?
    def totalBleedPoints(self):
        return self.resilience() + 3

    def missingBleedPoints(self):
        return self.totalBleedPoints() - self.bleedPoints()

    def hasBleedPoints(self):
        return self.bleedPoints() > 0

    def setBleedPoints(self, value):
        self.caller.db.bleed_points = value

    def addBleedPoints(self, value):
        if (self.caller.db.bleed_points + value) <= self.totalBleedPoints():
            self.caller.db.bleed_points += value
        else:
            self.resetBleedPoints()

    def resetBleedPoints(self):
        self.setBleedPoints(self.totalBleedPoints())

    def isAtMaxDeathPoints(self):
        return self.deathPoints() >= 3

    def addDeathPoints(self, value):
        if (self.deathPoints() + value) <= 3:
            self.caller.db.death_points += value
        else:
            self.setDeathPoints(3)

    def setDeathPoints(self, value, combatant=None):
        self.caller.db.death_points = value

    def hasDeathPoints(self, value = None):
        if value:
            return self.deathPoints() == value
        return self.deathPoints() > 0

    def missingDeathPoints(self):
        return 3 - self.deathPoints()

    def deathPoints(self):
        return self.caller.db.death_points

    def chirurgeon(self):
        return self.caller.db.chirurgeon

    def inCombat(self):
        return self.caller.db.in_combat

    def secondsUntilNextChirurgery(self, current_time):
        if not self.caller.db.last_chirurgery:
            return 0
        else:
            seconds_since_last_chirurgery = (int(current_time) - int(self.caller.db.last_chirurgery))
            return 900 - seconds_since_last_chirurgery

    def setChirurgeryTimer(self,current_time):
        self.caller.db.last_chirurgery = current_time


    def resetTough(self):
        self.caller.db.tough = self.caller.db.total_tough

    def addWeakness(self):
        self.caller.db.weakness = 1

    def removeWeakness(self):
        self.caller.db.weakness = 0

    #Now Combat
    def stunsRemaining(self):
        return self.caller.db.stun

    def hasStunsRemaining(self,message=None):
        if message and self.stunsRemaining() <= 0:
            self.message(message)

        return self.stunsRemaining()

    def getRightHand(self):
        return self.combatStats.get("right_slot", '')

    def getLeftHand(self):
        return self.combatStats.get("left_slot", '')

    def getWeapon(self):
        right_hand = self.getRightHand()
        left_hand = self.getLeftHand()
        if right_hand.db.damage >= 0:
            return right_hand
        elif left_hand.db.damage >= 0:
            return left_hand
        else:
            return None

    def isArmed(self,message=None):
        if message and not self.getRightHand() and not self.getLeftHand():
            self.message(message)
            return False
        else:
            return True

    def isUnarmed(self,message=None):
        if message and self.isArmed():
            self.message(message)
            return False
        else:
            return True

    def rollAttack(self):
        die_result = self.helper.fayneChecker(self.combatStats.get("master_of_arms", 0), self.combatStats.get("wylding_hand", 0))

        # Get damage result and damage for weapon type
        attack_result = (die_result + self.caller.db.weapon_level) - self.combatStats.get("dmg_penalty",
                                                                                      0) - self.combatStats.get("weakness",
                                                                                                            0) - self.combatStats.get(
            "stun_penalty", 0)
        return attack_result

    def isTwoHanded(self):
        return self.combatStats.get("two_handed", 0)

    def av(self):
        return self.caller.db.av

    def determineHitLocation(self,victim):
        return self.helper.shotFinder(self.caller.db.targetArray)

    def isAlive(self,message=None):
        is_alive = True if self.caller.db.death_points else False
        if message and not is_alive:
            self.message(message)

        return is_alive

    def hasWeakness(self,message=None):
        weakness = self.combatStats.get("weakness", 0)
        if message and weakness:
            self.message(message)
        return weakness

    def setStuns(self, value):
        self.caller.db.stun = value

    def decreaseStuns(self, value):
        new_stun_value = self.stunsRemaining() - value
        if new_stun_value < 0 or value < 0:
            new_stun_value = 0

        self.setStuns(new_stun_value)

    def stun(self):
        self.caller.db.skip_turn = True

    def hasDamageVulnerability(self):
        return

    def getVictim(self, target):
        # Get target if there is one
        self.target = self.caller.search(target)
        return Combatant(self.target)

    def getDamage(self):
        if self.combatStats.get("two_handed", False):
            return 1
        else:
            return 2

    def setAv(self, amount):
        #TODO: Should we set Max/Min?
        self.caller.db.av = amount

    def getShield(self):
        return self.caller.db.shield

    def getArmorSpecialist(self):
        return self.caller.db.armor_specialist

    def getArmor(self):
        return self.caller.db.armor

    def getTough(self):
        return self.caller.db.tough

    def hasChirurgeonsKit(self):
        kit_type, uses = self.helper.getKitTypeAndUsesItem()
        has_kit = False
        if (kit_type == 'chirurgeon') and (uses > 0) :
            has_kit = True

        return has_kit

    def useChirurgeonsKit(self):
        self.helper.useKit()

    def takeShieldDamage(self, amount):
        return self.alternateDamage(amount, 'shield_value')

    def takeArmorSpecialistDamage(self, amount):
        return self.alternateDamage(amount, "armor_specialist")

    def takeArmorDamage(self, amount):
        return self.alternateDamage(amount, "tough")

    def takeToughDamage(self, amount):
        return self.alternateDamage(amount, "armor")

    def alternateArmorSpecialistDamage(self, amount):
        return self.alternateDamage(amount, "armor_specialist")

    def takeBodyDamage(self, amount):
        return self.alternateDamage(amount, "body")

    def takeBleedDamage(self, amount):
        return self.alternateDamage(amount, "bleed_points")

    def takeDeathDamage(self, amount, combatant):
        if self.caller.db.creature_color:
            weapon = combatant.getWeapon()
            if weapon and (weapon.db.color == self.caller.db.creature_color):
                return self.alternateDamage(amount, "death_points")
            else:
                return 0
        else:
            return self.alternateDamage(amount, "death_points")

    def alternateDamage(self, amount, type):
        remaining_damage = amount

        if self.caller.attributes.get(type):
            if self.caller.attributes.get(type):
                # How much damage is left after the shield
                remaining_damage = amount - self.caller.attributes.get(type)
                if remaining_damage < 0:
                    remaining_damage = 0

                # Damage the shield
                if amount >= self.caller.attributes.get(type):
                    new_value = 0
                else:
                    new_value = self.caller.attributes.get(type) - amount

                obj_to_set = self.caller.attributes.get(type, return_obj=True)
                obj_to_set.value = new_value

        return remaining_damage

    def updateAv(self):
        self.caller.db.av = self.caller.db.shield_value + self.caller.db.armor + self.caller.db.tough + self.caller.db.armor_specialist



    def takeDamage(self, combatant, amount, shot_location):
        if self.av():
            #Take Damage to Armor
            amount = self.takeShieldDamage(amount)
            if amount > 0:
                amount = self.takeArmorSpecialistDamage(amount)
                if amount > 0:
                    amount = self.takeArmorDamage(amount)
                    if amount > 0:
                        amount = self.takeToughDamage(amount)

            #In case we took any damage, refresh our AV
            self.updateAv()

        if amount > 0:
            #We have damage that made it through armor!
            #TODO: Check with spence that this is right, if we hit the torso, and the hit goes through all the armor, should they go down?
            #TODO: Or does this only happen if they're totally unarmored when they take damage
            if shot_location == "torso" and amount < self.body():
                amount = self.body()

            if self.body() > 0:
                amount = self.takeBodyDamage(amount)

            if amount > 0 and self.bleedPoints() > 0:
                self.addWeakness()
                amount = self.takeBleedDamage(amount)
                self.message(
                    "|430You are bleeding profusely from many wounds and can no longer use any active martial skills.\n|n")
                self.broadcast(
                    f"|025{self.name} is bleeding profusely from many wounds and will soon lose consciousness.|n")

            if amount > 0 and self.deathPoints() > 0:
                self.addWeakness()
                self.takeDeathDamage(amount, combatant)
                self.message("|300You are unconscious and can no longer move of your own volition.|n")
                self.broadcast(f"|025{self.name} does not seem to be moving.|n")

