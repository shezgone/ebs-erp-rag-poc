import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.mock_erp import load_mock_erp_data
from src.ontology.mapper import build_knowledge_graph
from src.rag.retriever import GraphRetriever

def main():
    print("--- EBS ERP RAG PoC Initialization ---")

    # 1. Load Data
    print("[1] Loading ERP dummy data...")
    erp_data = load_mock_erp_data()
    print(f"    Loaded {len(erp_data['customers'])} customers, {len(erp_data['orders'])} orders.")

    # 2. Build Ontology (Graph)
    print("[2] Mapping Data to Ontology (Knowledge Graph)...")
    kg = build_knowledge_graph(erp_data)
    print(f"    Graph constructed with {len(kg)} triples.")

    # Serialize for inspection (optional)
    # kg.serialize(destination="erp_graph.ttl", format="turtle")

    # 3. Retrieval (Simulating RAG Context Retrieval)
    retriever = GraphRetriever(kg)
    
    # Scenario A: Sales & Finance
    target_customer = "EBS 테크"  
    print(f"\n[3.1] 사용자 질문: '{target_customer}가 최근 주문 대금을 지불했나요?'")
    context_a = retriever.get_context_string("customer_history", target_customer)
    print(f"      >> 검색된 컨텍스트:\n{context_a}")

    # Scenario B: Sales & Finance (New Customer with unpaid bill)
    target_customer_new = "스타트업 허브"
    print(f"\n[3.2] 사용자 질문: '{target_customer_new}의 결제 상태는 어떤가요?'")
    context_b = retriever.get_context_string("customer_history", target_customer_new)
    print(f"      >> 검색된 컨텍스트:\n{context_b}")

    # Scenario C: Production & Inventory
    print(f"\n[3.3] 사용자 질문: '생산에 필요한 원자재 재고가 충분한가요?'")
    context_c = retriever.get_context_string("stock_check", "원자재")
    print(f"      >> 검색된 컨텍스트:\n{context_c}")

    print("\n[4] LLM 답변 생성 단계 (Mocked)")
    print(f"    입력 프롬프트: '검색된 컨텍스트를 바탕으로 {target_customer_new}의 재무 리스크와 원자재 부족 상황을 보고해줘.'")
    print("    생성 시작...")

    # Here you would call: llm.invoke(prompt + context)

if __name__ == "__main__":
    main()
