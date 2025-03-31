import unittest
import os
import tempfile
import platform
from unittest.mock import patch, MagicMock
from app import app  # Assuming your app.py is in the same directory

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up a test client before each test."""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index_route(self):
        """Test if the index route returns a 200 status code."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_target_route(self):
        """Test if the add_target route returns a 200 status code and correct message."""
        response = self.app.post('/api/targets', json={'name': 'test_target', 'ip': '192.168.1.1'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], "Target test_target with IP 192.168.1.1 added successfully!")

    def test_login_success(self):
        """Test successful login."""
        response = self.app.post('/login', data={'username': 'admin', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_login_failure(self):
        """Test failed login."""
        response = self.app.post('/login', data={'username': 'wrong', 'password': 'wrong'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'error', response.data)

    @patch('subprocess.Popen')
    def test_connect_vpn_success(self, mock_popen):
        """Test successful VPN connection."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"test vpn file content")
            temp_file_path = temp_file.name

        with open(temp_file_path, 'rb') as file:
            data = {'vpn-file': (file, 'test.ovpn')}
            response = self.app.post('/connect-vpn', data=data, content_type='multipart/form-data', follow_redirects=True)

        os.remove(temp_file_path)
        self.assertEqual(response.status_code, 302) #redirect
        mock_popen.assert_called_once()

    def test_connect_vpn_no_file(self):
        """Test VPN connection without a file."""
        response = self.app.post('/connect-vpn', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 302) #redirect
        self.assertIn(b'error', response.data)

    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        """Test successful command execution."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Command output"
        mock_run.return_value = mock_result

        response = self.app.post('/execute-command', data={'command': 'ls'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['output'], "Command output")

    @patch('subprocess.run')
    def test_execute_command_failure(self, mock_run):
        """Test failed command execution."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Command error"
        mock_run.return_value = mock_result

        response = self.app.post('/execute-command', json={'command': 'invalid_command'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['output'], "Command error")

if __name__ == '__main__':
    unittest.main()
