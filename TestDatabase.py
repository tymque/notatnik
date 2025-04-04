import unittest
from unittest.mock import patch, MagicMock



class TestDatabase(unittest.TestCase):

    @patch('mysql.connector.connect')
    def setUp(self, mock_connect):
        self.mock_db = MagicMock()
        self.mock_cursor = MagicMock()

        self.mock_db.cursor.return_value = self.mock_cursor
        mock_connect.return_value = self.mock_db

        from database import Database
        self.db = Database()

    def test_create_database(self):
        self.db.create_database()

        def normalize_sql(call):
            query_str = call.args[0] if isinstance(call.args[0], str) else call.args[0][0]
            return " ".join(query_str.split())

        expected_calls = [
            "CREATE TABLE IF NOT EXISTS user( id int PRIMARY KEY AUTO_INCREMENT, username varchar(50), password varchar(256) )",
            "CREATE TABLE IF NOT EXISTS note( id int PRIMARY KEY AUTO_INCREMENT, user_id int, content text, date timestamp, FOREIGN KEY (user_id) REFERENCES user(id) )"
        ]

        executed_calls = [normalize_sql(call) for call in self.mock_cursor.execute.call_args_list]

        for expected_call in expected_calls:
            self.assertIn(expected_call, executed_calls)

        self.mock_db.commit.assert_called_once()

    def test_create_user_success(self):
        self.mock_cursor.rowcount = 0
        result = self.db.create_user("test_user", "password123")
        self.mock_cursor.execute.assert_any_call("INSERT INTO user VALUES (NULL, %s, SHA2(%s, 256))", ("test_user", "password123"))
        self.assertGreaterEqual(self.mock_db.commit.call_count, 1)
        self.assertEqual(result, "success")

    def test_create_user_username_taken(self):
        self.mock_cursor.rowcount = 1
        result = self.db.create_user("existing_user", "password123")
        self.assertEqual(result, "username_taken")

    def test_delete_user(self):
        self.db.delete_user(1)
        self.mock_cursor.execute.assert_any_call("DELETE FROM note WHERE user_id = 1")
        self.mock_cursor.execute.assert_any_call("DELETE FROM user WHERE id = 1")
        self.mock_db.commit.assert_called_once()

    def test_login_success(self):
        self.mock_cursor.fetchone.return_value = (1, "test_user", "hashed_password")
        result = self.db.login("test_user", "password123")
        self.assertEqual(result, (1, "test_user", "hashed_password"))

    def test_login_fail(self):
        self.mock_cursor.fetchone.return_value = None
        result = self.db.login("wrong_user", "password123")
        self.assertIsNone(result)

    def test_create_note(self):
        self.db.create_note(1, "Test note content")
        self.mock_cursor.execute.assert_called_with("INSERT INTO note VALUES (NULL, %s, %s, NULL)",
                                                    (1, "Test note content"))
        self.assertGreaterEqual(self.mock_db.commit.call_count, 1)

    def test_edit_note(self):
        self.db.edit_note(1, "Updated content")
        self.mock_cursor.execute.assert_called_with("UPDATE note SET content = %s, date = NULL WHERE id = %s", ("Updated content", 1))
        self.assertGreaterEqual(self.mock_db.commit.call_count, 1)

    def test_delete_note(self):
        self.db.delete_note(1)
        self.mock_cursor.execute.assert_called_with("DELETE FROM note WHERE id = 1")
        self.mock_db.commit.assert_called_once()

    def test_select_all_notes(self):
        self.mock_cursor.fetchall.return_value = [(1, 1, "Test note", "2025-04-03")]
        result = self.db.select_all_notes(1)
        self.mock_cursor.execute.assert_called_with("SELECT * FROM note WHERE user_id LIKE '1' ORDER BY date DESC")
        self.assertEqual(result, [(1, 1, "Test note", "2025-04-03")])

    def test_search_notes(self):
        self.mock_cursor.fetchall.return_value = [(1, 1, "Test note", "2025-04-03")]
        result = self.db.search(1, "Test")
        self.mock_cursor.execute.assert_called_with(
            "SELECT * FROM note WHERE content LIKE '%Test%' AND user_id = 1 ORDER BY date DESC")
        self.assertEqual(result, [(1, 1, "Test note", "2025-04-03")])


if __name__ == '__main__':
    unittest.main()