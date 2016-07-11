import pandas as pd
import copy
import networkx as nx
import pygraphviz as pgv

class FormalConceptAnalysys:
    def __init__(self):
        """
        ToDo:
        - 呼びだされた時にコンテキストがあれば読み込みgenerate_context関数呼ぶ
        """
        pass

    def genetate_context(self, data):
        '''
        context生成関数
        argument:
            name:読み込むCSVファイルのディレクトリ
        return:
            cotnext:pandasのフレーム形式のデータベース
        現状はカラム、ローともに無し
        '''
        self.context = pd.read_csv(data,header=None)
        return self.context

    def test_generate_context(self):
        """
        テストコードのcontext生成関数
        テストではCSVファイルを読み込まず,ここで適当なデータを読み込む
        """
        #テスト用コンテキスト
        df_test = pd.DataFrame([
            [1, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 1, 1],
            [0, 0, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
        ])
        self.context = df_test
        return self.context

    def intuitive_generation(self, context):
        '''
        直感的コンセプトラティス生成アルゴリズム
        argument:
            context:
        return:
            lattice:
        '''
        pass

    def next_closure_generation(self, context):
        '''
        NextClosureコンセプトラティス生成アルゴリズム
        argument:
            context: pandasのDataFrame形式のcontext
        return:
            lattice: Networkx形式のFormalConceptLattice
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
            #print("A", A)
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
        #print(lattice)
        #return lattice
        self.lattice = lattice
        V = lattice
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
        self.graph = G
        return G

if __name__ == '__main__':
    fca = FormalConceptAnalysys()
    hoge = fca.test_generate_context()
    piyo = fca.next_closure_generation(hoge)
#今はここは作った関数のテストを書いてある
    # context = pd.read_csv('./test/hoge.csv',header=None)
    # lat = next_closure_generation(context)
    # G = fca.create_Hasse_diagram(piyo)
    #A = nx.nx_agraph.to_agraph(piyo)
    #A.layout()
    #A.draw('./test/out.pdf')
