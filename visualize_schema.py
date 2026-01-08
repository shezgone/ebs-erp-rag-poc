from rdflib import Graph
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Mac OS 기준)
try:
    rc('font', family='AppleGothic') 
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

from src.ontology.schema import EBS, EX

def visualize_ontology_schema():
    """
    한글 스키마 시각화
    """
    G = nx.DiGraph()

    # 클래스 (노드) - 한글 이름
    classes = [
        "고객", "주문", "품목", 
        "공급사", "발주",
        "작업지시", "재고기록", "창고",
        "매출송장", "매입송장"
    ]

    for cls in classes:
        G.add_node(cls, color='lightblue', style='filled')

    # 관계 (엣지) - 한글 Predicate
    relationships = [
        ("주문", "주문자", "고객"),
        ("주문", "포함품목", "품목"), 
        ("매출송장", "청구주문", "주문"),
        
        ("발주", "발급대상", "공급사"),
        ("발주", "발주품목", "품목"),
        ("매입송장", "지불발주", "발주"),

        ("작업지시", "생산품목", "품목"),
        
        ("재고기록", "위치", "창고"),
        ("재고기록", "대상품목", "품목"),
    ]

    for src, pred, dst in relationships:
        if src in classes and dst in classes: 
            G.add_edge(src, dst, label=pred)

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=1.2)  

    # 노드 그리기
    nx.draw_networkx_nodes(G, pos, node_size=4000, node_color="#E0F7FA", alpha=1.0, edgecolors="#006064")
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_family='AppleGothic')

    # 엣지 그리기
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, arrowsize=25, width=1.5)
    
    # 엣지 라벨 (Predicate)
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color="darkblue", font_family='AppleGothic')

    plt.title("EBS ERP 한글 온톨로지 스키마", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    
    output_path = "ontology_schema_kr.png"
    plt.savefig(output_path)
    print(f"한글 스키마 시각화 저장 완료: {output_path}")

if __name__ == "__main__":
    visualize_ontology_schema()
