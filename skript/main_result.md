Ein ideales Hexagon gibt uns ein Dreieck, das durch die geodätischen Diagonalen gegeben ist.
[Animiere Figure 5]
Wir zeigen nun den folgenden Satz.
*Für jedes ideale Hexagon ist der alternierende Umfang bis auf das Vorzeichen genau zweimal der Umfang von dem Dreieck,
das durch die geodätischen Diagonalen aufgespannt wird.*

_Beweis:_
Ein semiideales Dreieck ist ein hyperbolisches Dreieck mit zwei idealen Knoten, also am Rand des Kreises und einem
Knoten in der hyperbolischen Ebene. In unserem idealen Sechseck gibt es drei semiideale Dreiecke - Y_1, Y_2 und Y_3 -
sowie drei semiideale Dreiecke, die das innere Dreieck schneiden - G_1, G_2 und G_3.

Wir definieren uns nun eine ähnliche Größe wie den alternierenden Umfang. Wenn wir die Seiten eines semiidealen Dreiecks
betrachten und jeweils disjunkte Horodisks (deutsch?) entfernen und nun die Seite, die die beiden Randpunkte verbindet,
von den anderen beiden Seiten abziehen, kommen wir auf eine ähnliche Definition wie der alternierende Umfang.
[Bild einfügen]
Da wir jeweils die gleiche Länge hinzufügen und wieder abziehen, hängt diese Größe nicht von den Horodisks, die wir
wählen, ab.

Die Dreiecke G_k und Y_k teilen sich genau einen Knoten.
[Animation jeden Knoten für k=1,2,3 einmal kurz markieren]
Es gibt jeweils eine Isometrie I_k, die diese Knoten aufeinander abbildet, also I_k(Y_k) = G_k.
_evtl noch weiter erläutern..._

Also gilt A(Y_k) = A(G_k). Wenn wir das alles aufsummieren, kommen wir auf
[Formel animieren, zuerst alle Formeln aufschreiben, dann zusammenaddieren]
A(Y_1) + A(Y_2) + A(Y_3) - (A(G_1) + A(G_2) + A(G_3)) = 0

Wenn wir uns diese Formel genauer betrachten, können wir sehen, dass die einzelnen Summanden aus Geodätischen, die
benachbarte Punkte auf dem Rand verbinden bestehen und denen, die gegenüberliegende Punkte verbinden. Wenn wir erstere
zusammenaddieren, bekommen wir unseren gesuchten alternierenden Umfang A(P) bis auf das Vorzeichen. Wenn wir den Rest
aufsummieren, bekommen wir zweimal den Umfang von T_P.
_todo vllt. noch genauer erklären_

_Recap Theorem 3.1_

Nun können wir damit die finale Formulierung des Sieben Kreise Satzes beweisen. Wir sagen, dass ein Hexagon eine
Punktreflexionssymmetrie hat, falls es eine nichttriviale Isometrie gibt, die einen einzelnen Fixpunkt hat und unter
welcher das Hexagon invariant bleibt.
[Animation Beispiel Punktreflexionssymmetrie]
Diese Abbildung nennen wir dann eine Punktreflexion. Sie bildet gegenüberliegende Seiten aufeinander ab.

Die finale Formulierung des Sieben Kreise Satzes lautet wie folgt:
Die folgenden drei Aussagen sind äquivalent:

- Die Geodätischen, die die gegenüberliegenden Seiten von P verbinden, treffen sich an einem Punkt.
- P hat eine Punktreflexion.
- Der alternierende Umfang von P ist 0.

Um eine Äquivalenz zu zeigen, müssen wir drei Richtungen beweisen.

1 -> 2:
