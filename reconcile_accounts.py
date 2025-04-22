#IMPORTANTE: para o código fucnionar corretamente, é essencial que os arquivos transactions1.csv e transactions2.csv estejam no mesmo diretório que o arquivo do código.py

#Importando as bibliotecas necessárias:
import csv
from pathlib import Path
from pprint import pprint
from datetime import datetime, timedelta

#Caminho para os arquivos:
transactions1_path = Path("transactions1.csv")
transactions2_path = Path("transactions2.csv")

#A função 'read_csv_to_list' irá ler e colocar em linha o conteúdo dos arquivos:
def read_csv_to_list(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        return [row for row in csv.reader(csvfile)]

#A função 'sort_transactions_by_date' ordena as transações em ordem crescente de data:
def sort_transactions_by_date(transactions):
    return sorted(transactions, key=lambda row: datetime.strptime(row[0], '%Y-%m-%d'))
#Isso garante que as correspondências sempre sejam feitas de acordo com a transação que ocorre mais cedo
#Por exemplo, no arquivo 'transactions1_modificado.csv' foi adicionada a linha '2020-12-05,Jurídico,60.00,LinkSquares' antes da linha '2020-12-04,Jurídico,60.00,LinkSquares'
#O output será 'FOUND' para a linha '2020-12-04,Jurídico,60.00,LinkSquares', mesmo ela vindo depois no arquivo original, porque a transação aconteceu antes

#Definindo a estrutura dos arquivos, como um dicionário, a partir das colunas para evitar erros na correspondência:
def to_structured_list(transactions):
    return [
        {'date': datetime.strptime(row[0], '%Y-%m-%d'), 'row': row.copy(), 'matched': False}    #Aqui, também está sendo adicionada a coluna 'matched', ela garante que uma vez que a correpondência de uma linha tenha sido realizada, ela não irá se repetir (ser reutilizada)
        for row in transactions
    ]

#Função 'reconcile_accounts':
def reconcile_accounts(transactions1, transactions2):
    #Chamando a função 'sort_transactions_by_date' para ordenar os arquivos por data:
    transactions1 = sort_transactions_by_date(transactions1)
    transactions2 = sort_transactions_by_date(transactions2)

    #Estruturando (separando) em colunas os arquivos transactions1 e transactions2:    
    t1 = to_structured_list(transactions1)
    t2 = to_structured_list(transactions2)

    #Guardando os vetores (listas) dos arquivos correspondidos:
    out1 = []
    out2 = []

    #Loop que irá correr as linhas do arquivo transacitions1 e suas colunas em busca da correspondência no transacitions2:
    for trans1 in t1:
        date1 = trans1['date']
        category, value, desc = trans1['row'][1:]
        found = False

        #Loop a partir das datas das transações:
        for delta in [timedelta(days=-1), timedelta(days=0), timedelta(days=1)]:  #Lembrando que o critério para o match de uma transação pode ser feita para datas de -1 dia, datas exatas ou datas de +1 dia
            target_date = date1 + delta

            #Loop que irá correr as linhas do arquivo transactions2:
            for trans2 in t2:
                if trans2['matched']:
                    continue
                if trans2['row'][1:] != [category, value, desc]:
                    continue
                if trans2['date'] != target_date:
                    continue

                #Encontrando os matches (correspondências):
                trans1['matched'] = True
                trans2['matched'] = True
                out1.append(trans1['row'] + ['FOUND'])    #Quando uma correspondência é encontrada, escrever na nova coluna 'FOUND'
                out2.append(trans2['row'] + ['FOUND'])
                found = True
                break

            if found:
                break

        #Se nenhum match for encontrado, então escrever na nova coluna 'MISSING':
        if not found:
            out1.append(trans1['row'] + ['MISSING'])

    for trans2 in t2:
        if not trans2['matched']:
            out2.append(trans2['row'] + ['MISSING'])

    return out1, out2

#Chamando os arquivos transactions1.csv e transactions2.csv:
transactions1 = read_csv_to_list(transactions1_path)
transactions2 = read_csv_to_list(transactions2_path)

#Realizando a correspondência dos arquivos transactions1.csv e transactions2.csv:
out1, out2 = reconcile_accounts(transactions1, transactions2)

'''
#Printando os arquivos originais transactions1.csv e transactions2.csv
print("Arquivo transactions1.csv:")
pprint(transactions1)
print("Arquivo transactions2.csv:")
pprint(transactions2)
'''

print("Correspondência dos arquivos em ordem crescente de data:")
pprint(out1)
pprint(out2)

#COMENTÁRIO FINAL: como a principal forma de verificar a correspondência entre os arquivos transactions1 e transactions2 é através das datas das transações, acredito que o excel seria uma ferramenta mais dinâmica, interativa e visual do que um código em python. Apesar de que também é possível combinar essas duas ferramentas através da biblioteca Pandas, por exemplo, ao invés de converter os arquivos .xlsx para .csv ou usar a função função 'read_csv_to_list', o que encurtaria o tempo computacional do código
#A princial vantagem do código em relação ao excel, contudo, está na possibilidade de ampliar o banco de dados: os arquivos transactions1 e transactions2 são curtos, com apenas 6 linhas, mas o código acima conseguiria trabalhar facilmente com milhares de linhas de transações ao longo de décadas, o que seria uma desvantagem para o excel