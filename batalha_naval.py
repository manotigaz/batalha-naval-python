import os
import random
import time

TABULEIRO_TAMANHO = 9
ARQUIVO_RANKING = 'ranking.txt'

tabuleiro_jogador = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
tabuleiro_bot = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
exibir_computador = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
exibir_jogador = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]

estado = {
    'restante_jogador': 5,
    'restante_bot': 5,
    'pontos_jogador': 0,
}

def limpar_tabuleiros():
    global tabuleiro_jogador, tabuleiro_bot, exibir_computador, exibir_jogador, estado
    tabuleiro_jogador = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
    tabuleiro_bot = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
    exibir_computador = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
    exibir_jogador = [['🌊'] * TABULEIRO_TAMANHO for _ in range(TABULEIRO_TAMANHO)]
    estado = {
        'restante_jogador': 5,
        'restante_bot': 5,
        'pontos_jogador': 0,
    }


def obter_nome():
    while True:
        nome = input('Digite seu nome: ').strip()
        if nome:
            return nome
        print('Nome não pode ficar em branco. Digite novamente.')


def salvar_pontuacao(nome, pontos):
    with open(ARQUIVO_RANKING, 'a', encoding='utf-8') as arquivo:
        arquivo.write(f'{nome};{pontos}\n')


def exibir_ranking():
    print('=====================================================')
    print('Ranking dos Jogadores')
    print('=====================================================')

    if not os.path.exists(ARQUIVO_RANKING):
        print('Nenhuma pontuação registrada ainda.')
        print()
        return

    pontuacoes = []
    with open(ARQUIVO_RANKING, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split(';')
            if len(partes) != 2:
                continue
            nome_arquivo, pontos_texto = partes
            try:
                pontuacoes.append((nome_arquivo, int(pontos_texto)))
            except ValueError:
                continue

    if not pontuacoes:
        print('Nenhuma pontuação válida encontrada.')
        print()
        return

    pontuacoes.sort(key=lambda item: item[1], reverse=True)
    for posicao, (nome_arquivo, pontos) in enumerate(pontuacoes, start=1):
        print(f'{posicao}. {nome_arquivo} - {pontos} pontos')
    print()


print(' ')
print('Jogo Batalha Naval')
print(' ')

nome = obter_nome()

def menu():
    print('=====================================================')
    print(f'Bem Vindo Ao Jogo {nome}')
    print('=====================================================')
    print('1. Começar o jogo')
    print('2. Ver ranking')
    print('3. Regras')
    print('4. Sair')
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
        print(f'Sua pontuação final: {estado["pontos_jogador"]} pontos')
        salvar_pontuacao(nome, estado['pontos_jogador'])
        print('Pontuação salva em', ARQUIVO_RANKING)
        print()

    elif escolha == '2':
        exibir_ranking()

    elif escolha == '3':
        print('Regras do Jogo:')
        print('1. O objetivo do jogo é afundar os navios do oponente.')
        print('2. Cada jogador tem um tabuleiro de 9x9.')
        print('3. Os jogadores se revezam para atacar.')
        print('4. O primeiro a destruir todos os navios vence.')
        print('=====================================================')

    elif escolha == '4':
        print('Saindo do jogo...')
        raise SystemExit

    else:
        print('Opção inválida. Por favor, escolha uma opção válida.')


def exibir_tabuleiro(tabuleiro, ocultar=False):
    print('   ' + ' '.join(f'{i:2}' for i in range(TABULEIRO_TAMANHO)))
    for i, linha in enumerate(tabuleiro):
        if ocultar:
            linha = ['🌊' if celula == '🚢' else celula for celula in linha]
        print(f'{i:2} ' + ' '.join(linha))
    print()


def posicao():
    exibir_tabuleiro(tabuleiro_jogador)
    time.sleep(1.5)

    print('Tabuleiro do Jogador:')
    print('Escolha a posição das suas 5 embarcações')
    time.sleep(1.5)

    contador = 0

    while contador < 5:
        try:
            linha = int(input('Digite a linha (0-8): '))
            coluna = int(input('Digite a coluna (0-8): '))
        except ValueError:
            print('Entrada inválida. Digite números de 0 a 8.')
            continue
        print()

        if 0 <= linha < TABULEIRO_TAMANHO and 0 <= coluna < TABULEIRO_TAMANHO:
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
            linha = random.randint(0, TABULEIRO_TAMANHO - 1)
            coluna = random.randint(0, TABULEIRO_TAMANHO - 1)

            if tabuleiro_bot[linha][coluna] == '🌊':
                tabuleiro_bot[linha][coluna] = '🚢'
                break


def ataque(estado):
    while True:
        try:
            linha = int(input('Digite a linha para atacar (0-8): '))
            coluna = int(input('Digite a coluna para atacar (0-8): '))
        except ValueError:
            print('Entrada inválida. Digite números de 0 a 8.')
            continue
        print()

        if 0 <= linha < TABULEIRO_TAMANHO and 0 <= coluna < TABULEIRO_TAMANHO:
            if tabuleiro_bot[linha][coluna] == '🚢':
                print('Acertou um navio!')
                exibir_computador[linha][coluna] = '🔥'
                tabuleiro_bot[linha][coluna] = '🔥'
                estado['restante_bot'] -= 1
                estado['pontos_jogador'] += 10

            elif tabuleiro_bot[linha][coluna] == '🌊':
                print('Água!')
                exibir_computador[linha][coluna] = '⚫'
                tabuleiro_bot[linha][coluna] = '⚫'
                estado['pontos_jogador'] += 1

            else:
                print('Você já atacou essa posição. Tente novamente.')
                continue

            break
        else:
            print('Posição inválida. Tente novamente.')


def ataque_bot(estado):
    while True:
        linha = random.randint(0, TABULEIRO_TAMANHO - 1)
        coluna = random.randint(0, TABULEIRO_TAMANHO - 1)

        if tabuleiro_jogador[linha][coluna] == '🚢':
            print('O computador acertou um navio!')
            exibir_jogador[linha][coluna] = '🔥'
            tabuleiro_jogador[linha][coluna] = '🔥'
            estado['restante_jogador'] -= 1
            break

        elif tabuleiro_jogador[linha][coluna] == '🌊':
            print('O computador errou! Água!')
            exibir_jogador[linha][coluna] = '⚫'
            tabuleiro_jogador[linha][coluna] = '⚫'
            break


def tabuleiro_lado(tab1, tab2, ocultar_tab2=False):
    print('Tabuleiro do Jogador:' + ' ' * 25 + 'Tabuleiro do Bot:')

    cabecalho = '   ' + ' '.join(f'{i:2}' for i in range(TABULEIRO_TAMANHO)) + ' ' * 6 + ' '.join(f'{i:2}' for i in range(TABULEIRO_TAMANHO))
    print(cabecalho)

    for i in range(TABULEIRO_TAMANHO):
        linha_tab1 = ' '.join(tab1[i])

        if ocultar_tab2:
            linha_tab2 = ' '.join('🌊' if celula == '🚢' else celula for celula in tab2[i])
        else:
            linha_tab2 = ' '.join(tab2[i])

        print(f'{i:2} {linha_tab1}     {i:2} {linha_tab2}')


def verificar_vitoria(estado):
    if estado['restante_bot'] == 0:
        estado['pontos_jogador'] += 50
        print('Parabéns! Você venceu!')
        print('Bônus de vitória: +50 pontos')
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
        try:
            menu()
        except SystemExit:
            break


if __name__ == '__main__':
    main()
