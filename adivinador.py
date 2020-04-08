def adivinar(intentos,guess):
    import random
    number = random.randint(0,100)
    if guess == number:
       print('Adivinaste en', 4-intentos , 'intentos')
       intentos = False
    else:
        if intentos !=1:
            print("No, te quedan", intentos-1 , "intentos")
            intentos -= 1
        else: 
            if guess != number:
                print("Te quedaste sin intentos")
                intentos = False
    return intentos

def adivinador():
    tries = 3
    while tries:
        number = int(input('Ingrese el numero: '))
        tries = adivinar(tries, number)
    return


adivinador()
