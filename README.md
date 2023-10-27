# Arvore B
Implementação de Árvore B em Python

## Equipe

- Stéfani
- Débora
- Maria Eduarda
- Tiago Ramos
- João
- Jael

## Descrição do Projeto

A Árvore B é uma estrutura de dados balanceada que é amplamente utilizada para armazenar e gerenciar dados de forma eficiente, especialmente em bancos de dados e sistemas de gerenciamento de arquivos. Neste projeto, implementamos a propriedade de inserção e remoção de elementos em uma Árvore B.

**Conceitos**

- **Nó:** Um nó é uma unidade básica de uma árvore B. Ele é composto por um valor, um ponteiro para o nó pai, um ponteiro para cada nó filho e um contador de filhos.
- **Folha:** Uma folha é um nó que não possui filhos.
- **Nó interno:** Um nó interno é um nó que possui pelo menos um filho.

**Percurso em árvores B**

Existem três tipos de percursos em árvores B:

- **Percurso em pré-ordem:** O percurso em pré-ordem visita o nó atual, seguido de seus filhos, da esquerda para a direita.
- **Percurso em pós-ordem:** O percurso em pós-ordem visita os filhos do nó atual, da esquerda para a direita, seguido do próprio nó.
- **Percurso em in-ordem:** O percurso em in-ordem visita os filhos do nó atual, da esquerda para a direita, terminando com o próprio nó.

**Inclusão em árvores B**

A inserção de um elemento em uma árvore B ocorre da seguinte forma:

1. Se o elemento já existir na árvore, ele não é inserido.
2. Se o elemento não existir na árvore, ele é inserido na folha mais à esquerda que possui um valor maior ou igual ao elemento.
3. Se a folha não tiver espaço para o elemento, ela é dividida em duas folhas. O elemento é inserido na nova folha.

**Exclusão em árvores B**

A remoção de um elemento em uma árvore B ocorre da seguinte forma:

1. Se o elemento não existir na árvore, ele não é removido.
2. Se o elemento existir na árvore, ele é removido da folha em que está.
3. Se a folha ficar vazia, ela é fundida com a folha à sua direita.

### Simulador da estrutura de Árvore B

O simulador da estrutura de Árvore B pode ser encontrado no endereço [Simulador de Árvore B](http://www.inf.ufsc.br/~aldo.vw/estruturas/simulador/B.html).

### Programa codificado

O programa codificado para as propriedades de inserção e remoção de elementos em uma árvore B pode ser encontrado no repositório GitHub do trabalho.
