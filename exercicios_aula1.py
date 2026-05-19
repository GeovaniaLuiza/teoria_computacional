from typing import List, Dict, Tuple, Optional
from itertools import product
import random
import time


# ==========================================================
# DADOS
# ==========================================================

TAREFAS = [
    {"nome": "Auth OAuth2", "custo": 8, "valor": 40},
    {"nome": "Dashboard métricas", "custo": 13, "valor": 55},
    {"nome": "Exportar CSV", "custo": 5, "valor": 20},
    {"nome": "Refactor serviço X", "custo": 20, "valor": 35},
    {"nome": "API notificações", "custo": 10, "valor": 60},
    {"nome": "Upgrade deps", "custo": 3, "valor": 15},
    {"nome": "Testes E2E checkout", "custo": 8, "valor": 50},
    {"nome": "Rate limiting", "custo": 6, "valor": 45},
    {"nome": "Docs OpenAPI", "custo": 4, "valor": 25},
    {"nome": "Cache Redis", "custo": 12, "valor": 70},
]

CAPACIDADE = 40


# ==========================================================
# FUNÇÃO AUXILIAR
# ==========================================================

def avaliar(ind: List[int]) -> Tuple[int, int]:
    custo = 0
    valor = 0

    for i in range(len(ind)):
        if ind[i] == 1:
            custo += TAREFAS[i]["custo"]
            valor += TAREFAS[i]["valor"]

    if custo > CAPACIDADE:
        return 0, custo

    return valor, custo


def imprimir(ind: List[int]):
    print("\nTarefas selecionadas:")
    custo = 0
    valor = 0

    for i in range(len(ind)):
        if ind[i] == 1:
            t = TAREFAS[i]
            print(f"- {t['nome']} (custo={t['custo']}, valor={t['valor']})")
            custo += t["custo"]
            valor += t["valor"]

    print(f"\nCusto total: {custo}")
    print(f"Valor total: {valor}")


# ==========================================================
# EXERCÍCIO 1 — BRUTE FORCE
# ==========================================================

def busca_exaustiva(tarefas: List[Dict], capacidade: int) -> Tuple[List[int], int]:

    n = len(tarefas)
    melhor = None
    melhor_valor = 0

    for combo in product([0, 1], repeat=n):
        custo = 0
        valor = 0

        for i in range(n):
            if combo[i] == 1:
                custo += tarefas[i]["custo"]
                valor += tarefas[i]["valor"]

        if custo <= capacidade and valor > melhor_valor:
            melhor_valor = valor
            melhor = combo

    return list(melhor), melhor_valor


# ==========================================================
# EXERCÍCIO 2 — GREEDY
# ==========================================================

def greedy(tarefas: List[Dict], capacidade: int) -> List[int]:

    n = len(tarefas)

    indices = sorted(
        range(n),
        key=lambda i: tarefas[i]["valor"] / tarefas[i]["custo"],
        reverse=True
    )

    sol = [0] * n
    cap = capacidade

    for i in indices:
        if tarefas[i]["custo"] <= cap:
            sol[i] = 1
            cap -= tarefas[i]["custo"]

    return sol


# ==========================================================
# EXERCÍCIO 3 — COMPLEXIDADE
# ==========================================================

def medir_complexidade():

    tamanhos = [5, 8, 10, 12, 14, 16]
    resultados = {}

    for n in tamanhos:
        tempos = []

        for _ in range(3):
            tarefas = [
                {"custo": random.randint(1, 10), "valor": random.randint(5, 50)}
                for _ in range(n)
            ]

            t0 = time.perf_counter()
            busca_exaustiva(tarefas, 30)
            t1 = time.perf_counter()

            tempos.append((t1 - t0) * 1000)

        resultados[n] = sum(tempos) / len(tempos)

    return resultados


def tabela_complexidade(tempos: Dict[int, float]):

    print("\n=== COMPLEXIDADE ===\n")

    prev = None

    print("n | tempo(ms) | razão | 2^n")

    for n in sorted(tempos.keys()):
        t = tempos[n]
        razao = "-" if prev is None else f"{t/prev:.2f}"

        print(f"{n} | {t:.2f} | {razao} | {2**n}")

        prev = t


# ==========================================================
# EXERCÍCIO 4 — HILL CLIMBING
# ==========================================================

def vizinhos(ind):

    res = []

    for i in range(len(ind)):
        v = ind[:]
        v[i] = 1 - v[i]
        res.append(v)

    return res


def hill_climbing(tarefas: List[Dict], capacidade: int):

    atual = greedy(tarefas, capacidade)
    atual_val, _ = avaliar(atual)

    for _ in range(1000):

        melhor = atual
        melhor_val = atual_val

        for v in vizinhos(atual):
            val, _ = avaliar(v)
            if val > melhor_val:
                melhor = v
                melhor_val = val

        if melhor_val <= atual_val:
            break

        atual = melhor
        atual_val = melhor_val

    return atual, atual_val


# ==========================================================
# DEBRIEF
# ==========================================================

def comparar():

    print("\n================ DEBRIEF ================")

    t0 = time.perf_counter()
    bf, bf_val = busca_exaustiva(TAREFAS, CAPACIDADE)
    bf_t = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    gr = greedy(TAREFAS, CAPACIDADE)
    gr_val, _ = avaliar(gr)
    gr_t = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    hc, hc_val = hill_climbing(TAREFAS, CAPACIDADE)
    hc_t = (time.perf_counter() - t0) * 1000

    print(f"\nBrute Force → {bf_val} | {bf_t:.2f} ms")
    print(f"Greedy      → {gr_val} | {gr_t:.2f} ms")
    print(f"Hill Climb  → {hc_val} | {hc_t:.2f} ms")

    print("""
Brute Force  | O(2^n)      | ótimo ✔ | não escala ❌
Greedy       | O(n log n)  | não ❌  | escala ✔
Hill Climb   | O(n²)       | não ❌  | local ⚠
""")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("\n=== BRUTE FORCE ===")
    sol, val = busca_exaustiva(TAREFAS, CAPACIDADE)
    imprimir(sol)

    print("\n=== GREEDY ===")
    sol = greedy(TAREFAS, CAPACIDADE)
    imprimir(sol)

    print("\n=== COMPLEXIDADE ===")
    tempos = medir_complexidade()
    tabela_complexidade(tempos)

    print("\n=== HILL CLIMBING ===")
    sol, val = hill_climbing(TAREFAS, CAPACIDADE)
    imprimir(sol)

    comparar()