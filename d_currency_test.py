import unittest
import visualize_dc as v
import sys
import sqlite3
import pprint
sys.path.insert(0, '/Users/G_bgyl/si507/final_project/okcoin_lib')

# digital_currency_final_project_test.py


class AccessDatabase(unittest.TestCase):

    def test_okcoin_table(self):
        conn = sqlite3.connect(v.DBNAME)
        cur = conn.cursor()

        sql = 'SELECT DISTINCT [type] FROM Okcoin'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('bids',), result_list)
        self.assertEqual(len(result_list), 2)

        sql = '''
            SELECT *
            FROM Okcoin
            WHERE [type]="asks"
            ORDER BY volume DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()

        self.assertEqual(len(result_list), 200)
        self.assertEqual(result_list[0][4], 125)
        self.assertEqual(result_list[0][1], 'BTC')

        conn.close()





class StorageDatabase(unittest.TestCase):

    def test_Coinbase_table(self):
        conn = sqlite3.connect(v.DBNAME)
        cur = conn.cursor()

        sql = 'SELECT DISTINCT [year] FROM Coinbase'
        results = cur.execute(sql)
        result_list_2 = results.fetchall()

        self.assertIn((2018,), result_list_2)
        self.assertEqual(len(result_list_2), 6)

        sql = '''
            SELECT *
            FROM Coinbase
            WHERE year=2014
            ORDER BY spot_price DESC
            limit 10
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 10)
        self.assertEqual(result_list[0][5], 6)
        self.assertEqual(result_list[0][3], 'USD')

        conn.close()



class ProcessingDatabase(unittest.TestCase):
    pass

    def test_company_search(self):
        boxplot = v.boxplot(2017)

        self.assertEqual(boxplot[0][0], 979.56)
        rate_bar=v.rate_bar(2015)
        # pprint.pprint(rate_bar)
        self.assertTrue(rate_bar[1] == 14.98 and rate_bar[2] == -12.6)
        line_chart=v.line_chart(2016)

        self.assertEqual(line_chart[6][0], '2016-01-07')
        self.assertEqual(line_chart[7][1], 456.35)

        area_depth = v.area_depth('bids')
        print(area_depth)
        self.assertGreater(area_depth[3][1], 0.01)


if __name__ == '__main__':
    unittest.main()
