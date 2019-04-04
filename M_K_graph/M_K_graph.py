M_DIMENSION = 4


def get_stddev(diff):
    mean = sum(diff) / len(diff)

    sqr_i_minus_mean = []
    for i in range(M_DIMENSION):
        tmp = (diff[i] - mean) ** 2
        sqr_i_minus_mean.append(tmp)

    dispersion = sum(sqr_i_minus_mean) / len(sqr_i_minus_mean)
    return dispersion ** 0.5


def normalize_matrix(m):
    coefs = [0.0 for i in range(M_DIMENSION)]
    for col in range(M_DIMENSION):
        col_sum = 0
        for row in range(M_DIMENSION):
            col_sum+=m[row][col] 
        coefs[col] = 1 / col_sum

    for row in range(M_DIMENSION):
        for col in range(M_DIMENSION):
            m[row][col]*=coefs[col]
            m[row][col] = 1 - m[row][col] #probability to go out from position

    return m


def calc(matrix):
    matrix = normalize_matrix(matrix)
    vektor_old = [1 / M_DIMENSION for i in range(M_DIMENSION)]
    diff_btw_old_and_new_vektor = [0.0 for i in range(M_DIMENSION)]
 
    for iter in range(30):
        vektor_new = [0.0 for i in range(M_DIMENSION)]

        for row  in range(M_DIMENSION):
            for col  in range(M_DIMENSION):
                vektor_new[row]+=  matrix[row][col] * vektor_old[row]
            diff_btw_old_and_new_vektor[row] = vektor_new[row] - vektor_old[row]

        #we may not use it
        #stddev = get_stddev(diff_btw_old_and_new_vektor)

        vektor_old = vektor_new

    normalized_vector = [1 / sum(vektor_new) * x for x in vektor_new]
    return normalized_vector