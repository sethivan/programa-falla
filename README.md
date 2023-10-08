# programa-falla
Programa en Python de gestió de la Falla Sants Patrons

## Introducció
La creació d'aquest programa per al control de l'oficina de la falla apareix, en un principi, per la falta d'opcions en el programa actual. El fet que les rifes, les domiciliacions, les loteries, les quotes o els descomptes familiars s'hagen de passar manualment comporta una pèrdua de temps molt important de cara a dur una correcta gestió de la falla. Si a això afegim el fet de que el programa (i el pc on s'executa) te molts anys i no hi ha copia de seguretat, es una raó molt important com per a ficar-se mans a l'obra per a construir un programa més estable, actual, portable i, sobretot, amb moltes més opcions i automatismes.

El programa s'ha d'encarregar de les següents tasques:
- Donar d'alta i baixa fallers.
- Agrupar els fallers per famílies.
- Crear un exercici nou en el que es calculen automàticament les quotes per edat, els descomptes familiars i el pendent o sobrant de l'any anterior de forma que mostre directament la quota final a pagar.
- Assignar automàticament les rifes a aquells fallers que els toque per edat quan ho requerisca l'administrador.
- Calcular automàticament els pagaments de loteria i els beneficis derivats de la venda a partir de les dades d'arreplega de loteria de cada faller ingressada al sistema per l'administrador.
- Controlar els pagaments de quota, loteria i rifa realitzats pels fallers tant en metàl·lic com per ingrés bancari o domiciliació.
- Crear i mantenir automàticament l'historial de cada faller i poder-lo modificar manualment en cas que siga necessari.

## Descripció del problema
Hem de crear una aplicació d'escriptori amb la qual gestionar el dia a dia d'una associació amb un volum alt d'associats, de forma que pugam dispossar de la major quantitat possible d'automatismes que ens ajuden a realitzar les diferents gestions d'una forma fàcil, ràpida i segura.

## Objectius
L'objectiu principal es dur la gestió automatitzada de la falla a la seua màxima expressió. Hem de reduir al mínim els processos manuals que comporten errors en gestió d'assignacions, pagaments, cens d'associats, etc.
A més, necessitem que totes aquestes accions queden emmagatzemades, de forma que es puga tindre accés a qualsevol moviment de diners, alta, baixa o qualsevol gestió que s'haja fet en la falla en qualsevol exercici anterior.
A part d'això, tenim l'objectiu de poder traure informes en pdf o qualsevol altre format per a proveïr a secretaría o altre departament de l'associació del que puguen necessitar d'una forma ràpida i fiable.

## Instruccions d'ús
Per a poder utilitzar el programa 
