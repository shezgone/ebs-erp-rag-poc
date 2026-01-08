# EBS ERP RAG PoC (Knowledge Graph Based)

이 프로젝트는 EBS ERP 시스템의 정형 데이터를 **Knowledge Graph(지식 그래프)** 기반의 **RAG(Search-Augmented Generation)** 시스템으로 구축하는 Proof of Concept (PoC)입니다. 
전통적인 키워드 검색이나 단순 벡터 검색의 한계를 넘어, ERP 내의 복잡한 개체 간 관계(주문-청구, 자재-생산, 구매-공급사 등)를 구조적으로 탐색하여 정확한 답변을 제공하는 것을 목표로 합니다.

## 📌 주요 특징

1.  **ERP 온톨로지 매핑 (Ontology Mapping)**
    -   RDB(관계형 데이터베이스)의 테이블 구조를 RDF(Resource Description Framework) Triple로 변환
    -   `rdflib`를 사용하여 정확도 100%의 Rule-based 매핑 구현 (Financial/Order 데이터 정합성 보장)
    -   한글 스키마 (`http://example.org/schema/kr/`) 적용

2.  **지식 그래프 기반 검색 (Graph-based Retrieval)**
    -   SPARQL 쿼리를 통해 Cross-Domain 지식 탐색
    -   단순 텍스트 매칭이 아닌 "관계"를 추적하여 답변 (예: "미납된 주문이 있는 고객은?")
    -   영업(Sales), 구매(Purchasing), 생산(Production), 재무(Finance), 재고(Inventory) 모듈 연결

3.  **한국어 시나리오 데이터**
    -   한국 기업 환경에 맞는 가상 ERP 데이터(Mock Data) 구축
    -   다양한 RAG 시나리오 테스트 가능 (미수금 확인, 재고 부족 알림 등)

## 🛠️ 프로젝트 구조

```text
ebs-erp-rag-poc/
├── .venv/                     # Python 가상환경
├── src/
│   ├── main.py                # 메인 실행 스크립트 (시나리오 검증용)
│   ├── data/
│   │   └── mock_erp.py        # ERP 가상 데이터 생성 (Pandas DataFrame)
│   ├── ontology/
│   │   ├── schema.py          # RDF 네임스페이스 및 스키마 정의
│   │   └── mapper.py          # DataFrame -> RDF Graph 변환 로직
│   └── rag/
│       └── retriever.py       # SPARQL 기반 컨텍스트 검색기
├── interactive_rag.py         # 대화형 RAG 검색 세션 프로그램
├── visualize_schema.py        # 온톨로지 스키마 시각화 스크립트
├── inspect_data.py            # ERP 테이블 데이터 조회 유틸리티
├── ontology_schema_kr.png     # 생성된 스키마 시각화 이미지
└── requirements.txt           # 의존성 패키지 목록
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 실행 방법

**기본 시나리오 검증**
사전에 정의된 주요 비즈니스 시나리오(미수금 체크, 재고 확인 등)를 실행합니다.
```bash
python src/main.py
```

**대화형 검색 (Interactive Mode)**
터미널에서 직접 질문하며 RAG 검색을 테스트할 수 있습니다.
```bash
python interactive_rag.py
```
*   예시 질문:
    *   "**스타트업 허브**의 주문 결제 상태는?"
    *   "**원자재** 재고가 부족한지 확인해줘"
    *   "**EBS 테크**의 최근 거래 내역은?"

**데이터 확인**
현재 로딩된 가상 ERP 테이블 전체를 조회합니다.
```bash
python inspect_data.py
```

**스키마 시각화**
온톨로지 구조를 다이어그램 이미지(`ontology_schema_kr.png`)로 생성합니다.
```bash
python visualize_schema.py
```

## 📊 데이터 모델 (Schema)

이 PoC는 다음과 같은 핵심 엔티티와 관계를 모델링했습니다.

*   **고객 (Customer)**: `주문`을 함
*   **주문 (Order)**: `매출송장`과 연결됨 (청구/미납 여부)
*   **품목 (Item)**: 완제품(서비스) 또는 원자재
*   **재고 (Stock)**: 특정 `창고`에 있는 품목의 `수량`
*   **작업지시 (WorkOrder)**: 품목 생산을 위한 상태(`진행중`, `대기중`)
*   **매입/매출 송장 (Invoice)**: 재무적 흐름 추적

---
Developed for EBS ERP RAG Project PoC.
