'''
Epidemic modelling

Torres Shi

Functions for running a simple epidemiological simulation
'''

import random
import click

# This seed should be used for debugging purposes only!  Do not refer
# to it in your code.
TEST_SEED = 20170217

def count_infected(city):
    '''
    Count the number of infected people

    Inputs:
      city (list of strings): the state of all people in the
        simulation at the start of the day
    Returns (int): count of the number of people who are
      currently infected
    '''
    num_infected = 0
    for x in city:
      if x[0] == "I":
        num_infected += 1

    return num_infected


def has_an_infected_neighbor(city, position):
    '''
    Determine whether a person has an infected neighbor

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check

    Returns:
      True, if the person has an infected neighbor, False otherwise.
    '''

    # This function should only be called when the person at position
    # is susceptible to infection.
    assert city[position] == "S"
    infected_neighbor = False
    
    if len(city) > 1:
      if position == 0:
        if city[position + 1][0] == "I":
          infected_neighbor = True
      elif position == len(city) - 1:
        if city[position - 1][0] == "I":
          infected_neighbor = True
      else:
        if city[position + 1][0] == "I" or city[position - 1 ][0] == "I":
          infected_neighbor = True
    elif len(city) == 1:
      pass
    
    return infected_neighbor


def advance_person_at_position(city, position, days_contagious):
    '''
    Compute the next state for the person at the specified position.

    Inputs:
      city (list): the state of all people in the simulation at the
        start of the day
      position (int): the position of the person to check
      days_contagious (int): the number of a days a person is infected

    Returns: (string) disease state of the person after one day
    '''
    next_stage = ""

    if city[position] == "S":
      if has_an_infected_neighbor(city, position) == True:
        next_stage = "I0"
      else:
        next_stage = "S"
    elif city[position][0] == "I":
      if int(city[position][1:]) + 1 < days_contagious:
        next_stage = "I" + str(int(city[position][1:]) + 1)
      elif int(city[position][1:]) + 1 >= days_contagious:
        next_stage = "R"
    elif city[position] == "R":
      next_stage = "R"
    elif city[position] == "V":
      next_stage = "V"

    return next_stage


def simulate_one_day(starting_city, days_contagious):
    '''
    Move the simulation forward a single day.

    Inputs:
      starting_city (list): the state of all people in the simulation at the
        start of the day
      days_contagious (int): the number of a days a person is infected

    Returns:
      new_city (list): disease state of the city after one day
    '''

    new_city_state = []
    new_individual_state = ""

    for i, p in enumerate(starting_city):
      new_individual_state = advance_person_at_position(starting_city, i, days_contagious)
      new_city_state.append(new_individual_state)

    return new_city_state


def run_simulation(starting_city, days_contagious,
                   random_seed=None, vaccine_effectiveness=0.0):
    '''
    Run the entire simulation

    Inputs:
      starting_city (list): the state of all people in the city at the
        start of the simulation
      days_contagious (int): the number of a days a person is infected
      random_seed (int): the random seed to use for the simulation
      vaccine_effectiveness (float): the chance that a vaccination will be
        effective

    Returns tuple (list of strings, int): the final state of the city
      and the number of days actually simulated.
    '''
    random.seed(random_seed)

    day_count = 0

    vac_state = vaccinate_city(starting_city, vaccine_effectiveness)
    final_state = vac_state.copy()

    # any() operator from https://stackoverflow.com/questions/16380326/check-if-substring-is-in-a-list-of-strings/16380569
    while any("I" in i for i in final_state):
      final_state = simulate_one_day(final_state, days_contagious)
      day_count += 1

    return (final_state, day_count)


def vaccinate_city(starting_city, vaccine_effectiveness):
    '''
    Vaccinate everyone in a city

    Inputs:
      starting_city (list): the state of all people in the simulation at the
        start of the simulation
      vaccine_effectiveness (float): the chance that a vaccination will be
        effective

    Returns:
      new_city (list): state of the city after vaccinating everyone in the city
    '''

    new_city = []

    for i, state in enumerate(starting_city):
      if state == "S":
        if random.random() < vaccine_effectiveness:
          state = "V"
      new_city.append(state)

    return new_city


def calc_avg_days_to_zero_infections(
        starting_city, days_contagious,
        random_seed, vaccine_effectiveness,
        num_trials):
    '''
    Conduct N trials with the specified vaccine effectiveness and
    calculate the average number of days for a city to reach zero
    infections

    Inputs:
      starting_city (list): the state of all people in the city at the
        start of the simulation
      days_contagious (int): the number of a days a person is infected
      random_seed (int): the starting random seed. Use this value for
        the FIRST simulation, and then increment it once for each
        subsequent run.
      vaccine_effectiveness (float): the chance that a vaccination will be
        effective
      num_trials (int): the number of trials to run

    Returns (float): the average number of days for a city to reach zero
      infections
    '''
    assert num_trials > 0

    actual_trial = 0
    num_days = 0

    while actual_trial < num_trials:
      num_days += run_simulation(starting_city, days_contagious, random_seed, vaccine_effectiveness)[1]
      actual_trial += 1
      random_seed += 1

    avg_num_days = num_days / num_trials

    return avg_num_days


################ Do not change the code below this line #######################


@click.command()
@click.argument("city", type=str)
@click.option("--days-contagious", default=2, type=int)
@click.option("--random_seed", default=None, type=int)
@click.option("--vaccine-effectiveness", default=0.0, type=float)
@click.option("--num-trials", default=1, type=int)
@click.option("--task-type", default="single",
              type=click.Choice(['single', 'average']))
def cmd(city, days_contagious, random_seed, vaccine_effectiveness,
        num_trials, task_type):
    '''
    Process the command-line arguments and do the work.
    '''

    # Convert the city string into a city list.
    city = [p.strip() for p in city.split(",")]
    emsg = ("Error: people in the city must be susceptible ('S'),"
            " recovered ('R'), or infected ('Ix', where *x* is an integer")
    for p in city:
        if p[0] == "I":
            try:
                _ = int(p[1])
            except ValueError:
                print(emsg)
                return -1
        elif p not in {"S", "R"}:
            print(emsg)
            return -1

    if task_type == "single":
        print("Running one simulation...")
        final_city, num_days_simulated = run_simulation(
            city, days_contagious, random_seed, vaccine_effectiveness)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials...")
        avg_days = calc_avg_days_to_zero_infections(
            city, days_contagious, random_seed, vaccine_effectiveness,
            num_trials)
        msg = ("Over {} trial(s), on average, it took {:3.1f} days for the "
               "number of infections to reach zero")
        print(msg.format(num_trials, avg_days))

    return 0


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter
