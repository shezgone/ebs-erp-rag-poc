import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data.mock_erp import load_mock_erp_data
from src.ontology.mapper import build_knowledge_graph
from src.rag.retriever import GraphRetriever

def interactive_session():
    print("--- EBS ERP RAG 대화형 세션 시작 ---")
    print("데이터 로딩 중...")
    
    erp_data = load_mock_erp_data()
    kg = build_knowledge_graph(erp_data)
    retriever = GraphRetriever(kg)
    
    print("준비 완료! (종료하려면 'exit' 또는 'quit' 입력)")
    print("사용 가능한 질문 유형: \n 1. 고객명 ('EBS 테크', '미래 학교', '스타트업 허브') -> 주문/결제 내역 조회 \n 2. '원자재' -> 재고 현황 조회")
    print("-" * 50)

    while True:
        try:
            user_input = input("\n질문을 입력하세요 >> ").strip()
            
            if user_input.lower() in ['exit', 'quit', '종료']:
                print("세션을 종료합니다.")
                break
            
            if not user_input:
                continue

            # Simple Intent Recognition (Rule-based for PoC)
            # In real system, this would be an LLM classifier
            context = ""
            if "원자재" in user_input or "재고" in user_input:
                print(f"[System] 재고 조회 의도 감지됨 -> '원자재' 필터 적용")
                context = retriever.get_context_string("stock_check", "원자재")
            else:
                # Assume customer query, try to find known customer names
                found_cust = None
                known_customers = ['EBS 테크', '미래 학교', '에듀 코프', '스타트업 허브']
                for cust in known_customers:
                    if cust in user_input:
                        found_cust = cust
                        break
                
                if found_cust:
                     print(f"[System] 고객 조회 의도 감지됨 -> '{found_cust}'")
                     context = retriever.get_context_string("customer_history", found_cust)
                else:
                    print("[System] ⚠️ 질문에서 고객명이나 '원자재' 키워드를 찾을 수 없습니다.")
                    print("예시: 'EBS 테크 이력 보여줘', '원자재 재고 어때?'")
                    continue

            print("\n----- [검색된 지식 그래프 컨텍스트] -----")
            print(context)
            print("---------------------------------------")
            print("(이 컨텍스트가 LLM 프롬프트에 주입되어 최종 답변이 생성됩니다)")
            
        except KeyboardInterrupt:
            print("\n종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    interactive_session()
