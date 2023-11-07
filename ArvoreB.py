class NoArvoreB:
    def __init__(self, eh_folha=True):
        self.eh_folha = eh_folha
        self.chaves = []
        self.filhos = []


class ArvoreB:
    def __init__(self, t):
        self.raiz = NoArvoreB(eh_folha=True)
        self.t = t

    def inserir(self, chave):
        raiz = self.raiz
        if len(raiz.chaves) == (2 * self.t - 1):
            novo_no = NoArvoreB(eh_folha=False)
            novo_no.filhos.append(raiz)
            self.dividir_filho(novo_no, 0)
            self.raiz = novo_no
        self.inserir_nao_cheio(self.raiz, chave)

    def inserir_nao_cheio(self, x, chave):
        i = len(x.chaves) - 1
        if x.eh_folha:
            while i >= 0 and chave < x.chaves[i]:
                i -= 1
            x.chaves.insert(i + 1, chave)
        else:
            while i >= 0 and chave < x.chaves[i]:
                i -= 1
            i += 1
            if len(x.filhos[i].chaves) == (2 * self.t - 1):
                self.dividir_filho(x, i)
                if chave > x.chaves[i]:
                    i += 1
            self.inserir_nao_cheio(x.filhos[i], chave)

    def dividir_filho(self, x, i):
        t = self.t
        y = x.filhos[i]
        z = NoArvoreB(eh_folha=y.eh_folha)
        x.filhos.insert(i + 1, z)
        x.chaves.insert(i, y.chaves[t - 1])
        z.chaves = y.chaves[t:]
        y.chaves = y.chaves[:t - 1]
        if not y.eh_folha:
            z.filhos = y.filhos[t:]
            y.filhos = y.filhos[:t]

    def buscar(self, chave, x=None, nivel=0):
        if x is None:
            x = self.raiz
        i = 0
        print(
            f"Nível {nivel}: Procurando por chave {chave} em {', '.join(map(str, x.chaves))}")

        while i < len(x.chaves) and chave > x.chaves[i]:
            i += 1

        if i < len(x.chaves) and chave == x.chaves[i]:
            print(
                f"Nível {nivel}: Chave {chave} encontrada em {', '.join(map(str, x.chaves))}")
            return True
        elif x.eh_folha:
            print(
                f"Nível {nivel}: Chave {chave} não encontrada em {', '.join(map(str, x.chaves))}")
            return False
        else:
            print(
                f"Nível {nivel}: Descendo para filho {i} de {', '.join(map(str, x.chaves))}")
            return self.buscar(chave, x.filhos[i], nivel + 1)

    def remover(self, chave):
        if not self.raiz.chaves:
            return print ("Árvore vazia")
        self.raiz = self.remover_recursivo(self.raiz, chave)
        if not self.raiz.chaves:
            if self.raiz.filhos:
                self.raiz = self.raiz.filhos[0]

    def remover_recursivo(self, no, chave):
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        if i < len(no.chaves) and chave == no.chaves[i]:
            if no.eh_folha:
                no.chaves.pop(i)
            else:
                if len(no.filhos[i].chaves) >= self.t:
                    predecessor = self.obter_predecessor(no, i)
                    no.chaves[i] = predecessor
                    no.filhos[i] = self.remover_recursivo(
                        no.filhos[i], predecessor)
                else:
                    if len(no.filhos[i + 1].chaves) >= self.t:
                        sucessor = self.obter_sucessor(no, i)
                        no.chaves[i] = sucessor
                        no.filhos[i +
                                  1] = self.remover_recursivo(no.filhos[i + 1], sucessor)
                    else:
                        self.juntar_filhos(no, i)
                        no.filhos[i] = self.remover_recursivo(
                            no.filhos[i], chave)
        else:
            if no.eh_folha:
                return no
            if len(no.filhos[i].chaves) < self.t:
                if i > 0 and len(no.filhos[i - 1].chaves) >= self.t:
                    no.filhos[i] = self.pegar_do_irmao_esquerdo(no, i)
                elif i < len(no.filhos) - 1 and len(no.filhos[i + 1].chaves) >= self.t:
                    no.filhos[i] = self.pegar_do_irmao_direito(no, i)
                else:
                    self.juntar_filhos(no, i)
                    if len(no.chaves) == 0:
                        return no.filhos[0]
                return self.remover_recursivo(no.filhos[i], chave)
            else:
                no.filhos[i] = self.remover_recursivo(no.filhos[i], chave)
        return no

    def obter_predecessor(self, no, idx):
        atual = no.filhos[idx]
        while not atual.eh_folha:
            atual = atual.filhos[-1]
        return atual.chaves[-1]

    def obter_sucessor(self, no, idx):
        atual = no.filhos[idx + 1]
        while not atual.eh_folha:
            atual = atual.filhos[0]
        return atual.chaves[0]

    def pegar_do_irmao_esquerdo(self, no, idx):
        filho = no.filhos[idx]
        irmao_esquerdo = no.filhos[idx - 1]

        filho.chaves.insert(0, no.chaves[idx - 1])
        no.chaves[idx - 1] = irmao_esquerdo.chaves.pop()
        if not irmao_esquerdo.eh_folha:
            filho.filhos.insert(0, irmao_esquerdo.filhos.pop())

    def pegar_do_irmao_direito(self, no, idx):
        filho = no.filhos[idx]
        irmao_direito = no.filhos[idx + 1]

        filho.chaves.append(no.chaves[idx])
        no.chaves[idx] = irmao_direito.chaves.pop(0)
        if not irmao_direito.eh_folha:
            filho.filhos.append(irmao_direito.filhos.pop(0))

    def juntar_filhos(self, no, idx):
        filho_esquerdo = no.filhos[idx]
        filho_direito = no.filhos[idx + 1]

        filho_esquerdo.chaves.append(no.chaves.pop(idx))
        filho_esquerdo.chaves.extend(filho_direito.chaves)
        if not filho_direito.eh_folha:
            filho_esquerdo.filhos.extend(filho_direito.filhos)
        no.filhos.pop(idx + 1)

    def mostrar(self, x=None, nivel=0):
        if x is None:
            x = self.raiz

        if nivel == 0:
            print(f"Nivel {nivel}: [{', '.join(map(str, x.chaves))}]")
        else:
            print(f"Nivel {nivel}: [{', '.join(map(str, x.chaves))}]")

        nivel += 1
        if not x.eh_folha:
            for i in range(len(x.filhos)):
                if i < len(x.chaves):
                    self.mostrar(x.filhos[i], nivel)
                else:
                    self.mostrar(x.filhos[i], nivel)


arvore_b = ArvoreB(3)  # Arvore de ordem 2, quantidade maxima de chaves = 4 (na inserção da quarta chave ela divide o nó)
chaves = [1, 2, 3, 7, 9, 10, 14, 15, 16, 17,
          22, 23, 24, 28, 31, 32, 33, 34, 40, 41, 42]

for chave in chaves:
    arvore_b.inserir(chave)

print("\nArvore B: ")
arvore_b.mostrar()

print("\nUsando a funcao buscar para encontrar o numero 7: ")
print(arvore_b.buscar(7))

print("\nUsando a funcao buscar para encontrar o numero 25: ")
print(arvore_b.buscar(25))


print("\nUsando a funcao remover: (remove o numero 24)")
arvore_b.remover(24)
arvore_b.mostrar(arvore_b.raiz)
