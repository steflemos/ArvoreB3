class NoArvoreB: # Classe que inicializa o nó da árvore B:
    def __init__(self, eh_folha=True):
        self.eh_folha = eh_folha
        self.chaves = []
        self.filhos = []

class ArvoreB: # Classe que representa a árvore B
    def __init__(self, t):
        self.raiz = NoArvoreB()
        self.t = t  # t é a ordem da árvore B

    def inserir(self, chave):
        # Função para inserir uma chave na árvore B
        raiz = self.raiz
        if len(raiz.chaves) == (2 * self.t) - 1:
            # Se o nó raiz estiver cheio, cria um novo nó raiz
            novo_no = NoArvoreB(eh_folha=False)
            novo_no.filhos.append(raiz)
            self.dividir_filho(novo_no, 0)
            self.raiz = novo_no
            self.inserir_nao_cheio(novo_no, chave)
        else:
            self.inserir_nao_cheio(raiz, chave)

    def inserir_nao_cheio(self, x, chave):
        # Função para inserir uma chave em um nó não cheio
        i = len(x.chaves) - 1
        if x.eh_folha:
            x.chaves.append(None)
            while i >= 0 and chave < x.chaves[i]:
                x.chaves[i + 1] = x.chaves[i]
                i -= 1
            x.chaves[i + 1] = chave
        else:
            while i >= 0 and chave < x.chaves[i]:
                i -= 1
            i += 1
            if len(x.filhos[i].chaves) == (2 * self.t) - 1:
                self.dividir_filho(x, i)
                if chave > x.chaves[i]:
                    i += 1
            self.inserir_nao_cheio(x.filhos[i], chave)

    def dividir_filho(self, x, i):
        # Função para dividir um filho de um nó
        t = self.t
        y = x.filhos[i]
        z = NoArvoreB(eh_folha=y.eh_folha)
        x.filhos.insert(i + 1, z)
        x.chaves.insert(i, y.chaves[t - 1])
        z.chaves = y.chaves[t:(2 * t - 1)]
        y.chaves = y.chaves[0:(t - 1)]
        if not y.eh_folha:
            z.filhos = y.filhos[t:(2 * t)]
            y.filhos = y.filhos[0:t]

    def buscar(self, chave, x=None):
        # Função para buscar uma chave na árvore B
        if x is None:
            x = self.raiz
        i = 0
        while i < len(x.chaves) and chave > x.chaves[i]:
            i += 1
        if i < len(x.chaves) and chave == x.chaves[i]:
            return True
        elif x.eh_folha:
            return False
        else:
            return self.buscar(chave, x.filhos[i])

    def remover(self, chave):
        # Função para remover uma chave da árvore B
        if not self.raiz.chaves:
            return
        if chave in self.raiz.chaves:
            if len(self.raiz.chaves) == 1:
                if self.raiz.filhos:
                    self.raiz = self.raiz.filhos[0]
                else:
                    self.raiz.chaves.remove(chave)
            else:
                self.remover_chave_do_no(self.raiz, chave)
        else:
            self.remover_chave_do_no(self.raiz, chave)

    def remover_chave_do_no(self, no, chave):
        # Função para remover uma chave de um nó
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1
        if i < len(no.chaves) and chave == no.chaves[i]:
            if no.eh_folha:
                no.chaves.remove(chave)
            else:
                chave_pred = self.obter_predecessor(no, i)
                if len(no.filhos[i].chaves) >= self.t:
                    no.chaves[i] = chave_pred
                    self.remover_chave_do_no(no.filhos[i], chave_pred)
                else:
                    chave_succ = self.obter_sucessor(no, i)
                    no.chaves[i] = chave_succ
                    self.remover_chave_do_no(no.filhos[i + 1], chave_succ)
        else:
            if no.eh_folha:
                return
            if len(no.filhos[i].chaves) < self.t:
                self.corrigir_filho(no, i)
            self.remover_chave_do_no(no.filhos[i], chave)

    def obter_predecessor(self, no, idx):
        # Função para obter o predecessor de uma chave
        atual = no.filhos[idx]
        while not atual.eh_folha:
            atual = atual.filhos[-1]
        return atual.chaves[-1]

    def obter_sucessor(self, no, idx):
        # Função para obter o sucessor de uma chave
        atual = no.filhos[idx + 1]
        while not atual:
            atual = atual.filhos[0]
        return atual.chaves[0]

    def corrigir_filho(self, no, idx):
        # Função para corrigir um filho após a remoção de uma chave
        if idx > 0 and len(no.filhos[idx - 1].chaves) >= self.t:
            self.pegar_do_irmao_esquerdo(no, idx)
        elif idx < len(no.filhos) - 1 and len(no.filhos[idx + 1].chaves) >= self.t:
            self.pegar_do_irmao_direito(no, idx)
        else:
            if idx < len(no.filhos):
                self.juntar_filhos(no, idx)
            else:
                self.juntar_filhos(no, idx - 1)

    def pegar_do_irmao_esquerdo(self, no, idx):
        # Função para pegar uma chave do irmão esquerdo
        filho = no.filhos[idx]
        irmao_esquerdo = no.filhos[idx - 1]

        filho.chaves.insert(0, no.chaves[idx - 1])
        no.chaves[idx - 1] = irmao_esquerdo.chaves.pop()
        if not irmao_esquerdo.eh_folha:
            filho.filhos.insert(0, irmao_esquerdo.filhos.pop())

    def pegar_do_irmao_direito(self, no, idx):
        # Função para pegar uma chave do irmão direito
        filho = no.filhos[idx]
        irmao_direito = no.filhos[idx + 1]

        filho.chaves.append(no.chaves[idx])
        no.chaves[idx] = irmao_direito.chaves.pop(0)
        if not irmao_direito.eh_folha:
            filho.filhos.append(irmao_direito.filhos.pop(0))

    def juntar_filhos(self, no, idx):
        # Função para juntar dois filhos
        filho_esquerdo = no.filhos[idx]
        filho_direito = no.filhos[idx + 1]

        filho_esquerdo.chaves.append(no.chaves.pop(idx))
        filho_esquerdo.chaves.extend(filho_direito.chaves)
        if not filho_direito.eh_folha:
            filho_esquerdo.filhos.extend(filho_direito.filhos)

    
    def mostrar(self, x=None, nivel=0):
        # Função para exibir a árvore B
        if x is None:
            x = self.raiz
        print(f"Nível {nivel}: {x.chaves}")
        nivel += 1
        if not x.eh_folha:
            for filho in x.filhos:
                self.mostrar(filho, nivel)

# Exemplo de uso:
arvore_b = ArvoreB(3)  # Árvore B de ordem 3
chaves = [3, 7, 1, 5, 9, 2, 4, 6, 8, 10, 89,
        54, 22, 24, 96, 16, 13, 28, 31, 48, 102]

for chave in chaves:
    arvore_b.inserir(chave)

arvore_b.mostrar()  # Exibir a árvore B
print(arvore_b.buscar(5))  # True
print(arvore_b.buscar(14))  # False

# Para remover um valor, você pode usar:
arvore_b.remover(24)
arvore_b.mostrar()  # Exibir a árvore B após a remoção da chave 7
