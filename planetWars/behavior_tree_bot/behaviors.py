import sys
sys.path.insert(0, '../')
from planet_wars import issue_order




# use distance and growth rate to determine if player planet can conquer enemies weakest planet
def attack_weakest_enemy_planet(state,):
    # # (1) If we currently have a fleet in flight, abort plan.
    # if len(state.my_fleets()) >= 1:
    #     return False

    # # (2) Find my strongest planet.
    # strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # # (3) Find the weakest enemy planet.
    # weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # if not strongest_planet or not weakest_planet:
    #     # No legal source or destination
    #     return False
    # else:
    #     # (4) Send half the ships from my strongest planet to the weakest enemy planet.
    #     return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)



    my_target_planets = [state.planets[f.destination_planet] for f in state.my_fleets()]
    valid_planets = [p for p in state.enemy_planets() if p not in my_target_planets]

    if len(valid_planets) < 1:
        return False

    solutions = []

    valid_planets.sort(key=lambda t: t.num_ships, reverse=True)

    attack_planets = state.my_planets()
    attack_planets.sort(key=lambda t: t.num_ships, reverse=True)

    for enemy_planets in valid_planets:
        # use sorted list to get the strongest 
        attacking_planet = attack_planets[0]
        if attacking_planet:
            # sends only the amount needed to conquer planet
            require_ships = (enemy_planets.num_ships + 1 + state.distance(attacking_planet.ID, enemy_planets.ID) * enemy_planets.growth_rate)
  
            solutions.append(
                issue_order(state, attacking_planet.ID, enemy_planets.ID, require_ships)
            )


    if not solutions:
        return False
    else:
        return solutions




def spread_to_weakest_neutral_planet(state):
    # # (1) If we currently have a fleet in flight, just do nothing.
    # if len(state.my_fleets()) >= 1:
    #     return False

    # # (2) Find my strongest planet.
    # strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # # (3) Find the weakest neutral planet.
    # weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    # if not strongest_planet or not weakest_planet:
    #     # No legal source or destination
    #     return False
    # else:
    #     # (4) Send half the ships from my strongest planet to the weakest enemy planet.
    #     return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)



    # this modification allows bot to seek neutral planets and send their strongest planet to fully conquer it
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # assign target planets using the tuple 'destination planet' in Fleet
    target_planets = [state.planets[f.destination_planet] for f in state.fleets]
    # assign neutral planets by looking through list in planets p
    valid_planets = [p for p in state.neutral_planets() if p not in target_planets]

    # if no neutral planets or player has no strongest planet, false
    if not strongest_planet or len(valid_planets) <= 0:
        return False

    # consider weaker planets first by sorting them weakest to strongest in the avaliable p
    weakest_planets = sorted(
        valid_planets,
        key=lambda p: (p.num_ships, -p.growth_rate),
    )

    # amount of ships the strongest planet has aka(the number of the planet)
    strongest_planet_remaining_ships = strongest_planet.num_ships

    solutions = []
    # go through the list of weakest planets that is now sorted, if the strongest planet has enough ships to conquer it
    # add to solutions, deduct amount of ships used
    for p in weakest_planets:
        # sends enough ships to claim planet + 1
        require_ships = p.num_ships + 1
        if (strongest_planet_remaining_ships - require_ships>= strongest_planet.num_ships / 2):

            solutions.append(issue_order(state, strongest_planet.ID, p.ID, require_ships))
            strongest_planet_remaining_ships -= require_ships

    return solutions
