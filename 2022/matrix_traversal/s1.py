def matrix_clockwise_traversal(matrix):
    result = []
    t, b = 0, len(matrix) - 1
    le, r = 0, len(matrix[0]) - 1
    while t <= b and le <= r:
        # right movement
        for i in range(le, r + 1):
            result.append(matrix[t][i])
        t += 1
        # down movement
        for i in range(t, b + 1):
            result.append(matrix[i][r])
        r -= 1
        # left movement
        if t <= b:
            for i in range(r, le - 1, -1):
                result.append(matrix[b][i])
        b -= 1
        # up movement
        if le <= r:
            for i in range(b, t - 1, -1):
                result.append(matrix[i][le])
        le += 1
    return result
if __name__ == '__main__':
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    print(matrix_clockwise_traversal(matrix))
