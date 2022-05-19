# PROYECTO COMPILADORES
# CARLOS ALFONSO SANCHEZ ROSALES
# A01703280 
# ITESM CAMPUS QRO
# 29 ABRIL 2022

#PARA CORRER ES python3 lexer.py, e ingresamos el numero y posteriormente las n instrucciones.

#FUNCION PARA DETERMINAR LOS FIRSTS DE LAS NOTERMINALES, A PARTIR DE SUS PRODUCCIONES
# SE APLICAN LAS TRES REGLAS, POR LO CUAL, SE DIVIDE LA PRODUCCIÓN PARA IR EVALUANDO EL PRIMER ELEMENTO Y ES QUE SI
# SE APLICA LA PRIMER REGLA SI EL PRIMER X ES TERMINAL SE AGREGA, SI ES UN NO TERMINAL REALIZA LA RECURSION PARA CALCULAR LOS
# SIGUIENTES FIRSTS DE LA TERMINAL ENCONTRADA
# AGREGA EL EPSILON SI SE ENCUENTRA EL CASO, ESTO LO AGREGAMOS A LA LISTA FIRST PARA PODER IR GUARDANDOLOS.
def getTerminals (inputsaux, term, terminales, noterminales) :
    firsts = []
    for renglon in inputsaux:
        aux = renglon.split()
        if aux[0] == term and term != aux[2]:
            if not aux[2] in noterminales :
                if not aux[2] in firsts:
                    firsts.append(aux[2])
            else :
                firtsaux = []
                firtsaux = getTerminals(inputsaux, aux[2], terminales, noterminales)
                for first in firtsaux:
                    if first not in firsts:
                        firsts.append(first)
    return firsts

#FUNCION PARA OBTENER LOS FOLLOWS DE UNA NO TERMINAL A PARTIR DE UNA GRAMATICA
#SE VALIDAN LAS TRES REGLAS, EN EL PRIMER CASO SE EVALUA SI HAY 2 O MÁS PRODUCCIONES CON LA TERMINAL
# QUE ESTAMOS EVALUANDO EL FOLLOW, COMO PRIMERO SI ES LA PRIMERA TERMINAL SE AÑADE EL $ POR DEFAULT
# PARA DESPUÉS VALIDAMOS SI EN EL LADO DERECHO DE LA PRODUCCION ESTA  LA TERMINAL
# SI VEMOS QUE EL TERMINAL ESTA AL FINAL ACTIVAMOS PARA LA REGLA 3
# EN CASO CONTRARIO SI VEMOS QUE SIGUE UN  NOTERMINAL DESPUES DE LA NOTERMINAL
# OBTENEMOS LOS FIRSTS EXCEPTO EL EPSILON LO AGREGAMOS A LA LISTA DE FOLLOWS SI ENCONTRAMOS UN EPSILON ACTIVAMOS LA 3RA REGLA
# SI ES UN TERMINAL, LO AÑADIMOS SOLAMENTE A LA LISTA DE FOLLOWS
# FINALMENTE SI LA REGLA TRES SE ACTIVO SI EL LADO IZQUIERDO ES DIFERENTE DEL VALOR ENTONCES OBTENEMOS LOS FOLLOWS DE IZQUIERDA
# Y LO AGREGAMOS AL FOLLOW EXCEPTO EL EPSILON
# FINALMENTE REGRESAMOS
def getFollows(inputsaux, term, terminales, noterminales):
    follows = []
    #print('1. ', term)
    for renglon in inputsaux:
        regla3 = False
        left, right = renglon.split(' -> ')
        aux = right.split()
        size_r = len(aux)
        #print(' El tamaño es de ', size_r)
        #print(' Term is ', term, ' and not terminal is ', noterminales[0])
        #print('El tamaño de term', len(term), ' el tamaño de notermial es ', len(noterminales[0]))
        #print(term == noterminales[0])
        if term == noterminales[0] and not '$' in follows:
            #print(' Es el primero, así que se añade $')
            follows.append('$')
        contador = 0
        for val in aux:
            #print('Estamos buscando si en ', aux, ' esta ', term)
            if val == term:
                #print( ' El valor ', val, ' es igual al term ', term)
                #print('contador es ', contador + 1, ' tamaño es ', size_r)
                if contador + 1 == size_r:
                    regla3 = True
                else:
                    if aux[contador + 1] in noterminales:
                        #print('aux es', aux[contador + 1])
                        firsts = getTerminals(inputsaux,aux[contador + 1],terminales, noterminales )
                        #print(firsts)
                        if '\'' in firsts:
                            regla3 = True

                        for first in firsts:
                            if first != '\'' and not first in follows:
                                follows.append(first)
                    else:
                        follows.append(aux[contador + 1])
                if regla3:
                    #print('left is ', left)
                    if left != val:
                        #print('Left si es diferente de val')
                        auxFollow = getFollows(inputsaux, left.strip(), terminales, noterminales)
                        #print('auxFollo es ', auxFollow)
                        for follow in auxFollow:
                            if not follow in follows and follow != '\'':
                                follows.append(follow)
                
            contador += 1

    #print('follows de ', term , ' son ', follows)
    return follows
        
