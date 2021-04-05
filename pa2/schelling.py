"""
CS121: Schelling Model of Housing Segregation

  Program for simulating a variant of Schelling's model of
  housing segregation.  This program takes six parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: a home at Location (k, l) is in
        the neighborhood of the home at Location (i,j) if 0 <= k < N,
        0 <= l < N, and 0 <= |i-k| + |j-l| <= R.

    similarity_satisfaction_range (lower bound and upper bound) -
         acceptable range for ratio of the number of
         homes of a similar color to the number
         of occupied homes in a neighborhood.

   patience - number of satisfactory homes that must be visited before choosing
              the last one visited.

   max_steps - the maximum number of passes to make over the city
               during a simulation.

  Sample: python3 schelling.py --grid_file=tests/a20-sample-writeup.txt --r=1
         --sim_lb=0.40 --sim_ub=0.7 --patience=3 --max_steps=1
  The sample command is shown on two lines, but should be entered on
  a single line in the linux command-line
"""

import click
import utility


def similarity_score(grid, location, R):
    """
    Calculate the similarity score at a given location and R value

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
    Returns: float
    """
    x, y = location
    S = 0
    H = 0
    
    for i in range(x-R, x+1+R):
        if len(grid[0])-1 >= i >= 0:
            for j in range(y-R, y+1+R):
                if len(grid)-1 >= j >= 0:
                    if abs(x - i) + abs(y - j) in range(0, R+1) and grid[i][j] != "F":
                        H += 1
                        if grid[i][j] == grid[x][y]:
                            S += 1
                
    result = S / H

    return result
    


def is_satisfied(grid, R, location, sim_sat_range):
    '''
    Determine whether or not the homeowner at a specific location is
    satisfied using an R-neighborhood centered around the location.
    That is, is does their similarity score fall with the specified
    range (inclusive)

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
    Returns: bool
    '''
    x, y = location

    assert grid[x][y] != "F"

    satisfied = False

    if sim_sat_range[0] <= similarity_score(grid, location, R) <= sim_sat_range[1]:
        satisfied = True
        
    return satisfied


def relocating_one_home(grid, location, R, sim_sat_range, patience, homes_for_sale):
    '''
    Perform one attempt of relocation in a given location.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory homes that must be visited before choosing
          the last one visited.
        home_for_sale (list of tuples): a list of locations with homes for sale
        location (int, int): a grid location

    Returns: (bool) whether the attempt of relocation is successful 
    '''
    x, y = location

    if grid[x][y] == "M":
        original = "M"
    elif grid[x][y] == "B":
        original = "B"

    succ_reloc = False

    if is_satisfied(grid, R, location, sim_sat_range) == False:
        for candidate in homes_for_sale:
            i, j = candidate
            grid[i][j] = grid[x][y]
            grid[x][y] = "F"
            # swapping the value of the elements in the home_for_sale temporarily
            if is_satisfied(grid, R, candidate, sim_sat_range) == True:
                if patience > 1:
                    patience -= 1
                    grid[i][j] = "F"
                    grid[x][y] = original
                    # changing the value of the for_sale list back
                elif patience == 1:
                    homes_for_sale.remove(candidate)
                    homes_for_sale.insert(0, location)
                    succ_reloc = True
                    break
            else:
                grid[i][j] = "F"
                grid[x][y] = original
                # changing the value of the for_sale list back   

    return succ_reloc

def simulating_one_wave(grid, R, sim_sat_range, patience, wave, homes_for_sale):
    '''
    Perform one wave of relocation.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory homes that must be visited before choosing
          the last one visited.
        wave (str): the type of the wave ("M" or "B")
        home_for_sale (list of tuples): a list of locations with homes for sale

    Returns: (int) number of relocations done in this wave 
    '''

    reloc_in_a_wave = 0

    for x, row in enumerate(grid):
        for y, location in enumerate(row):
            if location == wave:
                if relocating_one_home(grid, (x, y), R, sim_sat_range, patience, homes_for_sale) == True:
                    reloc_in_a_wave += 1

    return reloc_in_a_wave


def simulating_one_step(grid, R, sim_sat_range, patience, homes_for_sale):
    '''
    Perform one step of relocation.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory homes that must be visited before choosing
          the last one visited.
        home_for_sale (list of tuples): a list of locations with homes for sale

    Returns: (int) number of relocations done in this step 
    '''

    step = ["M", "B"]
    reloc_in_a_step = 0

    for wave in step:
        reloc_in_a_step += simulating_one_wave(grid, R, sim_sat_range, patience, wave, homes_for_sale)

    return reloc_in_a_step

def do_simulation(grid, R, sim_sat_range, patience, max_steps, homes_for_sale):
    '''
    Do a full simulation.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory homes that must be visited before choosing
          the last one visited.
        max_steps (int): maximum number of steps to do
        for_sale (list of tuples): a list of locations with homes for sale

    Returns: (int) The number of relocations completed.
    '''

    finished_steps = 0
    total_reloc = 0
    current_reloc = 0

    while max_steps > finished_steps:
        current_reloc = total_reloc
        total_reloc += simulating_one_step(grid, R, sim_sat_range, patience, homes_for_sale)
        finished_steps += 1
        if total_reloc == current_reloc:
            break

    return total_reloc


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1,
              help="neighborhood radius")
@click.option('--sim_lb', type=float, default=0.40,
              help="Lower bound of similarity range")
@click.option('--sim_ub', type=float, default=0.70,
              help="Upper bound of similarity range")
@click.option('--patience', type=int, default=1, help="patience level")
@click.option('--max_steps', type=int, default=1)
def cmd(grid_file, r, sim_lb, sim_ub, patience, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)
    for_sale = utility.find_homes_for_sale(grid)
    sim_sat_range = (sim_lb, sim_ub)


    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    num_relocations = do_simulation(grid, r, sim_sat_range, patience,
                                    max_steps, for_sale)

    if len(grid) < 20:
        print("Final state of the city:")
        for row in grid:
            print(row)
        print()

    print("Total number of relocations done: " + str(num_relocations))

if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
