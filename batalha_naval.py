"""
BATALHA NAVAL - Usando Matrizes (listas 10x10)

MATRIZ DO JOGO:
  '.' = agua
  'N' = navio (oculto ao jogador)
  'X' = acerto
  'O' = erro (agua)

NAVIOS:
  Porta-avioes (5), Cruzador (4), Destroyer (3), Submarino (2)

PONTUACAO:
  Acerto:  +100 pontos
  Erro:    -10 pontos
  Vitoria: +500 bonus
"""

import random
import os

TAMANHO = 10
ARQUIVO_RANKING = "ranking.txt"

NAVIOS = [
    ("Porta-avioes", 5),
    ("Cruzador",     4),
    ("Destroyer",    3),
    ("Submarino",    2),
]


# ── Matrizes ──────────────────────────────────────

def criar_tabuleiro():
    return [['.' ] * TAMANHO for _ in range(TAMANHO)]


def posicionar_navios(tabuleiro):
    navios_info = []
    for nome, tamanho in NAVIOS:
        posicionado = False
        while not posicionado:
            direcao = random.choice(['H', 'V'])
            if direcao == 'H':
                r = random.randint(0, TAMANHO - 1)
                c = random.randint(0, TAMANHO - tamanho)
                celulas = [(r, c + i) for i in range(tamanho)]
            else:
                r = random.randint(0, TAMANHO - tamanho)
                c = random.randint(0, TAMANHO - 1)
                celulas = [(r + i, c) for i in range(tamanho)]

            if all(tabuleiro[r][c] == '.' for r, c in celulas):
                for r, c in celulas:
                    tabuleiro[r][c] = 'N'
                navios_info.append({"nome": nome, "celulas": set(celulas), "hits": set()})
                posicionado = True
    return navios_info


# ── Exibicao ─────────────────────────────────────

def exibir_tabuleiro(tabuleiro, revelar=False):
    print("   " + "  ".join(str(i + 1).rjust(2) for i in range(TAMANHO)))
    for i, linha in enumerate(tabuleiro):
        letra = chr(ord('A') + i)
        celulas = []
        for c in linha:
            if c == 'X':
                celulas.append(' X')
            elif c == 'O':
                celulas.append(' o')
            elif c == 'N' and revelar:
                celulas.append(' #')
            else:
                celulas.append(' .')
        print(f"{letra}  {'  '.join(celulas)}")


# ── Ataque ────────────────────────────────────────

def atacar(tabuleiro, navios_info, linha, col):
    celula = tabuleiro[linha][col]
    if celula in ('X', 'O'):
        return 'ja_atacado', None
    if celula == 'N':
        tabuleiro[linha][col] = 'X'
        for navio in navios_info:
            if (linha, col) in navio["celulas"]:
                navio["hits"].add((linha, col))
                if navio["hits"] == navio["celulas"]:
                    return 'afundou', navio["nome"]
        return 'acerto', None
    tabuleiro[linha][col] = 'O'
    return 'erro', None


def todos_afundados(navios_info):
    return all(n["hits"] == n["celulas"] for n in navios_info)


def parse_posicao(entrada):
    entrada = entrada.strip().upper()
    if len(entrada) < 2:
        return None
    letra = entrada[0]
    if letra not in "ABCDEFGHIJ":
        return None
    try:
        col = int(entrada[1:]) - 1
    except ValueError:
        return None
    if not (0 <= col < TAMANHO):
        return None
    return ord(letra) - ord('A'), col


# ── Ranking ───────────────────────────────────────

def salvar_pontuacao(nome, pontuacao, venceu):
    resultado = "VITORIA" if venceu else "DERROTA"
    with open(ARQUIVO_RANKING, "a", encoding="utf-8") as f:
        f.write(f"{pontuacao} | {resultado} | {nome}\n")


def exibir_ranking():
    print("\n=== RANKING ===")
    if not os.path.exists(ARQUIVO_RANKING):
        print("Nenhuma partida registrada.")
        return
    entradas = []
    with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
        for linha in f:
            partes = [p.strip() for p in linha.strip().split("|")]
            if len(partes) == 3:
                try:
                    entradas.append((int(partes[0]), partes[1], partes[2]))
                except ValueError:
                    pass
    entradas.sort(reverse=True)
    for pos, (pts, res, nome) in enumerate(entradas[:10], 1):
        print(f"  {pos}. {nome:<20} {pts:>6} pts  ({res})")
    print()


# ── Jogo ──────────────────────────────────────────

def jogar(nome):
    tabuleiro = criar_tabuleiro()
    navios    = posicionar_navios(tabuleiro)
    pontuacao = 0
    turno     = 1

    print("\nNavios posicionados! Boa sorte!\n")

    while True:
        print(f"\n--- Turno {turno} | Pontuacao: {pontuacao} ---")
        exibir_tabuleiro(tabuleiro, revelar=False)

        entrada = input("Ataque (ex: B5): ").strip()
        pos = parse_posicao(entrada)
        if pos is None:
            print("Posicao invalida. Use letra A-J + numero 1-10.")
            continue

        linha, col = pos
        resultado, afundou = atacar(tabuleiro, navios, linha, col)

        if resultado == 'ja_atacado':
            print("Voce ja atacou essa posicao!")
            continue
        elif resultado == 'acerto':
            pontuacao += 100
            print(f"ACERTO! +100 pontos. Total: {pontuacao}")
        elif resultado == 'afundou':
            pontuacao += 300
            print(f"AFUNDOU o {afundou}! +300 pontos. Total: {pontuacao}")
        elif resultado == 'erro':
            pontuacao -= 10
            print(f"Agua... -10 pontos. Total: {pontuacao}")

        if todos_afundados(navios):
            pontuacao += 500
            print(f"\nPARABENS {nome}! Voce destruiu toda a frota!")
            print(f"Pontuacao final: {pontuacao}")
            exibir_tabuleiro(tabuleiro, revelar=True)
            salvar_pontuacao(nome, pontuacao, venceu=True)
            return

        turno += 1


# ── Menu principal ────────────────────────────────

def main():
    print("=== BATALHA NAVAL ===")
    nome = input("Digite seu nome: ").strip() or "Anonimo"

    while True:
        print("\n[1] Jogar")
        print("[2] Ver Ranking")
        print("[0] Sair")
        escolha = input("Escolha: ").strip()

        if escolha == '1':
            jogar(nome)
        elif escolha == '2':
            exibir_ranking()
        elif escolha == '0':
            print("Ate logo!")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
