#coding=utf-8
from celestaunit.celestaunit import CelestaUnit, clean_db
from jugmsk.basic_operations import post_order, get_aggregate_report
from jugmsk._jugmsk_orm import OrderHeaderCursor

class test_basic_operations(CelestaUnit):
    
    request1 = {
           'id': 'no1',
           'date': '2017-01-02',
           'customer_id': 'CUST1',
           'customer_name': u'Василий',
           'lines': [
               {'item_id': 'A',
                'qty': 5
                },
                {'item_id': 'B',
                'qty': 4
                }    
               ]
           }
    
    request2 = {
       'id': 'no2',
       'date': '2017-01-03',
       'customer_id': 'CUST1',
       'customer_name': u'Андрей',
       'lines': [
           {'item_id': 'A',
            'qty': 3
            }    
           ]
       }

    
    def test_document_is_put_to_db(self):
        #Вызываем тестируемую процедуру
        post_order(self.context, test_basic_operations.request1)
        #Проверяем, что данные попали в базу
        header = OrderHeaderCursor(self.context)
        header.tryFirst()
        self.assertEquals('no1', header.id)
        
    
    def test_report_returns_aggregated_qtys(self):
        post_order(self.context, test_basic_operations.request1)
        post_order(self.context, test_basic_operations.request2)
        
        result = get_aggregate_report(self.context)
        self.assertEquals(8, result['A'])
        self.assertEquals(4, result['B'])
    
    def setUp(self):
        CelestaUnit.setUp(self)
        clean_db(self.context)