"""
Jogo de Batalha Naval em Python
Modo: 2 Jogadores Human vs Human
"""

import random
from typing import List, Tuple
from enum import Enum


class CelulaTipo(Enum):
    AGUA = '~'
    NAVIO = 'N'
    ACERTO = 'X'
    ERRO = 'O'


class Direcao(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Tabuleiro:
    """Classe para gerenciar o tabuleiro do jogo"""
    
    def __init__(self, tamanho: int = 10):
        self.tamanho = tamanho
        self.grid = [[CelulaTipo.AGUA for _ in range(tamanho)] for _ in range(tamanho)]
        self.navios = []
        
    def pode_colocar_navio(self, linha: int, coluna: int, tamanho: int, direcao: Direcao) -> bool:
        """Verifica se é possível colocar um navio"""
        if direcao == Direcao.HORIZONTAL:
            if coluna + tamanho > self.tamanho:
                return False
            for c in range(coluna, coluna + tamanho):
                if self.grid[linha][c] != CelulaTipo.AGUA:
                    return False
                # Verifica células adjacentes
                for adj_l in range(max(0, linha - 1), min(self.tamanho, linha + 2)):
                    for adj_c in range(max(0, c - 1), min(self.tamanho, c + 2)):
                        if (adj_l, adj_c) != (linha, c) and self.grid[adj_l][adj_c] == CelulaTipo.NAVIO:
                            return False
        else:  # VERTICAL
            if linha + tamanho > self.tamanho:
                return False
            for l in range(linha, linha + tamanho):
                if self.grid[l][coluna] != CelulaTipo.AGUA:
                    return False
                # Verifica células adjacentes
                for adj_l in range(max(0, l - 1), min(self.tamanho, l + 2)):
                    for adj_c in range(max(0, coluna - 1), min(self.tamanho, coluna + 2)):
                        if (adj_l, adj_c) != (l, coluna) and self.grid[adj_l][adj_c] == CelulaTipo.NAVIO:
                            return False
        return True
    
    def colocar_navio(self, linha: int, coluna: int, tamanho: int, direcao: Direcao) -> bool:
        """Coloca um navio no tabuleiro"""
        if not self.pode_colocar_navio(linha, coluna, tamanho, direcao):
            return False
        
        posicoes = []
        if direcao == Direcao.HORIZONTAL:
            for c in range(coluna, coluna + tamanho):
                self.grid[linha][c] = CelulaTipo.NAVIO
                posicoes.append((linha, c))
        else:  # VERTICAL
            for l in range(linha, linha + tamanho):
                self.grid[l][coluna] = CelulaTipo.NAVIO
                posicoes.append((l, coluna))
        
        self.navios.append(Navio(tamanho, posicoes))
        return True
    
    def receber_ataque(self, linha: int, coluna: int) -> str:
        """Recebe um ataque e retorna o resultado"""
        if linha < 0 or linha >= self.tamanho or coluna < 0 or coluna >= self.tamanho:
            return "FORA"
        
        celula = self.grid[linha][coluna]
        
        if celula == CelulaTipo.ACERTO or celula == CelulaTipo.ERRO:
            return "JA_ATACADO"
        
        if celula == CelulaTipo.NAVIO:
            self.grid[linha][coluna] = CelulaTipo.ACERTO
            # Marca o navio como atingido
            for navio in self.navios:
                if (linha, coluna) in navio.posicoes:
                    navio.acertos += 1
                    if navio.acertos == navio.tamanho:
                        return "AFUNDADO"
            return "ACERTO"
        else:
            self.grid[linha][coluna] = CelulaTipo.ERRO
            return "ERRO"
    
    def exibir(self, revelar_navios: bool = False) -> None:
        """Exibe o tabuleiro"""
        print("\n  ", end="")
        for i in range(self.tamanho):
            print(f"{i:2}", end=" ")
        print()
        
        for i, linha in enumerate(self.grid):
            print(f"{i:2}", end=" ")
            for j, celula in enumerate(linha):
                if revelar_navios and celula == CelulaTipo.NAVIO:
                    print(f"{celula.value:2}", end=" ")
                elif celula in [CelulaTipo.ACERTO, CelulaTipo.ERRO]:
                    print(f"{celula.value:2}", end=" ")
                else:
                    print(f"{celula.value:2}", end=" ")
            print()
    
    def exibir_publico(self) -> None:
        """Exibe o tabuleiro sem revelar a posição dos navios"""
        print("\n  ", end="")
        for i in range(self.tamanho):
            print(f"{i:2}", end=" ")
        print()
        
        for i, linha in enumerate(self.grid):
            print(f"{i:2}", end=" ")
            for celula in linha:
                if celula in [CelulaTipo.ACERTO, CelulaTipo.ERRO]:
                    print(f"{celula.value:2}", end=" ")
                else:
                    print(" ~ ", end=" ")
            print()
    
    def todos_navios_afundados(self) -> bool:
        """Verifica se todos os navios foram afundados"""
        return all(navio.acertos == navio.tamanho for navio in self.navios)


class Navio:
    """Classe para representar um navio"""
    
    def __init__(self, tamanho: int, posicoes: List[Tuple[int, int]]):
        self.tamanho = tamanho
        self.posicoes = posicoes
        self.acertos = 0


class Jogador:
    """Classe para representar um jogador"""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.tabuleiro_proprio = Tabuleiro()
        self.tabuleiro_inimigo = Tabuleiro()
        self.tabuleiro_inimigo.grid = [[CelulaTipo.AGUA for _ in range(10)] for _ in range(10)]
    
    def configurar_navios(self) -> None:
        """Permite que o jogador configure seus navios"""
        tamanhos_navios = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        
        print(f"\n{'='*40}")
        print(f"Configuração de Navios - {self.nome}")
        print(f"{'='*40}")
        
        for i, tamanho in enumerate(tamanhos_navios, 1):
            navios_colocados = False
            while not navios_colocados:
                self.tabuleiro_proprio.exibir(revelar_navios=True)
                print(f"\nNavio {i}/{len(tamanhos_navios)} - Tamanho: {tamanho}")
                
                try:
                    coluna = int(input("Coluna (0-9): "))
                    linha = int(input("Linha (0-9): "))
                    direcao_input = input("Direção (h=horizontal, v=vertical): ").lower()
                    
                    direcao = Direcao.HORIZONTAL if direcao_input == 'h' else Direcao.VERTICAL
                    
                    if self.tabuleiro_proprio.colocar_navio(linha, coluna, tamanho, direcao):
                        navios_colocados = True
                    else:
                        print("❌ Posição inválida! Tente novamente.")
                except (ValueError, IndexError):
                    print("❌ Entrada inválida! Use números entre 0-9.")
        
        print(f"\n✓ Navios configurados com sucesso para {self.nome}!")
    
    def fazer_ataque(self, tabuleiro_inimigo: Tabuleiro) -> str:
        """Faz um ataque no tabuleiro do inimigo"""
        ataque_valido = False
        while not ataque_valido:
            try:
                coluna = int(input(f"\n{self.nome}, informe coluna (0-9): "))
                linha = int(input(f"{self.nome}, informe linha (0-9): "))
                resultado = tabuleiro_inimigo.receber_ataque(linha, coluna)
                
                if resultado == "FORA":
                    print("❌ Coordenadas fora do tabuleiro!")
                    continue
                elif resultado == "JA_ATACADO":
                    print("❌ Já foi disparado nesse local!")
                    continue
                else:
                    ataque_valido = True
                    return resultado, linha, coluna
            except ValueError:
                print("❌ Entrada inválida! Use números entre 0-9.")
    
    def exibir_status_ataque(self, resultado: str, linha: int, coluna: int) -> None:
        """Exibe o resultado do ataque"""
        if resultado == "ACERTO":
            print(f"🎯 ACERTO em ({linha}, {coluna})!")
        elif resultado == "ERRO":
            print(f"💧 Água em ({linha}, {coluna})")
        elif resultado == "AFUNDADO":
            print(f"⚓ NAVIO AFUNDADO em ({linha}, {coluna})!")


class BatalhaNaval:
    """Classe principal do jogo"""
    
    def __init__(self):
        self.jogador1 = None
        self.jogador2 = None
        self.rodada = 0
    
    def inicializar_jogo(self) -> None:
        """Inicializa o jogo"""
        print("\n" + "="*50)
        print("     BEM-VINDO A BATALHA NAVAL!")
        print("="*50)
        
        nome1 = input("\nDigite o nome do Jogador 1: ").strip()
        nome2 = input("Digite o nome do Jogador 2: ").strip()
        
        self.jogador1 = Jogador(nome1)
        self.jogador2 = Jogador(nome2)
    
    def configurar_jogo(self) -> None:
        """Configura os navios dos jogadores"""
        input("\n✓ Pressione ENTER para começar a configuração dos navios...")
        self.jogador1.configurar_navios()
        
        input("\n✓ Pressione ENTER para o próximo jogador...")
        self.jogador2.configurar_navios()
    
    def exibir_turno(self, jogador_atacante: Jogador, jogador_defensor: Jogador) -> None:
        """Exibe a situação do turno"""
        print("\n" + "="*50)
        print(f"TURNO DE {jogador_atacante.nome}")
        print("="*50)
        print(f"\nTabuleiro do {jogador_defensor.nome} (linha de fogo):")
        jogador_defensor.tabuleiro_proprio.exibir_publico()
        print(f"\nSeu tabuleiro ({jogador_atacante.nome}):")
        jogador_atacante.tabuleiro_proprio.exibir()
    
    def jogar(self) -> None:
        """Executa o loop principal do jogo"""
        self.inicializar_jogo()
        self.configurar_jogo()
        
        print("\n" + "="*50)
        print("           COMEÇANDO O JOGO!")
        print("="*50)
        
        while True:
            # Turno do Jogador 1
            self.exibir_turno(self.jogador1, self.jogador2)
            resultado, linha, coluna = self.jogador1.fazer_ataque(self.jogador2.tabuleiro_proprio)
            self.jogador1.exibir_status_ataque(resultado, linha, coluna)
            
            if self.jogador2.tabuleiro_proprio.todos_navios_afundados():
                print(f"\n{'='*50}")
                print(f"🏆 {self.jogador1.nome} VENCEU! 🏆")
                print(f"{'='*50}")
                break
            
            input("\nPressione ENTER para o próximo turno...")
            
            # Turno do Jogador 2
            self.exibir_turno(self.jogador2, self.jogador1)
            resultado, linha, coluna = self.jogador2.fazer_ataque(self.jogador1.tabuleiro_proprio)
            self.jogador2.exibir_status_ataque(resultado, linha, coluna)
            
            if self.jogador1.tabuleiro_proprio.todos_navios_afundados():
                print(f"\n{'='*50}")
                print(f"🏆 {self.jogador2.nome} VENCEU! 🏆")
                print(f"{'='*50}")
                break
            
            input("\nPressione ENTER para o próximo turno...")


def main():
    """Função principal"""
    jogo = BatalhaNaval()
    jogo.jogar()
    
    print("\nObrigado por jogar Batalha Naval!")


if __name__ == "__main__":
    main()
