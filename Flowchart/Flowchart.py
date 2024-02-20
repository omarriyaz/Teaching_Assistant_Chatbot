def main():
    print(" ")
    print("The Teaching Assistant Chatbot Flowchart")
    print(" ")

    while True:
        print("Flowchart decisions: A new Chat is created")
        print(" ")
        print("1. Upload a PDF to the chatbot")
        print("2. Ask questions")
        print("3. Open settings")
        print("4. Exit")
        print(" ")

        choice = input("Enter your choice (1/2/3/4): ")
        print(" ")

        if choice == "1":
            upload_pdf()
        elif choice == "2":
            ask_questions()
        elif choice == "3":
            open_settings()
        elif choice == "4":
            print("Exiting the flowchart.")
            print(" ")
            print(" ")
            print(" ")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            print(" ")
            print(" ")
            print(" ")


def upload_pdf():
    file_name = input("Enter the name of the PDF file: ")
    print(" ")
    print(f"Uploading PDF named '{file_name}'...")
    print(" ")
    print(f"PDF '{file_name}' uploaded successfully.")
    print(" ")
    print(" ")
    print(" ")


def ask_questions():
    print("Ask the chatbot a question, then it will generate an answer for it")
    print(" ")
    while True:
        question = input("Ask your question (or type 'exit' to return to the flowchart): ")
        print(" ")
        
        if question.lower() == "exit":
            print("Returning to the flowchart.")
            print(" ")
            print(" ")
            print(" ")
            break
        else:
            print(f"Answering question: {question}")
            print(" ")
            print("Response generated.")
            print(" ")

def open_settings():
    print("Opening settings...")
    print(" ")
    print("Settings opened, user can change settings here")
    print(" ")
    input("Press Enter to return to the flowchart...")

if __name__ == "__main__":
    main()