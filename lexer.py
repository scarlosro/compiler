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

from cmath import pi
from email import header


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


def getTerminalsOnlyOne (inputsaux, term, terminales, noterminales, production) :
    firsts = []
    for renglon in inputsaux:
        if renglon == production:
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
def getFollows(inputsaux, term, terminales, noterminales, lastcall = None):
    follows = []
    for renglon in inputsaux:
        regla3 = False
        left, right = renglon.split(' -> ')
        aux = right.split()
        size_r = len(aux)
        if term == noterminales[0] and not '$' in follows:
            follows.append('$')
        contador = 0
        for val in aux:
            if val == term:
                if contador + 1 == size_r:
                    regla3 = True
                else:
                    if aux[contador + 1] in noterminales:
                        firsts = getTerminals(inputsaux,aux[contador + 1],terminales, noterminales )
                        if '\'' in firsts:
                            regla3 = True

                        for first in firsts:
                            if first != '\'' and not first in follows:
                                follows.append(first)
                    else:
                        follows.append(aux[contador + 1])
                if regla3:
                    if left != lastcall:
                        auxFollow = getFollows(inputsaux, left.strip(), terminales, noterminales,val)
                        for follow in auxFollow:
                            if not follow in follows and follow != '\'':
                                follows.append(follow)
                
            contador += 1

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
        if left.strip() == term:
            _startswith.append(renglon)

    
    auxFirst = []
    epsilon = 0

    if len(_startswith) > 1:
        for prod in _startswith:
            aux = prod.split()
            firstaux = []
            valu = aux[2].strip()
            if valu in terminales:
                firstaux.append(valu)
            else: 
                firstaux = getTerminals(inputsaux, valu, terminales, noterminales)
            for first in firstaux:
                if not first in auxFirst:
                    auxFirst.append(first)
                else:
                    return False
                if aux[2] == '\'':
                    epsilon += 1
        
        if (epsilon == 1 ):
            follows = getFollows(inputsaux, term, terminales, noterminales)
            firsts = getTerminals(inputsaux, term, terminales, noterminales)
            intersec = list(set(follows) & set(firsts))

            if(len(intersec) > 0 ):
                return False
        else:
            if (epsilon > 1):
                return False
    
    return True

def BuildHtmlRow(columns, isHeader=False):
	result = "<tr>"

	if isHeader:
		rowStart = "<th style=\"border: 1px solid black\">"
		rowEnd = "</th>"
	else:
		rowStart = "<td style=\"border: 1px solid black\">"
		rowEnd = "</td>"
	

	for _, value in enumerate(columns) :
		result += f"\n{rowStart} {value} {rowEnd}\n"
	
	result += "</tr>\n"

	return result


def  generateTable(inputsaux, terminales, noterminales):

    columnas = terminales
    columnas.append('$')

    tabla = {}
    for noterminal in noterminales:
        tabla[noterminal] = {}

    for noterminal in noterminales:
        for index, production in enumerate(inputsaux):
            left, _ = production.split(' -> ')
            if left == noterminal:
                firsts = getTerminalsOnlyOne(inputsaux, noterminal, terminales,noterminales, production)
                for first in firsts:
                    if first == "\'":
                        follows = getFollows(inputsaux, noterminal, terminales, noterminales)
                        for follow in follows:
                            new_production = "%s -> ' '" % (noterminal)
                            tabla[noterminal][follow] = new_production
                    else:
                        tabla[noterminal][first] = production

        
    html_output = ''' 
		<!DOCTYPE html>
		<html>
		<body>
		<table style="border: 1px solid black"> '''

    header_name = "Non Terminal"
    header = []
    header.append(header_name)
    for terminal in terminales:
        header.append(terminal)
    
    html_output += BuildHtmlRow(header, True)
    
    for key, values in tabla.items():
        elements = []
        elements.append(key)
        for index, terminal in enumerate(header):
            if index != 0:
                element = ''
                try:
                    element = values[terminal]
                except KeyError:
                    pass
                elements.append(element)
        html_output += BuildHtmlRow(elements)
    
    html_output += '''
		</table>
		</body>
		</html> '''
    
    file = open('output.html', "w")
    file.write(html_output)
    file.close()

    return tabla
        

def checkString(inputsaux, input, tabla):
    #print(inputsaux)
    pila = []
    left, _ = inputsaux[0].split(' -> ') 
    first_symbol = left

    #print(first_symbol)
    pila.append('$')
    pila.append(first_symbol)

    input_fila = input.split(" ")
    input_fila.append('$')

    while True:
        #print('Pila: ', pila)
        #print('Fila ', input_fila)
        if pila == []:
            return True
        else:
            element = pila[-1]
            fila_element = input_fila[0]

            if element == fila_element:
                pila.pop()
                input_fila.pop(0)
                continue
                
            try:
                element = tabla[element][fila_element]
            except KeyError:
                #print('elemento es ', element, 'fila es ', fila_element)
                return False

            pila.pop()
            _, right = element.split(' -> ')

            #print(right)
            if right == "\' \'":
                #print("true")
                continue

            tokens = right.split(" ")
            tokens.reverse()
            for token in tokens:
                pila.append(token)

#AUXILIARES PARA GUARDAR ENTRADAS, Y SEPARAR IZQUIERDA DE LA -> Y DERECHA
inputs = []
cadenasValidad = []
left=[]
right=[]


#LEEMOS EL NUMERO DE ENTRADAS QUE TENDREMOS
veces = int(input())
n_validar = int(input())


#EMPEZAMOS A LEER Y LO GUARDAMOS EN UNA LISTA INPUTS
for i in range(0,veces):
    _input = input()
    inputs.append(_input)

for i in range(0, n_validar):
    _cadena = input()
    cadenasValidad.append(_cadena)

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
    tabla = generateTable(inputs,Terminal,NonTerminal)
    for cadena in cadenasValidad:
        #print(cadena)
        if checkString(inputs, cadena, tabla):
            print('Yes!!!')
        else:
            print('No !!!')
else: 
    print('Grammar is not LL(1)!')






    