import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from app import app, users, tasks

class TodoAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset in-memory storage before each test
        users.clear()
        tasks.clear()
        app.user_id_counter = 1
        app.task_id_counter = 1

    # Test user creation
    def test_create_user(self):
        response = self.app.post('/users', data=json.dumps({"username": "Vasu"}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["username"], "Vasu")
        self.assertIn("id", data)

    # Test login success
    def test_login_success(self):
        # First create a user
        self.app.post('/users', data=json.dumps({"username": "Vasu"}), content_type='application/json')
        response = self.app.post('/login', data=json.dumps({"username": "Vasu"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())

    # Test login failure
    def test_login_failure(self):
        response = self.app.post('/login', data=json.dumps({"username": "Unknown"}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    # Test adding a task
    def test_add_task(self):
        # Create user and simulate login
        self.app.post('/users', data=json.dumps({"username": "TaskUser"}), content_type='application/json')
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            response = client.post('/tasks', data=json.dumps({"title": "Test Task", "priority": "high"}), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertEqual(data["title"], "Test Task")
            self.assertEqual(data["user_id"], 1)

    # Test updating a task
    def test_update_task(self):
        self.app.post('/users', data=json.dumps({"username": "UpdateUser"}), content_type='application/json')
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            task_resp = client.post('/tasks', data=json.dumps({"title": "Old Task"}), content_type='application/json')
            task_id = task_resp.get_json()["id"]

            update_resp = client.patch(f'/tasks/{task_id}', data=json.dumps({"title": "Updated Task", "completed": True}), content_type='application/json')
            self.assertEqual(update_resp.status_code, 200)
            updated_task = update_resp.get_json()
            self.assertEqual(updated_task["title"], "Updated Task")
            self.assertTrue(updated_task["completed"])

    # Test deleting a task
    def test_delete_task(self):
        self.app.post('/users', data=json.dumps({"username": "DeleteUser"}), content_type='application/json')
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1
            task_resp = client.post('/tasks', data=json.dumps({"title": "Task To Delete"}), content_type='application/json')
            task_id = task_resp.get_json()["id"]

            del_resp = client.delete(f'/tasks/{task_id}')
            self.assertEqual(del_resp.status_code, 200)
            self.assertEqual(del_resp.get_json()["message"], "Task deleted")

    # Test logout route
    def test_logout_route(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HD To-Do App", response.data)

if __name__ == '__main__':
    unittest.main()
