def cartesian_product(l1, l2):
    prod = []
    for i in l1:
        prod.extend([(i, j) for j in l2])
    return prod
