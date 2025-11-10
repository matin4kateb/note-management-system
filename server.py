# ----------------------------------------------
#           Note Management System
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
    query = """
        CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """   
    conn = sqlite3.connect(DB_FILE)    
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()

# implementing gRPC service
class NoteServiceServicer(note_pb2_grpc.NoteServiceServicer):
    def CreateNote(self, request, context):
        conn = sqlite3.connect(DB_FILE)
        cur  = conn.cursor()
        cur.execute("INSERT INTO notes VALUES (?, ?)", (request.title, request.content))
        conn.commit()
        note_id = cur.lastrowid
        conn.close()
        return note_pb2.CreateNoteResponse(id=note_id)
    
    def GetNote(self, request, context):
        conn = sqlite3.connect(DB_FILE)
        cur  = conn.cursor()
        cur.execute("SELECT title, content FROM notes WHERE id = ?", (request.id,))
        row = cur.fetchone()
        conn.close()
        
        if row:
            return note_pb2.GetNoteResponse(title=row[0], content=row[1])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("[!] Note not found")
            return note_pb2.GetNoteResponse()
        
    def DeleteNote(self, request, context):
        conn = sqlite3.connect(DB_FILE)
        cur  = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", (request.id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return note_pb2.DeleteNoteResponse(success=deleted)
    
    def ListNotes(self, request, context):
        conn = sqlite3.connect(DB_FILE)
        cur  = conn.cursor()
        cur.execute("SELECT id, title, content FROM notes")
        rows = cur.fetchall()
        conn.close()
        
        notes = [note_pb2.Note(id=r[0], title=r[1], content=r[2]) for r in rows]
        return note_pb2.ListNotesResponse(notes=notes)
    
# run server
def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    note_pb2_grpc.add_NoteServiceServicer_to_server(NoteServiceServicer, server)
    server_port = input("[+] Enter port number to run server: ")
    server.add_insecure_port(f'127.0.0.1:{server_port}')
    server.start()
    print(f"[+] gRPC Server started on port {server_port}")
    print("[+] Server is running...")
    server.wait_for_termination()
    
if __name__=="__main__":
    serve()