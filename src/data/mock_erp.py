import pandas as pd
from typing import Dict

def load_mock_erp_data() -> Dict[str, pd.DataFrame]:
    """
    Simulates fetching tables from EBS ERP Database including
    Sales, Finance, Purchasing, Production, and Inventory.
    Korean Data for rich scenarios.
    """
    
    # --- SALES & MASTER ---
    # 1. Customer Table (T_CUST)
    customers = pd.DataFrame({
        'cust_id': ['C001', 'C002', 'C003', 'C004'],
        'name': ['EBS 테크', '미래 학교', '에듀 코프', '스타트업 허브'],
        'segment': ['대기업', '공공', '대기업', '중소기업']
    })

    # 2. Product/Item Table (T_ITEM)
    items = pd.DataFrame({
        'item_id': ['I100', 'I200', 'I300', 'RM01', 'RM02', 'RM03'],
        'item_name': ['ERP 라이선스 프로', '클라우드 스토리지 1TB', 'AI 유지보수', '서버 랙', '냉각 팬', '고성능 CPU'],
        'type': ['서비스', '서비스', '서비스', '원자재', '원자재', '원자재'],
        'cost': [5000, 200, 1000, 500, 50, 800]
    })

    # 3. Order Table (T_ORD_HEAD)
    orders = pd.DataFrame({
        'order_id': ['O5001', 'O5002', 'O5003', 'O5004'],
        'cust_id': ['C001', 'C003', 'C004', 'C002'],
        'order_date': ['2024-01-15', '2024-02-10', '2024-02-28', '2024-03-05']
    })

    # --- PURCHASING ---
    # 4. Supplier Table (T_SUPPLIER)
    suppliers = pd.DataFrame({
        'supp_id': ['S01', 'S02', 'S03'],
        'supp_name': ['글로벌 칩스', '메탈 웍스', '패스트 부품'],
        'rating': ['A', 'B', 'C']
    })

    # 5. Purchase Order (T_PO_HEAD)
    purchase_orders = pd.DataFrame({
        'po_id': ['PO901', 'PO902', 'PO903'],
        'supp_id': ['S01', 'S02', 'S03'],
        'po_date': ['2023-12-20', '2024-01-05', '2024-02-20']
    })

    # 6. Purchase Order Lines (T_PO_LINE)
    po_lines = pd.DataFrame({
        'po_id': ['PO901', 'PO901', 'PO902', 'PO903'],
        'item_id': ['RM01', 'RM02', 'RM01', 'RM03'], # Buying raw materials
        'qty': [50, 200, 20, 100]
    })

    # --- INVENTORY ---
    # 7. Inventory Stock (T_STOCK)
    stock = pd.DataFrame({
        'wh_id': ['제1창고', '제1창고', '제2창고', '제1창고'],
        'item_id': ['RM01', 'RM02', 'RM01', 'RM03'],
        'on_hand_qty': [40, 150, 10, 5] # RM03 (CPU) is very low (5 units)
    })

    # --- PRODUCTION ---
    # 8. Work Order (T_WORK_ORD)
    work_orders = pd.DataFrame({
        'wo_id': ['WO-1001', 'WO-1002', 'WO-1003'],
        'item_id': ['I200', 'I200', 'I300'],
        'status': ['완료', '진행중', '대기중'],
        'start_date': ['2024-01-10', '2024-02-01', '2024-03-10']
    })

    # --- FINANCE ---
    # 9. AP Invoices (T_AP_INV) - Paying Suppliers
    ap_invoices = pd.DataFrame({
        'inv_id': ['INV-S01-001', 'INV-S03-001'],
        'po_id': ['PO901', 'PO903'],
        'amount': [25000, 80000],
        'due_date': ['2024-01-20', '2024-03-20']
    })

    # 10. AR Invoices (T_AR_INV) - Billing Customers
    ar_invoices = pd.DataFrame({
        'inv_id': ['INV-C001-001', 'INV-C004-001'],
        'order_id': ['O5001', 'O5003'],
        'amount': [55000, 3000],
        'status': ['납부완료', '미납']
    })

    return {
        "customers": customers,
        "items": items,
        "orders": orders,
        "suppliers": suppliers,
        "purchase_orders": purchase_orders,
        "po_lines": po_lines,
        "stock": stock,
        "work_orders": work_orders,
        "ap_invoices": ap_invoices,
        "ar_invoices": ar_invoices
    }
