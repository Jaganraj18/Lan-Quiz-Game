# Lan-Quiz-Game
LAN Quiz Game is a lightweight, real-time multiplayer quiz application that lets players join through a browser using the server’s LAN IP address or QR code. It is built for classrooms, LAN parties, events, or fun local group quizzes.  Players join instantly, answer questions at their own pace, and receive immediate score results.

Introduction

LAN Quiz Game allows multiple players to join using any device connected to the same network. Players enter their name, wait in the lobby, and answer quiz questions in real time. The server handles communication, scoring, and quiz control, while the client provides a smooth, responsive UI.

Perfect for classrooms, LAN parties, training sessions, and group activities.





🚀 Features

🎮 Real-time multiplayer gameplay

🌐 Join via LAN IP or QR code

💡 Modern neon-styled UI with smooth animations

⚡ Instant scoring and results

🧠 Dynamic question loading from questions.json

🔄 Previous/Next question navigation

🛠 Admin console for starting, viewing players, and managing quiz


🛠 Technology Stack

Backend: Python 3, WebSockets, asyncio

Frontend: HTML5, CSS3, JavaScript

Server: Python HTTP Server

Extra: QR Code auto-generation for quick joining


📁 Project Structure

├── lan_quiz.html       # Main frontend UI

├── server.py           # WebSocket + HTTP server

├── questions.json      # Question bank

└── assets/             # Backgrounds/graphics 


⚙️ Installation & Setup

1️⃣ Install dependencies

pip install websockets qrcode

2️⃣ Start the server

python server.py

3️⃣ Join the game

Players can join by:

-Opening the generated LAN URL shown in the terminal OR scanning the QR code

-Then enter your name and wait for the quiz to start.

4️⃣ Admin controls

Inside the server console:

1 → Start Quiz  

2 → View Connected Players  

3 → Exit  


📝 Adding Questions

Edit questions.json using this format:

{

  "question": "What is the capital of Japan?",
  
  "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
  
  "answer": "3"

}

"answer" is the option number (1, 2, 3, or 4).

Note:-

Create a folder name as assets for (login-bg.svg) for interactive background for login page.
