# ----------------------------------------------
#           Note Management System (Server)
#   by Mohammad Matin Kateb
#   GitHub: https://github.com/matin4kateb
# ----------------------------------------------

import sqlite3
from concurrent import futures
import grpc
import note_pb2
import note_pb2_grpc

DB_FILE = "notes.db"


# database setup
def init_db():
    # initialize SQLite database if not exists.
    query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(query)
    print("[+] Database initialized successfully.")


# implementing the gRPC service
class NoteServiceServicer(note_pb2_grpc.NoteServiceServicer):
    def CreateNote(self, request, context):
        # create a new note
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO notes (title, content) VALUES (?, ?)",
                    (request.title, request.content),
                )
                note_id = cur.lastrowid
            print(f"[+] Note created with ID #{note_id}")
            return note_pb2.CreateNoteResponse(id=note_id)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {str(e)}")
            return note_pb2.CreateNoteResponse()

    def GetNote(self, request, context):
        # retrieve a note by ID
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT title, content FROM notes WHERE id = ?", (request.id,))
            row = cur.fetchone()

        if row:
            print(f"[+] Note fetched (ID={request.id})")
            return note_pb2.GetNoteResponse(title=row[0], content=row[1])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Note not found.")
            return note_pb2.GetNoteResponse()

    def DeleteNote(self, request, context):
        # delete a note by ID
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM notes WHERE id = ?", (request.id,))
            deleted = cur.rowcount > 0

        if deleted:
            print(f"[-] Note deleted (ID={request.id})")
        else:
            print(f"[!] Delete failed — note #{request.id} not found.")

        return note_pb2.DeleteNoteResponse(success=deleted)

    def ListNotes(self, request, context):
        # return all notes
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, title, content FROM notes")
            rows = cur.fetchall()

        notes = [note_pb2.Note(id=r[0], title=r[1], content=r[2]) for r in rows]
        print(f"[i] Returned {len(notes)} note(s).")
        return note_pb2.ListNotesResponse(notes=notes)


# run gRPC server
def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    note_pb2_grpc.add_NoteServiceServicer_to_server(NoteServiceServicer(), server)
    
    host = input("[+] Enter host address (default: 0.0.0.0): ").strip() or "0.0.0.0"
    port = input("[+] Enter port number (default: 50051): ").strip() or "50051"
    server.add_insecure_port(f"{host}:{port}")

    server.start()
    print(f"[+] gRPC Server started on port {port}")
    print("[+] Server is running... Press Ctrl+C to stop.")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[!] Server stopped manually.")


if __name__ == "__main__":
    serve()
