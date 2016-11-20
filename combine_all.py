from copy import deepcopy

from regression import (
    IGNORE,
    add_voting_data,
    clean_data,
    monthly_filenames,
    read_data,
)


for filename in monthly_filenames():
    ignore = deepcopy(IGNORE)
    ignore += "delegates"
    target = "votes"
    #ignore += "votes"
    #target = "deleagates"
    data = read_data(filename)
    full_data = add_voting_data(data)
    cleaned, headers = clean_data(full_data, ignore)
    import pdb; pdb.set_trace()
    # Write the data here
    x, y = seperate_x_y(data, target)
