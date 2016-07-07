import pandas as pd
import copy
import networkx as nx
import pygraphviz as pgv

class FormalConceptAnalysys:
    def __init__(self):
        pass

    def genetate_context(self, name):
        '''
        context生成関数
        argument:
            name:読み込むCSVファイルのディレクトリ
        return:
            cotnext:pandasのフレーム形式のデータベース
        '''
        self.context = pd.read_csv(name,header=None)
        return context

    def intuitive_generation(self, context):
        '''
        直感的コンセプトラティス生成アルゴリズム
        argument:
            context: pandas.core.frame.DataFrameのcontextテーブル
        return:
            lattice: 考え中
            networkxのグラフか、コンセプト集合
        '''
        pass

    def create_Hasse_diagram(self, V):
        '''
        ノード集合Vからnetworkxの有向グラフで
        推移簡約な半順序集合のHasse図を出力する関数
        arguments:
            V:半順序集合を表すlist
        return:
            G:集合Vから作った推移簡約な、networkxのDiGraphのグラフG
        '''
        E = [(u, v) for u in V for v in V if u < v]
        F = []
        for u,v in E:
            for w in filter(lambda w: u < w, V):
                if (w, v) in E:
                    break
            else:
                F.append((tuple(u), tuple(v)))
        W = map(tuple, V)
        G = nx.DiGraph()
        G.add_nodes_from(W)
        G.add_edges_from(F)
        return G

    def next_closure_generation(self, fsdfcontext):
        '''
        NextClosureコンセプトラティス生成アルゴリズム
        argument:
            context: pandas.core.frame.DataFrameのcontextテーブル
        return:
            lattice:
            概念束の集合(属性の集合)
        '''
        l,c = context.shape
        objects = [i for i in range(1, l + 1)]
        attributes = [i for i in range(1, c + 1)]
        context.columns=attributes
        context.index=objects

        max_index = l
        min_index = 1

        lattice = []
        A = set()
        while True:
            print("A", A)
            lattice.append(A)
            #start next closure
            i = max_index
            i = i + 1
            succ = False
            while not succ and i != min_index:
                i = i - 1
                if i not in A:
                    B = (A & {j for j in range(1,i)}) | {i}
                    M = set(attributes)
                    for b in B:
                        for a in attributes:
                            if not context.ix[b, a]:
                                M = M - {a}
                    C = set(objects)
                    for m in M:
                        for o in objects:
                            if not context.ix[o, m]:
                                C = C - {o}
                    if (i in (C - A)) and (A & {j for j in range(1,i)} == C & {j for j in range(1,i)}):
                    #if i ∈ (C - A) and A ∩ {1,2, ... , i - 1} = C ∩ {1,2, ... , i - 1}
                        A = C
                        succ = True
            #end next closure
            if not succ:
                break
        print(lattice)
        return lattice

if __name__ == '__main__':
    fca = FormalConceptAnalysys()
    print(type(fca))
#今はここは作った関数のテストを書いてある
    # context = pd.read_csv('./test/hoge.csv',header=None)
    # lat = next_closure_generation(context)
    # G = create_Hasse_diagram(lat)
    # A = nx.nx_agraph.to_agraph(G)
    # A.layout()
    # A.draw('./test/out.pdf')
