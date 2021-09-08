# pdf2epub

pdf2epub konvertiert eine exemplarische, als pdf vorliegende Masterarbeit in ein ebook im epub-Format.

# Start
über Konsole
python3 main.py
Keine Angabe von Parametern notwendig
Auswahl der Datei siehe 'Hinweise'

# Hinweise
Die Auswahl der pdf-Datei, die gewandelt wird ist momentan hart codiert. Sie befindet sich im Unterordner /testfiles und wurde dort mit Latex erstellt. Die Auswahl kann in in main.py geändert werden.
Benötigt werden die Bibliotheken:
xml.dom.minidom (meist in Installation enthalten)
pdfminer.six

Zur Konvertierung von xhtml zu epub wird pandoc verwendet. Pandoc muss auf dem PC installiert sein und über die Konsole aufgerufen werden können.

## Verarbeitungspipeline
### 1. pdf2dom
Mithilfe der Bibliotheken pdfminer und minidom wird das pdf-Dokument eingelesen und in ein Document Object Model (DOM) konvertiert. Die Objekte/Knoten des Modells sind in diesem Fall: Page, Textgroup, Textbox, Textline und Text.
Eine Page enthälte Textgoups und Textboxen als Kinder. Eine Textgroup kann weitere Textgroups oder Textboxen als Kinder enthalten. Eine Textbox enthält Textlines als Kinder. Eine Textline enthält wiederum Text. Das Objekt Text enthält einen Buchstaben (der eigentliche Text) und Informationen zu Schriftart, -größe und -farbe.
### 2. domdocument2pages
Für die Repräsentation des Dokuments sind eigene hirarchische Objekte angelegt,sogenannte Pages. Der Name kommt daher, dass eine Liste von Pages den Knoten in der Baumstruktur dieser Objekte darstellt. Der hirarchische Aufbau des Baums und der Objekte ist ähnlich dem des DOMs, die eigenen Objekte enthalten im Vergleich zu den DOM-Objekten allerdings weitere Attribute und sind für die interne Weiterverarbeitung besser geeignet. Die einzelnen Buchstaben im DOM werden durch Wörter oder Fließtext ersetzt, die dann Kinder der Textlines sind. Jede Textline besitzt zudem die Variable 
Bei der Umwandlung des DOM in Pages wird das Dokument in Betracht auf die Schrift analysiert. Die Informationen aus dieser Analyse finden sich anschließend als Objektattribute wieder.
### 3. pages2book
Als Vorstufe zur Konvertierung in epub ist ein xhtml-Dokument nötig. Als Vorstufe dafür muss die Baumstruktur der Pages in eine Struktur umgewandelt werden, in der jedes Objekt ein Element in xhtml als Pendant besitzt. Diese Struktur ist intern als Book angelegt. Book ist dabei der Knoten. Er enthält als Blätter Objekte, die sich in ein xhtml-string wandeln lassen.
Die größte Herausforderung dabei ist es die einzelnen Abschnitte des Dokumentes bzw der Pages zu kategorisieren. Was ist eine überschrift, was ist ein Abschnitt, was eine Tabelle? Dies lässt sich nicht mit hundertprozentiger Gewissheit sagen, weshalb hier Heuristiken verwendet werden. Die Heuristiken werden in zwei Iterationen auf alle Textzeilen im Dokument angewandt. Sie versuchen herauszufinden zu welcher Art von Element die jeweilige Textzeile gehört. Dafür enthält jede Textzeile eine Variable Dort gibt es für jeden Hinweis auf eine Kategorie Punkt für die jeweilige Kategorie. Nach dem Durchlaufen aller Heuristiken wird die Kategorie mit den meisten Punkten als die wahrscheinlichste betrachtet.
Die sogenannten 'einfachen' Heuristiken im ersten Schritt arbeiten nur mit den Informationen, die bereits in den Pages-Objekten enthalten sind. Sie teilen sich erneut in drei Schritte auf: Heuristiken für Reguläre Ausdrücke, für Schriftanalyse und für Inhalts- bzw Layoutanalyse.
Im zweiten Schritt werden die Erkenntnisse aus dem ersten Schritt von den Heuristiken benutzt und es kann zum Beispiel geschaut werden welche Kategorie für bestimmte interessierende Objekte wahrscheinlich ist.
### 4. book2epub
Die letzte Funktion erzeugt aus den Book-Blatt-Elementen ein xhtml Dokument. Mit Hilfe von Pandoc wird dieses anschließend in epub gewandelt.

## Verbesserungspotenzial
Die Heuristiken in Punkt 3 decken längst nicht alle Elemente ab, die in einem Dokument / eine Masterarbeit vorkommen können. Bei folgenden Elementen ist es sinnvoll sie noch zu implementieren, oder ihre Erkennung zu verbessern.
### Tabellen
Erkannt werden die Beschriftungen für Tabellen (Unter- / Überschriften). Der Inhalt der Tabellen selbst wird bisher weder als Tabelle erkannt, noch in ein entsprechendes Objekt überführt. Für die Erkennung von Tabellen müsste erst analysiert werden, wie diese im DOM repräsentiert werden (Vermutlich eine Textbox pro Zelle, gesammelt in einer Textgroup). Ein sehr starkes Indiz ist auch ein Tabellenbeschriftung in der Nachbarschaft zum Element. Anschließend müssen die einzelnen Zellen über ihre Position erkannt werden und in ein Book-Element überführt werden (zweidimensionales Array bietet sich an). Dieses wiederum muss eine Funktion besitzen, die den Inhalt als xhtml ausgibt (<table> </table>). 
### Listen
Nummerierte Listen werden aufgrund der Regeulären Ausdrücke derzeit oft als Überschriften erkannt. Um dies zu verhindern könnte man die Gewichtung des Punktesystems verändern oder negative Punkte für Überschriften bei 'normaler' Schriftgröße geben. Eine weitere Idee wäre die Lage zu überprüfen, da Aufzählungen meist eingerückt sind. Auch die Untersuchung benachbarter Elemente wäre sinnvoll (Es folgen keine zwei Überschriften der gleichen Hirarchie aufeinander.)
### Bilder
Pdfminder verarbeitet keine Bilder. Bilder sind im DOM somit gar nicht repräsentiert.
### Code
Code wird momentan ebenfalls nicht erkannt. Erkennungsmerkmale wären hier tatsächlich die Schriftfarbe im Vergleich zum restlichen Text und meist eine andere Schriftart.
