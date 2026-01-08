from typing import Dict
import pandas as pd
from rdflib import Graph, Literal, URIRef, RDF
from src.ontology.schema import EBS, EX, C, P

def build_knowledge_graph(erp_data: Dict[str, pd.DataFrame]) -> Graph:
    g = Graph()
    g.bind("ebs", EBS)
    g.bind("ex", EX)

    # --- 1. 마스터 데이터 (고객, 품목, 공급사) ---
    if 'customers' in erp_data:
        for _, row in erp_data['customers'].iterrows():
            uri = EBS[f"Customer/{row['cust_id']}"]
            g.add((uri, RDF.type, C.고객))
            g.add((uri, P.이름, Literal(row['name'])))
            g.add((uri, P.고객유형, Literal(row['segment'])))

    if 'items' in erp_data:
        for _, row in erp_data['items'].iterrows():
            uri = EBS[f"Item/{row['item_id']}"]
            g.add((uri, RDF.type, C.품목))
            g.add((uri, P.이름, Literal(row['item_name'])))
            g.add((uri, P.품목유형, Literal(row['type'])))
            g.add((uri, P.표준원가, Literal(row['cost'])))

    if 'suppliers' in erp_data:
        for _, row in erp_data['suppliers'].iterrows():
            uri = EBS[f"Supplier/{row['supp_id']}"]
            g.add((uri, RDF.type, C.공급사))
            g.add((uri, P.이름, Literal(row['supp_name'])))
            g.add((uri, P.등급, Literal(row['rating'])))

    # --- 2. 영업 및 재무 (주문, 매출송장) ---
    if 'orders' in erp_data:
        for _, row in erp_data['orders'].iterrows():
            ord_uri = EBS[f"Order/{row['order_id']}"]
            cust_uri = EBS[f"Customer/{row['cust_id']}"]
            g.add((ord_uri, RDF.type, C.주문))
            g.add((ord_uri, P.주문자, cust_uri))
            g.add((ord_uri, P.주문일, Literal(row['order_date'])))
    
    if 'ar_invoices' in erp_data:
        for _, row in erp_data['ar_invoices'].iterrows():
            inv_uri = EBS[f"Invoice/AR/{row['inv_id']}"]
            ord_uri = EBS[f"Order/{row['order_id']}"]
            g.add((inv_uri, RDF.type, C.매출송장))
            g.add((inv_uri, P.청구주문, ord_uri))
            g.add((inv_uri, P.금액, Literal(row['amount'])))
            g.add((inv_uri, P.상태, Literal(row['status'])))

    # --- 3. 구매 및 재무 (발주, 매입송장) ---
    if 'purchase_orders' in erp_data:
        for _, row in erp_data['purchase_orders'].iterrows():
            po_uri = EBS[f"PO/{row['po_id']}"]
            supp_uri = EBS[f"Supplier/{row['supp_id']}"]
            g.add((po_uri, RDF.type, C.발주))
            g.add((po_uri, P.발급대상, supp_uri))
            g.add((po_uri, P.발주일, Literal(row['po_date'])))
    
    if 'po_lines' in erp_data:
        for _, row in erp_data['po_lines'].iterrows():
            po_uri = EBS[f"PO/{row['po_id']}"]
            item_uri = EBS[f"Item/{row['item_id']}"]
            g.add((po_uri, P.발주품목, item_uri)) 

    if 'ap_invoices' in erp_data:
        for _, row in erp_data['ap_invoices'].iterrows():
            inv_uri = EBS[f"Invoice/AP/{row['inv_id']}"]
            po_uri = EBS[f"PO/{row['po_id']}"]
            g.add((inv_uri, RDF.type, C.매입송장))
            g.add((inv_uri, P.지불발주, po_uri))
            g.add((inv_uri, P.금액, Literal(row['amount'])))

    # --- 4. 재고 및 생산 ---
    if 'stock' in erp_data:
        for _, row in erp_data['stock'].iterrows():
            item_uri = EBS[f"Item/{row['item_id']}"]
            wh_uri = EBS[f"Warehouse/{row['wh_id']}"]
            inv_rec_uri = EBS[f"Stock/{row['wh_id']}/{row['item_id']}"]
            
            g.add((inv_rec_uri, RDF.type, C.재고기록))
            g.add((inv_rec_uri, P.대상품목, item_uri))
            g.add((inv_rec_uri, P.위치, wh_uri))
            g.add((inv_rec_uri, P.수량, Literal(row['on_hand_qty'])))

    if 'work_orders' in erp_data:
        for _, row in erp_data['work_orders'].iterrows():
            wo_uri = EBS[f"WO/{row['wo_id']}"]
            item_uri = EBS[f"Item/{row['item_id']}"]
            g.add((wo_uri, RDF.type, C.작업지시))
            g.add((wo_uri, P.생산품목, item_uri))
            g.add((wo_uri, P.상태, Literal(row['status'])))

    return g
