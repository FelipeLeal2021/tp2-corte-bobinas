import random
import copy

bobinas = [1200] * 5
larguras_tiras = {'A': 400, 'B': 350, 'C': 300}

# Entrada da demanda
print("Informe a demanda mínima de tiras para cada tipo:")
demanda_A = int(input("Quantidade de tiras do tipo A (400 mm): "))
demanda_B = int(input("Quantidade de tiras do tipo B (350 mm): "))
demanda_C = int(input("Quantidade de tiras do tipo C (300 mm): "))
demandas = {'A': demanda_A, 'B': demanda_B, 'C': demanda_C}

# Padrões fixos
padroes_corte = [
    {'A': 2, 'C': 1},
    {'B': 3},
    {'A': 1, 'B': 1, 'C': 1}
]

# Avalia solução e para se atender demanda
def avaliar_solucao_com_parada(solucao, bobinas, larguras_tiras, demandas):
    perda_total = 0
    producao = {'A': 0, 'B': 0, 'C': 0}
    solucao_final = []

    for i, padrao in enumerate(solucao):
        if all(producao[tipo] >= demandas[tipo] for tipo in demandas):
            solucao_final += [{}] * (len(bobinas) - len(solucao_final))
            break
        solucao_final.append(padrao)
        largura_usada = sum(qtd * larguras_tiras[tipo] for tipo, qtd in padrao.items())
        sobra = bobinas[i] - largura_usada if padrao else 0
        perda_total += sobra
        for tipo, qtd in padrao.items():
            producao[tipo] += qtd

    return perda_total, producao, solucao_final

# Gerar solução aleatória
def gerar_solucao_inicial(bobinas, padroes):
    return [random.choice(padroes) for _ in bobinas]

# Gerar vizinhos
def gerar_vizinhos(solucao, padroes):
    vizinhos = []
    for i in range(len(solucao)):
        for padrao in padroes:
            if solucao[i] != padrao:
                vizinho = copy.deepcopy(solucao)
                vizinho[i] = padrao
                vizinhos.append(vizinho)
    return vizinhos

# Verifica se produção atende demanda
def atende_demanda(producao, demandas):
    return all(producao[tipo] >= demandas[tipo] for tipo in demandas)

# Busca Local com parada por demanda atendida
def busca_local(bobinas, padroes, larguras_tiras, demandas, tentativas=30):
    melhor_solucao = None
    menor_perda = float('inf')
    melhor_producao = None

    for _ in range(tentativas):
        solucao_ini = gerar_solucao_inicial(bobinas, padroes)
        perda_atual, producao_atual, solucao_atual = avaliar_solucao_com_parada(solucao_ini, bobinas, larguras_tiras, demandas)

        while True:
            vizinhos = gerar_vizinhos(solucao_atual, padroes)
            melhor_vizinho = None
            melhor_perda_local = perda_atual

            for vizinho in vizinhos:
                perda_vizinho, producao_vizinho, solucao_ajustada = avaliar_solucao_com_parada(vizinho, bobinas, larguras_tiras, demandas)
                if atende_demanda(producao_vizinho, demandas) and perda_vizinho < melhor_perda_local:
                    melhor_perda_local = perda_vizinho
                    melhor_vizinho = solucao_ajustada
                    producao_temp = producao_vizinho

            if melhor_vizinho:
                solucao_atual = melhor_vizinho
                perda_atual = melhor_perda_local
                producao_atual = producao_temp
            else:
                break

        if atende_demanda(producao_atual, demandas) and perda_atual < menor_perda:
            melhor_solucao = solucao_atual
            menor_perda = perda_atual
            melhor_producao = producao_atual

    return melhor_solucao, menor_perda, melhor_producao

# Exibir tabela
def exibir_tabela(solucao):
    print("\nTabela de Cortes (por bobina):")
    print(f"{'Bobina':<8} {'Corte A':<8} {'Corte B':<8} {'Corte C':<8}")
    for i, padrao in enumerate(solucao):
        a = padrao.get('A', 0)
        b = padrao.get('B', 0)
        c = padrao.get('C', 0)
        print(f"{i+1:<8} {a:<8} {b:<8} {c:<8}")

# Execução
solucao_final, perda_total, producao_final = busca_local(bobinas, padroes_corte, larguras_tiras, demandas)

if solucao_final:
    exibir_tabela(solucao_final)
    print("Perda Total:", perda_total, "mm")
    print("\nProdução Final:")
    for tipo in producao_final:
        print(f"Tiras tipo {tipo}: {producao_final[tipo]} (Demanda: {demandas[tipo]})")
    bobinas_usadas = sum(1 for padrao in solucao_final if padrao != {})
    print(f"Bobinas usadas: {bobinas_usadas}")
    print(f"Bobinas não usadas: {5 - bobinas_usadas}")
else:
    print("\nNão foi possível atender à demanda com 5 bobinas.")
