# 🗒️ Note Management System (gRPC + SQLite)

A simple **Note Management System** implemented in **Python** using **gRPC** and **SQLite**.  
This project was created as an assignment for the **Distributed Systems** course.

---

## ⚙️ Features
- Create a note (title + content)
- Get a note by ID
- Delete a note by ID
- List all notes  
- Uses **SQLite** as a lightweight local database on the server side.

---

## 🧩 Requirements & Installation

Make sure you have **Python 3.8+** installed, then install the required packages:

```bash
pip install grpcio grpcio-tools
````

SQLite is built into Python and does not require a separate installation.

---

## 🚀 How to Run

### 1️⃣ Generate gRPC code

Run one of these scripts to generate `note_pb2.py` and `note_pb2_grpc.py` from `note.proto`:

* On **Windows**:

  ```bash
  gen_proto.bat
  ```
* On **Linux/macOS**:

  ```bash
  bash gen_proto.sh
  ```

### 2️⃣ Start the server

```bash
python server.py
```

### 3️⃣ Run the client

```bash
python client.py
```

---

## 🧠 Notes

* The server stores all notes in a **SQLite** database file named `notes.db`.
* The default gRPC server address is `0.0.0.0:50051`.
* You can easily change the address or port in the source code if needed.

---

**Author:** Mohammad Matin Kateb
**Course:** Distributed Systems — Fall 2025
