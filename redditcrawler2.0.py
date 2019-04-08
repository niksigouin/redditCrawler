import sys, pprint, json, csv, re, datetime

from psaw import PushshiftAPI
# today = str(datetime.datetime.now())

# TODO:
# -Change filter examples for subs or comments
# -Add which terms were used


# Fonction de selection des filtres a appliquers
def filterselect():
    # Demande a l'utilisateur filtres et garde dans le resultat dans user_input
    choices = '''
**************** ENTER FILTERS ****************
 (USE COMMAS TO DELIMIT MULTIPLE FILTERS)

 [id].........= Identifier of post/comment		
 [title]......= Title of submission (SUB ONLY)
 [author].....= Author of comment/submission
 [body].......= Text of a comment (COMMENT ONLY)
 [selftext]...= Text of a submisson (SUB ONLY)
 [subreddit]..= Name of subreddit posted to

***********************************************
'''
    user_input = input(choices)
    # Separe le resultat a chaque virgule et converti le tout en liste
    input_list = user_input.split(',')
    filter_list = [str(x.strip()) for x in input_list]
    # print(filter_list)
    return filter_list

def searchterms():
    ui = input('Single [S] or Multi? [M]')
    terme_list = []

    if ui == 's':

        print('user single')


    elif ui == 'm':
        termes = input('Enter termes: ')
        terme_list.append(termes)
        print('user mutli ', terme_list)

    return terme_list


def searchreddit():
    while True:
        api = PushshiftAPI()
        search_sub = api.search_submissions()
        #Demande l'utilisateur ce qu'il veux rechercher
        ur = input('''
****** What would you like to search in? ******
   [sub] = Submissons (Reddit post)		
   [com] = Comments   (Reddit comments)
   --------------------------------------
               [e]  = EXIT
***********************************************
''')

        #comparaison du resultat pour savoir si la recherche s'effectu dans les 'submissions' ou les 'comments'
        if ur == 'sub':
            #Crée une liste vide pour les résultat à venir
            results = []
            search_terms = input('**************** SEARCH TERMS? ****************\n')
            search_limit = input('**************** OUTPUT LIMIT *****************\n')
            #Appel l'API avec appelation de l'utilisateur pour le choix du terme de recher, la limite de recherches ainsi que les filtres a utiliser.
            gen = api.search_submissions(q = searchterms(), limit=int(search_limit), filter = filterselect())
            #Ajoute a la liste chacun des éléments trouve selon les parametres demandé et la PRINT
            for r in gen:
                results.append(r)
            # print(results)

        elif ur == 'com':
            # Crée une liste vide pour les résultats à venir
            results = []
            search_terms = input('**************** SEARCH TERMS? ****************\n')
            search_limit = input('**************** OUTPUT LIMIT *****************\n')
            # Appel l'API avec appelation de l'utilisateur pour le choix du terme de recher, la limite de recherches ainsi que les filtres a utiliser.
            gen = api.search_comments(q = search_terms, limit=int(search_limit), filter = filterselect())
            # Ajoute a la liste chacun des éléments trouve selon les parametres demandé et la PRINT
            for r in gen:
                results.append(r)
                # print(results)
            #Terminer le loop si l'utilisateur appel EXIT
        elif ur == 'exit' or 'e':
            break
        #Pour tout autres choix, continuer la loop
        else:
            print('Invalid choice')
            continue

        ui = input('''
***************** SAVE OUTPUT *****************
    SAVE TO .CSV FILE? (Compatible w/ excel)
	        [y] = Yes
                [n] = No
                  ----OR----
	[h] = View in command line
''')

        if ui == 'y':
            # filename = input('file name: ')
            with open(search_terms + '.csv', 'w', encoding='utf-8') as new_file:
                csv_writer = csv.writer(new_file, delimiter=',')
                for line in results:
                    csv_writer.writerow(line)
        elif ui == 'h':
            pprint.pprint(results)

searchreddit()
# searchterms()