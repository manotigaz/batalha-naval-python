import random
import time

tabuleiro_jogador = [['🌊'] * 9 for _ in range(9)]
tabuleiro_bot = [['🌊'] * 9 for _ in range(9)]
exibir_computador = [['🌊'] * 9 for _ in range(9)]
exibir_jogador = [['🌊'] * 9 for _ in range(9)]

estado = {
    'restante_jogador': 5,
    'restante_bot': 5,
}

def limpar_tabuleiros():
    global tabuleiro_jogador, tabuleiro_bot, exibir_computador, exibir_jogador, estado
    tabuleiro_jogador = [['🌊'] * 9 for _ in range(9)]
    tabuleiro_bot = [['🌊'] * 9 for _ in range(9)]
    exibir_computador = [['🌊'] * 9 for _ in range(9)]
    exibir_jogador = [['🌊'] * 9 for _ in range(9)]
    estado = {
        'restante_jogador': 5,
        'restante_bot': 5,
    }

print(' ')
print('Jogo Batalha Naval')
print(' ')

def menu():
    print('1. Começar o jogo')
    print('2. Regras')
    print('3. Sair')
    escolha = input('Digite uma opção: ')
    print()

    if escolha == '1':
        limpar_tabuleiros()
        posicao()
        posicao_bot()
        while True:
            tabuleiro_lado(tabuleiro_jogador, exibir_computador, ocultar_tab2=True)
            ataque(estado)
            if verificar_vitoria(estado):
                break
            time.sleep(0.5)
            ataque_bot(estado)
            tabuleiro_lado(exibir_jogador, exibir_computador, ocultar_tab2=True)
            if verificar_vitoria(estado):
                break
        print('Fim do jogo.')

    elif escolha == '2':
        print('Regras do Jogo:')
        print('1. O objetivo do jogo é afundar os navios do oponente.')
        print('2. Cada jogador tem um tabuleiro de 9x9.')
        print('3. Os jogadores se revezam para atacar.')
        print('4. O primeiro a destruir todos os navios vence.')

    elif escolha == '3':
        print('Saindo do jogo...')

    else:
        print('Opção inválida. Por favor, escolha uma opção válida.')


def exibir_tabuleiro(tabuleiro, ocultar=False):
    print("   " + " ".join(f"{i:2}" for i in range(9)))
    for i, linha in enumerate(tabuleiro):
        if ocultar:
            linha = ['🌊' if celula == '🚢' else celula for celula in linha]
        print(f"{i:2} " + " ".join(linha))
    print()


def posicao():
    exibir_tabuleiro(tabuleiro_jogador)
    time.sleep(1.5)

    print('Tabuleiro do Jogador:')
    print('Escolha a posição das suas 5 embarcações')
    time.sleep(1.5)

    contador = 0

    while contador < 5:
        linha = int(input('Digite a linha (0-8): '))
        coluna = int(input('Digite a coluna (0-8): '))
        print()

        if 0 <= linha < 9 and 0 <= coluna < 9:
            if tabuleiro_jogador[linha][coluna] == '🌊':
                tabuleiro_jogador[linha][coluna] = '🚢'
                contador += 1
                exibir_tabuleiro(tabuleiro_jogador)
            else:
                print('Posição ocupada. Tente novamente.')
        else:
            print('Fora dos limites.')


def posicao_bot():
    for _ in range(5):
        while True:
            linha = random.randint(0, 8)
            coluna = random.randint(0, 8)

            if tabuleiro_bot[linha][coluna] == '🌊':
                tabuleiro_bot[linha][coluna] = '🚢'
                break


def ataque(estado):
    while True:
        linha = int(input('Digite a linha para atacar (0-8): '))
        coluna = int(input('Digite a coluna para atacar (0-8): '))
        print()

        if 0 <= linha < 9 and 0 <= coluna < 9:
            if tabuleiro_bot[linha][coluna] == '🚢':
                print('Acertou um navio!')
                exibir_computador[linha][coluna] = '🔥'
                estado['restante_bot'] -= 1

            elif tabuleiro_bot[linha][coluna] == '🌊':
                print('Água!')
                exibir_computador[linha][coluna] = '⚫'

            else:
                print('Você já atacou essa posição. Tente novamente.')
                continue

            break
        else:
            print('Posição inválida. Tente novamente.')


def ataque_bot(estado):
    while True:
        linha = random.randint(0, 8)
        coluna = random.randint(0, 8)

        if tabuleiro_jogador[linha][coluna] == '🚢':
            print('O computador acertou um navio!')
            exibir_jogador[linha][coluna] = '🔥'
            estado['restante_jogador'] -= 1
            break

        elif tabuleiro_jogador[linha][coluna] == '🌊':
            print('O computador errou! Água!')
            exibir_jogador[linha][coluna] = '⚫'
            break


def tabuleiro_lado(tab1, tab2, ocultar_tab2=False):
    print("Tabuleiro do Jogador:" + " " * 25 + "Tabuleiro do Bot:")

    cabecalho = "   " + " ".join(f"{i:2}" for i in range(9)) + " " * 6 + " ".join(f"{i:2}" for i in range(9))
    print(cabecalho)

    for i in range(9):
        linha_tab1 = " ".join(tab1[i])

        if ocultar_tab2:
            linha_tab2 = " ".join('🌊' if celula == '🚢' else celula for celula in tab2[i])
        else:
            linha_tab2 = " ".join(tab2[i])

        print(f"{i:2} {linha_tab1}     {i:2} {linha_tab2}")


def verificar_vitoria(estado):
    if estado['restante_bot'] == 0:
        print('Parabéns! Você venceu!')
        print()
        print('Jogo desenvolvido por: Tiago Duarte')
        return True

    elif estado['restante_jogador'] == 0:
        print('O computador venceu! Tente novamente.')
        print()
        print('Jogo desenvolvido por: Tiago Duarte')
        return True
    return False


def main():
    while True:
        menu()


if __name__ == '__main__':
    main()
