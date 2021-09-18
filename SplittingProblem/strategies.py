from random import shuffle as random_shuffle

def base_onestep_strat(permutation, workpiece_lengths):
    return sorted(permutation, key=lambda x: workpiece_lengths[x], reverse=True)

def base_multistep_strat(permutation, _):
    random_shuffle(permutation)
