# Résumé

L'outil de résumé est basé sur le calcul de similarité entre les phrases d'un texte.

On utilise l'outil de prétraitement de texte en français [french_preprocessing](https://github.com/anaishoareau/french_preprocessing).

L'outil de résumé est inspiré de l'article [Understand text summarization and create your own summarizer in python](https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70) proposé sur Towards Datascience.


<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Gestion-d'affichage-du-Notebook" data-toc-modified-id="Gestion-d'affichage-du-Notebook-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Gestion d'affichage du Notebook</a></span></li><li><span><a href="#Imports" data-toc-modified-id="Imports-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Imports</a></span></li><li><span><a href="#Chargement-des-outils" data-toc-modified-id="Chargement-des-outils-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Chargement des outils</a></span></li><li><span><a href="#Définition-des-entrées" data-toc-modified-id="Définition-des-entrées-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Définition des entrées</a></span></li><li><span><a href="#Résumé" data-toc-modified-id="Résumé-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Résumé</a></span></li></ul></div>

## Gestion d'affichage du Notebook


```python
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

CSS = """.output {align-items: center;}"""
HTML('<style>{}</style>'.format(CSS))
```


<style>.container { width:100% !important; }</style>





<style>.output {align-items: center;}</style>



## Imports


```python
# -*- coding: utf-8 -*-
from summarization import SimilaritySummary, tokenize_sentences
from french_preprocessing.french_preprocessing import FrenchPreprocessing
```

## Chargement des outils


