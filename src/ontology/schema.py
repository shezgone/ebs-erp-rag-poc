from rdflib import Namespace, RDF, RDFS, OWL

# 네임스페이스 정의 (한글 스키마 적용)
EBS = Namespace("http://ebs.co.kr/erp/")
EX = Namespace("http://example.org/schema/kr/")  # kr 스키마

# 클래스 이름 정의 (코드 가독성을 위해 상수로 정의)
class C:
    고객 = EX.고객
    품목 = EX.품목
    주문 = EX.주문
    공급사 = EX.공급사
    발주 = EX.발주
    작업지시 = EX.작업지시
    재고기록 = EX.재고기록
    창고 = EX.창고
    매출송장 = EX.매출송장
    매입송장 = EX.매입송장

# 속성 이름 정의
class P:
    # 마스터
    이름 = EX.이름
    고객유형 = EX.고객유형
    품목유형 = EX.품목유형
    표준원가 = EX.표준원가
    등급 = EX.등급
    
    # 영업/주문
    주문자 = EX.주문자
    주문일 = EX.주문일
    포함품목 = EX.포함품목 # Order -> Item (단순화)
    
    # 재무
    청구주문 = EX.청구주문 # Invoice -> Order
    지불발주 = EX.지불발주 # Invoice -> PO
    금액 = EX.금액
    상태 = EX.상태 # 결제상태, 진행상태 등
    만기일 = EX.만기일
    
    # 구매
    발급대상 = EX.발급대상 # PO -> Supplier
    발주품목 = EX.발주품목 # PO -> Item
    발주일 = EX.발주일
    
    # 생산/재고
    생산품목 = EX.생산품목
    대상품목 = EX.대상품목 # Stock -> Item
    위치 = EX.위치
    수량 = EX.수량

def get_namespaces():
    return {
        "ebs": EBS,
        "ex": EX
    }

# Expanded Concepts for new domains
def bind_extended_namespaces(g):
    g.bind("ebs", EBS)
    g.bind("ex", EX)
    g.bind("foaf", Namespace("http://xmlns.com/foaf/0.1/"))

