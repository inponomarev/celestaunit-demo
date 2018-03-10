#coding=utf-8
from _jugmsk_orm import OrderHeaderCursor, OrderLineCursor, OrderedQtyCursor
import datetime

def post_order(context, doc):
    header = OrderHeaderCursor(context)
    line = OrderLineCursor(context)
    header.id = doc['id']
    header.date = datetime.datetime.strptime(doc['date'], '%Y-%m-%d')
    header.customer_id = doc['customer_id']
    header.customer_name = doc['customer_name']
    header.insert()
    lineno = 0
    for docline in doc['lines']:
        lineno += 1
        line.line_no = lineno
        line.order_id = doc['id']
        line.item_id = docline['item_id']
        line.qty = docline['qty']
        line.insert()
    
 
def get_aggregate_report(context):
    result = {}
    ordered_qty = OrderedQtyCursor(context)
    for ordered_qty in ordered_qty.iterate():
        result[ordered_qty.item_id] = ordered_qty.qty
    return result