```python
# Définition des stop_words pour notre cas d'usage
stop_words = ["ok", "mais", "cf", "n'", "ne", "pas", "plus", "bonjour", "merci", "on", "je", "tu", "il", "elle", "nous","vous","ils", "elles", "y","y'","m", "l", "d", "t", "qu", "s","c","m'",'hein', 'celle-là', 'ceux-ci', 'dring', 'sa', 'ollé', 'en', 'a', "d'", 'plutôt', 'auxquels', 'celles-ci', 'dès', 'tel', 'lui-meme', 'quelle', 'les', 'dont', 'aie', 'quand', 'pour', 'où', 'lès', 'suivant', 'ho', 'memes', 'hem', 'surtout', 'mien', 'tellement', 'qui', 'le', 'quels', 'tant', 'une', 'tien', 'ohé', 'i', 'mêmes', 'ceux', "l'", 'quelque', 'si', 'unes', 'lequel', 'tous', 'chacune', 'son', 'que', 'quel', 'au', 'ai', 'celui-là', 'chaque', 'ouste', 'es', 'hep', 'elles-mêmes', 'lors', 'cette', 'cependant', 'toc', 'tsouin', 'chacun', 'seule', 'siennes', 'hum', 'la', 'certains', "t'", 'trop', 'dans', 'desquels', 'lui', 'hors', 'celles-là', 'lui-même', 'pouah', 'toi-même', 'boum', 'vive', 'rend', 'mes', 'vos', 'nous', "qu'", 'des', 'tiens', 'hé', 'lorsque', 'zut', 'vlan', 'mienne', 'na', 'ma', 'selon', "s'", 'vous-mêmes', 'eh', 'ah', 'ses', 'meme', 'lesquels', 'miens', 'vôtres', 'paf', 'pif', 'quant-à-soi', 'tes', "c'", 'sien', 'ça', 'lesquelles', 'tout', 'telles', 'même', 'ces', 'maint', 'notre', 'quanta', 'elle-même', 'aupres', 'bas', 'votre', 'plusieurs', 'moi', 'par', 'hurrah', 'bah', 'laquelle', 'auxquelles', 'vé', 'peux', 'pure', 'tiennes', "aujourd'hui", 'hormis', 'couic', 'vous', 'ore', 'envers', 'moindres', 'aucune', 'gens', 'ouias', 'cela', 'quelles', 'aux', 'pff', 'etc', 'toutefois', 'leurs', 'ton', 'clic', 'las', 'pfut', "t'", 'toutes', 'cet', 'ta', 'da', 'toute', 'aucun', 'o', 'sapristi', 'quoi', 'desquelles', 'té', 'vôtre', 'euh', 'pres', 'as', 'fi', 'ci', 'allo', 'oh', "s'", 'quiconque', 'floc', 'avec', 'se', 'bat', 'tic', 'jusqu', "qu'", 'unique', 'certes', 'celles', 'dire', 'tienne', 'ha', 'nôtre', 'jusque', 'tac', 'ceux-là', 'sienne', 'uns', 'ouf', 'moi-même', 'et', 'vers', 'miennes', 'autrefois', 'houp', 'été', 'à', "d'", 'nouveau', 'être', 'peu', 'dite', "s'", 'dit', 'elles', 'tels', 'ou', 'toi', 'entre', 'avoir', 'hop', 'delà', 'nos', 'tres', 'telle', 'voilà', 'dessous', 'soit', 'autres', 'psitt', 'hélas', 'anterieur', 'hou', 'près', 'auquel', 'juste', 'chut', 'un', 'stop', 'eux', 'ès', 'vifs', 'ce', 'quoique', 'du', 'moi-meme', 'mon', 'brrr', 'sous', 'parmi', 'deja','déja','celle', 'siens', 'suffisant', 'â', "l'", 'apres', 'sans', 'soi-même', 'là', 'pur', 'via', 'differentes', 'specifique', 'holà', 'tsoin', 'pan', 'car', 'donc', 'dits', 'merci', 'particulièrement', 'nous-mêmes', 'personne', 'allô', 'soi', 'voici', 'sur', 'vif', 'celle-ci', 'malgré', 'puis', 'sauf', 'autre', 'hui', 'ceci', 'leur', 'celui-ci', 'necessairement', 'sacrebleu', 'hue', 'eux-mêmes', 'outre', 'alors', 'desormais', 'plouf', 'longtemps', 'malgre', 'après', 'de', 'oust', 'neanmoins', 'certain', 'crac', 'depuis', 'olé', 'hi', 'te', 'puisque', "m'", 'me', 'ô', 'celui', 'aussi', 'rares', 'chiche', 'rien', 'pfft', "c'", 'vu', 'clac', 'duquel', 'aavons', 'avez', 'ont', 'eu', 'avais', 'avait', 'avions', 'aviez', 'avaient', 'eus', 'eut', 'eûmes', 'eûtes', 'eurent', 'aurai', 'auras', 'aura', 'aurons', 'aurez', 'auront', 'aurais', 'aurait', 'aurions', 'auriez', 'auraient', 'aies', 'ait', 'ayons', 'ayez', 'aient', 'eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent', 'ayant', 'suis', 'est', 'sommes', 'êtes', 'sont', 'étais', 'était', 'étions', 'étiez', 'étaient', 'fus', 'fut', 'fûmes', 'fûtes', 'furent', 'serai', 'seras', 'sera', 'serons', 'serez', 'seront', 'serais', 'serait', 'serions', 'seriez', 'seraient', 'sois', 'soyons', 'soyez', 'soient', 'fusse', 'fusses', 'fût', 'fussions', 'fussiez', 'fussent', 'étant']
stop_words_completed = ['m’', 'flac', 'désormais', 'cinq', 'naturelles', 'differents', 'cent', 'nombreux', 'dernier', 'exterieur', 'peut', 'allaient', 'maximale', 'retour', 'relative', 'remarquable', 'cher', 'tenir', 'chers', 'anterieure', 'afin', 'suivants', 'chez', 'comment', 'partant', 'autrement', 'abord', 'beau', 'd’', 'différentes', 'precisement', 'vives', 'possessif', 'vivat', 'pourrait', 'enfin', 'effet', 'treize', 'comparables', 'pire', 'parseme', 'compris', 'devers', 'peuvent', 'permet', 'possessifs', 'procedant', 'ainsi', 'bigre', 'avant', 'revoilà', 'naturelle', 'dessus', 'différente', 'quatre-vingt', 'beaucoup', 'comparable', 'dehors', 'tenant', 'trente', 'minimale', 'suit', 'troisièmement', 'néanmoins', 'ouverts', 'seulement', 'douzième', 'suffit', 'j’', 'toujours', 'quinze', 'ouverte', 'assez', 'anterieures', 'absolument', 'parlent', 'quelconque', 'notamment', 'combien', 't’', 'dix', 'directement', 'onze', 'sixième', 'cinquantaine', 'speculatif', 'dedans', 'différent', 'qu’', 'onzième', 'pu', 'subtiles', 'parler', 'suivre', 'avons', 'quant', 'parfois', 'environ', 'possible', 'non', 'probante', 'bravo', 'moyennant', 'durant', 'restent', 'quelques', 'different', 'certaine', 'première', 'restant', 'devant', 'troisième', 'dix-sept', 'parle', 'premièrement', 'mince', 'revoici', 'c’', 'necessaire', 'uniformement', 'importe', 'ailleurs', 'neuvième', 'ouvert', 'faisaient', 'derrière', 'neuf', 'aujourd', 'etais', 'pense', 'tente', 'seul', 'dix-neuf', 'sein', 'autrui', 'certaines', 'huitième', "j'", 'rarement', 'reste', 'vingt', 'encore', 'derriere', 'parce', 'naturel', 'egale', 'très', 'comme', 'rare', 'quatorze', 'directe', 'quatrième', 'etre', 'façon', 'chères', 'trois', 'nombreuses', 'souvent', 'vas', 'dixième', 'touchant', 'superpose', 'devra', 'strictement', 'plein', 'contre', 'etait', 'multiple', 'semblent', 'egales', "quelqu'un", 'exactement', 'deuxièmement', 'font', 's’', 'deux', 'cinquantième', 'premier', 'tardive', 'etaient', 'concernant', 'diverses', 'attendu', 'debout', 'passé', 'diverse', 'suivante', 'seize', 'proche', 'restrictif', 'allons', 'excepté', 'sept', 'etant', 'divers', 'feront', 'cinquante', 'faisant', 'particulière', 'laisser', 'multiples', 'nul', 'semble', 'pouvait', 'rendre', 'maintenant', 'sait', 'ni', 'pourquoi', 'doit', 'relativement', 'extenso', 'egalement', 'douze', 'vais', 'dix-huit', 'bien', 'tend', 'uniques', 'prealable', 'basee', 'cinquième', 'chère', 'vont', 'derniere', 'deuxième', 'sent', 'n’', 'pourrais', 'va', 'specifiques', 'quatre', 'possibles', 'quarante', 'sinon', 'particulier', 'pendant', 'l’', 'mille', 'suffisante', 'moins', 'semblable', 'suivantes', 'six', 'semblaient', 'différents', 'doivent', 'huit', 'septième', 'fais', 'quatrièmement', 'soixante', 'fait', 'probable']

# Chargement des classes d'objets
f = FrenchPreprocessing(stopwords = stop_words+stop_words_completed)
ss = SimilaritySummary(f)
```

