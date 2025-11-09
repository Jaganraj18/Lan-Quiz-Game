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

🎨 Screenshots (Optional)

You can add your images like:

![Login Screen]<img width="1917" height="1017" alt="Screenshot 2025-11-03 214300" src="https://github.com/user-attachments/assets/445ecb93-5d3c-42da-a3ba-439acde85cfc" />


![Waiting Screen]<img width="1919" height="911" alt="Screenshot 2025-10-18 115520" src="https://github.com/user-attachments/assets/dd8e9400-3de2-4f2c-91c5-f29ff2d47b83" />



![Quiz Screen]<img width="1919" height="1020" alt="Screenshot 2025-11-03 214432" src="https://github.com/user-attachments/assets/65758f28-5e90-4cf7-a065-3e3f12cee447" />


![Results Screen]<img width="1919" height="909" alt="Screenshot 2025-10-18 115337" src="https://github.com/user-attachments/assets/b48a2c61-191d-45e7-8914-194ad6e62ff9" />


![Server Screen]<img width="1919" height="1017" alt="Screenshot 2025-11-03 214212" src="https://github.com/user-attachments/assets/50c16ed6-53ed-45df-b598-576f909094d3" />
<img width="1919" height="1019" alt="Screenshot 2025-11-03 214539" src="https://github.com/user-attachments/assets/2dafd195-2358-485a-9453-43f038254396" />


Note:-

Create a folder name as assets for (login-bg.svg) for interactive background for login page.
