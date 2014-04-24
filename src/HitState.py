##  @file HitState.py
#   @author Josh Halstead
#   @date Spring 2014
#
#   Source File for the "HitState" type.

from State import *
from SimulationDelta import *

## A type of ephemeral state (i.e. timeout = 0) that represents taking damage
#  after being hit. Damage is hardcoded as a -1 penalty to current health.
class HitState(State):
    ### Constructors ###
    
    ## Constructs a hit state instance with the given string identifier.
    #
    #  @param identifier A string identifier that represents the name of the
    #  instance state.
    #  @param damage An integer that represents how much health is lost when
    #  entering the state.
    def __init__(self, identifier, damage):
        super(HitState, self).__init__(identifier, timeout=float(0))
        self._damage = damage

    ### Public Methods ###

    ## @return The amount of damage inflicted by a hit.
    def get_damage(self):
        return self._damage

    ### Private Methods ###

    ## @return A zero "SimulationDelta" because the state is ephemeral (i.e.
    #  there is no guarantee that a step will occur)
    def _calc_step_changes(self, time_delta):
        return SimulationDelta()

    ## @return A "SimulationDelta" where damage, in the form of a -1 reduction
    #  to current health.
    def _calc_arrival_changes( self ):
        return SimulationDelta(
                PhysicalState(
                    volume=CompositeHitbox(), 
                    velocity=(0, 0),
                    mass=0.0,
                    curr_health=-self._damage,
                    max_health=0
                )
               )

    ## Returns a zero "SimulationDelta" because the damage is only applied on
    #  arrival.
    #
    #  @override
    def _calc_departure_changes( self ):
        return SimulationDelta()
