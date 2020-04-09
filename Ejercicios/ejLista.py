def ejLista ():
    lista = [[2, 2, 5, 6], [0, 3, 7, 4], [8, 8, 5, 2], [1, 5, 6, 1]]
    accumulator = 0
    print('La lista original es: ')
    for x in range(len(lista)):
            print(lista[x])
    print('El tercer subarray es: ', lista[2])
    for row in range(len(lista)):
        for column in range(len(lista[0])):
            accumulator = accumulator + lista[row][column]
            if row == column:
                lista [row][column] = 0
    print('La suma de todos los elementos es igual a: ', accumulator)
    print('La lista con los elementos de la diagonal principal = 0 queda: ')
    for x in range(len(lista)):
            print(lista[x])
    lista = [[2, 2, 5, 6], [0, 3, 7, 4], [8, 8, 5, 2], [1, 5, 6, 1]]
    for row in range(len(lista)):
        for column in range(len(lista[0])):
            if lista[row][column]%2:
                lista [row][column] = 0
            else:
                lista [row][column] = 1
    print('Si reemplazo los elementos pares por 0 y los impares por 1 la lista queda: ')
    for x in range(len(lista)):
            print(lista[x])
ejLista()
