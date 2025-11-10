print("--- ✅✅✅ RUNNING THE CORRECT AND LATEST VERSION OF SERVER.PY ✅✅✅ ---")

import asyncio
import websockets
import json
import socket
import http.server
import socketserver
import threading
import qrcode
import random

# --- Configuration ---
HTTP_PORT = 8000
WEBSOCKET_PORT = 8765

class GameServer:
    def __init__(self):
        self.clients = {}  # {websocket: {"name": "player_name"}}
        self.lock = asyncio.Lock()
        self.questions = []
        self.current_quiz_answers = [] # Stores the correct answers for the current round
        self.load_questions()

    def load_questions(self):
        """Loads questions from questions.json."""
        try:
            with open('questions.json', 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
            print(f"[+] Successfully loaded {len(self.questions)} questions.")
        except Exception as e:
            print(f"[!] ERROR loading questions.json: {e}")
            self.questions = []

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception: IP = '127.0.0.1'
        finally: s.close()
        return IP

    def generate_qr_code(self, url):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        print("Scan the QR Code to Join:")
        qr.print_ascii()

    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(*[ws.send(json.dumps(message)) for ws in self.clients])

    async def update_player_list(self):
        """Sends the current list of connected players."""
        player_names = [data['name'] for data in self.clients.values()]
        await self.broadcast({"type": "player_update", "players": player_names})

    async def handle_client(self, websocket, path):
        """Handles a single client connection and their quiz submission."""
        try:
            login_data = json.loads(await websocket.recv())
            if login_data['type'] == 'login':
                name = login_data.get('name', 'Anonymous')
                async with self.lock:
                    self.clients[websocket] = {"name": name}
                print(f"[+] Client Connected: {name}")
                await self.update_player_list()

                async for message in websocket:
                    data = json.loads(message)
                    if data['type'] == 'submit_quiz':
                        await self.score_quiz(websocket, data.get('answers', []))
        
        except websockets.exceptions.ConnectionClosed:
            print(f"[-] Client Disconnected.")
        finally:
            async with self.lock:
                if websocket in self.clients:
                    del self.clients[websocket]
            await self.update_player_list()
    
    async def score_quiz(self, websocket, client_answers):
        """Scores a submitted quiz and sends back the result."""
        score = 0
        async with self.lock:
            # Ensure the quiz hasn't been reset while client was answering
            if not self.current_quiz_answers:
                return 

            for i, correct_ans in enumerate(self.current_quiz_answers):
                if i < len(client_answers) and client_answers[i] == correct_ans:
                    score += 1
        
        total = len(self.current_quiz_answers)
        print(f"[+] Scoring {self.clients[websocket]['name']}: {score}/{total}")
        await websocket.send(json.dumps({
            "type": "quiz_end",
            "score": score,
            "total_questions": total
        }))


    async def admin_interface(self):
        """Handles input from the server admin."""
        loop = asyncio.get_event_loop()
        while True:
            await loop.run_in_executor(None, self.show_admin_menu)
            command = await loop.run_in_executor(None, input, "> ")
            
            if command == "1": # Start Quiz
                if not self.questions:
                    print("\n[!] No questions loaded from questions.json.")
                    continue
                
                # Shuffle and prepare the quiz for broadcasting
                quiz_set = self.questions[:]
                random.shuffle(quiz_set)
                
                # Store correct answers on the server
                async with self.lock:
                    self.current_quiz_answers = [q['answer'] for q in quiz_set]

                # Create a "safe" version of questions without answers to send to clients
                questions_for_clients = [{ "question": q["question"], "options": q["options"] } for q in quiz_set]
                
                print(f"\n[+] Starting quiz with {len(questions_for_clients)} questions!")
                await self.broadcast({
                    "type": "start_quiz",
                    "questions": questions_for_clients
                })

            elif command == "2": # View Clients
                print("\n--- Connected Clients ---")
                if not self.clients: print("No clients connected.")
                else:
                    for data in self.clients.values(): print(f"  - {data['name']}")
                print("------------------------\n")

            elif command == "3": # Exit
                print("Shutting down server...")
                break
            else:
                print("Invalid command.")
        
        # Graceful shutdown
        active_clients = list(self.clients.keys())
        if active_clients:
            await asyncio.gather(*[ws.close(code=1000, reason='Server shutdown') for ws in active_clients])

    def show_admin_menu(self):
        print("\n--- Server Admin Menu ---")
        print("1. Start Quiz (Sends all questions to clients)")
        print("2. View Connected Clients")
        print("3. Exit")
        print("-------------------------")


def run_http_server(port, directory="."):
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
        def do_GET(self):
            if self.path == '/': self.path = '/lan_quiz.html'
            return super().do_GET()
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"[+] HTTP server started at http://localhost:{port}")
        httpd.serve_forever()

async def main():
    server = GameServer()
    local_ip = server.get_local_ip()
    game_url = f"http://{local_ip}:{HTTP_PORT}"

    print("\n" + "="*50)
    print("      🚀 LAN QUIZ SERVER IS LIVE! 🚀")
    print("="*50 + "\n")
    print(f"Players can join at: \033[1m\033[96m{game_url}\033[0m\n")
    server.generate_qr_code(game_url)

    http_thread = threading.Thread(target=run_http_server, args=(HTTP_PORT,), daemon=True)
    http_thread.start()

    async def websocket_handler(ws, path=None):
        await server.handle_client(ws, path)

    async with websockets.serve(websocket_handler, "0.0.0.0", WEBSOCKET_PORT):
        print(f"\n[+] WebSocket server listening on port {WEBSOCKET_PORT}")
        print("\n--- Use this console to manage the quiz ---\n")
        await server.admin_interface()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shut down by user.")