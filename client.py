# ----------------------------------------------
#           Note Management System (Client)
#   by Mohammad Matin Kateb
#   GitHub: https://github.com/matin4kateb
# ----------------------------------------------

import grpc
import note_pb2
import note_pb2_grpc
import os
import platform


def clear_screen():
    """Cross-platform screen clear."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def print_line():
    print("=-=" * 20)


def print_menu():
    menu = """
        Note Management System
    ----------------------------------
    1- Create Note
    2- Get Note
    3- List Notes
    4- Delete Note
    5- Exit
    """
    print(menu)


def create_note(stub, title, content):
    try:
        response = stub.CreateNote(note_pb2.CreateNoteRequest(title=title, content=content))
        print(f"[+] Note created successfully with ID #{response.id}")
    except grpc.RpcError as e:
        print(f"[!] RPC Error: {e.code().name} - {e.details()}")


def get_note(stub, note_id):
    try:
        response = stub.GetNote(note_pb2.GetNoteRequest(id=int(note_id)))
        print(f"[+] Note fetched:\nTitle: {response.title}\nContent: {response.content}")
    except grpc.RpcError as e:
        print(f"[!] RPC Error: {e.code().name} - {e.details()}")
    except ValueError:
        print("[!] Invalid ID. Please enter a number.")


def list_notes(stub):
    """Fetch and display all notes from the gRPC server."""
    try:
        response = stub.ListNotes(note_pb2.ListNotesRequest())
        notes = getattr(response, "notes", [])
        if not notes:
            print("[i] No notes found.")
            return
        print("[*] Notes:")
        for note in notes:
            print(f"  [{note.id}] {note.title} - {note.content}")
    except grpc.RpcError as e:
        print(f"[!] RPC Error: {e.code().name} - {e.details()}")


def delete_note(stub, note_id):
    try:
        response = stub.DeleteNote(note_pb2.DeleteNoteRequest(id=int(note_id)))
        if response.success:
            print(f"[-] Note #{note_id} deleted successfully.")
        else:
            print(f"[!] Failed to delete note #{note_id}. It may not exist.")
    except grpc.RpcError as e:
        print(f"[!] RPC Error: {e.code().name} - {e.details()}")
    except ValueError:
        print("[!] Invalid ID. Please enter a number.")


def run():
    host = input("[+] Enter server address (default: 127.0.0.1): ").strip() or "127.0.0.1"
    port = input("[+] Enter server port (default: 50051): ").strip() or "50051"

    print(f"[+] Connecting to {host}:{port} ...")
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = note_pb2_grpc.NoteServiceStub(channel)

    print("[+] Connection established successfully")

    try:
        while True:
            print_line()
            print_menu()
            option = input("[+] Enter option: ").strip()

            clear_screen()

            if option == "1":
                title = input("[+] Enter note title: ")
                content = input("[+] Enter note content: ")
                create_note(stub, title, content)

            elif option == "2":
                note_id = input("[+] Enter note ID: ")
                get_note(stub, note_id)

            elif option == "3":
                list_notes(stub)

            elif option == "4":
                note_id = input("[+] Enter note ID: ")
                delete_note(stub, note_id)

            elif option == "5":
                print("Goodbye!")
                break

            else:
                print("[!] Invalid input. Please choose a valid option.")

    finally:
        channel.close()


if __name__ == "__main__":
    run()