## Définition des entrées


```python
text = """Les vacances d'été.

Les vacances d'été en France durent 6 semaines et ont habituellement lieu entre Juillet et Septembre. En France, le début des vacances est souligné par les soldes d'été.

Il faut savoir que les étudiants comme les travailleurs attendent ces vacances avec impatiente. La majorité des Français ne restent pas dans leur région durant les vacances d'été.

Le sud du pays, l'Italie ou l'Espagne sont notamment les destinations touristiques les plus prisées des vacanciers en raison du climat perpétuellement froid dans le nord du pays.

Toutefois, certaines personnes ne disposent pas d'un budget spécial pour financer ce type de détente. Ils préfèrent alors rester à la maison et profitent du temps libre pour visiter leurs familles ou se balader en ville."""

print(text)
```

    Les vacances d'été.
    
    Les vacances d'été en France durent 6 semaines et ont habituellement lieu entre Juillet et Septembre. En France, le début des vacances est souligné par les soldes d'été.
    
    Il faut savoir que les étudiants comme les travailleurs attendent ces vacances avec impatiente. La majorité des Français ne restent pas dans leur région durant les vacances d'été.
    
    Le sud du pays, l'Italie ou l'Espagne sont notamment les destinations touristiques les plus prisées des vacanciers en raison du climat perpétuellement froid dans le nord du pays.
    
    Toutefois, certaines personnes ne disposent pas d'un budget spécial pour financer ce type de détente. Ils préfèrent alors rester à la maison et profitent du temps libre pour visiter leurs familles ou se balader en ville.
    


```python
sentences = " | ".join(tokenize_sentences(text, f)) # Définitions des phrases pour le résumé
preprocessed_text = f.preprocessing(sentences) # Texte prétraité servant au calcul des similarités
top_n = 5 # Nombre de phrases du résumé

print(preprocessed_text)
```

    vacance | vacance France devoir 6 semaine habituellement lieu juillet septembre | France début vacance souligner solde | falloir savoir étudiant travailleur attendre vacance impatiente | majorité français région vacance | sud pays Italie Espagne destination touristique prisé vacancier raison climat perpétuellement froid nord pays | personne disposer budget spécial financer type détente | préférer rester maison profiter temps libre visiter famille balader ville |
    

## Résumé


```python
ss.generate_summary(text, preprocessed_text, top_n = top_n)
```




    "les vacances d' été en france durent 6 semaines et ont habituellement lieu entre juillet et septembre | en france , le début des vacances est souligné par les soldes d' été | il faut savoir que les étudiants comme les travailleurs attendent ces vacances avec impatiente | le sud du pays , l' italie ou l' espagne sont notamment les destinations touristiques les plus prisées des vacanciers en raison du climat perpétuellement froid dans le nord du pays | toutefois , certaines personnes ne disposent pas d' un budget spécial pour financer ce type de détente"




```python

```
