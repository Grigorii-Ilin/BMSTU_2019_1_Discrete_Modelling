
def get_stddev(diff):
    mean = sum(diff) / len(diff)

    sqr_i_minus_mean = []
    for i in range(len(diff)):
        tmp = (diff[i] - mean) ** 2
        sqr_i_minus_mean.append(tmp)

    dispersion = sum(sqr_i_minus_mean) / len(sqr_i_minus_mean)
    return dispersion ** 0.5


def calc(matrix):
    vektorOld = [0.0 for i in range(len(matrix))]
    vektorOld[0]=1.0

    diff_btw_old_and_new_vektor = [0.0 for i in range(len(matrix))]
 
    for iter in range(30):
        vektorNew = [0.0 for i in range(len(matrix))]

        for row  in range(len(matrix)):
            for col  in range(len(matrix)):
                vektorNew[col]+=  matrix[row][col] * vektorOld[row]
            diff_btw_old_and_new_vektor[row] = vektorNew[row] - vektorOld[row]

        stddev = get_stddev(diff_btw_old_and_new_vektor)
        print(iter, stddev)
        vektorOld = vektorNew

    return vektorNew