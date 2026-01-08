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
            print(f"\n[LOG] 1️⃣  사용자 자연어 쿼리 수신: \"{user_input}\"")

            # Simple Intent Recognition (Rule-based for PoC)
            # In real system, this would be an LLM classifier
            context = ""
            print(f"[LOG] 2️⃣  의도 분석 및 엔티티 추출 중...")
            
            # Normalize for matching (remove whitespace to handle typos like 'EBS테크')
            user_input_norm = user_input.replace(" ", "")

            if "원자재" in user_input_norm or "재고" in user_input_norm:
                print(f"[LOG]    -> 의도: 재고 현황 조회 (Intent: StockCheck)")
                print(f"[LOG]    -> 추출 엔티티: '원자재'")
                context = retriever.get_context_string("stock_check", "원자재")
            else:
                # Assume customer query, try to find known customer names
                found_cust = None
                known_customers = ['EBS 테크', '미래 학교', '에듀 코프', '스타트업 허브']
                for cust in known_customers:
                    # Check matching ignoring spaces (e.g. '스타트업허브' matches '스타트업 허브')
                    if cust.replace(" ", "") in user_input_norm:
                        found_cust = cust
                        break
                
                if found_cust:
                     print(f"[LOG]    -> 의도: 고객 주문 이력 조회 (Intent: CustomerHistory)")
                     print(f"[LOG]    -> 추출 엔티티: '{found_cust}'")
                     context = retriever.get_context_string("customer_history", found_cust)
                else:
                    print("[System] ⚠️ 질문에서 고객명이나 '원자재' 키워드를 찾을 수 없습니다.")
                    print("예시: 'EBS 테크 이력 보여줘', '원자재 재고 어때?'")
                    continue

            print("\n[LOG] 3️⃣  최종 검색된 컨텍스트 (LLM 입력용):")
            print("=" * 40)
            print(context)
            print("=" * 40)
            
            # 4. Mock LLM Generation
            print(f"\n[LOG] 4️⃣  LLM 최종 답변 생성 (Simulation)...")
            final_answer = mock_llm_response(user_input, context)
            print("\n🤖 [AI Assistant]:", final_answer)
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")

def mock_llm_response(query, context):
    """
    Simulates an LLM generating a natural language response based on the retrieved context.
    """
    if "기록이 없습니다" in context:
        return "죄송합니다. 해당 조건에 맞는 정보를 찾을 수 없습니다."
    
    if "미납" in context:
        return f"현재 조회된 정보에 따르면, 해당 고객에게 **미납된 주문**이 존재합니다. 재무 리스크 관리가 필요할 수 있으니 담당 부서 확인을 권장합니다.\n(근거: {context.strip()})"
        
    if "납부완료" in context:
        return f"확인 결과, 해당 고객의 최근 주문 건들은 모두 **정상적으로 결제 완료**되었습니다. 우수 고객으로 판단됩니다."
        
    if "원자재" in context:
        # Simple extraction logic for demo
        import re
        lines = context.split('\n')
        low_stock = [line for line in lines if "5개" in line or "10개" in line] # Mock low stock logic
        
        if low_stock:
             return f"현재 원자재 재고 현황을 확인했습니다. 일부 품목의 재고가 부족해 보입니다.\n특히 다음 항목에 주의하세요: {', '.join([l.split(':')[0] for l in low_stock])}.\n생산 일정에 차질이 없도록 발주가 필요합니다."
        else:
             return "현재 원자재 재고는 생산을 진행하기에 충분한 수준으로 파악됩니다."

    return "죄송합니다. 문맥을 기반으로 정확한 답변을 생성하기 어렵습니다."

if __name__ == "__main__":
    interactive_session()
