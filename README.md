# 🎮 Batalha Naval em Python

Um jogo clássico de Batalha Naval implementado em Python para 2 jogadores humanos.

## 📋 Características

- ✅ Sistema completo de tabuleiro (10x10)
- ✅ 10 navios por jogador (tamanhos variados)
- ✅ Modo 2 Jogadores
- ✅ Interface de linha de comando intuitiva
- ✅ Validação de posicionamento de navios
- ✅ Sistema de ataque e defesa

## 🚀 Como Executar

### Requisitos
- Python 3.6+

### Passos

1. Abra um terminal/PowerShell
2. Navegue até a pasta do jogo:
   ```
   cd "c:\Users\ritta\OneDrive\Área de Trabalho\batalha naval"
   ```
3. Execute o jogo:
   ```
   python batalha_naval.py
   ```

## 📖 Como Jogar

### Fase 1: Configuração dos Navios

Cada jogador posiciona seus navios:

- **Navio 1**: Tamanho 4
- **Navio 2-3**: Tamanho 3 (2 unidades)
- **Navio 4-6**: Tamanho 2 (3 unidades)
- **Navio 7-10**: Tamanho 1 (4 unidades)

**Instruções de Posicionamento:**
1. Escolha uma coluna (0-9)
2. Escolha uma linha (0-9)
3. Escolha a direção:
   - `h` = Horizontal
   - `v` = Vertical

**Regras:**
- Os navios não podem se tocar (nem na diagonal)
- Os navios não podem sair do tabuleiro

### Fase 2: Batalha

1. Jogadores se alternam disparando
2. Cada jogador escolhe coordenadas para atacar
3. Possíveis resultados:
   - 🎯 **ACERTO**: Atingiu um navio
   - 💧 **ÁGUA**: Errou
   - ⚓ **AFUNDADO**: Destruiu completamente um navio

4. O jogo termina quando todos os navios de um jogador são afundados

## 🎯 Símbolos do Tabuleiro

| Símbolo | Significado |
|---------|-----------|
| `~` | Água (célula vazia) |
| `N` | Navio (apenas visível no seu tabuleiro) |
| `X` | Acerto |
| `O` | Erro (água atacada) |

## 📐 Coordenadas

O tabuleiro usa coordenadas:
- **Linha**: 0-9 (vertical)
- **Coluna**: 0-9 (horizontal)

Exemplo:
```
  Coluna: 0  1  2  3  4  5  6  7  8  9
            ~  ~  ~  ~  ~  ~  ~  ~  ~  ~
  Linha 0: ~  ~  ~  ~  ~  ~  ~  ~  ~  ~
  Linha 1: ~  N  N  N  N  ~  ~  ~  ~  ~
  Linha 2: ~  ~  ~  ~  ~  ~  ~  ~  ~  ~
  ...
```

## 💡 Dicas

1. Distribua seus navios estrategicamente
2. Procure atacar de forma sistemática
3. Lembre-se das posições já atacadas
4. Navios maiores são mais fáceis de localizar

## 🔧 Estrutura do Código

```
batalha_naval.py
├── CelulaTipo (Enum)      - Tipos de células do tabuleiro
├── Direcao (Enum)         - Direções de posicionamento
├── Navio (Class)          - Representação de um navio
├── Tabuleiro (Class)      - Gerenciamento do tabuleiro
├── Jogador (Class)        - Dados do jogador
└── BatalhaNaval (Class)   - Lógica principal do jogo
```

## 📝 Exemplo de Execução

```
==================================================
     BEM-VINDO A BATALHA NAVAL!
==================================================

Digite o nome do Jogador 1: Alice
Digite o nome do Jogador 2: Bob

✓ Pressione ENTER para começar a configuração dos navios...
[... fase de configuração ...]

==================================================
           COMEÇANDO O JOGO!
==================================================

==================================================
TURNO DE Alice
==================================================
Alice, informe coluna (0-9): 5
Alice, informe linha (0-9): 3
✓ Pressione ENTER para o próximo turno...
```

## 🎓 Desenvolvimento

O código foi estruturado com:
- Uso de **Enums** para tipos e direções
- **Classes** bem definidas para cada conceito
- **Type hints** para melhor legibilidade
- **Tratamento de erros** para entrada do usuário

## ✨ Possíveis Melhorias Futuras

- [ ] Modo contra IA
- [ ] Diferentes níveis de dificuldade
- [ ] Sistema de pontuação
- [ ] Salvar/carregar jogo
- [ ] Interface gráfica (Tkinter/Pygame)
- [ ] Modo online multiplayer
- [ ] Histórico de ataques

---

**Divirta-se jogando! 🎮**