#FINALMENTE, TENEMOS EL SI ES UN LL(1), PARA ESTE CASO VAMOS EVALUANDO POR GRUPO DONDE HAYA DOS O MAS PRODUCCIONES DE 
# UNA NO TERMINAL, DADA, POR LO CUAL, ES LO PRIMERO QUE  SE EVALUA PARA PODER EVALUAR LAS TRES REGLAS
# POSTERIORMENTE VEMOS QUE LAS PRODUCCIONES NO EMPIECEN IGUAL, YA QUE EN CASO CONTRARIO
# SERÍA FALSO QUE ES LL1 Y TERMINA DE EVALUAR
# EN CASO CONTRARIO REVISAMOS SI HAY UN EPSILON, SI ES EEL CASO , OBTENEMOS EL FOLLOW Y FIRST DE LA TERMINAL
# Y VALIDAMOS QUE LA INTERSECCIÓN SEA NULA, EN CASO CONTRARIO NO ES LL(1)
# FINALMENTE, VALIDAMOS QUE SOLO A LO MAS HAYA 1 EPSILON, EN CASO CONTRARIO NUEVAMENTE NO ES LL(1)
# AL FINAL SI NO EVALUA SI CUMPLE CON LAS TRES REGLAS
def isLL (inputsaux, term, terminales, noterminales):
    _startswith = []
    for renglon in inputsaux:
        left, _ = renglon.split('-> ')
        #print(' left is size', left.strip(), 'term is ', len(term))
        if left.strip() == term:
            _startswith.append(renglon)

    
    auxFirst = []
    epsilon = 0

    if len(_startswith) > 1:
        #print('las producciones a analizar son: ', _startswith)
        for prod in _startswith:
            aux = prod.split()
            
            #print('result is ', aux[2].strip())
            firstaux = []
            valu = aux[2].strip()
            #print('aux es ', valu)
            #print( 'el largo de value es ', len(valu) , ' y es ', valu)
            if valu in terminales:
                firstaux.append(valu)
            else: 
                firstaux = getTerminals(inputsaux, valu, terminales, noterminales)
            #print('Los firsts de ', valu, ' son ', firstaux)
            for first in firstaux:
                if not first in auxFirst:
                    auxFirst.append(first)
                else:
                    #print(' No cumple en la primera')
                    return False
                if aux[2] == '\'':

                    epsilon += 1
        
        if (epsilon == 1 ):
            follows = getFollows(inputsaux, term, terminales, noterminales)
            firsts = getTerminals(inputsaux, term, terminales, noterminales)
            intersec = list(set(follows) & set(firsts))

            if(len(intersec) > 0 ):
                #print(' No cumple en la segunda')
                return False
        else:
            if (epsilon > 1):
                #print(' No cumple en la tercera')
                return False
    
    return True
    

