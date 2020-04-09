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
                print("La respuesta correcta era: " , number)
                intentos = False
    return intentos

def adivinador():
    tries = int(input("Deberá adivinar un numero del 0 al 100, indique cuantos intentos quiere: "))
    while tries:
        number = int(input('Ingrese un numero del 0 al 100: '))  
        tries = adivinar(tries, number)
    return


adivinador()
