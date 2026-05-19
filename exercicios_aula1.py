# ==========================================================
# Teoria da Computação — Exercícios Práticos em Python
# Sprint Planning e Otimização Computacional
# ==========================================================

from typing import List, Dict, Tuple
from itertools import product
import random
import time


# ==========================================================
# DADOS DO PROBLEMA
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

def avaliar_solucao(individuo: List[int]) -> Tuple[int, int]:
    custo_total = 0
    valor_total = 0

    for i in range(len(individuo)):
        if individuo[i] == 1:
            custo_total += TAREFAS[i]["custo"]
            valor_total += TAREFAS[i]["valor"]

    if custo_total > CAPACIDADE:
        return 0, custo_total

    return valor_total, custo_total


def imprimir(individuo: List[int]):
    print("\nTarefas selecionadas:")

    custo_total = 0
    valor_total = 0

    for i in range(len(individuo)):
        if individuo[i] == 1:
            t = TAREFAS[i]
            print(f"- {t['nome']} (custo={t['custo']}, valor={t['valor']})")
            custo_total += t["custo"]
            valor_total += t["valor"]

    print(f"\nCusto total: {custo_total}")
    print(f"Valor total: {valor_total}")


# ==========================================================
# EXERCÍCIO 1 — BRUTE FORCE
# ==========================================================

def brute_force():
    n = len(TAREFAS)

    melhor = [0] * n
    melhor_valor = 0

    for combo in product([0, 1], repeat=n):
        valor, custo = avaliar_solucao(combo)

        if custo <= CAPACIDADE and valor > melhor_valor:
            melhor_valor = valor
            melhor = combo

    return melhor, melhor_valor


# ==========================================================
# EXERCÍCIO 2 — GREEDY
# ==========================================================

def greedy():
    n = len(TAREFAS)

    indices = sorted(
        range(n),
        key=lambda i: TAREFAS[i]["valor"] / TAREFAS[i]["custo"],
        reverse=True
    )

    solucao = [0] * n
    capacidade_restante = CAPACIDADE

    for i in indices:
        if TAREFAS[i]["custo"] <= capacidade_restante:
            solucao[i] = 1
            capacidade_restante -= TAREFAS[i]["custo"]

    return solucao


# ==========================================================
# EXERCÍCIO 3 — COMPLEXIDADE
# ==========================================================

def medir():
    tamanhos = [5, 8, 10, 12, 14]

    for n in tamanhos:
        tarefas = TAREFAS[:n]

        inicio = time.perf_counter()

        for _ in range(1):
            list(product([0, 1], repeat=n))

        fim = time.perf_counter()

        print(f"n={n} tempo={fim - inicio:.5f}s")


# ==========================================================
# EXERCÍCIO 4 — HILL CLIMBING
# ==========================================================

def vizinhos(sol):
    res = []

    for i in range(len(sol)):
        novo = list(sol)
        novo[i] = 1 - novo[i]
        res.append(novo)

    return res


def hill_climb():
    atual = greedy()
    atual_valor, _ = avaliar_solucao(atual)

    while True:
        melhor_vizinho = atual
        melhor_valor = atual_valor

        for v in vizinhos(atual):
            valor, _ = avaliar_solucao(v)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_vizinho = v

        if melhor_valor <= atual_valor:
            break

        atual = melhor_vizinho
        atual_valor = melhor_valor

    return atual


# ==========================================================
# EXECUÇÃO PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    print("\n=== EXERCÍCIO 1 — BRUTE FORCE ===")
    sol, val = brute_force()
    imprimir(sol)
    print("Valor:", val)

    print("\n=== EXERCÍCIO 2 — GREEDY ===")
    sol = greedy()
    imprimir(sol)

    print("\n=== EXERCÍCIO 3 — COMPLEXIDADE ===")
    medir()

    print("\n=== EXERCÍCIO 4 — HILL CLIMBING ===")
    sol = hill_climb()
    imprimir(sol)