#AUXILIARES PARA GUARDAR ENTRADAS, Y SEPARAR IZQUIERDA DE LA -> Y DERECHA
inputs = []
left=[]
right=[]

#LEEMOS EL NUMERO DE ENTRADAS QUE TENDREMOS
veces = int(input())

#EMPEZAMOS A LEER Y LO GUARDAMOS EN UNA LISTA INPUTS
for i in range(0,veces):
    _input = input()
    inputs.append(_input)

#AUXILIAR PARA SACAR CADA ELEMENTO DE CADA RENGLON LEIDO
aux = []

#POR CADA RENGLON SACAMOS CADA ELEMENTO Y LO PONEMOS EN LISTA USAMOS FLAG PARA SABER SI ESTAMOS A LA IZQUIERDA O DERECHA DE LA FLECHA
#ADEMAS DE VERIFICAR SI YA ESTA EN ELEMENTO EN LA LISTA PARA NO DUPLICARLO
for renglon in inputs:
    aux = renglon.split()
    flag_sep = False
    for palabra in aux:
        if palabra == '->':
            flag_sep = True
        else:
            if flag_sep:
                if not palabra in left:
                    left.append(palabra)
            else :
                if not palabra in right:
                    right.append(palabra)


#ELIMINAMOS LA ' YA QUE ES EL CASO DE EPSILON
if "\'" in right:
    right.remove("\'")
if "\'" in left:
    left.remove("\'")

#VARIABLES AUXILIARES PARA DETERMINAR LAS TERMINALES Y NO TERMINALES
Terminal = []
NonTerminal = []
separator = ", "

#VERIFICAMOS QUE LAS PALABRAS DE LA IZQUIERDA  ESTAN EN LA DERECHA PARA DETERMINAR TERMINALES
for palabra in left:
    if not palabra in right:
        Terminal.append(palabra)

#Y VALIDAMOS QUE LAS QUE YA SON TERMINALES DE LADO DERECHO PARA AGREGAR LAS NO TERMINALES
for palabra in right:
    if not palabra in Terminal:
        NonTerminal.append(palabra)

#FINALMENTE DAMOS EL DISENO PARA ENLISTARLAS E IMPRIMIMOS
auxTerminal = separator.join(Terminal)
auxNTerminal = separator.join(NonTerminal)
#print('Terminal: ', auxTerminal)
#print('Non terminal: ', auxNTerminal)

# CICLO PARA SACAR LOS FIRSTS Y FOLLOS DE UN NO TERMINAL
for noterminal in NonTerminal:
    firsts = getTerminals(inputs, noterminal,Terminal, NonTerminal)
    #print(' firsts de ', noterminal, 'son ', firsts)
    cont = 0
    for word in firsts:
        #print(' El first es ', word)
        #print(word == '\'')
        if word == '\'':
            firsts[cont] = '\' \''
        cont += 1
    follows = getFollows(inputs, noterminal,Terminal, NonTerminal)
    aFirst = separator.join(firsts)
    aFollows = separator.join(follows)
    #print(' firsts previos', firsts)
    print(noterminal, '=> FIRST = {',aFirst,'}, FOLLOW = {', aFollows,'}')

#CICLO PARA EVALUAR SI ES LL(1), EN CUANTO ENCUENTRE QUE UN CONJUNTO NO CUMPLIO SE ROMPE EL CICLO Y SE DEFINE COMO NO LL YA QUE
# SIEMPRE DEBE CUMPLIR TODOS ESA REGLA
_isLL = True
for noterminal in NonTerminal:
    if _isLL:
        _isLL = isLL(inputs, noterminal,Terminal, NonTerminal)

if _isLL:
    _ans = 'Yes'
else: 
    _ans = 'No'

print('LL(1)?', _ans)





    