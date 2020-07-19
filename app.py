import unittest
from unittest.mock import patch
import app

class TestMyClassDocuments(unittest.TestCase):
    def setUp(self) -> None:
        self.dirs, self.docs = app.update_date()
        self.direct = app.Directories(self.dirs, self.docs)

    def test_get_doc(self):
        doc = self.direct.get_documents('10006')
        self.assertEqual(doc['type'], 'insurance')
        self.assertEqual(doc['name'], 'Аристарх Павлов')

    def test_init_direct(self):
        dirs, docs = app.update_date()
        self.assertEqual(3, len(docs))
        d1 = app.Directories(dirs, docs)
        self.assertEqual(len(d1.docs), 4)

    def test_not_get_doc(self):
        doc = self.direct.get_documents('10007')
        self.assertEqual(doc, None)

class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.dirs, self.docs = app.update_date()
        self.error_docs = [{"type": "insurance", "number": "10006"}]
        with patch('app.update_date', return_value=(self.dirs, self.docs)):
            with patch('app.input', return_value='q'):
                app.secretary_program_start()

    def test_not_raise_get_doc(self):
        with patch('app.update_date', return_value=(self.dirs, self.error_docs)):
            with patch('app.input', return_value='q'):
                app.secretary_program_start()
            app.get_all_doc_owners_names()

    @unittest.skip('skip for example')
    def test_delete(self):
        before_len = len(self.docs)
        with patch('app.input', return_value='10006'):
            app.delete_doc()
        self.assertLess(len(self.docs), before_len)

    def test_add_new_document_to_new_directory(self):
        before_len = len(self.docs)
        self.assertEqual(before_len, 3)
        with patch('app.input', size_effect=['10007', 'passport', 'testUser', '1']):
            app.add_new_doc()
        self.assertGreater(len(self.docs), before_len)
        self.assertEqual(len(self.docs), 4)


