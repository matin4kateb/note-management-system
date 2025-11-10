# ----------------------------------------------
#           Note Management System
#   by Mohammad Matin Kateb
#   GitHub: https://github.com/matin4kateb
# ----------------------------------------------

import grpc
import note_pb2
import note_pb2_grpc
from os import system

def create_note(stub, title, content):
    create_resp = stub.CreateNote(note_pb2.CreateNoteRequest(title=title, content=content))
    print(f"[+] Note created with ID {create_resp.id}")
    
def get_note(stub, note_id):
    try:
        response = stub.GetNote(note_pb2.GetNoteRequest(id=note_id))
        print(f"[+] Note fetched: {response.title} - {response.content}")
    except grpc.RpcError as e:
        print(f"[!] Error: {e.code()} - {e.details()}")
        
def list_notes(stub):
    list_resp = stub.ListNotes(note_pb2.ListNotesRequest())
    for n in list_resp.notes:
        print(f"[{n.id}] {n.title} - {n.content}")
        
def delete_note(stub, note_id):
    try:
        response = stub.DeleteNote(note_pb2.DeleteNoteRequest(id=note_id))
        if response.success:
            print(f"[-] Successfully deleted note #{note_id}")
        else:
            print(f"[!] Unable to delete note #{note_id}")
    except grpc.RpcError as e:
        print(f"[!] Error while attempting to delete: {e.code()} - {e.details()}")
    
def print_line():
    print("=-="*20)
    
def print_menu():
    menu="""        Note Management System
    options:
    1- Create Note
    2- Get Note
    3- List Notes
    4- Delete Note
    
    5- Exit
    """
    print(menu)

def run():
    host = input("[+] Enter server's address: ")
    port = input("[+] Enter server's port: ")
    print("[+] Establishing connection to the server...")
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = note_pb2_grpc.NoteServiceStub(channel)
    print("[+] Connection with server established successfully")
        
    while True:
        print_line()
        print_menu()
        
        option = input("[+] Enter option: ")
        if option == "1":   # create note
            system("CLS")
            title = input("[+] Enter note title: ")
            content = input("[+] Enter note content: ")
            create_note(stub, title, content)
            
        elif option == "2": # get note
            system("CLS")
            note_id = input("[+] Enter note ID: ")
            get_note(stub, note_id)
            
        elif option == "3": # list notes
            system("CLS")
            list_notes(stub)
            
        elif option == "4": # delete note
            system("CLS")
            note_id = input("[+] Enter note ID: ")
            delete_note(stub, note_id)
        
        elif option == "5":
            print("Bye Bye")
            break
        
        else:
            system("CLS")
            print("[!] Invalid input")
            continue