#IMPORTANTE: para o código fucnionar corretamente, é essencial que o arquivo my_file.txt esteja no mesmo diretório que o arquivo do código.py

#Importando as bibliotecas necessárias:
import io
from pathlib import Path

#A função 'last_lines' irá ler o arquivo my_file.txt em blocos de tamanho 8KB e gerar as linhas em ordem reversa
def last_lines(my_file: Path, buffer_size=io.DEFAULT_BUFFER_SIZE):
    file_size = my_file.stat().st_size

    #Caso o arquivo my_file.txt seja pequeno, como é o caso do exemplo, as linhas abaixo descrevem um código simples que nos dá as linhas em ordem reversa direto:
    if file_size < buffer_size:
        with my_file.open(encoding='utf-8') as f:   #A variável 'f', o file handler, é um ponteiro dentro do arquivo que permite navegar entre as linhas escritas nele
            lines = f.readlines()
        for line in reversed(lines):    #Revertendo a ordem das linhas do arquivo
            input()                     #Interatividade com o usuário no terminal. Cada vez que o 'enter' for pressionado, uma nova linha em ordem reversa será printada no terminal
            print(line.strip())         #Printando a linha em ordem reversa
        print("\nFim do arquivo")
        return

    #Caso o arquivo seja grande, que é a principal instrução do exercício, usar leitura reversa em blocos ('rb'=read binary):
    with my_file.open('rb') as f:
        f.seek(0, io.SEEK_END)          #Move o ponteiro file handler para o fim do arquivo
        block_end = f.tell()            #Enquanto o ponteiro não estiver no início do arquivo, o loop permanece ativo
        buffer = b""                    #Como iremos reverter as linhas em blocos, a variável 'buffer' armazena os dados do bloco atual mais qualquer sobra do bloco anterior para que linhas e/ou caracteres não sejam cortados na metade
        newline = b"\n"                 #Define que a quebra de linha (\n) indica o início e o fim de uma nova linha no arquivo

        #Enquanto o ponteiro não estiver no início do arquivo, o loop permanece ativo:
        while block_end > 0:
            #Define onde os blocos começam e terminam dentro do arquivo, baseado no tamanho 8Kb
            block_start = max(0, block_end - buffer_size)
            f.seek(block_start)
            block = f.read(block_end - block_start)
            buffer = block + buffer
            lines = buffer.split(newline)

            #Se uma linha for quebrada no meio devido a contagem em tamanho de 8KB dos blocos, o código irá guardar essa linha para ser a primeira do próximo bloco:
            if block_start != 0:
                buffer = lines.pop(0)
            else:
                buffer = b""

            #Interatividade com o usuário no terminal. Cada vez que o 'enter' for pressionado, uma nova linha em ordem reversa será printada no terminal:
            for line in reversed(lines):
                input()
                print(line.decode('utf-8').strip())

            block_end = block_start

        print("\nFim do arquivo")

#Caminho para o arquivo my_file.txt:
my_file = Path("my_file.txt")

#Interagindo para definir o tamanho do bloco:
resposta = input("Deseja inserir um tamanho personalizado para a leitura do arquivo? (s/n): ").strip().lower()
if resposta == 's':
    valor = input(f"Digite o tamanho em bytes (mínimo de 512 bytes): ").strip()
    if not valor.isdigit():
        raise ValueError("Valor inválido. Usando o tamanho padrão de 8192 bytes")
    buffer_size = int(valor)
    if buffer_size < 512:
        raise ValueError(f"Tamanho muito pequeno! Usando o valor mínimo de 512 bytes")
else:
    buffer_size = io.DEFAULT_BUFFER_SIZE

#Chamando a função last_lines:
last_lines(my_file)

#print(io.DEFAULT_BUFFER_SIZE)    #Tamanho dos blocos definido a partir do valor padrão io.DEFAULT_BUFFER_SIZE = 8192 bytes ou aprox 8KB

#COMENTÁRIO FINAL: reverter as linhas de um arquivo .txt é uma tarefa simples. O que o exercício propõe é colocar restrições realistas, pensando em situações de arquivos gigantescos, como bases de dados imensas, em que
#não dá pra usar a linha 'lines = f.readlines()' sem estourar a RAM da máquina