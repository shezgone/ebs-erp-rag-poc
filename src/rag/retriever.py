from rdflib import Graph

class GraphRetriever:
    def __init__(self, graph: Graph):
        self.graph = graph

    def query_customer_orders(self, customer_name: str):
        sparql_query = f"""
        PREFIX ex: <http://example.org/schema/kr/>
        
        SELECT ?orderDate ?status
        WHERE {{
            ?cust a ex:고객 ;
                  ex:이름 "{customer_name}" .
            ?order ex:주문자 ?cust ;
                   ex:주문일 ?orderDate .
            
            OPTIONAL {{
                ?inv ex:청구주문 ?order ;
                     ex:상태 ?status .
            }}
        }}
        """
        print(f"\n[DEBUG] 🛠️ Generated SPARQL Query:\n{sparql_query}")
        
        results = self.graph.query(sparql_query)
        print(f"[DEBUG] 📊 Graph Query Result: Found {len(results)} rows")
        
        output = []
        for row in results:
            status = str(row.status) if row.status else "청구 전"
            output.append({
                "date": str(row.orderDate),
                "status": status
            })
            print(f"       -> Row: Date={row.orderDate}, Status={status}")
            
        return output

    def query_production_dependencies(self, product_type: str):
        sparql_query_simple = f"""
        PREFIX ex: <http://example.org/schema/kr/>
        SELECT ?name ?qty ?wh
        WHERE {{
            ?item ex:품목유형 "{product_type}" ;
                  ex:이름 ?name .
            ?stock ex:대상품목 ?item ;
                   ex:수량 ?qty ;
                   ex:위치 ?wh .
        }}
        """
        print(f"\n[DEBUG] 🛠️ Generated SPARQL Query:\n{sparql_query_simple}")
        
        results = self.graph.query(sparql_query_simple)
        print(f"[DEBUG] 📊 Graph Query Result: Found {len(results)} rows")
        
        output = []
        for row in results:
             val_str = f"{row.name}: {row.qty}개 (위치: {row.wh.split('/')[-1]})"
             output.append(val_str)
             print(f"       -> Row: {val_str}")
             
        return output

    def get_context_string(self, query_type: str, param: str) -> str:
        """
        Formats retrieval results into context for an LLM.
        """
        if query_type == "customer_history":
            results = self.query_customer_orders(param)
            if not results:
                return f"고객 '{param}'에 대한 기록이 없습니다."
            context = [f"고객 '{param}' 주문 이력:"]
            for r in results:
                context.append(f"- 주문일: {r['date']}, 결제 상태: {r['status']}")
            return "\n".join(context)
            
        elif query_type == "stock_check":
             results = self.query_production_dependencies(param)
             return "현재 원자재 재고 현황:\n" + "\n".join(results)
             
        return "알 수 없는 요청입니다."
